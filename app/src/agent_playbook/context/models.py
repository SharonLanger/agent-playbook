"""Immutable application identity for one workflow invocation."""

from dataclasses import dataclass, field, replace
from uuid import uuid4


@dataclass(frozen=True, kw_only=True)
class ObservabilityContext:
    workflow_id: str
    workflow_run_id: str
    agent_type: str | None = None
    agent_run_id: str | None = None


@dataclass(frozen=True, kw_only=True)
class ExecutionContext:
    observability: ObservabilityContext
    correlation_id: str = field(default_factory=lambda: str(uuid4()))

    def for_agent(self, *, agent_type: str, agent_run_id: str) -> "ExecutionContext":
        return replace(
            self,
            observability=replace(
                self.observability, agent_type=agent_type, agent_run_id=agent_run_id
            ),
        )
