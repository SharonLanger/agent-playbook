from typing import Literal

from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    amount: int = 5000
    country: str = "DE"
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    def receive(self) -> int:
        self.state.calls.append("receive")
        return self.state.amount

    @router(receive)
    def check_amount(self, amount: int) -> Literal["large_order", "small_order"]:
        self.state.calls.append("check_amount")
        return "large_order" if amount > 1000 else "small_order"

    @router("large_order")
    def check_country(self) -> Literal["domestic_review", "export_review"]:
        self.state.calls.append("check_country")
        return "domestic_review" if self.state.country == "US" else "export_review"

    @listen("small_order")
    def auto_approve(self) -> str:
        self.state.calls.append("auto_approve")
        return "automatic"

    @listen("domestic_review")
    def domestic(self) -> str:
        self.state.calls.append("domestic")
        return "domestic"

    @listen("export_review")
    def export(self) -> str:
        self.state.calls.append("export")
        return "export"
