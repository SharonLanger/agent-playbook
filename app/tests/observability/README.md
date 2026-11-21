# Observability tests

Tests for `observability/` cover:

- Langfuse connections and observation-wrapper nesting and error behavior.
- Langfuse SDK delivery and workflow tracing.
- Application logging and its failure behavior.

The tests use independent fixtures and controlled integrations rather than the
personal examples. These automated checks do not establish live service or UI
acceptance.
