import pytest
from pydantic import field_validator

from agent_playbook.workflows.wf_03_conditional_route.flow import ConditionalRouteFlow
from agent_playbook.workflows.wf_03_conditional_route.state import Decision, ScoreState


@pytest.mark.parametrize(
    ("score", "expected", "chosen", "skipped"),
    [
        (80, "pass", "accept", "revise"),
        (60, "pass", "accept", "revise"),
        (59, "needs_work", "revise", "accept"),
        (40, "needs_work", "revise", "accept"),
    ],
)
def test_exactly_one_route(
    score: int,
    expected: Decision,
    chosen: str,
    skipped: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    flow = ConditionalRouteFlow(
        initial_state=ScoreState(score=score), tracing=False, suppress_flow_events=True
    )
    assert flow.kickoff() == expected
    assert flow.state.decision == expected
    output = capsys.readouterr().out
    assert output.count(f"[WF-03] {chosen} started") == 1
    assert f"[WF-03] {skipped} started" not in output


class RejectingState(ScoreState):
    @field_validator("decision")
    @classmethod
    def reject_terminal_assignment(cls, value: Decision | None) -> Decision | None:
        if value == "needs_work":
            raise ValueError("terminal failed")
        return value


def test_terminal_failure_is_not_a_decision(capsys: pytest.CaptureFixture[str]) -> None:
    flow = ConditionalRouteFlow(
        initial_state=RejectingState(score=40), tracing=False, suppress_flow_events=True
    )
    with pytest.raises(ValueError, match="terminal failed"):
        flow.kickoff()
    assert flow.state.decision is None
    assert "[WF-03] accept started" not in capsys.readouterr().out
