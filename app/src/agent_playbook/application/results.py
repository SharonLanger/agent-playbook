"""Immutable result with a native value and its CLI presentation."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from agent_playbook.workflows.errors import WorkflowExecutionError, WorkflowInputError

OutputT_co = TypeVar("OutputT_co", covariant=True)


@dataclass(frozen=True)
class RunResult(Generic[OutputT_co]):
    workflow_id: str
    output: OutputT_co
    serialized_output: str


__all__ = ["RunResult", "WorkflowExecutionError", "WorkflowInputError"]
