"""Application-facing workflow lifecycle; CrewAI owns step orchestration."""

from abc import ABC, abstractmethod
from typing import Generic, Mapping, TypeVar, final

from agent_playbook.config.models import CrewAISettings
from agent_playbook.context.models import ExecutionContext
from agent_playbook.workflows.errors import WorkflowOrderError
from agent_playbook.workflows.lifecycle import (
    WorkflowFailure,
    WorkflowPhase,
    WorkflowStatus,
)

OutputT_co = TypeVar("OutputT_co", covariant=True)


class Workflow(ABC, Generic[OutputT_co]):
    def __init__(
        self,
        *,
        settings: CrewAISettings,
        config: Mapping[str, object],
        context: ExecutionContext,
    ) -> None:
        self._context = context
        self._settings = settings
        self._config = config
        self._status = WorkflowStatus.CREATED
        self._failure: WorkflowFailure | None = None
        self._result: tuple[OutputT_co] | None = None

    @property
    def context(self) -> ExecutionContext:
        return self._context

    @property
    def status(self) -> WorkflowStatus:
        return self._status

    @property
    def failure(self) -> WorkflowFailure | None:
        return self._failure

    @property
    def result(self) -> OutputT_co:
        if self._result is None:
            raise WorkflowOrderError("Validated result is not available.")
        return self._result[0]

    def _begin(self, required: WorkflowStatus, running: WorkflowStatus) -> None:
        if self._status is not required:
            raise WorkflowOrderError(
                f"Expected {required.name}; current status is {self._status.name}."
            )
        self._status = running

    def _fail(self, phase: WorkflowPhase, error: Exception) -> None:
        self._failure = WorkflowFailure(phase, error)
        self._status = WorkflowStatus.FAILED

    @final
    def prepare(self, data: Mapping[str, object]) -> None:
        self._begin(WorkflowStatus.CREATED, WorkflowStatus.PREPARING)
        try:
            self._prepare(data)
        except Exception as error:
            self._fail(WorkflowPhase.PREPARE, error)
            raise
        self._status = WorkflowStatus.PREPARED

    @final
    def execute(self) -> object:
        self._begin(WorkflowStatus.PREPARED, WorkflowStatus.EXECUTING)
        try:
            output = self._execute()
        except Exception as error:
            self._fail(WorkflowPhase.EXECUTE, error)
            raise
        self._status = WorkflowStatus.EXECUTED
        return output

    @final
    def validate_output(self, output: object) -> OutputT_co:
        self._begin(WorkflowStatus.EXECUTED, WorkflowStatus.VALIDATING_OUTPUT)
        try:
            result = self._validate_output(output)
        except Exception as error:
            self._fail(WorkflowPhase.VALIDATE_OUTPUT, error)
            raise
        self._result = (result,)
        self._status = WorkflowStatus.OUTPUT_VALIDATED
        return result

    @final
    def serialize_output(self) -> str:
        self._begin(WorkflowStatus.OUTPUT_VALIDATED, WorkflowStatus.SERIALIZING)
        try:
            serialized = self._serialize_output()
        except Exception as error:
            self._fail(WorkflowPhase.SERIALIZE_OUTPUT, error)
            raise
        self._status = WorkflowStatus.COMPLETED
        return serialized

    @abstractmethod
    def _prepare(self, data: Mapping[str, object]) -> None: ...

    @abstractmethod
    def _execute(self) -> object: ...

    @abstractmethod
    def _validate_output(self, output: object) -> OutputT_co: ...

    @abstractmethod
    def _serialize_output(self) -> str: ...
