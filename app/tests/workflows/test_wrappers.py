"""Concrete wrappers preserve CrewAI behavior and classify phase failures."""

from typing import Mapping
from unittest.mock import patch

import pytest

from agent_playbook.config.models import CrewAISettings
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError
from agent_playbook.workflows.lifecycle import WorkflowPhase, WorkflowStatus
from agent_playbook.workflows.wf_01_step_sequence.workflow import StepSequenceWorkflow
from agent_playbook.workflows.wf_02_shared_state.workflow import SharedStateWorkflow
from agent_playbook.workflows.wf_03_conditional_route.workflow import (
    ConditionalRouteWorkflow,
)

SETTINGS = CrewAISettings(
    usage_telemetry_enabled=False, tracing_enabled=False, show_framework_events=False
)
CASES: tuple[tuple[type[Workflow[object]], str, object], ...] = (
    (StepSequenceWorkflow, "wf_01_step_sequence", "[Hello, workflow!]"),
    (SharedStateWorkflow, "wf_02_shared_state", 20),
    (ConditionalRouteWorkflow, "wf_03_conditional_route", "pass"),
)


@pytest.mark.parametrize("implementation,package,expected", CASES)
def test_real_wrapper_result(
    implementation: type[Workflow[object]], package: str, expected: object
) -> None:
    workflow = implementation(settings=SETTINGS, config={})
    workflow.prepare({})
    assert workflow.validate_output(workflow.execute()) == expected
    assert workflow.result == expected
    assert workflow.serialize_output() == str(expected)
    assert workflow.status is WorkflowStatus.COMPLETED


@pytest.mark.parametrize("implementation,package,expected", CASES)
@pytest.mark.parametrize("phase", list(WorkflowPhase))
def test_wrapper_failure_is_terminal_and_blocks_later_phases(
    implementation: type[Workflow[object]],
    package: str,
    expected: object,
    phase: WorkflowPhase,
) -> None:
    workflow = implementation(settings=SETTINGS, config={})
    original = ValueError("private failure")
    flow_class = {
        "wf_01_step_sequence": "StepSequenceFlow",
        "wf_02_shared_state": "SharedStateFlow",
        "wf_03_conditional_route": "ConditionalRouteFlow",
    }[package]
    target = f"agent_playbook.workflows.{package}.flow.{flow_class}"
    if phase is WorkflowPhase.PREPARE:
        with patch(target, side_effect=original):
            with pytest.raises(ValueError) as caught:
                workflow.prepare({})
    else:
        workflow.prepare({})
        if phase is WorkflowPhase.EXECUTE:
            with patch.object(workflow, "_execute", side_effect=original):
                with pytest.raises(ValueError) as caught:
                    workflow.execute()
        elif phase is WorkflowPhase.VALIDATE_OUTPUT:
            with pytest.raises(TypeError) as caught:
                workflow.execute()
                workflow.validate_output([])
        else:
            workflow.validate_output(workflow.execute())
            with patch.object(workflow, "_serialize_output", side_effect=original):
                with pytest.raises(ValueError) as caught:
                    workflow.serialize_output()
    assert workflow.status is WorkflowStatus.FAILED
    assert workflow.failure is not None
    assert workflow.failure.phase is phase and workflow.failure.cause is caught.value
    if phase is WorkflowPhase.SERIALIZE_OUTPUT:
        assert workflow.result == expected
    with pytest.raises(Exception):
        workflow.serialize_output()


@pytest.mark.parametrize(
    "implementation,invalid",
    [
        (StepSequenceWorkflow, {"extra": 1}),
        (SharedStateWorkflow, {"initial": True}),
        (SharedStateWorkflow, {"initial": 1001}),
        (SharedStateWorkflow, {"initial": "2"}),
        (SharedStateWorkflow, {"other": 1}),
        (ConditionalRouteWorkflow, {"score": -1}),
        (ConditionalRouteWorkflow, {"score": 101}),
        (ConditionalRouteWorkflow, {"score": "80"}),
        (ConditionalRouteWorkflow, {"score": True}),
        (ConditionalRouteWorkflow, {"score": 2.5}),
        (ConditionalRouteWorkflow, {"extra": 1}),
    ],
)
def test_invalid_input_never_constructs_or_kicks_off(
    implementation: type[Workflow[object]], invalid: Mapping[str, object]
) -> None:
    workflow = implementation(settings=SETTINGS, config={})
    with pytest.raises(WorkflowInputError):
        workflow.prepare(invalid)
    assert workflow.status is WorkflowStatus.FAILED
    assert (
        workflow.failure is not None and workflow.failure.phase is WorkflowPhase.PREPARE
    )
    with pytest.raises(Exception):
        workflow.execute()


def test_shared_state_rejects_boolean_output() -> None:
    workflow = SharedStateWorkflow(settings=SETTINGS, config={})
    workflow.prepare({})
    workflow.execute()
    with pytest.raises(TypeError):
        workflow.validate_output(True)
    assert (
        workflow.failure is not None
        and workflow.failure.phase is WorkflowPhase.VALIDATE_OUTPUT
    )
