import pytest
from pydantic import ValidationError

from agent_playbook.workflows.wf_03_conditional_route.state import ScoreInput


@pytest.mark.parametrize(
    "data",
    [
        {"score": -1},
        {"score": 101},
        {"score": "80"},
        {"score": True},
        {"score": 80.0},
        {"decision": "pass"},
        {"id": "injected"},
    ],
)
def test_invalid_score_input(data: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        ScoreInput.model_validate(data)
