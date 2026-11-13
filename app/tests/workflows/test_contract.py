"""Lifecycle transitions, failure records, and typed result storage."""

from dataclasses import dataclass
from inspect import isabstract
from typing import Mapping

import pytest

from agent_playbook.config.models import CrewAISettings
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowOrderError
from agent_playbook.workflows.lifecycle import WorkflowPhase, WorkflowStatus

SETTINGS = CrewAISettings(
    usage_telemetry_enabled=False, tracing_enabled=False, show_framework_events=False
)


@dataclass(frozen=True)
class ReviewResult:
    scores: tuple[int, ...]


class Probe(Workflow[ReviewResult | None]):
    def __init__(
        self,
        *,
        settings: CrewAISettings = SETTINGS,
        config: Mapping[str, object] = {},
        fail: WorkflowPhase | None = None,
    ) -> None:
        super().__init__(settings=settings, config=config)
        self.fail = fail
        self.seen: list[WorkflowStatus] = []
        self.value: ReviewResult | None = ReviewResult((2, 3))

    def _record(self, phase: WorkflowPhase) -> None:
        self.seen.append(self.status)
        if self.fail is phase:
            raise ValueError("private payload")

    def _prepare(self, data: Mapping[str, object]) -> None:
        self._record(WorkflowPhase.PREPARE)

    def _execute(self) -> object:
        self._record(WorkflowPhase.EXECUTE)
        return self.value

    def _validate_output(self, output: object) -> ReviewResult | None:
        self._record(WorkflowPhase.VALIDATE_OUTPUT)
        if output is not None and not isinstance(output, ReviewResult):
            raise TypeError("review result required")
        return output

    def _serialize_output(self) -> str:
        self._record(WorkflowPhase.SERIALIZE_OUTPUT)
        return str(self.result)


def test_complete_sequence_and_independent_results() -> None:
    first = Probe()
    second = Probe()
    with pytest.raises(WorkflowOrderError):
        _ = first.result
    with pytest.raises(WorkflowOrderError):
        first.execute()
    assert first.status is WorkflowStatus.CREATED
    first.prepare({})
    assert first.status is WorkflowStatus.PREPARED
    raw = first.execute()
    assert first.status is WorkflowStatus.EXECUTED
    result = first.validate_output(raw)
    assert result is first.result
    assert first.serialize_output() == str(result)
    assert first.status is WorkflowStatus.COMPLETED
    assert first.seen == [
        WorkflowStatus.PREPARING,
        WorkflowStatus.EXECUTING,
        WorkflowStatus.VALIDATING_OUTPUT,
        WorkflowStatus.SERIALIZING,
    ]
    with pytest.raises(WorkflowOrderError):
        first.prepare({})
    assert len(first.seen) == 4
    assert second.status is WorkflowStatus.CREATED
    second.value = None
    second.prepare({})
    assert second.validate_output(second.execute()) is None
    assert second.result is None


@pytest.mark.parametrize("phase", list(WorkflowPhase))
def test_hook_failure_is_terminal_and_preserves_cause(phase: WorkflowPhase) -> None:
    probe = Probe(fail=phase)
    with pytest.raises(ValueError) as failure:
        probe.prepare({})
        raw = probe.execute()
        probe.validate_output(raw)
        probe.serialize_output()
    assert probe.status is WorkflowStatus.FAILED
    assert probe.failure is not None
    assert probe.failure.phase is phase
    assert probe.failure.cause is failure.value
    with pytest.raises(WorkflowOrderError):
        probe.prepare({})
    assert probe.failure.cause is failure.value


def test_abstract_hooks_required() -> None:
    assert isabstract(Workflow)
