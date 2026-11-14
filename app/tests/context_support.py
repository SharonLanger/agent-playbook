"""Explicit identity for maintained direct-constructor tests."""

from agent_playbook.context.models import ExecutionContext, ObservabilityContext

TEST_CONTEXT = ExecutionContext(
    observability=ObservabilityContext(workflow_id="test", workflow_run_id="test-run"),
    correlation_id="test-correlation",
)
