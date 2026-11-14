"""Caller-controlled inputs and computed state have separate schemas."""

from pydantic import BaseModel, ConfigDict, Field


class NumberInput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    initial: int = Field(default=3, ge=-1000, le=1000)
    increment: int = Field(default=2, ge=-1000, le=1000)
    multiplier: int = Field(default=4, ge=-1000, le=1000)


class NumberState(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    initial: int = 3
    increment: int = 2
    multiplier: int = 4
    value: int = 0
    history: list[int] = Field(default_factory=list[int])

