"""Identity and isolation of application context without provider imports."""

from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from agent_playbook.context.models import ExecutionContext, ObservabilityContext


def root(run: str, correlation: str | None = None) -> ExecutionContext:
    identity = ObservabilityContext(workflow_id="selected", workflow_run_id=run)
    if correlation is None:
        return ExecutionContext(observability=identity)
    return ExecutionContext(observability=identity, correlation_id=correlation)


def test_fresh_identity_and_explicit_reuse() -> None:
    first, second = root("run-a"), root("run-b")
    for value in (first, second):
        assert str(UUID(value.correlation_id, version=4)) == value.correlation_id
        assert value.observability.agent_type is None
        assert value.observability.agent_run_id is None
    assert first.correlation_id != second.correlation_id
    reused = root("other-run", first.correlation_id)
    assert reused.correlation_id == first.correlation_id
    assert reused.observability.workflow_run_id != first.observability.workflow_run_id
    assert first.observability.workflow_run_id == "run-a"


def test_children_and_nested_helpers_preserve_parent_and_siblings() -> None:
    parent = root("nondefault-run", "nondefault-correlation")
    children = [
        parent.for_agent(agent_type=role, agent_run_id=run)
        for role, run in (("reviewer", "A1"), ("coder", "B1"), ("reviewer", "A2"))
    ]
    assert len({id(child) for child in children}) == 3
    assert len({id(child.observability) for child in children}) == 3
    for child in children:
        assert child is not parent and child.observability is not parent.observability
        assert child.correlation_id == parent.correlation_id
        assert child.observability.workflow_id == parent.observability.workflow_id
        assert (
            child.observability.workflow_run_id == parent.observability.workflow_run_id
        )
    assert [
        (child.observability.agent_type, child.observability.agent_run_id)
        for child in children
    ] == [("reviewer", "A1"), ("coder", "B1"), ("reviewer", "A2")]

    seen: list[ExecutionContext] = []

    def inner(value: ExecutionContext, fail: bool = False) -> ExecutionContext:
        seen.append(value)
        if fail:
            raise ValueError("injected")
        return value

    def outer(value: ExecutionContext, fail: bool = False) -> ExecutionContext:
        seen.append(value)
        result = inner(value, fail)
        assert result is value
        return result

    assert outer(children[0]) is children[0]
    with pytest.raises(ValueError, match="injected"):
        outer(children[1], fail=True)
    assert seen[0] is seen[1] is children[0]
    assert seen[2] is seen[3] is children[1]
    assert parent.observability.agent_type is parent.observability.agent_run_id is None
    assert children[1].observability.agent_type == "coder"
    assert children[1].observability.agent_run_id == "B1"
    assert children[2].observability.agent_run_id == "A2"


def test_ordinary_assignment_is_rejected() -> None:
    value = root("run")
    with pytest.raises(FrozenInstanceError):
        setattr(value, "correlation_id", "changed")
    with pytest.raises(FrozenInstanceError):
        setattr(value.observability, "workflow_id", "changed")
    assert value.observability.workflow_id == "selected"
    child = value.for_agent(agent_type="reviewer", agent_run_id="agent-1")
    with pytest.raises(FrozenInstanceError):
        setattr(child.observability, "agent_run_id", "changed")
    assert child.observability.agent_run_id == "agent-1"
    assert value.correlation_id != "changed"


def test_context_only_fresh_process_has_no_provider_or_network() -> None:
    import subprocess
    import sys

    program = """import sys
from agent_playbook.context.models import ExecutionContext, ObservabilityContext

def audit(event, args):
    if event.startswith("socket."):
        raise AssertionError(event)
sys.addaudithook(audit)
root = ExecutionContext(observability=ObservabilityContext(workflow_id="a", workflow_run_id="b"))
assert root.for_agent(agent_type="x", agent_run_id="y").correlation_id == root.correlation_id
assert not any(name.startswith(("crewai", "langfuse", "opentelemetry")) for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
