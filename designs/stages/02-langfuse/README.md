# Stage 02 — First Langfuse milestone

Status: **DRAFT FOR REVIEW — not an approved baseline or implemented feature.**
Prepared 2026-11-13 against main `a4264ac`. This package defines only the first
configuration and mock-trace milestone; it does not commit the rest of Stage 02.

## Intended result

Start self-hosted Langfuse, run one explicit smoke script, then open its UI and see
several clearly labelled mock workflow runs with nested steps, inputs, outputs and
durations. No Claude, Codex, model credentials or real workflow instrumentation is
needed for this first exercise.

1. Read [architecture and configuration](architecture.md).
2. Read [mock-data script and acceptance plan](smoke-plan.md).
3. Reconcile the upcoming workflow/context refactor before implementation or merge.

Sharon's update establishes the intended direction: a workflow ABC will hold a
per-run context. The exact base-class API, context type (ABC or concrete class),
construction and lifecycle names remain owned by that refactor. No corresponding
new proposal was found in the inspected main tree or workflow/refactor branch
searches. This draft records the dependency rather than inventing its API.

## Scope and dependency

- Application-wide configuration prepares the integration. Each workflow execution
  receives its own context and run-bound observability handle.
- Only the smoke script exports in this milestone. Normal WF-01/02/03 behavior
  remains unchanged and does not require a running Langfuse service.
- The smoke fixture simulates a workflow; it is not evidence of CrewAI integration.
  Using the real workflow ABC/context for it must follow the merged refactor.
- There is no new general logging backend, runtime adapter, child-context API,
  workflow checkpoint store, agent harness or automatic file capture.
- Manual root/step observations are sufficient; automatic CrewAI instrumentation
  comes in a separately reviewed follow-up to avoid duplicate spans.

This is a draft documentation PR to review alongside the workflow refactor.
Hold its merge until that refactor is merged and the ownership/API references have
been reconciled. Merging documentation alone does not prove deployment or runtime
verification. Implementation begins after the relevant design is explicitly approved.

## Placement and design authority

This permanent stage draft belongs under `designs/stages/02-langfuse/`.
It follows the [charter](../../charter.md), [principles](../../principles.md),
[target architecture](../../architecture.md), [structure](../../project-structure.md)
and [design contract](../../governance/design-contract.md). The
[observability exploration](../../explorations/observability.md) and
[event/projection discussion](../../explorations/agent-execution/architecture-notes.md)
inform it without committing their broader schemas.

Existing guarded files and Stage 01 contracts are unchanged. Before implementation,
review any required logical updates to architecture, project structure and the
affected stage baseline, and register a newly approved Stage 02 baseline. This
draft does not silently remove Stage 01's no-base-class/no-Langfuse restrictions.

Navigation and the Atlas Explorations view link this proposal as unapproved.
The Current view gains no implemented capability. Official `app/docs/` has no
change because no supported command, configuration or runtime behavior is added
by this PR. Implementation must add the corresponding setup/configuration guide.

## Principle assessment

| Principles | Application to this draft |
|---|---|
| 1, 3: approval and no drift | Proposal only; no guarded baseline edits; reconcile the workflow refactor first. |
| 2, 6: security and external configuration | External endpoint/settings; environment key references; no credentials in context metadata or traces. |
| 4, 9, 10: learning, scope and local-first | One self-hosted mock-data exercise before real integrations. |
| 5: isolated integration | SDK clients remain behind observability; workflows receive a run-bound handle. |
| 7, 8: quality and evidence | Planned offline tests plus opt-in live read-back; no deployment success claim. |
| 11, 13: preservation and sandbox | Historical work and personal examples remain untouched and uninspected. |
| 12, 14, 15: records and status | Canonical stage draft, discovery links, Atlas proposal status and explicit verification limits. |

Documentation verification is recorded in the PR. No Langfuse server or SDK smoke
script is deployed or executed by this documentation-only change.

