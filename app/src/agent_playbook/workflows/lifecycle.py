"""In-memory status for a single workflow attempt."""

from dataclasses import dataclass
from enum import Enum, auto


class WorkflowStatus(Enum):
    CREATED = auto()
    PREPARING = auto()
    PREPARED = auto()
    EXECUTING = auto()
    EXECUTED = auto()
    VALIDATING_OUTPUT = auto()
    OUTPUT_VALIDATED = auto()
    SERIALIZING = auto()
    COMPLETED = auto()
    FAILED = auto()


class WorkflowPhase(Enum):
    PREPARE = auto()
    EXECUTE = auto()
    VALIDATE_OUTPUT = auto()
    SERIALIZE_OUTPUT = auto()


@dataclass(frozen=True)
class WorkflowFailure:
    phase: WorkflowPhase
    cause: Exception
