# Application logging design

**DRAFT — selected direction; concrete milestone approval pending.**

Independent logging follow-on to completed Stage 02. It does not block Stage 03/04. Keep [PR #51](https://github.com/SharonLanger/agent-playbook/pull/51) draft and open; no merge or runtime implementation is authorized by this documentation update.

## Current direction

Python logging → OpenTelemetry OTLP/HTTP → local VictoriaLogs (storage, query and built-in UI). The runner initializes logging once per CLI run and uses context-manager cleanup to attempt bounded flush/shutdown on normal exit or exceptions. Workflow/agent calls use context + message, with optional event-specific fields, through small level helpers. No mandatory Collector, Fluent Bit, JSONL or structlog.

## Reading order

1. [Requirements](requirements.md)
2. [Decisions and unresolved choices](decisions.md)
3. [Direct OTLP research](research/2026-11-15-direct-otlp.md)
4. [M1 configuration sanity](m1-configuration-sanity/README.md)
5. [Progress](progress.md) and [repository impact](repository-updates.md)
6. [Deferred setup/CLI actions](action-items.md)

## Milestones

| ID / outcome | Design / approved SHA | Implementation | Acceptance / merge |
|---|---|---|---|
| [M1: local configuration and synthetic log visible](m1-configuration-sanity/README.md) | Draft design/tests/plan; no approved SHA | Not started | Pending; unmerged |
| M2: runner-owned context logging | Proposed boundary; detailed context, error and outage contract next | Not started | Pending |
| M3: component and umbrella Compose | Proposed for discussion; preserve Langfuse data/identity | Not started | Not approved |
| M4: setup and logging management CLI | Proposed for discussion; prerequisites, start/stop/status/open/check | Not started | Not approved |

M1 demonstrates the selected path with synthetic data. M2 connects it to normal workflow execution. Keep later details draft until needed; use the [milestone method](../../governance/stage-milestone-workflow.md).

Historical starting points: [kickoff](history/2026-11-15-kickoff.md), [earlier collector research](research/2026-11-15-victorialogs.md), [setup discussion](history/2026-11-15-replaceability-and-setup.md). LD15 supersedes the earlier collector recommendation.

M2 includes context mapping, optional-field rules, lifecycle cleanup, a small useful set of workflow/agent log calls, failure policy and practical filtering. M3 packages logging and Langfuse under a common Compose entry point without changing their independent ownership. M4 makes setup and operations discoverable. M2–M4 are an outline for discussion, not agreed detailed milestones. Stack-trace formatting and automatic observation/event duplication remain uncommitted follow-ups.
