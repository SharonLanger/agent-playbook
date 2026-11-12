from typing import Literal

from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    approved: bool = True
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    def begin(self) -> bool:
        self.state.calls.append("begin")
        return self.state.approved

    @router(begin)
    def choose(self, approved: bool) -> Literal["route_green", "route_red"]:
        self.state.calls.append("choose")
        return "route_green" if approved else "route_red"

    @listen("route_green")
    def accept(self) -> str:
        self.state.calls.append("accept")
        return "accepted"

    @listen("route_red")
    def revise(self) -> str:
        self.state.calls.append("revise")
        return "revision requested"
