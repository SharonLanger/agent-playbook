"""Shared workflow boundary errors."""


class WorkflowInputError(ValueError):
    """Explicit rejection of request input during preparation."""


class WorkflowExecutionError(RuntimeError):
    """Failure during setup, execution, validation or serialization."""


class WorkflowOrderError(RuntimeError):
    """A public lifecycle method was called out of order."""
