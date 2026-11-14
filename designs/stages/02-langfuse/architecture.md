# Langfuse setup and integration boundaries

Status: **Approved milestone boundaries; M1–M3 merged through PR #36, with local setup/mock-trace acceptance recorded on 2026-11-14; see [acceptance and limits](acceptance-2026-11-14.md). This document retains its original proposal examples as historical design context.**
[Milestones](milestones.md) · [Playground exercise](smoke-plan.md)

## What exists before a workflow context

Milestone 1 supplies the local service stack. Milestone 2 supplies external
configuration and a reusable Langfuse connection. Milestone 3 uses that connection
from a personal mock-data script. None requires the application runner, workflow
factory, workflow base class or context to change.

A standalone entry point owns its client lifetime and cleanup. Avoid a context
ABC, placeholder workflow fields, a generic event bus or speculative lifecycle
interfaces. The integration can be reused later without deciding the final
workflow-facing API now.

Milestone 4 will decide how the merged workflow context receives an observability
handle. The intended separation is shared integration setup versus per-run
observation/correlation; exact classes and signatures wait for that review.
Live clients are not workflow business state or a recoverability store.

## Proposed placement

The paths below are implemented on PR #36 for M1–M3. The application/runner/workflow/context boundary remains M4 only.

| Owner | Milestone and responsibility |
|---|---|
| `app/tooling/observability/` | M1 local Compose assets/instructions; M2 standalone connection-check entry point |
| `observability/adapters/langfuse/` in the runtime package | M2 connection/client setup; M3 narrow observation export needed by the example and independent tests |
| `config/` in the runtime package | M2 typed settings, environment references and sanitized validation |
| `app/examples/langfuse/` | M3 explicitly requested personal playground; editable success/failure scenarios |
| `app/tests/` | Independent fixtures and maintained tests; never imports or executes examples |
| Application/runner/workflow/context boundaries | M4 only, after the workflow refactor is merged and reconciled |

The playground may consume installed/public integration helpers, but the runtime,
test suite, setup, releases and gates must not consume playground code or data.
Deleting the playground must not change application behavior or check collection.
Its placement does not authorize inspecting other examples or routine future
maintenance of Sharon's sandbox.

The maintained connection checker is separate from the playground and suitable
for reuse by [doctor #37](https://github.com/SharonLanger/agent-playbook/issues/37).
Doctor is deferred; it is not a prerequisite or an implemented CLI command.

## Configuration proposal — milestone 2

Extend the existing external configuration system rather than creating a second
application loader. Preserve selection, local overrides and safe validation.
The PR #36 loader accepts this schema; this example records the approved M2 configuration shape:

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

Keep existing CrewAI settings. Normal workflow behavior remains unchanged;
a disabled Langfuse integration needs no keys, exporting client or network.
Use explicit enabled local configuration for the checker/playground. A disabled
connection check reports skipped, not authenticated success.

Project API keys come from the local project's settings. Infrastructure database,
authentication and object-store secrets are separate; keep them external and
untracked. Never dump full configuration, credentials or authorization headers
into diagnostics or trace metadata. Export only selected synthetic/run fields.

Start with the documented compatible family reviewed on 2026-11-13: server v4 and
Python SDK v5. At implementation choose and verify exact image versions/digests
and an exact SDK dependency in the lockfile. Recheck compatibility then; do not
use floating latest tags as the reproducible baseline.

Switching to Cloud later changes endpoint and project credentials. Historical
self-hosted traces do not migrate automatically.

## Local deployment and persistence — milestone 1

Base the setup on upstream Docker Compose, with local loopback access, replaced
example secrets and named persistent volumes.

| Component | Role |
|---|---|
| Langfuse Web | UI and API |
| Langfuse Worker | Background ingestion |
| PostgreSQL | Transactional application data, including organizations/projects |
| ClickHouse | Traces and observations |
| Redis/Valkey | Queue and cache |
| Local S3-compatible storage (MinIO) | Ingested events and blob storage |

The UI is not the data store. Normal stop/start preserves volumes; destructive
reset is separate and never part of the happy path. Persistence is not a backup
or a production availability guarantee. No optional gateway or LLM is required.

The initial browser URL is `http://localhost:3000`, with Python examples/checks
running on the host. A future containerized caller needs a reachable service URL;
its localhost is not the host machine.

## Reporting success and failure

M2 distinguishes reachable service, authenticated project access, skipped checks
and failure. Use bounded timeouts and actionable sanitized messages. A successful
connection check does not claim any trace has been persisted.

M3 sends real synthetic observations and flushes before exit. A printed trace URL
or successful SDK call alone is not proof of ingestion; Sharon checks the UI.
If the example also polls for visibility, report pending/timeout honestly.
Independent live tests may use bounded read-back and must fail on missing roots,
children or unexpected values; they use maintained fixtures, not the playground.

A deliberately failed mock step must be visibly ERROR with a useful message,
mark its mock root failed and stop later successful steps in that run. This is
distinct from a configuration/authentication/export failure. The example should
catch only its explicit simulated-step error for display and preserve unexpected
technical failures.

Choose actual workflow lifecycle hooks and fail-open/fail-closed behavior in M4.
No durable retry queue, resume mechanism, automatic filesystem capture or general
application-log store is introduced by M1–M3.

## Official references checked 2026-11-13

- [Docker Compose](https://langfuse.com/self-hosting/deployment/docker-compose)
- [Service architecture and storage](https://langfuse.com/self-hosting)
- [SDK compatibility and configuration](https://langfuse.com/docs/observability/sdk/overview)
- [Manual observations and nesting](https://langfuse.com/docs/observability/sdk/instrumentation)
- [SDK lifecycle and export options](https://langfuse.com/docs/observability/sdk/advanced-features)
- [Public API](https://langfuse.com/docs/api-and-data-platform/features/public-api)
