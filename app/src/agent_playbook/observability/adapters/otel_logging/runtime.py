"""Invocation-local OpenTelemetry logging setup and cleanup."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager

import requests
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.logging.handler import (  # pyright: ignore[reportMissingTypeStubs]
    LoggingHandler,  # pyright: ignore[reportMissingTypeStubs]
)
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from agent_playbook.config.models import LoggingSettings
from agent_playbook.observability.logging import logger, warn


@contextmanager
def logging_scope(settings: LoggingSettings) -> Iterator[None]:
    provider = None
    handler = None
    session = None
    previous_level = logger.level
    try:
        if settings.enabled:
            try:
                session = requests.Session()
                session.trust_env = False
                session.max_redirects = 0
                provider = LoggerProvider(
                    resource=Resource({"service.name": "agent-playbook"}),
                    shutdown_on_exit=False,
                )
                exporter = OTLPLogExporter(
                    endpoint=settings.endpoint, session=session, timeout=5, headers={}
                )
                provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
                handler = LoggingHandler(
                    logger_provider=provider, log_code_attributes=True
                )
                logger.setLevel(getattr(logging, settings.level))
                logger.addHandler(handler)
            except Exception:
                warn("Application logging initialization failed.")
        yield
    finally:
        if handler is not None:
            logger.removeHandler(handler)
            try:
                handler.close()
            except Exception:
                warn("Application logging handler cleanup failed.")
        if provider is not None:
            try:
                if not provider.force_flush(timeout_millis=10000):
                    warn("Application logging flush timed out.")
            except Exception:
                warn("Application logging flush failed.")
            try:
                provider.shutdown()
            except Exception:
                warn("Application logging shutdown failed.")
        if session is not None:
            try:
                session.close()
            except Exception:
                warn("Application logging transport cleanup failed.")
        logger.setLevel(previous_level)
