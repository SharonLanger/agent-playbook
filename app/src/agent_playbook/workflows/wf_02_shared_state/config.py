"""Strict arithmetic defaults for a configured WF-02 instance."""

from pydantic import BaseModel, ConfigDict, Field


class NumberDefaults(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
    initial: int = Field(default=3, ge=-1000, le=1000)
    increment: int = Field(default=2, ge=-1000, le=1000)
    multiplier: int = Field(default=4, ge=-1000, le=1000)


class SharedStateConfig(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
    defaults: NumberDefaults = Field(default_factory=NumberDefaults)
