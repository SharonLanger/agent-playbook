"""WF-02: mutate one typed state owned by this execution."""

from crewai.flow.flow import Flow, listen, start
from pydantic import PrivateAttr

from agent_playbook.context.models import ExecutionContext
from agent_playbook.workflows.wf_02_shared_state import steps
from agent_playbook.workflows.wf_02_shared_state.state import NumberState


class SharedStateFlow(Flow[NumberState]):
    _app_context: ExecutionContext = PrivateAttr()

    def __init__(
        self,
        *,
        context: ExecutionContext,
        initial_state: NumberState | None = None,
        tracing: bool | None = None,
        suppress_flow_events: bool = False,
    ) -> None:
        super().__init__(
            name=type(self).__name__,
            initial_state=initial_state,
            tracing=tracing,
            suppress_flow_events=suppress_flow_events,
        )
        self._app_context = context

    @property
    def context(self) -> ExecutionContext:
        return self._app_context

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
