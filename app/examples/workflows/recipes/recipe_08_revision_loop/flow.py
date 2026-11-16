"""Standalone deterministic CrewAI Flow; no application or sibling imports."""

from typing import Literal

from crewai.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field


class RecipeState(BaseModel):
    accept_on_attempt: int = Field(default=3, ge=1, le=10)
    max_attempts: int = Field(default=4, ge=1, le=10)
    attempt: int = 0
    revision: str = ""
    accepted: bool = False
    events: list[str] = Field(default_factory=list)
    result: dict = Field(default_factory=dict)


class RecipeFlow(Flow[RecipeState]):
    def mark(self, event: str) -> None:
        self.state.events.append(event)
        print(event, flush=True)

    @start()
    def initialize(self):
        self.mark("attempt:0")

    @listen(or_(initialize, "review_revise"))
    def fake_coder(self):
        self.state.attempt += 1
        self.state.revision = f"revision-{self.state.attempt}"
        self.mark(f"coder:{self.state.attempt}")

    @listen(fake_coder)
    def fake_reviewer(self):
        self.state.accepted = self.state.attempt >= self.state.accept_on_attempt
        self.mark(f"reviewer:{self.state.attempt}")

    @router(fake_reviewer)
    def decide_acceptance(self) -> Literal["review_accepted", "review_check_limit"]:
        return "review_accepted" if self.state.accepted else "review_check_limit"

    @router("review_check_limit")
    def check_limit(self) -> Literal["review_revise", "review_limit_reached"]:
        return (
            "review_limit_reached"
            if self.state.attempt >= self.state.max_attempts
            else "review_revise"
        )

    @listen(or_("review_accepted", "review_limit_reached"))
    def report(self):
        self.mark("report")
        self.state.result = {
            "status": "accepted" if self.state.accepted else "limit_reached",
            "attempts": self.state.attempt,
            "revision": self.state.revision,
        }
        return self.state.result
