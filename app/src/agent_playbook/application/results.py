"""Small shared success/error contracts; workflow state stays with its owner."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RunResult:
    workflow_id: str
    output: str


class WorkflowInputError(ValueError):
    """The request was rejected before executing any workflow steps."""


class WorkflowExecutionError(RuntimeError):
    """A selected workflow failed; __cause__ retains the original exception."""
