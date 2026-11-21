"""Exercise configuration precedence and coordination with synthetic fixtures."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import (
    ServiceSelection,
    load_configuration,
    load_service_selection,
)
from tooling import services


@pytest.fixture
def selection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for key in ("SYNTHETIC_LF_PUBLIC_MISSING", "SYNTHETIC_LF_SECRET_MISSING"):
        monkeypatch.delenv(key, raising=False)
    for name in ("LOGGING", "LANGFUSE"):
        monkeypatch.delenv(f"AGENT_PLAYBOOK_{name}_ENABLED", raising=False)
    selected = tmp_path / "selected.yaml"
    selected.write_text(
        """secrets: {file: local.env}
integrations:
  crewai:
    usage_telemetry_enabled: false
    tracing_enabled: false
    show_framework_events: false
  logging: {enabled: false}
  langfuse:
    enabled: false
    public_key: {env: SYNTHETIC_LF_PUBLIC_MISSING}
    secret_key: {env: SYNTHETIC_LF_SECRET_MISSING}
workflows: {}
"""
    )
    (tmp_path / "local.env").write_text("")
    return selected


@pytest.mark.parametrize(
    ("logging", "langfuse"),
    [(False, False), (True, False), (False, True), (True, True)],
)
def test_enabled_matrix_without_project_keys(
    selection: Path, logging: bool, langfuse: bool
) -> None:
    selection.with_name("selected.local.yaml").write_text(
        f"integrations: {{logging: {{enabled: {str(logging).lower()}}}, langfuse: {{enabled: {str(langfuse).lower()}}}}}"
    )
    assert load_service_selection(str(selection)) == ServiceSelection(logging, langfuse)
    with patch.object(services, "supervise_component", return_value=0) as component:
        assert services.main(["--start", "--config", str(selection)]) == 0
    assert [call.args[2] for call in component.call_args_list] == [
        name for name, enabled in (("logs", logging), ("langfuse", langfuse)) if enabled
    ]
    if langfuse:
        with pytest.raises(ConfigurationError, match="Required Langfuse"):
            load_configuration(str(selection))


def test_real_loader_precedence_and_status(
    selection: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selection.with_name("selected.local.yaml").write_text(
        "integrations: {logging: {enabled: true}, langfuse: {enabled: true}}\n"
        "secrets: {file: override.env}\n"
    )
    override = selection.with_name("override.env")
    override.write_text(
        "AGENT_PLAYBOOK_LOGGING_ENABLED=false\nAGENT_PLAYBOOK_LANGFUSE_ENABLED=false\n"
    )
    assert load_service_selection(str(selection)) == ServiceSelection(False, False)
    monkeypatch.setenv("AGENT_PLAYBOOK_LOGGING_ENABLED", "TrUE")
    assert load_service_selection(str(selection)) == ServiceSelection(True, False)
    with patch.object(services, "supervise_component", side_effect=[0, 1]) as component:
        assert services.main(["--status", "--config", str(selection)]) == 0
    assert [call.args[2] for call in component.call_args_list] == ["logs", "langfuse"]
    with patch.object(services, "supervise_component", side_effect=[1, 0]):
        assert services.main(["--status", "--config", str(selection)]) == 1
    with patch.object(services, "supervise_component", side_effect=[0, 2]):
        assert services.main(["--status", "--config", str(selection)]) == 2


@pytest.mark.parametrize(
    "failure", ["syntax", "tag", "quoted", "yaml-synonym", "dotenv", "process", "blank"]
)
def test_invalid_selection_blocks_start_but_reports_status(
    selection: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: str,
) -> None:
    if failure == "syntax":
        selection.write_text("SYNTHETIC-MARKER: [")
    elif failure == "tag":
        selection.with_name("selected.local.yaml").write_text(
            "integrations: {logging: {enabled: !!bool [SYNTHETIC-MARKER]}}"
        )
    elif failure in ("quoted", "yaml-synonym"):
        value = '"SYNTHETIC-MARKER"' if failure == "quoted" else "on"
        selection.with_name("selected.local.yaml").write_text(
            f"integrations: {{logging: {{enabled: {value}}}}}"
        )
    elif failure == "dotenv":
        selection.with_name("local.env").write_text("SYNTHETIC-MARKER")
    elif failure == "process":
        monkeypatch.setenv("AGENT_PLAYBOOK_LOGGING_ENABLED", "SYNTHETIC-MARKER")
    args = ["--config", "" if failure == "blank" else str(selection)]
    with patch.object(services, "supervise_component", return_value=0) as component:
        assert services.main(["--start", *args]) == 2
        component.assert_not_called()
        assert services.main(["--status", *args]) == 2
        assert [call.args[2] for call in component.call_args_list] == [
            "logs",
            "langfuse",
        ]
    captured = capsys.readouterr()
    assert "selection: unavailable" in captured.out
    assert "SYNTHETIC-MARKER" not in captured.out + captured.err


def test_stop_ignores_yaml_attempts_both_and_forwards_env_file() -> None:
    with (
        patch.object(services, "_select", side_effect=AssertionError),
        patch.object(
            services, "supervise_component", side_effect=[2, 0, 0, 0]
        ) as component,
    ):
        assert (
            services.main(
                ["--stop", "--config", "missing.yaml", "--env-file", "private.env"]
            )
            == 2
        )
        assert services.main(["--stop", "--env-file", "private.env"]) == 0
    calls = component.call_args_list
    assert [call.args[2] for call in calls] == ["langfuse", "logs"] * 2
    assert calls[0].args[0][-3:] == ["--stop", "--env-file", "private.env"]
    assert calls[1].args[0][-1:] == ["--stop"]


@pytest.mark.parametrize("selector", ["explicit", "environment", "default"])
def test_relative_selectors_survive_actual_subprocess_cwd(
    selection: Path, selector: str
) -> None:
    app = Path(__file__).resolve().parents[2]
    source = selection.parent / "checkout" / "app"
    shutil.copytree(app / "src" / "agent_playbook", source / "src" / "agent_playbook")
    (source / "tooling").mkdir()
    shutil.copy2(app / "tooling" / "services.py", source / "tooling" / "services.py")
    env = {"PATH": os.defpath, "PYTHONPATH": str(source / "src")}
    args: list[str] = []
    if selector == "explicit":
        args += ["--config", selection.name]
        env["AGENT_PLAYBOOK_CONFIG"] = "missing.yaml"
    elif selector == "environment":
        env["AGENT_PLAYBOOK_CONFIG"] = selection.name
    else:
        shutil.copy2(selection, source / "application.yaml")
        shutil.copy2(selection.with_name("local.env"), source / "local.env")
    result = subprocess.run(
        [sys.executable, "-m", "agent_playbook.cli", "services", "--start", *args],
        env=env,
        cwd=selection.parent,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("skipped") == 2


def test_langfuse_disabled_project_check_is_docker_free(selection: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_playbook.cli",
            "langfuse",
            "--check",
            "--config",
            str(selection),
        ],
        cwd=selection.parent,
        env={"PATH": str(selection.parent)},
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 3
    assert "disabled; no connection attempted" in result.stdout.lower()


@pytest.mark.skipif(os.name != "posix", reason="FIFO paths require POSIX")
@pytest.mark.parametrize("which", ["base", "local", "secrets"])
def test_selection_rejects_fifo_without_waiting_for_writer(
    selection: Path, which: str
) -> None:
    fifo = {
        "base": selection,
        "local": selection.with_name("selected.local.yaml"),
        "secrets": selection.with_name("local.env"),
    }[which]
    if fifo.exists():
        fifo.unlink()
    os.mkfifo(fifo)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_playbook.cli",
            "services",
            "--start",
            "--config",
            str(selection),
        ],
        cwd=selection.parent,
        env={"PATH": str(selection.parent)},
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 2
    assert "Service selection unavailable" in result.stderr
    assert "Traceback" not in result.stderr
