"""Context-aware application diagnostics using Python's standard logging."""

import logging
import math
import sys
from collections.abc import Mapping

from agent_playbook.context.models import ExecutionContext

LOGGER_NAME = "agent_playbook.application.logs"
logger = logging.getLogger(LOGGER_NAME)
logger.propagate = False
logger.addHandler(logging.NullHandler())
_RESERVED = set(logging.makeLogRecord({}).__dict__) | {
    "message",
    "asctime",
    "correlation_id",
    "workflow_id",
    "workflow_run_id",
    "agent_type",
    "agent_run_id",
    "trace_id",
    "span_id",
    "trace_flags",
    "otelTraceID",
    "otelSpanID",
    "otelTraceSampled",
}


def warn(message: str) -> None:
    """Fixed operational messages bypass the application exporter."""
    print(f"Warning: {message}", file=sys.stderr)


def _log(
    level: int,
    context: ExecutionContext,
    message: str,
    *,
    fields: Mapping[str, str | bool | int | float | None] | None = None,
    exception: BaseException | None = None,
) -> None:
    obs = context.observability
    extra: dict[str, str | bool | int | float] = {
        "correlation_id": context.correlation_id,
        "workflow_id": obs.workflow_id,
        "workflow_run_id": obs.workflow_run_id,
    }
    for key in ("agent_type", "agent_run_id"):
        value = getattr(obs, key)
        if value is not None:
            extra[key] = value
    rejected = False
    for key, value in (fields or {}).items():
        if value is None:
            continue
        if (
            not isinstance(key, str)  # pyright: ignore[reportUnnecessaryIsInstance]
            or key in _RESERVED
            or key.startswith(("exception.", "trace.", "span."))
            or not isinstance(value, (str, bool, int, float))  # pyright: ignore[reportUnnecessaryIsInstance]
            or isinstance(value, float)
            and not math.isfinite(value)
        ):
            rejected = True
            continue
        extra[key] = value
    if rejected:
        warn("Unsupported application logging fields omitted.")
    try:
        logger.log(
            level,
            message,
            extra=extra,
            exc_info=(type(exception), exception, exception.__traceback__)
            if exception
            else None,
            stacklevel=3,
        )
    except Exception:
        warn("Application logging emission failed.")


def log_debug(
    context: ExecutionContext,
    message: str,
    *,
    fields: Mapping[str, str | bool | int | float | None] | None = None,
    exception: BaseException | None = None,
) -> None:
    _log(logging.DEBUG, context, message, fields=fields, exception=exception)


def log_info(
    context: ExecutionContext,
    message: str,
    *,
    fields: Mapping[str, str | bool | int | float | None] | None = None,
    exception: BaseException | None = None,
) -> None:
    _log(logging.INFO, context, message, fields=fields, exception=exception)


def log_warning(
    context: ExecutionContext,
    message: str,
    *,
    fields: Mapping[str, str | bool | int | float | None] | None = None,
    exception: BaseException | None = None,
) -> None:
    _log(logging.WARNING, context, message, fields=fields, exception=exception)


def log_error(
    context: ExecutionContext,
    message: str,
    *,
    fields: Mapping[str, str | bool | int | float | None] | None = None,
    exception: BaseException | None = None,
) -> None:
    _log(logging.ERROR, context, message, fields=fields, exception=exception)
