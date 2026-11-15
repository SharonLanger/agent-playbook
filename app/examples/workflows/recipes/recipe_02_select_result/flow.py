"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

import asyncio

from crewai.flow import Flow, and_, listen, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    score_a: float = 70
    score_b: float = 90
    delay_a: float = Field(default=0.01, ge=0, le=1)
    delay_b: float = Field(default=0.02, ge=0, le=1)
    candidate_a: dict = Field(default_factory=dict)
    candidate_b: dict = Field(default_factory=dict)
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
    async def make_a(self):
        self.mark("A:start")
        await asyncio.sleep(self.state.delay_a)
        self.state.candidate_a = {"name": "A", "score": self.state.score_a}
        self.mark("A:done")

    @listen(begin)
    async def make_b(self):
        self.mark("B:start")
        await asyncio.sleep(self.state.delay_b)
        self.state.candidate_b = {"name": "B", "score": self.state.score_b}
        self.mark("B:done")

    @listen(and_(make_a, make_b))
    def choose(self):
        self.mark("join")
        # Python policy: highest score after ALL complete; A wins a tie.
        self.state.result = (
            self.state.candidate_a
            if self.state.score_a >= self.state.score_b
            else self.state.candidate_b
        )
        return self.state.result

    @listen(choose)
    def report(self):
        self.mark("report")
        return self.state.result
