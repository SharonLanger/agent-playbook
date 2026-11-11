"""Exercise command dispatch and exit semantics as a separate process."""

import subprocess
import sys


def test_run() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "agent_playbook.cli", "run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Python environment ready." in result.stdout


def test_unknown_command() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "agent_playbook.cli", "unknown"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "invalid choice" in result.stderr
