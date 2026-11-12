from typing import Literal

from crewai.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    reviews: int = 0
    target_reviews: int = Field(default=3, ge=1, le=10)
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    def write_draft(self) -> str:
        self.state.calls.append("write_draft")
        return "draft"

    @listen(or_(write_draft, "needs_revision"))
    def review(self) -> int:
        self.state.reviews += 1
        self.state.calls.append(f"review_{self.state.reviews}")
        return self.state.reviews

    @router(review)
    def decide(self, count: int) -> Literal["approved", "needs_revision"]:
        return "approved" if count >= self.state.target_reviews else "needs_revision"

    @listen("approved")
    def publish(self) -> str:
        self.state.calls.append("publish")
        return "published"
