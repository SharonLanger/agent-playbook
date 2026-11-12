import pytest
from pydantic import ValidationError

from agent_playbook.workflows.wf_02_shared_state.state import NumberInput, NumberState


@pytest.mark.parametrize(
    "data",
    [
        {"initial": "3"},
        {"initial": True},
        {"increment": 1.5},
        {"multiplier": 1001},
        {"initial": -1001},
        {"history": [999]},
        {"value": 9},
        {"id": "injected"},
    ],
)
def test_rejects_invalid_external_input(data: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        NumberInput.model_validate(data)


def test_bounds_and_state_ownership() -> None:
    assert NumberInput(initial=-1000, increment=1000, multiplier=0).initial == -1000
    first, second = NumberState(), NumberState()
    first.history.append(3)
    assert second.history == []
