"""A score is input; the route decision is computed by the workflow."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Decision = Literal["pass", "needs_work"]


class ScoreInput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    score: int = Field(default=80, ge=0, le=100)


class ScoreState(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    score: int = 80
    decision: Decision | None = None
