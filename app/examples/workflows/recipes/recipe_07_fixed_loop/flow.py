"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

from typing import Literal

from crewai.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    iterations: int = Field(default=3, ge=1, le=10)
    counter: int = 0
    values: list[int] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    result: dict = Field(default_factory=dict)


class RecipeFlow(Flow[RecipeState]):
    def mark(self, event: str) -> None:
        self.state.events.append(event)
        print(event, flush=True)

    @start()
    def initialize(self):
        self.mark("counter:0")

    @listen(or_(initialize, "loop_again"))
    def work(self):
        self.state.counter += 1
        self.state.values.append(self.state.counter * 2)
        self.mark(f"work:{self.state.counter}")

    @router(work)
    def check_bound(self) -> Literal["loop_again", "loop_done"]:
        return (
            "loop_again" if self.state.counter < self.state.iterations else "loop_done"
        )

    @listen("loop_done")
    def report(self):
        self.mark("report")
        self.state.result = {
            "count": self.state.counter,
            "values": list(self.state.values),
        }
        return self.state.result
