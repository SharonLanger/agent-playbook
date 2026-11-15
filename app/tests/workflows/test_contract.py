"""Lifecycle transitions, failure records, and typed result storage."""

from dataclasses import dataclass
from inspect import isabstract
from typing import Mapping

import pytest

from agent_playbook.config.models import CrewAISettings
from agent_playbook.context.models import ExecutionContext
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowOrderError
from agent_playbook.workflows.lifecycle import WorkflowPhase, WorkflowStatus
from tests.context_support import TEST_CONTEXT

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
        context: ExecutionContext = TEST_CONTEXT,
        fail: WorkflowPhase | None = None,
    ) -> None:
        super().__init__(settings=settings, config=config, context=context)
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


@pytest.mark.parametrize("status", list(WorkflowStatus))
def test_wrong_order_never_mutates_status_or_runs_hook(status: WorkflowStatus) -> None:
    class AtStatus(Probe):
        def set_status(self, value: WorkflowStatus) -> None:
            self._status = value

    probe = AtStatus()
    probe.set_status(status)
    before = probe.failure
    calls = len(probe.seen)
    for required, method in (
        (WorkflowStatus.CREATED, lambda: probe.prepare({})),
        (WorkflowStatus.PREPARED, probe.execute),
        (WorkflowStatus.EXECUTED, lambda: probe.validate_output(None)),
        (WorkflowStatus.OUTPUT_VALIDATED, probe.serialize_output),
    ):
        if status is required:
            continue
        with pytest.raises(WorkflowOrderError):
            method()
        assert probe.status is status and probe.failure is before
        assert len(probe.seen) == calls


def test_reentry_is_rejected_in_progress() -> None:
    class Reentry(Probe):
        def _prepare(self, data: Mapping[str, object]) -> None:
            assert self.status is WorkflowStatus.PREPARING
            with pytest.raises(WorkflowOrderError):
                self.prepare(data)
            super()._prepare(data)

    probe = Reentry()
    probe.prepare({})
    assert probe.status is WorkflowStatus.PREPARED
    assert probe.seen == [WorkflowStatus.PREPARING]


@pytest.mark.parametrize("interruption", [KeyboardInterrupt, SystemExit])
def test_interruptions_propagate(interruption: type[BaseException]) -> None:
    class Interrupted(Probe):
        def _execute(self) -> object:
            raise interruption()

    probe = Interrupted()
    probe.prepare({})
    with pytest.raises(interruption):
        probe.execute()
    assert probe.failure is None


@pytest.mark.parametrize(
    "missing", ["_prepare", "_execute", "_validate_output", "_serialize_output"]
)
def test_each_missing_hook_prevents_instantiation(missing: str) -> None:
    names = ("_prepare", "_execute", "_validate_output", "_serialize_output")
    incomplete = type(
        "Incomplete",
        (Workflow,),
        {name: getattr(Probe, name) for name in names if name != missing},
    )
    with pytest.raises(TypeError, match="abstract"):
        incomplete(settings=SETTINGS, config={}, context=TEST_CONTEXT)


@pytest.mark.parametrize("target", list(WorkflowPhase))
@pytest.mark.parametrize("caught", [True, False])
def test_reentry_in_every_phase(target: WorkflowPhase, caught: bool) -> None:
    class Reentry(Probe):
        def _record(self, phase: WorkflowPhase) -> None:
            if phase is target:
                invoke = {
                    WorkflowPhase.PREPARE: lambda: self.prepare({}),
                    WorkflowPhase.EXECUTE: self.execute,
                    WorkflowPhase.VALIDATE_OUTPUT: lambda: self.validate_output(None),
                    WorkflowPhase.SERIALIZE_OUTPUT: self.serialize_output,
                }[phase]
                if caught:
                    with pytest.raises(WorkflowOrderError):
                        invoke()
                else:
                    invoke()
            super()._record(phase)

    probe = Reentry()
    if caught:
        probe.prepare({})
        probe.validate_output(probe.execute())
        probe.serialize_output()
        assert probe.status is WorkflowStatus.COMPLETED
    else:
        with pytest.raises(WorkflowOrderError):
            probe.prepare({})
            probe.validate_output(probe.execute())
            probe.serialize_output()
        assert probe.failure is not None and probe.failure.phase is target
        assert probe.status is WorkflowStatus.FAILED


@pytest.mark.parametrize("target", list(WorkflowPhase))
@pytest.mark.parametrize("interruption", [KeyboardInterrupt, SystemExit])
def test_same_interruption_object_propagates(
    target: WorkflowPhase, interruption: type[BaseException]
) -> None:
    original = interruption()

    class Interrupted(Probe):
        def _record(self, phase: WorkflowPhase) -> None:
            if phase is target:
                raise original
            super()._record(phase)

    probe = Interrupted()
    with pytest.raises(interruption) as caught:
        probe.prepare({})
        probe.validate_output(probe.execute())
        probe.serialize_output()
    assert caught.value is original and probe.failure is None


def test_serialization_failure_retains_rich_result() -> None:
    probe = Probe(fail=WorkflowPhase.SERIALIZE_OUTPUT)
    probe.prepare({})
    result = probe.validate_output(probe.execute())
    with pytest.raises(ValueError):
        probe.serialize_output()
    assert probe.result is result and probe.status is WorkflowStatus.FAILED


def test_genuine_terminal_instances_reject_every_repeat_without_mutation() -> None:
    completed = Probe()
    completed.prepare({})
    completed.validate_output(completed.execute())
    completed.serialize_output()
    failed = Probe(fail=WorkflowPhase.EXECUTE)
    failed.prepare({})
    with pytest.raises(ValueError):
        failed.execute()
    assert failed.failure is not None
    for probe in (completed, failed):
        status, failure, calls = probe.status, probe.failure, len(probe.seen)
        for invoke in (
            lambda: probe.prepare({}),
            probe.execute,
            lambda: probe.validate_output(None),
            probe.serialize_output,
        ):
            with pytest.raises(WorkflowOrderError):
                invoke()
        assert (probe.status, probe.failure, len(probe.seen)) == (
            status,
            failure,
            calls,
        )


def test_independent_mutable_domain_state_and_failure() -> None:
    first = Probe(fail=WorkflowPhase.EXECUTE)
    second = Probe()
    first.prepare({})
    second.prepare({})
    with pytest.raises(ValueError):
        first.execute()
    result = second.validate_output(second.execute())
    second.serialize_output()
    first.seen.append(WorkflowStatus.FAILED)
    assert first.failure is not None and second.failure is None
    assert second.status is WorkflowStatus.COMPLETED
    assert second.result is result and WorkflowStatus.FAILED not in second.seen
