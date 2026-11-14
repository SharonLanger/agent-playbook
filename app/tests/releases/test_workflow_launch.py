import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.config.paths import configuration_path
from agent_playbook.releases import launcher


def test_json_remains_one_argument_and_error_is_propagated(tmp_path: Path) -> None:
    python = tmp_path / "release with spaces/venv/bin/python"
    raw = '{"future": "quoted "value" with spaces"}'
    with (
        patch.object(
            launcher.subprocess, "run", return_value=subprocess.CompletedProcess([], 2)
        ) as run,
    ):
        assert (
            launcher.launch_release(python, ["--workflow", "wf-03", "--input", raw])
            == 2
        )
    args = run.call_args.args[0]
    assert args == [
        str(python),
        "-I",
        "-m",
        "agent_playbook.cli",
        "run",
        "--workflow",
        "wf-03",
        "--input",
        raw,
    ]
    assert "PYTHONPATH" not in run.call_args.kwargs["env"]
    assert "PYTHONHOME" not in run.call_args.kwargs["env"]
    assert not run.call_args.kwargs.get("shell", False)


def test_launcher_passes_shared_path_without_adding_options_to_old_releases(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("AGENT_PLAYBOOK_CONFIG", raising=False)
    python = tmp_path / "venv/bin/python"
    with (
        patch.object(
            launcher.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)
        ) as run,
    ):
        assert launcher.launch_release(python) == 0
    assert run.call_args.args[0] == [
        str(python),
        "-I",
        "-m",
        "agent_playbook.cli",
        "run",
    ]
    assert run.call_args.kwargs["env"]["AGENT_PLAYBOOK_CONFIG"] == str(
        configuration_path()
    )


def test_launcher_preserves_explicit_configuration_and_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AGENT_PLAYBOOK_CONFIG", "/environment/settings.yaml")
    python = tmp_path / "venv/bin/python"
    explicit = "/explicit path/settings.yaml"
    with (
        patch.object(
            launcher.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)
        ) as run,
    ):
        assert launcher.launch_release(python, ["--config", explicit]) == 0
    assert run.call_args.args[0][-2:] == ["--config", explicit]
    assert (
        run.call_args.kwargs["env"]["AGENT_PLAYBOOK_CONFIG"]
        == "/environment/settings.yaml"
    )
