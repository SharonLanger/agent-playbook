"""WF-03: route to exactly one terminal listener; no join is needed."""

from crewai.flow.flow import Flow, listen, router, start
from pydantic import PrivateAttr

from agent_playbook.context.models import ExecutionContext
from agent_playbook.workflows.wf_03_conditional_route import steps
from agent_playbook.workflows.wf_03_conditional_route.state import Decision, ScoreState


class ConditionalRouteFlow(Flow[ScoreState]):
    _app_context: ExecutionContext = PrivateAttr()

    def __init__(
        self,
        *,
        context: ExecutionContext,
        initial_state: ScoreState | None = None,
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
    def begin(self) -> int:
        print("[WF-03] begin started")
        print("[WF-03] begin finished")
        return self.state.score

    @router(begin)
    def choose(self, score: int) -> Decision:
        print("[WF-03] choose started")
        decision = steps.decide(score)
        print("[WF-03] choose finished")
        return decision

    @listen("pass")
    def accept(self) -> Decision:
        print("[WF-03] accept started")
        self.state.decision = "pass"
        print("[WF-03] accept finished")
        return "pass"

    @listen("needs_work")
    def revise(self) -> Decision:
        print("[WF-03] revise started")
        self.state.decision = "needs_work"
        print("[WF-03] revise finished")
        return "needs_work"
