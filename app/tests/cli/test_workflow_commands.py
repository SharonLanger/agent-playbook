import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.cli import commands
from agent_playbook.workflows.wf_01_step_sequence import steps


def test_defaults_help_and_input(capsys: pytest.CaptureFixture[str]) -> None:
    assert commands.main(["dev-run"]) == 0
    assert "[WF-01] result: [Hello, workflow!]" in capsys.readouterr().out
    assert (
        commands.main(["dev-run", "--workflow", "wf-03", "--input", '{"score":40}'])
        == 0
    )
    assert "[WF-03] result: needs_work" in capsys.readouterr().out
    with pytest.raises(SystemExit) as exit:
        commands.main(["dev-run", "--help"])
    assert exit.value.code == 0
    help_text = capsys.readouterr().out
    assert "--workflow" in help_text and "--input" in help_text


def test_input_and_execution_exit_codes(capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        commands.main(["dev-run", "--workflow", "wf-03", "--input", '{"score":101}'])
        == 2
    )
    assert "Input error" in capsys.readouterr().err
    with patch.object(steps, "decorate_message", side_effect=ValueError("broken step")):
        assert commands.main(["dev-run"]) == 1
    output = capsys.readouterr()
    assert "wf-01 EXECUTE failed" in output.err
    assert "result:" not in output.out


def test_forwarding_is_raw_and_only_explicit_options() -> None:
    raw = '{"score": "new schema with spaces"}'
    with patch.object(commands, "present_release", return_value=17) as launch:
        assert (
            commands.main(
                ["run", "--version", "0.1.0", "--workflow", "future-id", "--input", raw]
            )
            == 17
        )
        launch.assert_called_once_with(
            "0.1.0", ["--workflow", "future-id", "--input", raw]
        )
    with patch.object(commands, "present_release", return_value=0) as launch:
        assert commands.main(["run"]) == 0
        launch.assert_called_once_with(None, [])


def test_direct_module_default() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "agent_playbook"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "[WF-01] result: [Hello, workflow!]" in result.stdout


def test_explicit_configuration_is_forwarded_to_selected_release() -> None:
    with patch.object(commands, "present_release", return_value=0) as launch:
        assert (
            commands.main(["run", "--config", "/path with spaces/settings.yaml"]) == 0
        )
        launch.assert_called_once_with(
            None, ["--config", "/path with spaces/settings.yaml"]
        )


def test_configured_aliases_and_phase_exit_codes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    selected = tmp_path / "settings.yaml"
    selected.write_text(fixture.read_text())
    for alias, raw, expected in (
        ("wf-02-custom", None, "24"),
        ("wf-02-custom", '{"initial":2}', "0"),
        ("wf-03-custom", None, "needs_work"),
        ("wf-03-custom", '{"score":60}', "pass"),
    ):
        arguments = ["dev-run", "--config", str(selected), "--workflow", alias]
        if raw is not None:
            arguments.extend(["--input", raw])
        assert commands.main(arguments) == 0
        assert f"[{alias.upper()}] result: {expected}" in capsys.readouterr().out
    assert (
        commands.main(["dev-run", "--config", str(selected), "--workflow", "missing"])
        == 2
    )
    assert "Input error" in capsys.readouterr().err
    assert (
        commands.main(
            [
                "dev-run",
                "--config",
                str(selected),
                "--workflow",
                "wf-02-custom",
                "--input",
                '{"initial":true}',
            ]
        )
        == 2
    )
    error = capsys.readouterr()
    assert "wf-02-custom PREPARE" in error.err and "initial (int_type)" in error.err
    assert "result:" not in error.out


@pytest.mark.parametrize(
    "target,phase",
    [
        ("__init__", "CONSTRUCTION"),
        ("_execute", "EXECUTE"),
        ("_validate_output", "VALIDATE_OUTPUT"),
        ("_serialize_output", "SERIALIZE_OUTPUT"),
        ("_prepare", "PREPARE"),
    ],
)
def test_all_runtime_failure_phases_exit_one_without_result(
    target: str, phase: str, capsys: pytest.CaptureFixture[str]
) -> None:
    from agent_playbook.workflows.errors import WorkflowInputError, WorkflowOrderError
    from agent_playbook.workflows.wf_01_step_sequence.workflow import (
        StepSequenceWorkflow,
    )

    original: Exception = (
        WorkflowInputError("constructor private")
        if target == "__init__"
        else WorkflowOrderError("order private")
        if target == "_prepare"
        else ValueError("phase private")
    )
    with patch.object(StepSequenceWorkflow, target, side_effect=original):
        assert commands.main(["dev-run"]) == 1
    output = capsys.readouterr()
    assert f"wf-01 {phase} failed" in output.err
    assert "result:" not in output.out
    assert "private" not in output.err
