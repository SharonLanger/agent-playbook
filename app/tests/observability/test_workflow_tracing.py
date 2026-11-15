"""RUN integration against the real SDK, runner, ABC and maintained Flows."""

import json
from collections.abc import Iterator, Mapping
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest
from langfuse import Langfuse, propagate_attributes
from openinference.instrumentation.crewai import CrewAIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanContext, StatusCode

from agent_playbook.application.workflow_runner import construct_workflow, run_workflow
from agent_playbook.cli.commands import present_workflow
from agent_playbook.config.models import CrewAISettings
from agent_playbook.context.models import ExecutionContext
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowExecutionError, WorkflowInputError


@pytest.fixture
def tracing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> Iterator[tuple[Langfuse, InMemorySpanExporter]]:
    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    config = tmp_path / "tracing.yaml"
    config.write_text(
        fixture.read_text()
        .replace(
            "integrations:\n",
            "integrations:\n  langfuse:\n    enabled: true\n    public_key: {env: LANGFUSE_PUBLIC_KEY}\n    secret_key: {env: LANGFUSE_SECRET_KEY}\n",
        )
        .replace("empty-secrets.env", str(fixture.with_name("empty-secrets.env")))
    )
    monkeypatch.setenv("AGENT_PLAYBOOK_CONFIG", str(config))
    key = f"pk-lf-{uuid4()}"
    monkeypatch.setenv("AGENT_PLAYBOOK_LANGFUSE_ENABLED", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", key)
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "CONFIGURATION_SECRET_SENTINEL")
    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    client = Langfuse(
        public_key=key,
        secret_key="CONFIGURATION_SECRET_SENTINEL",
        base_url="http://localhost:3000",
        tracer_provider=provider,
        span_exporter=exporter,
    )
    instrumentor = CrewAIInstrumentor()
    if instrumentor.is_instrumented_by_opentelemetry:
        instrumentor.uninstrument()
    instrumentor.instrument(tracer_provider=provider)
    with patch(
        "agent_playbook.observability.adapters.langfuse.connection.create_client",
        return_value=client,
    ):
        yield client, exporter
    instrumentor.uninstrument()
    client.shutdown()


def spans(tracing: tuple[Langfuse, InMemorySpanExporter]) -> tuple[ReadableSpan, ...]:
    tracing[0].flush()
    return tracing[1].get_finished_spans()


def span_context(span: ReadableSpan) -> SpanContext:
    result = span.get_span_context()
    assert result is not None
    return result


def metadata(span: ReadableSpan, field: str) -> object:
    value = (span.attributes or {})[f"langfuse.trace.metadata.{field}"]
    assert isinstance(value, str)
    return json.loads(value)


@pytest.mark.parametrize(
    "workflow,raw,expected,nodes",
    [
        ("wf-01", None, "[Hello, workflow!]", {"produce", "decorate", "finish"}),
        ("wf-02", None, "20", {"initialize", "add", "multiply", "finish"}),
        ("wf-03", '{"score":80}', "pass", {"begin", "choose", "accept"}),
        ("wf-03", '{"score":20}', "needs_work", {"begin", "choose", "revise"}),
    ],
)
def test_runner_hierarchy_and_exact_identity(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    workflow: str,
    raw: str | None,
    expected: str,
    nodes: set[str],
) -> None:
    contexts: list[ExecutionContext] = []

    def capture(*args: object, **kwargs: object) -> Workflow[object]:
        context = kwargs["context"]
        assert isinstance(context, ExecutionContext)
        contexts.append(context)
        return construct_workflow(*args, **kwargs)  # type: ignore[arg-type]

    with patch(
        "agent_playbook.application.workflow_runner.construct_workflow",
        side_effect=capture,
    ):
        result = run_workflow(workflow, raw)
    assert expected == result.serialized_output
    exported = spans(tracing)
    # Verify available root evidence before the known missing-child assertion.
    for span in exported:
        assert metadata(span, "correlation_id") == contexts[0].correlation_id
        assert metadata(span, "workflow_id") == workflow
        assert (
            metadata(span, "workflow_run_id")
            == contexts[0].observability.workflow_run_id
        )
        assert span.end_time is not None and span.start_time is not None
        assert span.end_time >= span.start_time
    assert len(exported) == len(nodes) + 2
    root = next(s for s in exported if s.name == workflow)
    kickoff = next(s for s in exported if "kickoff" in s.name)
    assert root.context is not None and kickoff.context is not None
    assert all(s.context is not None for s in exported)
    assert root.parent is None
    assert (
        kickoff.parent is not None
        and kickoff.parent.span_id == span_context(root).span_id
    )
    steps = [s for s in exported if (s.attributes or {}).get("flow.node.name")]
    assert {str((s.attributes or {})["flow.node.name"]) for s in steps} == nodes
    assert all(
        s.parent is not None and s.parent.span_id == span_context(kickoff).span_id
        for s in steps
    )
    assert len({span_context(s).span_id for s in exported}) == len(exported)
    assert {span_context(s).trace_id for s in exported} == {span_context(root).trace_id}
    for span in exported:
        assert metadata(span, "correlation_id") == contexts[0].correlation_id
        assert metadata(span, "workflow_id") == workflow
        assert (
            metadata(span, "workflow_run_id")
            == contexts[0].observability.workflow_run_id
        )
        assert (
            span.end_time is not None
            and span.start_time is not None
            and span.end_time >= span.start_time
        )
    assert not trace.get_current_span().get_span_context().is_valid
    payload = json.dumps(
        [
            {
                "attributes": dict(s.attributes or {}),
                "events": [
                    {"name": e.name, "attributes": dict(e.attributes or {})}
                    for e in s.events
                ],
                "status": s.status.description,
            }
            for s in exported
        ]
    )
    for forbidden in (
        "CONFIGURATION_SECRET_SENTINEL",
        "pk-lf-",
        "_app_context",
        "secrets",
    ):
        assert forbidden not in payload


def test_repeat_and_parent_restoration(
    tracing: tuple[Langfuse, InMemorySpanExporter],
) -> None:
    run_workflow("wf-02")
    run_workflow("wf-02")
    roots = [s for s in spans(tracing) if s.name == "wf-02"]
    assert len(roots) == 2 and len(spans(tracing)) == 12
    assert span_context(roots[0]).trace_id != span_context(roots[1]).trace_id
    for field in ("correlation_id", "workflow_run_id"):
        assert metadata(roots[0], field) != metadata(roots[1], field)
    with tracing[0].start_as_current_observation(name="external") as parent:
        run_workflow("wf-01")
        assert tracing[0].get_current_observation_id() == parent.id
        with pytest.raises(WorkflowInputError):
            run_workflow("wf-01", "invalid json")
        assert tracing[0].get_current_observation_id() == parent.id
    nested = [s for s in spans(tracing) if s.name == "wf-01"]
    assert all(
        s.parent is not None and f"{s.parent.span_id:016x}" == parent.id for s in nested
    )
    assert not trace.get_current_span().get_span_context().is_valid


def test_real_step_failure(tracing: tuple[Langfuse, InMemorySpanExporter]) -> None:
    cause = ValueError("controlled business failure")
    with patch(
        "agent_playbook.workflows.wf_02_shared_state.steps.multiply", side_effect=cause
    ):
        with pytest.raises(WorkflowExecutionError) as caught:
            run_workflow("wf-02")
    assert "EXECUTE" in str(caught.value) and caught.value.__cause__ is cause
    exported = spans(tracing)
    assert len([s for s in exported if s.status.status_code == StatusCode.ERROR]) == 3
    assert not any(
        (s.attributes or {}).get("flow.node.name") == "finish" for s in exported
    )
    assert all(
        s.status.status_code != StatusCode.ERROR
        for s in exported
        if (s.attributes or {}).get("flow.node.name") in {"initialize", "add"}
    )


class FixtureWorkflow(Workflow[str]):
    phase = ""
    cause = ValueError("controlled lifecycle failure")

    def __init__(
        self,
        *,
        settings: CrewAISettings,
        config: Mapping[str, object],
        context: ExecutionContext,
    ) -> None:
        if self.phase == "CONSTRUCTION":
            raise self.cause
        super().__init__(settings=settings, config=config, context=context)

    def _prepare(self, data: Mapping[str, object]) -> None:
        if self.phase == "PREPARE":
            raise self.cause

    def _execute(self) -> object:
        if self.phase == "EXECUTE":
            raise self.cause
        return "done"

    def _validate_output(self, output: object) -> str:
        if self.phase == "VALIDATE_OUTPUT":
            raise self.cause
        return str(output)

    def _serialize_output(self) -> str:
        if self.phase == "SERIALIZE_OUTPUT":
            raise self.cause
        return self.result


@pytest.mark.parametrize(
    "phase",
    [
        "CONSTRUCTION",
        "INPUT",
        "PREPARE",
        "EXECUTE",
        "VALIDATE_OUTPUT",
        "SERIALIZE_OUTPUT",
    ],
)
def test_lifecycle_failure_root(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    monkeypatch.setattr(FixtureWorkflow, "phase", phase)
    with patch(
        "agent_playbook.application.workflow_runner.workflow_registry",
        return_value={"step_sequence": FixtureWorkflow},
    ):
        with pytest.raises(
            WorkflowInputError if phase == "INPUT" else WorkflowExecutionError
        ) as caught:
            run_workflow("wf-01", "[" if phase == "INPUT" else None)
    assert phase in str(caught.value)
    if phase != "INPUT":
        assert caught.value.__cause__ is FixtureWorkflow.cause
    exported = spans(tracing)
    assert len(exported) == 1 and exported[0].status.status_code == StatusCode.ERROR
    assert exported[0].end_time is not None


def test_native_recovery_and_agent_isolation(
    tracing: tuple[Langfuse, InMemorySpanExporter],
) -> None:
    client = tracing[0]
    with client.start_as_current_observation(name="workflow"):
        with propagate_attributes(metadata={"correlation_id": "group"}):
            for agent in ("A", "B"):
                try:
                    with client.start_as_current_observation(name=agent):
                        with propagate_attributes(metadata={"agent_id": agent}):
                            with client.start_as_current_observation(
                                name=f"{agent}/tool"
                            ):
                                if agent == "A":
                                    raise ValueError("recovered")
                except ValueError:
                    pass
                with client.start_as_current_observation(name=f"checkpoint-{agent}"):
                    pass
    exported = spans(tracing)
    assert (
        next(s for s in exported if s.name == "workflow").status.status_code
        != StatusCode.ERROR
    )
    for span in exported:
        assert metadata(span, "correlation_id") == "group"
        if span.name in {"A", "A/tool", "B", "B/tool"}:
            assert metadata(span, "agent_id") == span.name[0]
        else:
            assert "langfuse.trace.metadata.agent_id" not in (span.attributes or {})
    assert all(
        s.status.status_code == StatusCode.ERROR
        for s in exported
        if s.name in {"A", "A/tool"}
    )
    assert all(
        s.status.status_code != StatusCode.ERROR
        for s in exported
        if s.name in {"B", "B/tool"}
    )


@pytest.mark.parametrize("raw,code", [(None, 0), ("[", 2)])
def test_cli_flush_after_close(
    tracing: tuple[Langfuse, InMemorySpanExporter], raw: str | None, code: int
) -> None:
    calls: list[bool] = []

    def flush() -> None:
        calls.append(not trace.get_current_span().get_span_context().is_valid)
        tracing[0].flush()
        assert tracing[1].get_finished_spans()

    with patch(
        "agent_playbook.observability.adapters.langfuse.runtime.flush_tracing",
        side_effect=flush,
    ):
        assert present_workflow("wf-01", raw) == code
    assert calls == [True]


@pytest.mark.parametrize("raw,code", [(None, 0), ("[", 2)])
def test_cleanup_failure_preserves_outcome(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    raw: str | None,
    code: int,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with (
        patch("langfuse.get_client", return_value=tracing[0]),
        patch.object(
            tracing[0], "flush", side_effect=RuntimeError("private cleanup secret")
        ),
    ):
        assert present_workflow("wf-01", raw) == code
    assert "Langfuse delivery attempt failed." in caplog.text
    assert "private cleanup secret" not in caplog.text


@pytest.mark.parametrize("enabled", [False, True])
def test_fresh_process_initialization_and_locality(
    tmp_path: Path, enabled: bool
) -> None:
    import os
    import subprocess
    import sys

    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    config = tmp_path / "application.yaml"
    config.write_text(
        fixture.read_text()
        .replace(
            "integrations:\n",
            "integrations:\n  langfuse:\n    enabled: "
            + str(enabled).lower()
            + "\n    base_url: http://127.0.0.1:3000\n    public_key: {env: LANGFUSE_PUBLIC_KEY}\n    secret_key: {env: LANGFUSE_SECRET_KEY}\n",
        )
        .replace("empty-secrets.env", str(fixture.with_name("empty-secrets.env")))
    )
    env = os.environ.copy()
    env.update(
        AGENT_PLAYBOOK_CONFIG=str(config),
        LANGFUSE_PUBLIC_KEY=f"pk-lf-{uuid4()}",
        LANGFUSE_SECRET_KEY="process-sentinel",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(fixture.with_name("native_tracing_process.py")),
            "enabled" if enabled else "disabled",
        ],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NATIVE_PROCESS_OK" in result.stdout


def test_recovered_child_through_runner(
    tracing: tuple[Langfuse, InMemorySpanExporter],
) -> None:
    class Recovered(FixtureWorkflow):
        def _execute(self) -> object:
            try:
                with tracing[0].start_as_current_observation(name="recoverable-child"):
                    raise ValueError("recoverable business failure")
            except ValueError:
                return "recovered"

    with patch(
        "agent_playbook.application.workflow_runner.workflow_registry",
        return_value={"step_sequence": Recovered},
    ):
        assert run_workflow("wf-01").output == "recovered"
    exported = spans(tracing)
    assert len(exported) == 2
    root = next(s for s in exported if s.name == "wf-01")
    child = next(s for s in exported if s.name == "recoverable-child")
    assert root.status.status_code != StatusCode.ERROR
    assert child.status.status_code == StatusCode.ERROR
    assert (
        child.parent is not None and child.parent.span_id == span_context(root).span_id
    )


def test_cli_flush_execution_failure(
    tracing: tuple[Langfuse, InMemorySpanExporter], capsys: pytest.CaptureFixture[str]
) -> None:
    cause = ValueError("business failure")
    calls: list[bool] = []

    def flush() -> None:
        calls.append(not trace.get_current_span().get_span_context().is_valid)
        tracing[0].flush()

    with (
        patch(
            "agent_playbook.workflows.wf_02_shared_state.steps.multiply",
            side_effect=cause,
        ),
        patch(
            "agent_playbook.observability.adapters.langfuse.runtime.flush_tracing",
            side_effect=flush,
        ),
    ):
        assert present_workflow("wf-02") == 1
    assert calls == [True]
    assert "Workflow failed: wf-02 EXECUTE failed." in capsys.readouterr().err
    assert (
        next(s for s in spans(tracing) if s.name == "wf-02").status.status_code
        == StatusCode.ERROR
    )


def test_setup_failure_needs_no_client(monkeypatch: pytest.MonkeyPatch) -> None:
    from agent_playbook.config.errors import ConfigurationError

    with patch(
        "agent_playbook.application.workflow_runner.assemble_runtime",
        side_effect=ConfigurationError("invalid fixture"),
    ):
        assert present_workflow("wf-01") == 2


@pytest.mark.parametrize("phase", ["", "EXECUTE"])
def test_configuration_excluded_from_root_payload(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    monkeypatch.setattr(FixtureWorkflow, "phase", phase)
    with patch(
        "agent_playbook.application.workflow_runner.workflow_registry",
        return_value={"step_sequence": FixtureWorkflow},
    ):
        if phase:
            with pytest.raises(WorkflowExecutionError):
                run_workflow("wf-01")
        else:
            assert run_workflow("wf-01").output == "done"
    exported = spans(tracing)
    assert len(exported) == 1
    payload = json.dumps(
        [
            {
                "attributes": dict(s.attributes or {}),
                "events": [
                    {"name": e.name, "attributes": dict(e.attributes or {})}
                    for e in s.events
                ],
                "status": s.status.description,
            }
            for s in exported
        ]
    )
    assert (bool(exported[0].events)) is bool(phase)
    for forbidden in (
        "CONFIGURATION_SECRET_SENTINEL",
        "pk-lf-",
        "ExecutionContext(",
        "ApplicationSettings(",
        "_settings",
        "secret_key",
    ):
        assert forbidden not in payload
