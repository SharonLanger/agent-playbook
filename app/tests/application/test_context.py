"""Actual runner, factory and wrapper context propagation."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.application.assembly import assemble_runtime
from agent_playbook.application.workflow_factory import (
    construct_workflow,
    create_workflow,
)
from agent_playbook.application.workflow_registry import workflow_registry
from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.context.models import ExecutionContext, ObservabilityContext
from agent_playbook.workflows.errors import WorkflowExecutionError

FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"


def test_runner_fresh_roots_and_alias(tmp_path: Path) -> None:
    config = tmp_path / "configuration.yaml"
    (tmp_path / "empty-secrets.env").write_text("")
    config.write_text(FIXTURE.read_text() + "  alias: {implementation: shared_state}\n")
    with patch(
        "agent_playbook.application.workflow_runner.construct_workflow",
        wraps=construct_workflow,
    ) as constructor:
        assert run_workflow("wf-02", config_path=str(config)).output == 20
        assert run_workflow("wf-02", config_path=str(config)).output == 20
        assert run_workflow("alias", config_path=str(config)).output == 20
    observed = [call.kwargs["context"] for call in constructor.call_args_list]
    assert all(isinstance(value, ExecutionContext) for value in observed)
    assert [x.observability.workflow_id for x in observed] == [
        "wf-02",
        "wf-02",
        "alias",
    ]
    assert len({id(x) for x in observed}) == 3
    assert len({x.correlation_id for x in observed}) == 3
    assert len({x.observability.workflow_run_id for x in observed}) == 3
    assert all(
        x.observability.agent_type is x.observability.agent_run_id is None
        for x in observed
    )


@pytest.mark.parametrize("selected", ["wf-01", "wf-02", "wf-03"])
def test_factory_forwarding(selected: str) -> None:
    application = assemble_runtime(str(FIXTURE))
    registry = workflow_registry()
    context = ExecutionContext(
        observability=ObservabilityContext(workflow_id=selected, workflow_run_id="run"),
        correlation_id="corr",
    )
    first = create_workflow(
        selected,
        application,
        application.integrations.crewai,
        registry,
        context=context,
    )
    assert first.context is context
    implementation = next(typ for typ in registry.values() if isinstance(first, typ))
    second = construct_workflow(
        selected, implementation, application.integrations.crewai, {}, context=context
    )
    assert second.context is context and second is not first


def test_context_construction_failure_has_existing_boundary() -> None:
    error = RuntimeError("injected")
    with patch(
        "agent_playbook.application.workflow_runner.ExecutionContext", side_effect=error
    ):
        with pytest.raises(
            WorkflowExecutionError, match="wf-01 CONSTRUCTION"
        ) as caught:
            run_workflow("wf-01", config_path=str(FIXTURE))
    assert caught.value.__cause__ is error


def test_runner_context_reaches_each_real_flow() -> None:
    from crewai.flow.flow import FlowState

    from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow
    from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
    from agent_playbook.workflows.wf_02_shared_state.state import NumberState
    from agent_playbook.workflows.wf_03_conditional_route.flow import (
        ConditionalRouteFlow,
    )
    from agent_playbook.workflows.wf_03_conditional_route.state import ScoreState

    seen_01: list[StepSequenceFlow] = []
    seen_02: list[SharedStateFlow] = []
    seen_03: list[ConditionalRouteFlow] = []

    def make_01(
        *,
        context: ExecutionContext,
        initial_state: FlowState | None = None,
        tracing: bool | None = None,
        suppress_flow_events: bool = False,
    ) -> StepSequenceFlow:
        flow = StepSequenceFlow(
            context=context,
            initial_state=initial_state,
            tracing=tracing,
            suppress_flow_events=suppress_flow_events,
        )
        seen_01.append(flow)
        return flow

    def make_02(
        *,
        context: ExecutionContext,
        initial_state: NumberState | None = None,
        tracing: bool | None = None,
        suppress_flow_events: bool = False,
    ) -> SharedStateFlow:
        flow = SharedStateFlow(
            context=context,
            initial_state=initial_state,
            tracing=tracing,
            suppress_flow_events=suppress_flow_events,
        )
        seen_02.append(flow)
        return flow

    def make_03(
        *,
        context: ExecutionContext,
        initial_state: ScoreState | None = None,
        tracing: bool | None = None,
        suppress_flow_events: bool = False,
    ) -> ConditionalRouteFlow:
        flow = ConditionalRouteFlow(
            context=context,
            initial_state=initial_state,
            tracing=tracing,
            suppress_flow_events=suppress_flow_events,
        )
        seen_03.append(flow)
        return flow

    cases = [
        (
            "wf-01",
            "agent_playbook.workflows.wf_01_step_sequence.flow.StepSequenceFlow",
            make_01,
            seen_01,
            "[Hello, workflow!]",
        ),
        (
            "wf-02",
            "agent_playbook.workflows.wf_02_shared_state.flow.SharedStateFlow",
            make_02,
            seen_02,
            20,
        ),
        (
            "wf-03",
            "agent_playbook.workflows.wf_03_conditional_route.flow.ConditionalRouteFlow",
            make_03,
            seen_03,
            "pass",
        ),
    ]
    for selected, flow_path, maker, seen, expected in cases:
        with (
            patch(
                "agent_playbook.application.workflow_runner.construct_workflow",
                wraps=construct_workflow,
            ) as factory,
            patch(flow_path, side_effect=maker),
        ):
            assert run_workflow(selected, config_path=str(FIXTURE)).output == expected
        assert factory.call_count == 1
        runner_context = factory.call_args.kwargs["context"]
        assert len(seen) == 1
        assert seen[0].context is runner_context
        assert runner_context.observability.workflow_id == selected
