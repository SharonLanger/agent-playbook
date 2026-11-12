from typing import Literal

from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    score: int = 80
    decision: str = ""
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    def begin(self) -> int:
        self.state.calls.append("begin")
        return self.state.score

    @router(begin)
    def choose(self, score: int) -> Literal["pass", "needs_work"]:
        self.state.calls.append("choose")
        return "pass" if score >= 60 else "needs_work"

    @listen("begin")
    def needs_work(self) -> str:
        self.state.calls.append("needs_work")
        self.state.decision = "needs_work"
        print("method needs_work completed; its NAME can trigger revise")
        return "needs_work"

    @listen("needs_work")
    def revise(self) -> str:
        self.state.calls.append("revise")
        self.state.decision = "needs_work"
        return "needs_work"

    @listen("pass")
    def accept(self) -> str:
        self.state.calls.append("accept")
        self.state.decision = "pass"
        return "pass"
