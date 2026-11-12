"""WF-02: mutate one typed state owned by this execution."""

from crewai.flow.flow import Flow, listen, start

from agent_playbook.workflows.wf_02_shared_state import steps
from agent_playbook.workflows.wf_02_shared_state.state import NumberState


class SharedStateFlow(Flow[NumberState]):
    @start()
    def initialize(self) -> None:
        print("[WF-02] initialize started")
        self.state.value = self.state.initial
        self.state.history = [self.state.value]
        print("[WF-02] initialize finished")

    @listen(initialize)
    def add(self) -> None:
        print("[WF-02] add started")
        self.state.value = steps.add(self.state.value, self.state.increment)
        self.state.history.append(self.state.value)
        print("[WF-02] add finished")

    @listen(add)
    def multiply(self) -> None:
        print("[WF-02] multiply started")
        self.state.value = steps.multiply(self.state.value, self.state.multiplier)
        self.state.history.append(self.state.value)
        print("[WF-02] multiply finished")

    @listen(multiply)
    def finish(self) -> int:
        print("[WF-02] finish started")
        print("[WF-02] finish finished")
        return self.state.value
