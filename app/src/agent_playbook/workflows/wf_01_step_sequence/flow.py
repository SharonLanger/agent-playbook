"""WF-01: pass a returned string through a start/listen chain."""

from crewai.flow.flow import Flow, FlowState, listen, start

from agent_playbook.workflows.wf_01_step_sequence import steps


class StepSequenceFlow(Flow[FlowState]):
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
