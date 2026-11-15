"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

import asyncio
from typing import Literal

from crewai.flow import Flow, and_, listen, or_, router, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    numbers: list[float] = Field(default_factory=lambda: [2, 4, 6], min_length=1)
    threshold: float = 10
    min_delay: float = Field(default=0.01, ge=0, le=1)
    max_delay: float = Field(default=0.02, ge=0, le=1)
    total: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    events: list[str] = Field(default_factory=list)
    result: dict = Field(default_factory=dict)


class RecipeFlow(Flow[RecipeState]):
    def mark(self, event: str) -> None:
        self.state.events.append(event)
        print(event, flush=True)

    @start()
    def calculate_sum(self):
        self.state.total = sum(self.state.numbers)
        self.mark("sum:done")

    @router(calculate_sum)
    def choose_followup(self) -> Literal["route_simple", "route_more"]:
        expanded = self.state.total > self.state.threshold
        self.mark("above" if expanded else "at_or_below")
        return "route_more" if expanded else "route_simple"

    @listen("route_simple")
    def keep_sum(self):
        self.mark("keep_sum")

    @listen("route_more")
    def start_more(self):
        self.mark("more_start")

    @listen(start_more)
    async def find_minimum(self):
        self.mark("min:start")
        await asyncio.sleep(self.state.min_delay)
        self.state.minimum = min(self.state.numbers)
        self.mark("min:done")

    @listen(start_more)
    async def find_maximum(self):
        self.mark("max:start")
        await asyncio.sleep(self.state.max_delay)
        self.state.maximum = max(self.state.numbers)
        self.mark("max:done")

    @listen(and_(find_minimum, find_maximum))
    def combine(self):
        self.mark("join")

    @listen(or_(keep_sum, combine))
    def report(self):
        self.mark("report")
        self.state.result = {
            "sum": self.state.total,
            "min": self.state.minimum,
            "max": self.state.maximum,
        }
        return self.state.result
