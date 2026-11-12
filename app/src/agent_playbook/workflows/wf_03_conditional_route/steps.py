"""The score threshold belongs to WF-03, not the shared runner."""

from agent_playbook.workflows.wf_03_conditional_route.state import Decision


def decide(score: int) -> Decision:
    return "pass" if score >= 60 else "needs_work"
