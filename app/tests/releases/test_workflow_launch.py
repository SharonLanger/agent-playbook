import subprocess
from pathlib import Path
from unittest.mock import patch

from agent_playbook.releases import selection


def test_json_remains_one_argument_and_error_is_propagated(tmp_path: Path) -> None:
    python = tmp_path / "release with spaces/venv/bin/python"
    raw = '{"future": "quoted "value" with spaces"}'
    with (
        patch.object(selection, "find_release", return_value=(python, "0.0.11")),
        patch.object(
            selection.subprocess, "run", return_value=subprocess.CompletedProcess([], 2)
        ) as run,
    ):
        assert (
            selection.run_release("0.0.11", ["--workflow", "wf-03", "--input", raw])
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
