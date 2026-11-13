"""Strict default score for a configured WF-03 instance."""

from pydantic import BaseModel, ConfigDict, Field


class ScoreDefaults(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
    score: int = Field(default=80, ge=0, le=100)


class ConditionalRouteConfig(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
    defaults: ScoreDefaults = Field(default_factory=ScoreDefaults)
