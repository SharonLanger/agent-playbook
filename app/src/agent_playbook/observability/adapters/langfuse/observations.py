"""Small explicit span writer; no workflow or global instrumentation hooks."""

from agent_playbook.config.models import LangfuseSettings
from agent_playbook.observability.adapters.langfuse.connection import create_client
from langfuse import Langfuse, LangfuseSpan


class Observation:
    def __init__(self, span: LangfuseSpan) -> None:
        self._span = span

    def child(self, name: str, input: object) -> "Observation":
        return Observation(
            self._span.start_observation(name=name, as_type="span", input=input)
        )

    def finish(self, *, output: object = None, error: str | None = None) -> None:
        if error is None:
            self._span.update(output=output)
        else:
            self._span.update(level="ERROR", status_message=error, output=output)
        self._span.end()


class LangfuseSession:
    def __init__(self, settings: LangfuseSettings) -> None:
        if not settings.enabled:
            raise ValueError("Langfuse must be enabled for observations")
        self._client: Langfuse = create_client(settings, tracing_enabled=True)

    def start_trace(
        self, *, run_id: str, name: str, input: object, metadata: dict[str, str]
    ) -> tuple[str, Observation]:
        trace_id = self._client.create_trace_id(seed=run_id)
        root = self._client.start_observation(
            trace_context={"trace_id": trace_id},
            name=name,
            as_type="span",
            input=input,
            metadata=metadata,
        )
        return trace_id, Observation(root)

    def trace_url(self, trace_id: str) -> str | None:
        try:
            return self._client.get_trace_url(trace_id=trace_id)
        except Exception:
            return None

    def flush(self) -> None:
        self._client.flush()

    def close(self) -> None:
        self._client.shutdown()
