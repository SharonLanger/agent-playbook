"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

import asyncio
from typing import Literal

from crewai.flow import Flow, and_, listen, or_, router, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    numbers: list[float] = Field(default_factory=lambda: [2, 4, 6], min_length=1)
    mode: Literal["basic", "detailed"] = "detailed"
    sum_delay: float = Field(default=0.01, ge=0, le=1)
    max_delay: float = Field(default=0.02, ge=0, le=1)
    total: float | None = None
    maximum: float | None = None
    events: list[str] = Field(default_factory=list)
    result: dict = Field(default_factory=dict)


class RecipeFlow(Flow[RecipeState]):
    def mark(self, event: str) -> None:
        self.state.events.append(event)
        print(event, flush=True)

    @start()
    def begin(self):
        self.mark("input")

    @router(begin)
    def choose_mode(self) -> Literal["route_basic", "route_detailed"]:
        self.mark(self.state.mode)
        return "route_basic" if self.state.mode == "basic" else "route_detailed"

    @listen("route_basic")
    def basic_sum(self):
        self.mark("basic_sum")
        self.state.total = sum(self.state.numbers)

    @listen("route_detailed")
    def start_detailed(self):
        self.mark("detailed_start")

    @listen(start_detailed)
    async def detailed_sum(self):
        self.mark("sum:start")
        await asyncio.sleep(self.state.sum_delay)
        self.state.total = sum(self.state.numbers)
        self.mark("sum:done")

    @listen(start_detailed)
    async def detailed_max(self):
        self.mark("max:start")
        await asyncio.sleep(self.state.max_delay)
        self.state.maximum = max(self.state.numbers)
        self.mark("max:done")

    @listen(and_(detailed_sum, detailed_max))
    def combine(self):
        self.mark("join")

    @listen(or_(basic_sum, combine))
    def report(self):
        self.mark("report")
        self.state.result = {
            "mode": self.state.mode,
            "sum": self.state.total,
            "max": self.state.maximum,
        }
        return self.state.result
