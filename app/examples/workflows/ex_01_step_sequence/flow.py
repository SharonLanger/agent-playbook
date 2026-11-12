from crewai.flow import Flow, listen, start
from pydantic import BaseModel, Field


class ExampleState(BaseModel):
    calls: list[str] = Field(default_factory=list)


class ExampleFlow(Flow[ExampleState]):
    @start()
    def produce(self) -> str:
        self.state.calls.append("produce")
        print("produce returns Hello")
        return "Hello"

    @listen(produce)
    def decorate(self, message: str) -> str:
        self.state.calls.append("decorate")
        print(f"decorate received {message!r}")
        return f"[{message}]"

    @listen(decorate)
    def finish(self, message: str) -> str:
        self.state.calls.append("finish")
        print(f"finish received {message!r}")
        return message
