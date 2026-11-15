"""Context follows real wrappers into CrewAI Flow instances."""

from unittest.mock import patch

import pytest

from agent_playbook.config.models import CrewAISettings
from agent_playbook.context.models import ExecutionContext, ObservabilityContext
from agent_playbook.workflows.wf_01_step_sequence.workflow import StepSequenceWorkflow
from agent_playbook.workflows.wf_02_shared_state.workflow import SharedStateWorkflow
from agent_playbook.workflows.wf_03_conditional_route.workflow import (
    ConditionalRouteWorkflow,
)

SETTINGS = CrewAISettings(
    usage_telemetry_enabled=False, tracing_enabled=False, show_framework_events=False
)


@pytest.mark.parametrize(
    "implementation,data,expected",
    [
        (StepSequenceWorkflow, {}, "[Hello, workflow!]"),
        (SharedStateWorkflow, {}, 20),
        (ConditionalRouteWorkflow, {"score": 80}, "pass"),
        (ConditionalRouteWorkflow, {"score": 40}, "needs_work"),
    ],
)
def test_real_flow_keeps_context_out_of_business_state_and_serialization(
    implementation: type[StepSequenceWorkflow]
    | type[SharedStateWorkflow]
    | type[ConditionalRouteWorkflow],
    data: dict[str, object],
    expected: object,
) -> None:
    context = ExecutionContext(
        observability=ObservabilityContext(
            workflow_id="distinct-workflow",
            workflow_run_id="distinct-run",
            agent_type="distinct-agent-type",
            agent_run_id="distinct-agent-run",
        ),
        correlation_id="distinct-correlation",
    )
    workflow = implementation(settings=SETTINGS, config={}, context=context)
    workflow.prepare(data)
    flow = vars(workflow)["_flow"]
    assert workflow.context is flow.context is context
    assert flow.tracing is False
    assert flow.suppress_flow_events is True
    forbidden = (
        "_app_context",
        "context",
        "observability",
        "correlation_id",
        "workflow_id",
        "workflow_run_id",
        "agent_type",
        "agent_run_id",
        "distinct-correlation",
        "distinct-workflow",
        "distinct-run",
        "distinct-agent-type",
        "distinct-agent-run",
    )
    before = flow.model_dump()
    assert "execution_context" in before  # CrewAI's own field is unchanged.
    for value in forbidden:
        assert value not in before
        if value != "context":
            assert value not in str(before)
        assert value not in str(flow.state)
    raw = workflow.execute()
    assert workflow.validate_output(raw) == expected
    assert flow.context is context
    after = flow.model_dump()
    assert "execution_context" in after
    for value in forbidden:
        assert value not in after
        if value != "context":
            assert value not in str(after)
        assert value not in str(flow.state)


def test_consecutive_flows_keep_original_context_and_result() -> None:
    first_context = ExecutionContext(
        observability=ObservabilityContext(
            workflow_id="wf-02", workflow_run_id="first"
        ),
        correlation_id="group",
    )
    second_context = ExecutionContext(
        observability=ObservabilityContext(
            workflow_id="wf-02", workflow_run_id="second"
        ),
        correlation_id="group",
    )
    first = SharedStateWorkflow(settings=SETTINGS, config={}, context=first_context)
    first.prepare({})
    first_result = first.validate_output(first.execute())
    second = SharedStateWorkflow(settings=SETTINGS, config={}, context=second_context)
    second.prepare({})
    assert second.validate_output(second.execute()) == first_result == 20
    assert first.context is first_context
    assert first.context.observability.workflow_run_id == "first"
    assert vars(first)["_flow"].state.value == 20
    from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow

    execution_error = RuntimeError("second kickoff failure")
    second_failing = SharedStateWorkflow(
        settings=SETTINGS, config={}, context=second_context
    )
    second_failing.prepare({})
    with patch.object(SharedStateFlow, "kickoff", side_effect=execution_error):
        with pytest.raises(RuntimeError) as caught:
            second_failing.execute()
    assert caught.value is execution_error
    assert first.context is first_context
    assert vars(first)["_flow"].context is first_context
    assert vars(first)["_flow"].state.value == first_result
    assert first.result == first_result
    failing = SharedStateWorkflow(settings=SETTINGS, config={}, context=second_context)
    with pytest.raises(Exception):
        failing.prepare({"initial": "invalid"})
    assert first.context is first_context
    assert vars(first)["_flow"].state.value == first_result


@pytest.mark.parametrize(
    "score,selected,skipped", [(80, "accept", "revise"), (40, "revise", "accept")]
)
def test_scheduled_decorated_paths_can_read_context(
    monkeypatch: pytest.MonkeyPatch, score: int, selected: str, skipped: str
) -> None:
    from agent_playbook.workflows.wf_03_conditional_route.flow import (
        ConditionalRouteFlow,
    )
    from agent_playbook.workflows.wf_03_conditional_route.state import ScoreState

    context = ExecutionContext(
        observability=ObservabilityContext(
            workflow_id="wf-03", workflow_run_id="scheduled"
        ),
        correlation_id="scheduled-correlation",
    )
    observed: list[str] = []
    original_begin = ConditionalRouteFlow.begin
    original_choose = ConditionalRouteFlow.choose
    original_accept = ConditionalRouteFlow.accept
    original_revise = ConditionalRouteFlow.revise

    def begin(self: ConditionalRouteFlow) -> int:
        assert self.context is context
        observed.append("begin")
        return original_begin(self)

    def choose(self: ConditionalRouteFlow, value: int) -> str:
        assert self.context is context
        observed.append("choose")
        return original_choose(self, value)

    def accept(self: ConditionalRouteFlow) -> str:
        assert self.context is context
        observed.append("accept")
        return original_accept(self)

    def revise(self: ConditionalRouteFlow) -> str:
        assert self.context is context
        observed.append("revise")
        return original_revise(self)

    monkeypatch.setattr(ConditionalRouteFlow, "begin", begin)
    monkeypatch.setattr(ConditionalRouteFlow, "choose", choose)
    monkeypatch.setattr(ConditionalRouteFlow, "accept", accept)
    monkeypatch.setattr(ConditionalRouteFlow, "revise", revise)
    flow = ConditionalRouteFlow(
        context=context,
        initial_state=ScoreState(score=score),
        tracing=False,
        suppress_flow_events=True,
    )
    assert flow.kickoff() == ("pass" if score == 80 else "needs_work")
    assert observed == ["begin", "choose", selected]
    assert skipped not in observed
