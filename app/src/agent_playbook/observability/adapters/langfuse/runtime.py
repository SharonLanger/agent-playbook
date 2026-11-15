"""Concrete native tracing setup and short-lived CLI delivery."""

import logging
import sys

from agent_playbook.config.models import LangfuseSettings


def initialize_tracing(settings: LangfuseSettings) -> None:
    """Reuse SDK resources and install automatic wrappers once per process."""
    if not settings.enabled:
        return
    from openinference.instrumentation.crewai import CrewAIInstrumentor

    from agent_playbook.observability.adapters.langfuse.connection import create_client

    create_client(settings, tracing_enabled=True)
    instrumentor = CrewAIInstrumentor()
    if not instrumentor.is_instrumented_by_opentelemetry:
        instrumentor.instrument()


def flush_tracing() -> None:
    """Attempt delivery after CLI scopes close, without changing its outcome."""
    if "openinference.instrumentation.crewai" not in sys.modules:
        return
    from openinference.instrumentation.crewai import CrewAIInstrumentor

    from langfuse import get_client

    if not CrewAIInstrumentor().is_instrumented_by_opentelemetry:
        return
    try:
        get_client().flush()
    except Exception:
        # Never include SDK exception text: it can contain configuration secrets.
        logging.getLogger(__name__).warning("Langfuse delivery attempt failed.")
