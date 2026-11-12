from crewai.flow import Flow, listen, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    def produce(self) -> str:
        self.state.calls.append("produce")
        return "route_green"

    @listen(produce)
    def by_reference(self, value: str) -> str:
        self.state.calls.append("by_reference")
        print(f"by_reference received {value!r}")
        return "reference_done"

    @listen("produce")
    def by_name(self, value: str) -> str:
        self.state.calls.append("by_name")
        print(f"by_name received {value!r}")
        return "name_done"

    @listen("route_green")
    def by_value(self) -> str:
        self.state.calls.append("by_value")
        return "unexpected"
