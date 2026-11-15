"""Fresh-process RUN-08/09/15 probe; no backend or framework monkeypatches."""

import sys
from unittest.mock import patch

attempts: list[str] = []


def audit(event: str, args: tuple[object, ...]) -> None:
    if event in {"socket.connect", "socket.getaddrinfo"}:
        attempts.append(event)
        raise RuntimeError("unexpected network attempt")


sys.addaudithook(audit)

from agent_playbook.application.workflow_runner import run_workflow  # noqa: E402
from agent_playbook.cli.commands import present_workflow  # noqa: E402
from agent_playbook.config.loader import load_configuration  # noqa: E402
from agent_playbook.workflows.errors import WorkflowInputError  # noqa: E402

if sys.argv[1] == "disabled":
    assert run_workflow("wf-02").serialized_output == "20"
    assert present_workflow("wf-01") == 0
    try:
        run_workflow("wf-01", "[")
    except WorkflowInputError:
        pass
    else:
        raise AssertionError("invalid input succeeded")
    assert "openinference.instrumentation.crewai" not in sys.modules
    from opentelemetry import trace
    from opentelemetry.trace import ProxyTracerProvider

    assert isinstance(trace.get_tracer_provider(), ProxyTracerProvider)
else:
    from langfuse import Langfuse
    from openinference.instrumentation.crewai import CrewAIInstrumentor
    from opentelemetry import trace
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    exporter = InMemorySpanExporter()
    clients: list[Langfuse] = []

    def create(**kwargs: object) -> Langfuse:
        assert kwargs["base_url"] == "http://127.0.0.1:3000"
        assert kwargs["tracing_enabled"] is True
        client = Langfuse(**kwargs, span_exporter=exporter)  # type: ignore[arg-type]
        clients.append(client)
        return client

    with patch(
        "agent_playbook.observability.adapters.langfuse.connection.Langfuse",
        side_effect=create,
    ):
        assert present_workflow("wf-02") == 0
        assert present_workflow("wf-02") == 0
        assert present_workflow("wf-01", "[") == 2
    assert CrewAIInstrumentor().is_instrumented_by_opentelemetry
    assert len(clients) == 3
    # Native resource caching retains exactly one processor on the shared provider.
    assert trace.get_tracer_provider() is not None
    for client in clients:
        assert client.get_current_trace_id() is None
    roots = [s for s in exporter.get_finished_spans() if s.parent is None]
    assert len(roots) == 3
    contexts = [s.get_span_context() for s in roots]
    assert all(context is not None for context in contexts)
    assert len({context.trace_id for context in contexts if context is not None}) == 3
    assert load_configuration().integrations.crewai.usage_telemetry_enabled is False
    assert load_configuration().integrations.crewai.tracing_enabled is False
    CrewAIInstrumentor().uninstrument()
    clients[0].shutdown()
    assert attempts == [], attempts
    assert len(exporter.get_finished_spans()) == 13
assert attempts == [], attempts
print("NATIVE_PROCESS_OK")
