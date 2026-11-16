"""LG contracts using real SDK export and independently maintained workflows."""

import logging
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from opentelemetry.instrumentation.logging.handler import (  # pyright: ignore[reportMissingTypeStubs]
    LoggingHandler,
)
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    InMemoryLogRecordExporter,
    SimpleLogRecordProcessor,
)

from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.config.loader import load_configuration
from agent_playbook.config.models import LoggingSettings
from agent_playbook.context.models import ExecutionContext, ObservabilityContext
from agent_playbook.observability.adapters.otel_logging.connection import (
    check_connection,
)
from agent_playbook.observability.adapters.otel_logging.runtime import logging_scope
from agent_playbook.observability.logging import log_debug, log_error, log_info, logger


@pytest.fixture
def exported() -> Iterator[InMemoryLogRecordExporter]:
    exporter = InMemoryLogRecordExporter()
    provider = LoggerProvider(shutdown_on_exit=False)
    provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))
    handler = LoggingHandler(logger_provider=provider, log_code_attributes=True)
    previous = logger.level
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    try:
        yield exporter
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous)
        provider.shutdown()


def context() -> ExecutionContext:
    return ExecutionContext(
        observability=ObservabilityContext(workflow_id="fixture", workflow_run_id="run")
    )


def test_lg01_lg02_lg11_context_schema_filter_and_replacement(
    exported: InMemoryLogRecordExporter, capsys: pytest.CaptureFixture[str]
) -> None:
    parent = context()
    a = parent.for_agent(agent_type="coder", agent_run_id="A")
    b = parent.for_agent(agent_type="reviewer", agent_run_id="B")
    for item in (parent, a, parent, b, context()):
        log_info(
            item,
            "selected",
            fields={"attempt": 2, "correlation_id": "bad", "nested": {}},  # pyright: ignore[reportArgumentType]
        )  # type: ignore[arg-type]
    records = [r.log_record for r in exported.get_finished_logs()]
    assert len(records) == 5
    for record, item in zip(records, (parent, a, parent, b, None), strict=True):
        assert (
            record.body == "selected"
            and record.timestamp
            and record.severity_text == "INFO"
        )
        assert record.attributes is not None and record.attributes["attempt"] == 2
        assert record.attributes["correlation_id"] != "bad"
        if item:
            assert record.attributes["correlation_id"] == item.correlation_id
        if item in (a, b):
            assert record.attributes["agent_run_id"] == item.observability.agent_run_id
        else:
            assert "agent_run_id" not in record.attributes
    assert parent.observability.agent_run_id is None
    assert "bad" not in capsys.readouterr().err
    logger.setLevel(logging.INFO)
    log_debug(parent, "filtered")
    assert len(exported.get_finished_logs()) == 5


def test_lg03_native_exception_chain(exported: InMemoryLogRecordExporter) -> None:
    try:
        try:
            raise ValueError("inner")
        except ValueError as error:
            raise RuntimeError("outer") from error
    except RuntimeError as error:
        log_error(context(), "failed", exception=error)
    attributes = exported.get_finished_logs()[0].log_record.attributes
    assert attributes and attributes["exception.type"] == "RuntimeError"
    assert "ValueError: inner" in str(attributes["exception.stacktrace"])
    assert "RuntimeError: outer" in str(attributes["exception.stacktrace"])
    assert "locals" not in attributes


def test_lg04_defaults_and_endpoint_rejection() -> None:
    assert not LoggingSettings().enabled and LoggingSettings().level == "DEBUG"
    for endpoint in (
        "http://example.org:9428/insert/opentelemetry/v1/logs",
        "http://127.0.0.1/insert/opentelemetry/v1/logs",
        "http://127.0.0.1:9428/wrong",
        "http://u:p@127.0.0.1:9428/insert/opentelemetry/v1/logs",
    ):
        with pytest.raises(ValueError):
            LoggingSettings(endpoint=endpoint)


def test_lg04_precedence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    config = tmp_path / "application.yaml"
    config.write_text(
        fixture.read_text()
        .replace("empty-secrets.env", str(fixture.with_name("empty-secrets.env")))
        .replace(
            "integrations:\n",
            "integrations:\n  logging:\n    enabled: true\n    level: WARNING\n",
        )
    )
    config.with_name("application.local.yaml").write_text(
        "integrations:\n  logging:\n    level: INFO\n"
    )
    assert load_configuration(str(config)).integrations.logging.level == "INFO"
    monkeypatch.setenv("AGENT_PLAYBOOK_LOGGING_LEVEL", "ERROR")
    assert load_configuration(str(config)).integrations.logging.level == "ERROR"


@pytest.mark.parametrize("failure", [False, True])
def test_lg05_lg06_lg07_lg09_runner_faults(
    exported: InMemoryLogRecordExporter,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: bool,
) -> None:
    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    monkeypatch.setenv("AGENT_PLAYBOOK_CONFIG", str(fixture))
    with patch(
        "agent_playbook.observability.adapters.langfuse.runtime.flush_tracing",
        side_effect=RuntimeError("SECRET_SENTINEL"),
    ):
        if failure:
            with pytest.raises(Exception):
                run_workflow("wf-02", "[")
        else:
            assert run_workflow("wf-02").serialized_output == "20"
            assert run_workflow("wf-02").serialized_output == "20"
    records = [r.log_record for r in exported.get_finished_logs()]
    assert len([r for r in records if r.body == "Workflow failed"]) == int(failure)
    assert len([r for r in records if r.body == "Workflow completed"]) == (
        0 if failure else 2
    )
    assert "SECRET_SENTINEL" not in str(records) + capsys.readouterr().err


def test_lg05_lg06_initialization_and_handler_cleanup(
    capsys: pytest.CaptureFixture[str],
) -> None:
    before = list(logger.handlers)
    with patch(
        "agent_playbook.observability.adapters.otel_logging.runtime.OTLPLogExporter",
        side_effect=RuntimeError("SECRET_SENTINEL"),
    ):
        with logging_scope(LoggingSettings(enabled=True)):
            pass
    assert logger.handlers == before
    assert "SECRET_SENTINEL" not in capsys.readouterr().err
    with patch.object(logger, "log", side_effect=RuntimeError("SECRET_SENTINEL")):
        log_error(context(), "safe")
    assert "SECRET_SENTINEL" not in capsys.readouterr().err


@pytest.mark.parametrize(
    "status, expected",
    [(200, "ok"), (401, "auth_failed"), (302, "failed"), (500, "failed")],
)
def test_lg12_health(status: int, expected: str) -> None:
    with patch("requests.Session.get") as request:
        request.return_value.status_code = status
        result = check_connection(LoggingSettings(enabled=True))
        assert result.status == expected and result.authentication == "not_applicable"
        assert request.call_args.kwargs == {"timeout": 5, "allow_redirects": False}
        assert request.call_args.args[0] == "http://127.0.0.1:9428/health"
    assert check_connection(LoggingSettings()).status == "skipped"


@pytest.mark.parametrize("operation", ["entry", "update", "exit"])
@pytest.mark.parametrize("business_failure", [False, True])
def test_lg06_native_fault_preserves_business(
    operation: str, business_failure: bool, capsys: pytest.CaptureFixture[str]
) -> None:
    from unittest.mock import MagicMock

    from pydantic import SecretStr

    from agent_playbook.config.models import LangfuseSettings
    from agent_playbook.workflows.errors import WorkflowExecutionError

    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    settings = load_configuration(str(fixture))
    settings = settings.model_copy(
        update={
            "integrations": settings.integrations.model_copy(
                update={
                    "langfuse": LangfuseSettings(
                        enabled=True,
                        public_key=SecretStr("public"),
                        secret_key=SecretStr("SECRET_SENTINEL"),
                    )
                }
            )
        }
    )
    client = MagicMock()
    manager = client.start_as_current_observation.return_value
    if operation == "entry":
        manager.__enter__.side_effect = RuntimeError("SECRET_SENTINEL")
    elif operation == "exit":
        manager.__exit__.side_effect = RuntimeError("SECRET_SENTINEL")
    else:
        client.update_current_span.side_effect = RuntimeError("SECRET_SENTINEL")
    cause = ValueError("business cause")
    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=settings,
        ),
        patch(
            "agent_playbook.application.workflow_runner.get_client", return_value=client
        ),
        patch(
            "agent_playbook.workflows.wf_02_shared_state.steps.multiply",
            side_effect=cause if business_failure else None,
            return_value=20,
        ) as step,
    ):
        if business_failure:
            with pytest.raises(WorkflowExecutionError) as caught:
                run_workflow("wf-02")
            assert caught.value.__cause__ is cause
        else:
            assert run_workflow("wf-02").workflow_id == "wf-02"
        assert step.call_count == 1
    assert "SECRET_SENTINEL" not in capsys.readouterr().err


def test_lg05_langfuse_initialization_warns_and_disables(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from pydantic import SecretStr

    from agent_playbook.application.assembly import assemble_runtime
    from agent_playbook.config.models import LangfuseSettings

    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    base = load_configuration(str(fixture))
    enabled = base.model_copy(
        update={
            "integrations": base.integrations.model_copy(
                update={
                    "langfuse": LangfuseSettings(
                        enabled=True,
                        public_key=SecretStr("public"),
                        secret_key=SecretStr("SECRET_SENTINEL"),
                    )
                }
            )
        }
    )
    with (
        patch("agent_playbook.config.loader.load_configuration", return_value=enabled),
        patch(
            "agent_playbook.observability.adapters.langfuse.runtime.initialize_tracing",
            side_effect=RuntimeError("SECRET_SENTINEL"),
        ),
    ):
        settings = assemble_runtime(str(fixture))
    assert not settings.integrations.langfuse.enabled
    assert "SECRET_SENTINEL" not in capsys.readouterr().err
    with patch(
        "agent_playbook.observability.adapters.langfuse.runtime.initialize_tracing"
    ) as initialize:
        assemble_runtime(str(fixture))
        initialize.assert_not_called()


def test_lg12_unreachable_and_script(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    import requests

    from tooling.logging.check_services import main

    with patch("requests.Session.get", side_effect=requests.Timeout("SECRET_SENTINEL")):
        assert check_connection(LoggingSettings(enabled=True)).status == "unreachable"
    with patch(
        "sys.argv", ["check_services", "--config", str(tmp_path / "missing.yaml")]
    ):
        assert main() == 2
    assert "SECRET_SENTINEL" not in capsys.readouterr().out


def test_lg08_log_only_keeps_global_trace_provider(
    exported: InMemoryLogRecordExporter,
) -> None:
    from opentelemetry import trace

    provider = trace.get_tracer_provider()
    active = trace.get_current_span().get_span_context()
    log_info(context(), "log without trace")
    assert trace.get_tracer_provider() is provider
    assert trace.get_current_span().get_span_context() == active
    record = exported.get_finished_logs()[0].log_record
    assert record.trace_id == active.trace_id


def test_lg12_script_reports_failed_enabled_component(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from agent_playbook.observability.adapters.langfuse.connection import (
        ConnectionResult as TraceResult,
    )
    from agent_playbook.observability.adapters.otel_logging.connection import (
        ConnectionResult as LogResult,
    )
    from tooling.logging.check_services import main

    fixture = Path(__file__).parents[1] / "fixtures/offline.yaml"
    with (
        patch("sys.argv", ["check_services", "--config", str(fixture)]),
        patch(
            "tooling.logging.check_services.check_langfuse",
            return_value=TraceResult("skipped", "http://localhost:3000"),
        ),
        patch(
            "tooling.logging.check_services.check_logging",
            return_value=LogResult("unreachable"),
        ),
    ):
        assert main() == 1
    assert (
        "logging: unreachable; authentication: not_applicable"
        in capsys.readouterr().out
    )
