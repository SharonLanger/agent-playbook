"""Exercise command dispatch and exit semantics as a separate process."""

import subprocess
import sys


def test_dev_run() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "agent_playbook.cli", "dev-run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[WF-01] result: [Hello, workflow!]" in result.stdout


def test_unknown_command() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "agent_playbook.cli", "unknown"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "invalid choice" in result.stderr


def test_cli_only_commands_do_not_import_frameworks() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import sys; from agent_playbook.cli.commands import main; "
            "assert main(['version']) == 0; "
            "assert not any(name in sys.modules for name in ('crewai', 'pydantic'))",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
