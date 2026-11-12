import pytest

from agent_playbook.workflows.wf_02_shared_state.steps import add, multiply


@pytest.mark.parametrize(
    ("initial", "increment", "multiplier", "expected"),
    [(3, 2, 4, 20), (10, -2, 3, 24), (-4, 2, -3, 6), (5, 7, 0, 0)],
)
def test_arithmetic(
    initial: int, increment: int, multiplier: int, expected: int
) -> None:
    assert multiply(add(initial, increment), multiplier) == expected
