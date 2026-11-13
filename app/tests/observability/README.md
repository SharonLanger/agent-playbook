# Observability tests

Deterministic tests for `observability/` live here. Langfuse connection tests
use independent fixtures and do not need the Docker service or personal examples.
The observation wrapper's nesting and error behavior is tested here without
loading the personal playground.
