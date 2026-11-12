"""The score threshold belongs to WF-03, not the shared runner."""

from agent_playbook.workflows.wf_03_conditional_route.state import Decision

PASS_THRESHOLD = 60


def decide(score: int) -> Decision:
    return "pass" if score >= PASS_THRESHOLD else "needs_work"
