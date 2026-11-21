"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

import asyncio
from typing import Literal

from crewai.flow import Flow, and_, listen, start
from pydantic import BaseModel, Field


class ExpectedCheckFailure(Exception):
    """Only this local business error becomes an outcome."""


class RecipeState(BaseModel):
    failed_checks: list[Literal["A", "B", "C", "D", "E"]] = Field(
        default_factory=lambda: ["A", "B"]
    )
    failure_threshold: int = Field(default=3, ge=1, le=5)
    outcomes: dict[str, dict] = Field(default_factory=dict)
    events: list[str] = Field(default_factory=list)
    result: dict = Field(default_factory=dict)


class RecipeFlow(Flow[RecipeState]):
    def mark(self, event: str) -> None:
        self.state.events.append(event)
        print(event, flush=True)

    @start()
    def begin(self):
        self.mark("input")

    async def check(self, name: str):
        self.mark(f"{name}:start")
        await asyncio.sleep(0.01)
        try:
            if name in self.state.failed_checks:
                raise ExpectedCheckFailure(f"{name} failed its local check")
        except ExpectedCheckFailure as error:
            outcome = {"status": "failed", "reason": str(error)}
        else:
            outcome = {"status": "success", "value": ord(name) - 64}
        self.state.outcomes[name] = outcome
        self.mark(f"{name}:done")

    @listen(begin)
    async def check_a(self):
        await self.check("A")

    @listen(begin)
    async def check_b(self):
        await self.check("B")

    @listen(begin)
    async def check_c(self):
        await self.check("C")

    @listen(begin)
    async def check_d(self):
        await self.check("D")

    @listen(begin)
    async def check_e(self):
        await self.check("E")

    @listen(and_(check_a, check_b, check_c, check_d, check_e))
    def summarize(self):
        self.mark("join")
        failures = sum(
            value["status"] == "failed" for value in self.state.outcomes.values()
        )
        self.state.result = {
            "outcomes": dict(self.state.outcomes),
            "failures": failures,
            "threshold": self.state.failure_threshold,
            "status": "failed"
            if failures >= self.state.failure_threshold
            else "returned",
        }
        self.mark("threshold")
        if failures >= self.state.failure_threshold:
            raise ValueError(
                f"recipe06: {failures} failures >= threshold {self.state.failure_threshold}"
            )
        return self.state.result

    @listen(summarize)
    def report(self):
        self.mark("report")
        return self.state.result
