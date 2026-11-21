"""RUN integration against the real SDK, runner, ABC and maintained Flows."""

import json
import os
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
        .replace("show_framework_events: false", "show_framework_events: true")
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
        ("wf-03", '{"score":60}', "pass", {"begin", "choose", "accept"}),
        ("wf-03", '{"score":59}', "needs_work", {"begin", "choose", "revise"}),
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
    attrs = root.attributes or {}
    assert json.loads(str(attrs["langfuse.observation.input"])) == (
        {} if raw is None else json.loads(raw)
    )
    observed_output = attrs["langfuse.observation.output"]
    assert (
        observed_output
        if isinstance(result.output, str)
        else json.loads(str(observed_output))
    ) == result.output
    assert (
        kickoff.name
        == {
            "wf-01": "StepSequenceFlow.kickoff",
            "wf-02": "SharedStateFlow.kickoff",
            "wf-03": "ConditionalRouteFlow.kickoff",
        }[workflow]
    )
    # LangfuseResourceManager scopes its tracer to the public project identifier.
    assert root.instrumentation_scope is not None
    assert root.instrumentation_scope.attributes == {
        "public_key": os.environ["LANGFUSE_PUBLIC_KEY"],
    }
    assert (
        kickoff.parent is not None
        and kickoff.parent.span_id == span_context(root).span_id
    )
    steps = [s for s in exported if (s.attributes or {}).get("flow.node.name")]
    assert {str((s.attributes or {})["flow.node.name"]) for s in steps} == nodes
    assert all(
        s.name
        == kickoff.name.removesuffix("kickoff")
        + str((s.attributes or {})["flow.node.name"])
        for s in steps
    )
    assert (kickoff.attributes or {}).get("flow_id")
    assert all(
        s.parent is not None and s.parent.span_id == span_context(kickoff).span_id
        for s in steps
    )
    by_id = {span_context(s).span_id: s for s in exported}
    for child in exported:
        if child.parent is not None:
            parent = by_id[child.parent.span_id]
            assert parent.start_time is not None and parent.end_time is not None
            assert child.start_time is not None and child.end_time is not None
            assert (
                parent.start_time
                <= child.start_time
                <= child.end_time
                <= parent.end_time
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
    for span in exported:
        scope = span.instrumentation_scope
        scope_attributes = dict(scope.attributes or {}) if scope else {}
        if "public_key" in scope_attributes:
            assert scope is not None and scope.name == "langfuse-sdk"
            assert (
                scope_attributes.pop("public_key") == os.environ["LANGFUSE_PUBLIC_KEY"]
            )
        # Only that native public scope identifier is exempt from payload policy.
        for forbidden in (
            "CONFIGURATION_SECRET_SENTINEL",
            "pk-lf-",
            "ApplicationSettings(",
        ):
            assert forbidden not in json.dumps(
                {
                    "resource": dict(span.resource.attributes),
                    "scope": scope_attributes,
                }
            )
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


def test_repeat_invocations(
    tracing: tuple[Langfuse, InMemorySpanExporter],
) -> None:
    run_workflow("wf-02")
    run_workflow("wf-02")
    roots = [s for s in spans(tracing) if s.name == "wf-02"]
    assert len(roots) == 2 and len(spans(tracing)) == 12
    assert span_context(roots[0]).trace_id != span_context(roots[1]).trace_id
    for field in ("correlation_id", "workflow_run_id"):
        assert metadata(roots[0], field) != metadata(roots[1], field)


@pytest.mark.parametrize("raw", [None, "invalid json"])
def test_external_parent_restoration(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    raw: str | None,
) -> None:
    with tracing[0].start_as_current_observation(name="external") as parent:
        if raw is None:
            run_workflow("wf-01")
        else:
            with pytest.raises(WorkflowInputError):
                run_workflow("wf-01", raw)
        assert tracing[0].get_current_observation_id() == parent.id
    nested = [s for s in spans(tracing) if s.name == "wf-01"]
    assert len(nested) == 1
    assert nested[0].parent is not None
    assert f"{nested[0].parent.span_id:016x}" == parent.id
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
    attrs = exported[0].attributes or {}
    assert "langfuse.observation.output" not in attrs
    if phase in {"CONSTRUCTION", "INPUT", "PREPARE"}:
        assert "langfuse.observation.input" not in attrs


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
        .replace("show_framework_events: false", "show_framework_events: true")
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


def test_explicit_quiet_override_is_preserved(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "false")
    assert run_workflow("wf-01").serialized_output == "[Hello, workflow!]"
    exported = spans(tracing)
    assert len(exported) == 1 and exported[0].name == "wf-01"


def test_committed_framework_default(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from agent_playbook.config.loader import load_configuration

    app = Path(__file__).parents[2]
    selected = tmp_path / "application.yaml"
    selected.write_text(
        (app / "application.yaml")
        .read_text()
        .replace(
            "~/.config/agent-playbook/secrets.env",
            str(app / "tests/fixtures/empty-secrets.env"),
        )
    )
    monkeypatch.setenv("AGENT_PLAYBOOK_LANGFUSE_ENABLED", "false")
    settings = load_configuration(str(selected))
    assert settings.integrations.crewai.show_framework_events is True
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "false")
    assert (
        load_configuration(str(selected)).integrations.crewai.show_framework_events
        is False
    )


def test_round2_simultaneous_production_logs_and_native_traces(
    tracing: tuple[Langfuse, InMemorySpanExporter],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from opentelemetry.sdk._logs.export import InMemoryLogRecordExporter

    from agent_playbook.observability.logging import log_error, logger

    class Recovered(FixtureWorkflow):
        def _execute(self) -> object:
            try:
                raise ValueError("recovered operation")
            except ValueError as error:
                log_error(self.context, "Recovered operation", exception=error)
            return "recovered"

    from opentelemetry.sdk._logs import LoggerProvider

    original_flush = LoggerProvider.force_flush
    cleanups: list[bool] = []

    def flush(provider: LoggerProvider, timeout_millis: int = 30000) -> bool:
        cleanups.append(not trace.get_current_span().get_span_context().is_valid)
        return original_flush(provider, timeout_millis)

    logs = InMemoryLogRecordExporter()
    monkeypatch.setenv("AGENT_PLAYBOOK_LOGGING_ENABLED", "true")
    global_provider = trace.get_tracer_provider()
    handlers = list(logger.handlers)
    with (
        patch.object(LoggerProvider, "force_flush", flush),
        patch(
            "agent_playbook.observability.adapters.otel_logging.runtime.OTLPLogExporter",
            return_value=logs,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"step_sequence": Recovered},
        ),
    ):
        result = run_workflow("wf-01")
    assert result.output == "recovered" and logger.handlers == handlers
    assert cleanups == [True]
    assert trace.get_tracer_provider() is global_provider
    root = next(s for s in spans(tracing) if s.name == "wf-01")
    records = [record.log_record for record in logs.get_finished_logs()]
    assert [r.body for r in records if r.severity_text == "ERROR"] == [
        "Recovered operation"
    ]
    assert records[-1].body == "Workflow completed"
    for record in records:
        assert record.trace_id == span_context(root).trace_id
        assert record.span_id == span_context(root).span_id
        assert record.attributes is not None
        for field in ("correlation_id", "workflow_id", "workflow_run_id"):
            assert record.attributes[field] == metadata(root, field)
    assert root.status.status_code != StatusCode.ERROR
