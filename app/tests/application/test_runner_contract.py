"""Runner uses the public contract and keeps phase-specific failure boundaries."""

from unittest.mock import Mock, patch

import pytest

from agent_playbook.application.results import WorkflowExecutionError
from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.config.models import (
    ApplicationSettings,
    CrewAISettings,
    IntegrationSettings,
)
from agent_playbook.workflows.errors import WorkflowInputError

SETTINGS = CrewAISettings(
    usage_telemetry_enabled=False, tracing_enabled=False, show_framework_events=False
)
APPLICATION = ApplicationSettings(
    integrations=IntegrationSettings(crewai=SETTINGS), workflows={}
)


def test_runner_calls_public_methods_in_order_and_returns_native_object() -> None:
    value = {"nested": [1, 2]}
    workflow = Mock()
    workflow.execute.return_value = "raw"
    workflow.validate_output.return_value = value
    workflow.serialize_output.return_value = "display"
    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={},
        ),
        patch(
            "agent_playbook.application.workflow_runner.create_workflow",
            return_value=workflow,
        ),
    ):
        result = run_workflow("alias", '{"x": 3}')
    assert result.output is value and result.serialized_output == "display"
    assert [call[0] for call in workflow.method_calls] == [
        "prepare",
        "execute",
        "validate_output",
        "serialize_output",
    ]
    workflow.prepare.assert_called_once_with({"x": 3})
    workflow.serialize_output.assert_called_once_with()


@pytest.mark.parametrize(
    "method", ["prepare", "execute", "validate_output", "serialize_output"]
)
def test_failure_stops_later_methods(method: str) -> None:
    workflow = Mock()
    workflow.execute.return_value = 1
    workflow.validate_output.return_value = 1
    getattr(workflow, method).side_effect = ValueError("private-value")
    workflow.failure = None
    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={},
        ),
        patch(
            "agent_playbook.application.workflow_runner.create_workflow",
            return_value=workflow,
        ),
    ):
        with pytest.raises(WorkflowExecutionError) as failure:
            run_workflow("alias")
    assert isinstance(failure.value.__cause__, ValueError)
    assert "private-value" not in str(failure.value)
    names = [call[0] for call in workflow.method_calls]
    assert (
        names
        == ["prepare", "execute", "validate_output", "serialize_output"][: len(names)]
    )
    assert names[-1] == method


def test_prepare_input_error_is_exit_two_category() -> None:
    workflow = Mock()
    workflow.prepare.side_effect = WorkflowInputError("input field rejected")
    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={},
        ),
        patch(
            "agent_playbook.application.workflow_runner.create_workflow",
            return_value=workflow,
        ),
    ):
        with pytest.raises(WorkflowInputError):
            run_workflow("alias")
    workflow.execute.assert_not_called()
