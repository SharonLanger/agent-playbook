import pytest

from agent_playbook.workflows.wf_03_conditional_route.state import Decision
from agent_playbook.workflows.wf_03_conditional_route.steps import decide


@pytest.mark.parametrize(
    ("score", "expected"),
    [(0, "needs_work"), (59, "needs_work"), (60, "pass"), (100, "pass")],
)
def test_threshold(score: int, expected: Decision) -> None:
    assert decide(score) == expected
