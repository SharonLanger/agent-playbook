from unittest.mock import patch

import pytest

from agent_playbook.workflows.wf_02_shared_state import steps
from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
from agent_playbook.workflows.wf_02_shared_state.state import NumberState


@pytest.mark.parametrize(
    ("initial", "increment", "multiplier", "history"),
    [
        (3, 2, 4, [3, 5, 20]),
        (10, -2, 3, [10, 8, 24]),
        (3, 2, 0, [3, 5, 0]),
        (-1000, 0, 1, [-1000, -1000, -1000]),
        (1000, 0, -1, [1000, 1000, -1000]),
    ],
)
def test_kickoff_state(
    initial: int, increment: int, multiplier: int, history: list[int]
) -> None:
    flow = SharedStateFlow(
        initial_state=NumberState(
            initial=initial, increment=increment, multiplier=multiplier
        ),
        tracing=False,
        suppress_flow_events=True,
    )
    assert flow.kickoff() == history[-1]
    assert flow.state.history == history
    assert flow.state.value == history[-1]


def test_independent_runs() -> None:
    first = SharedStateFlow(tracing=False, suppress_flow_events=True)
    second = SharedStateFlow(
        initial_state=NumberState(initial=10, increment=-2, multiplier=3),
        tracing=False,
        suppress_flow_events=True,
    )
    assert first.kickoff() == 20
    assert second.kickoff() == 24
    assert first.state.history == [3, 5, 20]
    assert second.state.history == [10, 8, 24]


def test_failed_add_skips_multiply(capsys: pytest.CaptureFixture[str]) -> None:
    flow = SharedStateFlow(tracing=False, suppress_flow_events=True)
    with patch.object(steps, "add", side_effect=RuntimeError("add failed")):
        with pytest.raises(RuntimeError, match="add failed"):
            flow.kickoff()
    assert flow.state.history == [3]
    assert "[WF-02] multiply started" not in capsys.readouterr().out
