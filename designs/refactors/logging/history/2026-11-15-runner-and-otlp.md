# Runner-owned logging and first milestone — 2026-11-15

Sharon selected Python/OpenTelemetry direct to local VictoriaLogs after simplifying the earlier JSONL/collector proposal. He agreed to small level helpers accepting context and message, leaving exact context and extra/exception fields for later.

He clarified that startup means the CLI runner's run invocation: initialize once, execute workflow(s), flush during cleanup. No daemon, public API/package delivery or generic initialization framework now.

For locality, use reputable official self-hosted documentation and a pinned version. Do not perform a source audit or expand ordinary read/write checks into a product-validation campaign. A small reproducible synthetic smoke is useful; source-backed expectations are distinct from locally observed results.

Latest instruction authorizes updating decisions/specifications and drafting an initial configuration milestone. M1 therefore has a concrete design/test/plan, with no implementation approval inferred. The earlier collector recommendation remains preserved as superseded history. Exact context type and production outage behavior remain M2 decisions.
