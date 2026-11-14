"""WF-01: pass a returned string through a start/listen chain."""

from crewai.flow.flow import Flow, FlowState, listen, start
from pydantic import PrivateAttr

from agent_playbook.context.models import ExecutionContext
from agent_playbook.workflows.wf_01_step_sequence import steps


class StepSequenceFlow(Flow[FlowState]):
    _app_context: ExecutionContext = PrivateAttr()

    def __init__(
        self,
        *,
        context: ExecutionContext,
        initial_state: FlowState | None = None,
        tracing: bool | None = None,
        suppress_flow_events: bool = False,
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            tracing=tracing,
            suppress_flow_events=suppress_flow_events,
        )
        self._app_context = context

    @property
    def context(self) -> ExecutionContext:
        return self._app_context

    @start()
    def produce(self) -> str:
        print("[WF-01] produce started")
        message = steps.make_message()
        print("[WF-01] produce finished")
        return message

    @listen(produce)
    def decorate(self, message: str) -> str:
        print("[WF-01] decorate started")
        decorated = steps.decorate_message(message)
        print("[WF-01] decorate finished")
        return decorated

    @listen(decorate)
    def finish(self, message: str) -> str:
        print("[WF-01] finish started")
        print("[WF-01] finish finished")
        return message
