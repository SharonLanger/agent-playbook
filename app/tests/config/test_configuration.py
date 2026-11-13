"""Configuration precedence, validation, privacy and framework startup boundaries."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.cli import commands
from agent_playbook.config import paths
from agent_playbook.config.crewai import configure_crewai
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration

FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"


def copy_config(tmp_path: Path) -> Path:
    selected = tmp_path / "application.yaml"
    selected.write_text(FIXTURE.read_text())
    return selected


def test_nested_local_overlay_environment_precedence_and_reload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    local = tmp_path / "application.local.yaml"
    local.write_text("integrations:\n  crewai:\n    show_framework_events: true\n")
    settings = load_configuration(str(selected)).integrations.crewai
    assert settings.show_framework_events
    assert not settings.tracing_enabled and not settings.usage_telemetry_enabled
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "false")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events
    monkeypatch.delenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS")
    local.write_text("integrations:\n  crewai:\n    show_framework_events: false\n")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events


def test_explicit_path_wins_and_development_default_ignores_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    monkeypatch.setenv("AGENT_PLAYBOOK_CONFIG", str(tmp_path / "missing.yaml"))
    load_configuration(str(selected))
    with pytest.raises(ConfigurationError, match="Cannot read"):
        load_configuration()
    monkeypatch.delenv("AGENT_PLAYBOOK_CONFIG")
    monkeypatch.chdir(tmp_path)
    assert (
        paths.configuration_path()
        == Path(paths.__file__).resolve().parents[3] / "application.yaml"
    )
    with patch.object(paths, "SOURCE_COMMIT", "installed-commit"):
        with pytest.raises(ConfigurationError, match="Select an external"):
            paths.configuration_path()


@pytest.mark.parametrize(
    "contents",
    [
        "[]",
        "null",
        "integrations: [",
        "integrations: {}",
        "integrations:\n  crewai:\n    tracing_enabled: secret-marker",
        FIXTURE.read_text() + "unknown: secret-marker\n",
        FIXTURE.read_text().replace("tracing_enabled: false", "tracing_enabled: 0"),
        FIXTURE.read_text().replace(
            "tracing_enabled: false", 'tracing_enabled: "false"'
        ),
        '!!python/object/apply:os.system ["touch should-not-exist"]',
    ],
)
def test_invalid_configuration_is_private_and_starts_no_steps(
    tmp_path: Path, contents: str, capsys: pytest.CaptureFixture[str]
) -> None:
    selected = tmp_path / "invalid.yaml"
    selected.write_text(contents)
    assert commands.main(["dev-run", "--config", str(selected)]) == 2
    captured = capsys.readouterr()
    assert "Configuration error" in captured.err
    assert "secret-marker" not in captured.err
    assert "started" not in captured.out
    assert not Path("should-not-exist").exists()


def test_environment_reference_and_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace(
            "show_framework_events: false",
            "show_framework_events: {env: MY_FLOW_EVENTS}",
        )
    )
    with pytest.raises(ConfigurationError, match="MY_FLOW_EVENTS is missing"):
        load_configuration(str(selected))
    monkeypatch.setenv("MY_FLOW_EVENTS", "true")
    assert load_configuration(str(selected)).integrations.crewai.show_framework_events
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "false")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "secret-marker")
    with pytest.raises(ConfigurationError) as failure:
        load_configuration(str(selected))
    assert "secret-marker" not in str(failure.value)


def test_changed_import_settings_require_fresh_process(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace("tracing_enabled: false", "tracing_enabled: true")
    )
    with pytest.raises(ConfigurationError, match="fresh process"):
        configure_crewai(load_configuration(str(selected)).integrations.crewai)


def test_invalid_configuration_precedes_framework_import(tmp_path: Path) -> None:
    selected = tmp_path / "missing.yaml"
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "from agent_playbook.cli.commands import main; "
            "import sys; code=main(['dev-run','--config',sys.argv[1]]); "
            "assert code == 2; assert 'crewai' not in sys.modules",
            str(selected),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_legacy_local_override_is_not_silently_ignored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("AGENT_PLAYBOOK_CONFIG", raising=False)
    legacy = tmp_path / "configs/application.local.yaml"
    legacy.parent.mkdir()
    legacy.write_text("private-local-values")
    with patch.object(
        paths, "__file__", str(tmp_path / "src/agent_playbook/config/paths.py")
    ):
        with pytest.raises(ConfigurationError, match="Legacy local override"):
            paths.configuration_path()
        assert paths.configuration_path("explicit.yaml").name == "explicit.yaml"
        assert legacy.read_text() == "private-local-values"
        target = tmp_path / "application.local.yaml"
        target.write_text("current-local-values")
        with pytest.raises(ConfigurationError, match="Move or merge"):
            paths.configuration_path()
        assert target.read_text() == "current-local-values"
        legacy.unlink()
        assert paths.configuration_path() == tmp_path / "application.yaml"


def test_import_settings_are_applied_before_framework_import(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace(
            "usage_telemetry_enabled: false", "usage_telemetry_enabled: true"
        )
    )
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import os,sys; "
            "from agent_playbook.config.loader import load_configuration; "
            "from agent_playbook.config.crewai import configure_crewai; "
            "configure_crewai(load_configuration(sys.argv[1]).integrations.crewai); "
            "assert 'crewai' not in sys.modules; "
            "assert os.environ['CREWAI_DISABLE_TELEMETRY']=='false'; "
            "assert os.environ['CREWAI_TRACING_ENABLED']=='false'",
            str(selected),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_same_code_reads_edited_configuration_on_next_invocation(
    tmp_path: Path,
) -> None:
    selected = copy_config(tmp_path)
    env = os.environ.copy()
    env["AGENT_PLAYBOOK_CONFIG"] = str(selected)
    command = [sys.executable, "-I", "-m", "agent_playbook.cli", "dev-run"]
    first = subprocess.run(
        command, env=env, cwd=tmp_path, capture_output=True, text=True, timeout=60
    )
    selected.write_text(
        selected.read_text().replace(
            "show_framework_events: false", "show_framework_events: true"
        )
    )
    second = subprocess.run(
        command, env=env, cwd=tmp_path, capture_output=True, text=True, timeout=60
    )
    assert first.returncode == second.returncode == 0, first.stderr + second.stderr
    assert "result: [Hello, workflow!]" in first.stdout
    assert "result: [Hello, workflow!]" in second.stdout
    assert first.stdout != second.stdout
