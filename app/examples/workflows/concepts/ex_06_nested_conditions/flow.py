import asyncio

from crewai.flow import Flow, and_, listen, or_, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    delay_a: float = Field(default=0.02, ge=0, le=2)
    delay_b: float = Field(default=0.04, ge=0, le=2)
    delay_c: float = Field(default=0.06, ge=0, le=2)
    joined_count: int = 0
    join_payload: str = ""
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    async def a(self) -> str:
        self.state.calls.append("a_started")
        await asyncio.sleep(self.state.delay_a)
        self.state.calls.append("a_finished")
        return "A"

    @start()
    async def b(self) -> str:
        self.state.calls.append("b_started")
        await asyncio.sleep(self.state.delay_b)
        self.state.calls.append("b_finished")
        return "B"

    @start()
    async def c(self) -> str:
        self.state.calls.append("c_started")
        await asyncio.sleep(self.state.delay_c)
        self.state.calls.append("c_finished")
        return "C"

    @listen(and_(a, or_(b, c)))
    def joined(self, value: str) -> str:
        self.state.joined_count += 1
        self.state.join_payload = value
        self.state.calls.append("joined")
        return "joined"
