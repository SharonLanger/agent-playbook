from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.application.results import (
    WorkflowExecutionError,
    WorkflowInputError,
)
from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.workflows.wf_01_step_sequence import steps


@pytest.mark.parametrize(
    ("workflow", "raw"),
    [
        ("unknown", None),
        ("wf-01", ""),
        ("wf-01", "[]"),
        ("wf-01", "null"),
        ("wf-01", "3"),
        ("wf-01", '{"unknown":1}'),
        ("wf-02", '{"initial":true}'),
        ("wf-03", '{"score":101}'),
    ],
)
def test_invalid_input_starts_no_steps(
    workflow: str, raw: str | None, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(WorkflowInputError):
        run_workflow(workflow, raw)
    assert "started" not in capsys.readouterr().out


def test_selected_results_and_fresh_runs(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_workflow().output == "[Hello, workflow!]"
    assert run_workflow("wf-02").output == 20
    assert (
        run_workflow("wf-02", '{"initial":10,"increment":-2,"multiplier":3}').output
        == 24
    )
    assert run_workflow("wf-02").output == 20
    capsys.readouterr()
    result = run_workflow("wf-03", '{"score":40}')
    assert result.workflow_id == "wf-03" and result.output == "needs_work"
    output = capsys.readouterr().out
    assert "WF-01" not in output and "WF-02" not in output


def test_step_value_error_keeps_execution_category_and_cause() -> None:
    original = ValueError("step bug")
    with patch.object(steps, "decorate_message", side_effect=original):
        with pytest.raises(WorkflowExecutionError) as failure:
            run_workflow()
    assert failure.value.__cause__ is original


def test_configuration_precedes_unknown_workflow(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="Cannot read"):
        run_workflow("unknown", config_path=str(tmp_path / "missing.yaml"))
