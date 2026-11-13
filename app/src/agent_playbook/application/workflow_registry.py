"""Stable implementation keys to concrete workflow classes."""

from typing import Mapping

from agent_playbook.workflows.contracts import Workflow


def workflow_registry() -> Mapping[str, type[Workflow[object]]]:
    from agent_playbook.workflows.wf_01_step_sequence.workflow import (
        StepSequenceWorkflow,
    )
    from agent_playbook.workflows.wf_02_shared_state.workflow import SharedStateWorkflow
    from agent_playbook.workflows.wf_03_conditional_route.workflow import (
        ConditionalRouteWorkflow,
    )

    return {
        "step_sequence": StepSequenceWorkflow,
        "shared_state": SharedStateWorkflow,
        "conditional_route": ConditionalRouteWorkflow,
    }
