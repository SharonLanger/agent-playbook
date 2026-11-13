"""Select the newest complete release without changing old installations."""

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.cli import commands
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.releases import discovery, launcher


def add_release(app: Path, folder: str, release_version: str, timestamp: int) -> Path:
    directory = app / "dist" / folder
    executable = directory / "venv" / "bin" / "python"
    executable.parent.mkdir(parents=True)
    executable.touch()
    (executable.parent / "agent-playbook").touch()
    manifest = directory / "release.json"
    manifest.write_text(json.dumps({"version": release_version}))
    import os

    os.utime(manifest, ns=(timestamp, timestamp))
    return executable


def test_latest_release_and_version_filter(tmp_path: Path) -> None:
    app = tmp_path / "app"
    with patch.object(
        discovery, "__file__", str(app / "src/agent_playbook/releases/discovery.py")
    ):
        first = add_release(app, "0.0.1-aaa", "0.0.1", 100)
        newer = add_release(app, "0.0.1-aaa-2", "0.0.1", 200)
        latest = add_release(app, "0.1.0-bbb", "0.1.0", 300)
        assert discovery.find_release(None) == (latest, "0.1.0")
        assert discovery.find_release("0.0.1") == (newer, "0.0.1")
        assert discovery.find_release("0.0.2") is None
        assert first.exists()


def test_explicit_release_directory(tmp_path: Path) -> None:
    installed = add_release(tmp_path, "0.2.0-abc", "0.2.0", 100)
    assert discovery.find_release(None, tmp_path / "dist") == (installed, "0.2.0")


def test_missing_release_reports_selection_without_launching(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with (
        patch.object(commands, "find_release", return_value=None),
        patch.object(commands, "launch_release") as launch,
    ):
        assert commands.present_release("0.9.0") == 2
        launch.assert_not_called()
    assert "No installed release version 0.9.0" in capsys.readouterr().err


def test_launcher_configuration_error_is_an_actionable_cli_error(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    with (
        patch.object(
            commands,
            "find_release",
            return_value=(tmp_path / "venv/bin/python", "0.1.0"),
        ),
        patch.object(
            commands,
            "launch_release",
            side_effect=ConfigurationError("Move or merge old override"),
        ),
    ):
        assert commands.present_release(None) == 2
    error = capsys.readouterr().err
    assert "Configuration error: Move or merge old override" in error
    assert "Traceback" not in error


def test_incomplete_release_is_skipped_and_exit_code_propagates(tmp_path: Path) -> None:
    app = tmp_path / "app"
    with patch.object(
        discovery, "__file__", str(app / "src/agent_playbook/releases/discovery.py")
    ):
        installed = add_release(app, "0.0.1-good", "0.0.1", 100)
        incomplete = app / "dist/0.0.1-incomplete"
        incomplete.mkdir()
        (incomplete / "release.json").write_text('{"version":"0.0.1"}')
        unverified = add_release(app, "0.0.1-unverified", "0.0.1", 300)
        (unverified.parents[2] / "release.json").write_text(
            json.dumps({"version": "0.0.1", "verified": False})
        )
        with patch.object(
            launcher.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 17),
        ) as process:
            assert commands.present_release(None) == 17
            assert process.call_args.args[0] == [
                str(installed),
                "-I",
                "-m",
                "agent_playbook.cli",
                "run",
            ]
