from pathlib import Path
from typing import Literal

from crewai.flow import Flow, listen, or_, router, start
from crewai.flow.persistence import SQLiteFlowPersistence, persist
from pydantic import BaseModel, Field

DATABASE = Path(__file__).parent / ".runtime" / "flow_states.db"
DATABASE.parent.mkdir(exist_ok=True)


class ExampleState(BaseModel):
    company: str = "Example Co"
    employees: int = 5000
    summary: str = ""
    tier: str = ""
    runs: int = 0
    calls: list[str] = Field(default_factory=list)


@persist(SQLiteFlowPersistence(str(DATABASE)))
class ExampleFlow(Flow[ExampleState]):
    @start()
    def enrich(self) -> int:
        self.state.runs += 1
        self.state.calls.append("enrich")
        self.state.summary = f"{self.state.company}: {self.state.employees} employees"
        return self.state.employees

    @router(enrich)
    def classify(self, employees: int) -> Literal["enterprise", "smb"]:
        return "enterprise" if employees >= 1000 else "smb"

    @listen("enterprise")
    def account_team(self) -> str:
        self.state.tier = "enterprise"
        self.state.calls.append("account_team")
        return self.state.tier

    @listen("smb")
    def nurture_team(self) -> str:
        self.state.tier = "smb"
        self.state.calls.append("nurture_team")
        return self.state.tier

    @listen(or_(account_team, nurture_team))
    def record(self) -> str:
        self.state.calls.append("record")
        return f"{self.state.tier}: run {self.state.runs}"
