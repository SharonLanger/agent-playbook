"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

import asyncio

from crewai.flow import Flow, and_, listen, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    numbers: list[float] = Field(default_factory=lambda: [2, 4, 6], min_length=1)
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

    @listen(begin)
    async def calculate_sum(self):
        self.mark("sum:start")
        await asyncio.sleep(self.state.sum_delay)
        self.state.total = sum(self.state.numbers)
        self.mark("sum:done")

    @listen(begin)
    async def find_maximum(self):
        self.mark("max:start")
        await asyncio.sleep(self.state.max_delay)
        self.state.maximum = max(self.state.numbers)
        self.mark("max:done")

    @listen(and_(calculate_sum, find_maximum))
    def combine(self):
        self.mark("join")
        self.state.result = {"sum": self.state.total, "max": self.state.maximum}
        return self.state.result

    @listen(combine)
    def report(self):
        self.mark("report")
        return self.state.result
