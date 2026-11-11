"""Select the newest complete release without changing old installations."""

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

from agent_playbook.releases import selection


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
        selection, "__file__", str(app / "src/agent_playbook/releases/selection.py")
    ):
        first = add_release(app, "0.0.1-aaa", "0.0.1", 100)
        newer = add_release(app, "0.0.1-aaa-2", "0.0.1", 200)
        latest = add_release(app, "0.1.0-bbb", "0.1.0", 300)
        assert selection.find_release(None) == (latest, "0.1.0")
        assert selection.find_release("0.0.1") == (newer, "0.0.1")
        assert selection.find_release("0.0.2") is None
        assert first.exists()


def test_incomplete_release_is_skipped_and_exit_code_propagates(tmp_path: Path) -> None:
    app = tmp_path / "app"
    with patch.object(
        selection, "__file__", str(app / "src/agent_playbook/releases/selection.py")
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
            selection.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 17),
        ) as process:
            assert selection.run_release(None) == 17
            assert process.call_args.args[0] == [
                str(installed),
                "-I",
                "-m",
                "agent_playbook.cli",
                "run",
            ]
