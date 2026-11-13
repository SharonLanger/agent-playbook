# First milestone — configuration and run context

Status: **DRAFT — proposed responsibilities, not executable configuration.**
[Review entry point](README.md) · [Smoke plan](smoke-plan.md)

## Application lifetime versus workflow lifetime

| Lifetime | Created/owned by | Contents |
|---|---|---|
| Application/integration lifetime | Application assembly | Validated Langfuse settings and reusable adapter/client for one configured project |
| One workflow invocation | Runner, using the merged workflow/context contract | Fresh run identity, workflow identity, correlation and an observability handle bound to that run |
| One workflow step | Run-bound observation handle | Step observation, parent relationship, timing and selected inputs/outputs |

Every workflow holds its context, as requested. The context provides everything
the workflow needs to report observations, but does not construct a separate SDK
client for each step. Assembly supplies the configured integration; the runner
creates the per-run binding. The context's ABC/concrete representation remains
a decision for the workflow refactor. Do not add a competing base class here.

Keep workflow business state (for example WF-02's value and history) distinct from
execution context. Live client/observer objects do not belong in serializable
workflow state or checkpoints.

The context's minimum semantic information is workflow ID, run ID and a run-bound
observer. The adapter records the actual trace ID and current step/span ID for
correlation. Application run IDs and backend trace IDs are not assumed identical;
record their mapping rather than passing an arbitrary UUID as an OTel trace ID.
Routine log records can later carry the same identifiers. This milestone does not
build log storage or route all Python logger messages into Langfuse.

## Proposed ownership

All paths below are candidate placements within existing component boundaries,
not files or commands already implemented.

| Owner | Responsibility and boundary |
|---|---|
| `application/assembly.py` | Construct/configure the Langfuse adapter once per application configuration; own shutdown |
| `application/workflow_runner.py` | Create per-run context, open/finish the root observation and report outcome |
| Workflow ABC/context from pending refactor | Hold/access the context; no Langfuse SDK imports in workflow logic |
| `observability/` | Small provider-neutral observation boundary, correlation and selected metadata |
| `observability/adapters/langfuse/` | SDK-specific creation, updates, export and trace lookup |
| `config/` | Validate settings and environment references; sanitize configuration errors |
| `app/tooling/observability/` | Local Compose assets and explicitly invoked smoke/seed script |
| `app/tests/` | Independent fixtures and offline contract tests; opt-in live integration test |

Do not add a general event bus or copy the future agent event schema for this
exercise. Use only the observation operations needed for a root, nested steps
and results. Exact method names and filenames follow the merged refactor.

## Configuration proposal

Extend the existing external configuration system rather than creating a second
loader. Preserve file selection, local overrides and sanitized validation.
The following is a **proposed schema example**; today's loader does not accept it:

```yaml
integrations:
  langfuse:
    enabled: false
    base_url: http://localhost:3000
    environment: local
    public_key:
      env: LANGFUSE_PUBLIC_KEY
    secret_key:
      env: LANGFUSE_SECRET_KEY
```

Keep the existing CrewAI settings alongside it. Ordinary application execution
defaults to observability disabled. Disabled mode must not construct an exporting
client, require keys or initiate a connection. For the explicit smoke exercise,
select a dedicated external configuration with Langfuse enabled and valid project
keys. Use a separate smoke project to keep synthetic traces out of later real runs.

Keys come from the self-hosted project's settings. Infrastructure database
credentials, authentication secrets and object-store credentials are separate
from these project API keys; keep them in ignored deployment configuration.
Never copy the complete configuration or context object into trace metadata.
Only allowlisted workflow/run/source fields are exported.

Start with the currently documented compatible family: Langfuse server v4 and
Python SDK v5. At implementation time choose exact tested server/worker image
versions or digests and an exact SDK dependency in the lockfile. A floating
`latest` tag is not the reproducible implementation. Check the current compatibility
matrix before selecting pins.

A later switch to Langfuse Cloud changes the base URL and project credentials,
with the same adapter/observation contract. Existing self-hosted data does not
move automatically; historical migration is a separate task.

## Self-hosted services and persistence

Use the upstream Docker Compose deployment as the starting point, with local
loopback access, changed example secrets and named persistent volumes.

| Component | What it keeps/does |
|---|---|
| Langfuse Web | UI and API |
| Langfuse Worker | Background ingestion and processing |
| PostgreSQL | Transactional application data such as organizations/projects |
| ClickHouse | Traces and observations |
| Redis/Valkey | Cache and job queue |
| S3-compatible storage (local MinIO) | Ingested events and blob/attachment storage |

The UI reads from this service stack; it is not the data store. Container restarts
must retain named-volume data. The normal stop command preserves volumes. Any
volume-deleting reset is separate, explicitly destructive and never part of a
default setup/check command. Local persistence is not a backup or a production
availability guarantee. No optional AI gateway or LLM provider is required here.

The default browser URL is `http://localhost:3000`. The application and smoke
script run on the host for this first milestone. If they later run inside Docker,
configure a reachable service URL; container `localhost` is not the host.

## Lifecycle and failures

Open a root for one run, create nested step observations, close them, record the
root output and end the run. Flush at the smoke script's end and shut down its
client in a finalization path. A long-lived API would retain its integration
client across requests and shut it down with the application.

For this first milestone, the dedicated smoke command fails visibly and returns
nonzero on missing configuration, authentication failure, export/read-back timeout
or mismatched data. It must not claim success merely because the SDK did not raise.
A transport flush alone is not proof that async server ingestion completed.

Normal workflows remain disabled for Langfuse in this milestone, so their outcomes
do not depend on telemetry. Decide fail-open versus fail-closed behavior explicitly
before enabling real workflow instrumentation. No durable retry queue or recovery
guarantee is introduced here.

## Official references checked 2026-11-13

- [Docker Compose](https://langfuse.com/self-hosting/deployment/docker-compose)
- [Service architecture and storage](https://langfuse.com/self-hosting)
- [SDK compatibility and self-host/cloud configuration](https://langfuse.com/docs/observability/sdk/overview)
- [Manual observations and nesting](https://langfuse.com/docs/observability/sdk/instrumentation)
- [SDK lifecycle and export options](https://langfuse.com/docs/observability/sdk/advanced-features)
- [Public API and read access](https://langfuse.com/docs/api-and-data-platform/features/public-api)

