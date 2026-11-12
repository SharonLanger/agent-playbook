"""Select and construct a fresh workflow; import only after runtime assembly."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from agent_playbook.application.results import WorkflowInputError

if TYPE_CHECKING:
    from agent_playbook.config.models import CrewAISettings
    from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow
    from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
    from agent_playbook.workflows.wf_03_conditional_route.flow import (
        ConditionalRouteFlow,
    )

type WorkflowId = Literal["wf-01", "wf-02", "wf-03"]


def validate_workflow_id(workflow_id: str) -> WorkflowId:
    if workflow_id == "wf-01" or workflow_id == "wf-02" or workflow_id == "wf-03":
        return workflow_id
    raise WorkflowInputError(
        f"Unknown workflow {workflow_id!r}; use wf-01, wf-02 or wf-03."
    )


def create_workflow(
    workflow_id: WorkflowId, data: dict[str, object], settings: CrewAISettings
) -> StepSequenceFlow | SharedStateFlow | ConditionalRouteFlow:
    if workflow_id == "wf-01":
        from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow

        if data:
            raise WorkflowInputError(
                "wf-01 accepts no input fields; use {} or omit --input."
            )
        return StepSequenceFlow(
            tracing=settings.tracing_enabled,
            suppress_flow_events=not settings.show_framework_events,
        )
    if workflow_id == "wf-02":
        from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
        from agent_playbook.workflows.wf_02_shared_state.state import (
            NumberInput,
            NumberState,
        )

        numbers = NumberInput.model_validate(data)
        return SharedStateFlow(
            initial_state=NumberState(
                initial=numbers.initial,
                increment=numbers.increment,
                multiplier=numbers.multiplier,
            ),
            tracing=settings.tracing_enabled,
            suppress_flow_events=not settings.show_framework_events,
        )
    from agent_playbook.workflows.wf_03_conditional_route.flow import (
        ConditionalRouteFlow,
    )
    from agent_playbook.workflows.wf_03_conditional_route.state import (
        ScoreInput,
        ScoreState,
    )

    score = ScoreInput.model_validate(data)
    return ConditionalRouteFlow(
        initial_state=ScoreState(score=score.score),
        tracing=settings.tracing_enabled,
        suppress_flow_events=not settings.show_framework_events,
    )
