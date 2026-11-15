"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

import asyncio

from crewai.flow import Flow, and_, listen, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    fail_a: bool = True
    delay_a: float = Field(default=0.01, ge=0, le=1)
    delay_b: float = Field(default=0.04, ge=0, le=1)
    value_a: str | None = None
    value_b: str | None = None
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
    async def branch_a(self):
        self.mark("A:start")
        await asyncio.sleep(self.state.delay_a)
        if self.state.fail_a:
            self.mark("A:error")
            raise ValueError("recipe05: deliberate A failure")
        self.state.value_a = "A complete"
        self.mark("A:done")

    @listen(begin)
    async def branch_b(self):
        self.mark("B:start")
        try:
            await asyncio.sleep(self.state.delay_b)
            self.state.value_b = "B complete"
            self.mark("B:done")
        except asyncio.CancelledError:
            self.mark("B:cancelled")
            raise

    @listen(and_(branch_a, branch_b))
    def combine(self):
        self.mark("join")
        self.state.result = {"A": self.state.value_a, "B": self.state.value_b}
        return self.state.result

    @listen(combine)
    def report(self):
        self.mark("report")
        return self.state.result
