"""Independent checks for the narrow observation adapter; no personal examples."""

from unittest.mock import Mock, patch

from pydantic import SecretStr

from agent_playbook.config.models import LangfuseSettings
from agent_playbook.observability.adapters.langfuse import observations


def test_explicit_trace_nesting_error_and_cleanup() -> None:
    settings = LangfuseSettings(
        enabled=True,
        public_key=SecretStr("pk-lf-test"),
        secret_key=SecretStr("sk-lf-test"),
    )
    client = Mock()
    root_span = Mock()
    child_span = Mock()
    client.create_trace_id.return_value = "1" * 32
    client.start_observation.return_value = root_span
    root_span.start_observation.return_value = child_span
    client.get_trace_url.return_value = (
        "http://localhost:3000/project/p/traces/" + "1" * 32
    )

    with patch.object(observations, "create_client", return_value=client) as factory:
        session = observations.LangfuseSession(settings)
    factory.assert_called_once_with(settings, tracing_enabled=True)
    client.start_observation.assert_not_called()

    trace_id, root = session.start_trace(
        run_id="fresh-run",
        name="mock",
        input={"initial": 3},
        metadata={"source": "mock"},
    )
    assert trace_id == "1" * 32
    client.create_trace_id.assert_called_once_with(seed="fresh-run")
    assert client.start_observation.call_args.kwargs["trace_context"] == {
        "trace_id": trace_id
    }
    assert client.start_observation.call_args.kwargs["metadata"] == {"source": "mock"}

    child = root.child("add", {"left": 3, "right": 2})
    child.finish(error="purposeful error")
    root.finish(error="purposeful error")
    root_span.start_observation.assert_called_once()
    assert child_span.update.call_args.kwargs["level"] == "ERROR"
    child_span.end.assert_called_once_with()
    assert root_span.update.call_args.kwargs["level"] == "ERROR"
    root_span.end.assert_called_once_with()

    assert (
        session.trace_url(trace_id)
        == "http://localhost:3000/project/p/traces/" + trace_id
    )
    session.flush()
    session.close()
    client.flush.assert_called_once_with()
    client.shutdown.assert_called_once_with()
