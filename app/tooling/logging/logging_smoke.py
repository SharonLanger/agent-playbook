"""Emit one synthetic record to an explicitly local OTLP/HTTP endpoint."""

import argparse
import logging
from urllib.parse import urlsplit
from uuid import uuid4

import requests
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.logging.handler import (  # pyright: ignore[reportMissingTypeStubs]
    LoggingHandler,
)
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

DEFAULT_ENDPOINT = "http://127.0.0.1:9428/insert/opentelemetry/v1/logs"
TIMEOUT_SECONDS = 5


def local_endpoint(value: str) -> str:
    """Reject alternate hosts/protocols/paths before constructing an exporter."""
    try:
        url = urlsplit(value)
        valid = (
            url.scheme == "http"
            and url.hostname == "127.0.0.1"
            and url.path == "/insert/opentelemetry/v1/logs"
            and url.username is None
            and url.password is None
            and not url.query
            and not url.fragment
            and (url.port is None or 1 <= url.port <= 65535)
            and url.netloc in ("127.0.0.1", f"127.0.0.1:{url.port}")
        )
    except ValueError:
        valid = False
    if not valid:
        raise argparse.ArgumentTypeError(
            "endpoint must be http://127.0.0.1[:PORT]/insert/opentelemetry/v1/logs"
        )
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", type=local_endpoint, default=DEFAULT_ENDPOINT)
    args = parser.parse_args()
    endpoint: str = args.endpoint
    correlation_id = str(uuid4())
    logger = logging.getLogger("agent-playbook-logging-smoke")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    with requests.Session() as session:
        session.trust_env = False
        # Requests raises TooManyRedirects before following the first redirect.
        session.max_redirects = 0
        provider = LoggerProvider(
            resource=Resource({"service.name": logger.name}),
            shutdown_on_exit=False,
        )
        try:
            exporter = OTLPLogExporter(
                endpoint=endpoint, session=session, timeout=TIMEOUT_SECONDS, headers={}
            )
            provider.add_log_record_processor(
                BatchLogRecordProcessor(
                    exporter, export_timeout_millis=TIMEOUT_SECONDS * 1000
                )
            )
            handler = LoggingHandler(level=logging.INFO, logger_provider=provider)
            logger.addHandler(handler)
            try:
                logger.info(
                    "Logging smoke check",
                    extra={
                        "workflow_id": "logging-smoke",
                        "workflow_run_id": str(uuid4()),
                        "correlation_id": correlation_id,
                    },
                )
                if not provider.force_flush(timeout_millis=TIMEOUT_SECONDS * 1000):
                    print("Warning: local flush timed out; delivery is unconfirmed.")
            finally:
                logger.removeHandler(handler)
                handler.close()
        finally:
            provider.shutdown()
    print(f"correlation_id: {correlation_id}")
    print(f"UI: http://{urlsplit(endpoint).netloc}/select/vmui")
    print("Delivery unconfirmed: find this correlation_id in the local UI.")


if __name__ == "__main__":
    main()
