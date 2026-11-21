# SDK-native exception capture

Reviewed 2026-11-15 for LOG-31/32. Source evidence only, not a runtime test.

The OpenTelemetry logging handler at v0.66b2:
- Converts Python LogRecord extra fields into OTel attributes.
- Reads exc_info and fills exception.type, exception.message and exception.stacktrace.
- Calls Python traceback.format_exception for the stack; ordinary chained exceptions are formatted by the standard library.
- Uses the first exception argument for exception.message when available; do not claim a custom str(exception) representation.
- Maps Python WARNING/CRITICAL to OTel WARN/FATAL.
- Has built-in recursive-emission protection.
- Its handler.flush starts a thread. Therefore the application lifecycle should use the provider's documented force_flush/shutdown APIs and verify their actual limits, rather than assuming logging.Handler.flush is a synchronous delivery guarantee.

Sources:
- [Pinned handler](https://github.com/open-telemetry/opentelemetry-python-contrib/blob/v0.66b2/instrumentation/opentelemetry-instrumentation-logging/src/opentelemetry/instrumentation/logging/handler.py)
- [Python logging API](https://docs.python.org/3/library/logging.html)
- [Python traceback API](https://docs.python.org/3/library/traceback.html)
- [OpenTelemetry Logs SDK](https://opentelemetry-python.readthedocs.io/en/latest/sdk/_logs.html)

Use these facilities; do not reconstruct exceptions or native SDK internals. Source was read through GitHub after the public web fetch of the pinned file failed. No live service or exported exception record was tested in this design session.
