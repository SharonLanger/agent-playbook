# Stage 02 — Langfuse milestones

Status: **Milestones 1–3 implemented on PR #36, with four open review findings; Sharon's local acceptance remains pending.**
Milestone 1's fixed checkpoint remains available; see
[findings](findings.md) and the [local operation guide](../../../app/docs/langfuse-local.md).
Milestone 2 adds a project connection check, and milestone 3 adds the explicit
mock playground. Milestone 4 remains deferred and unimplemented.

## Start here

Latest: [the four review findings](review-2026-11-13.md) and the
[proposed single-branch verification plan](verification-simplification-plan.md).
The review found a trace-delivery defect, misleading export-success reporting,
main integration conflicts and stale design status. The new plan proposes one
combined manual exercise and simpler start/stop commands. Sharon agreed with
the Docker usability direction and requested a complete newcomer setup guide,
explicit installation/version requirements and management scripts. Those
requirements are recorded in the plan; implementation remains paused for joint
main-conflict decisions. No fixes, helper implementation or conflict resolutions have
been applied by this documentation update. Earlier checkpoint instructions below
remain historical context; do not treat M3 as ready for acceptance until the
delivery findings are resolved.

Read [the four milestones and local checkpoints](milestones.md), then
[configuration and ownership](architecture.md) and the
[playground/manual exercise](smoke-plan.md).
Implementing agents must follow [verification before handoff](verification.md).
The [M1 brief](implementation-handoff.md) covers setup and its port follow-up.
The [M2/M3 handoff](connection-playground-handoff.md) and
[separate verification files](user-verification.md) record their scope and
exact local checkpoints.

The goal is gradual, visible progress: first an empty working UI, then a connection
check, then editable mock traces, and finally real workflow integration.
Milestones are acceptance checkpoints, not commit counts or mandatory separate PRs.

## Dependency and PR policy

Milestones 1–3 can proceed independently of the workflow refactor. They must not
create a workflow context, a context ABC, placeholder context fields or a competing
workflow lifecycle. Only milestone 4 waits for the workflow refactor to merge.

Keep PR #36 as the existing design/review thread. Prefer sequential checkpoints on
one implementation branch rather than a stack of overlapping milestone PRs.
A separate PR is useful only for independently reviewable work with checked file
overlap; do not promise zero conflicts. Shared dependency/configuration files and
the generated Atlas can still overlap with other work. Recheck the actual branches
before proposing a split or merge.

The earlier blanket instruction to hold all Langfuse work until the workflow
refactor merges is superseded by this milestone separation. This PR remains draft
for review; it is not merged by this update.

## Playground versus verification

Sharon explicitly requested a personal playground at `app/examples/langfuse/`.
Its `run.py` lets him send mock runs, change inputs and choose which
step fails, then inspect the result in Langfuse. It is a learning tool, not the
application's test suite or a required release check.

Maintain connection checks outside examples. Tests and deterministic fixtures
belong in `app/tests/` and must never import, inspect or execute the playground.
Deleting examples must leave application checks and behavior unchanged. This
implementation accessed only the specifically requested new Langfuse example,
not the workflow examples.

When implementing the requested playground, the agent must smoke-run its success
and selected failure scenarios before delivery. This targeted manual verification
is authorized for the new Langfuse example; it is not an automated application
gate or permission to inspect other examples. See [verification.md](verification.md).

The future CLI diagnostic feature is tracked in
[issue #37 — doctor](https://github.com/SharonLanger/agent-playbook/issues/37).
It does not block the small standalone connection check.

## Authority and documentation impact

This permanent stage material belongs under `designs/stages/02-langfuse/`.
It follows the [charter](../../charter.md), [principles](../../principles.md),
[target architecture](../../architecture.md), [structure](../../project-structure.md)
and [design contract](../../governance/design-contract.md). The
[observability exploration](../../explorations/observability.md) and
[event/projection discussion](../../explorations/agent-execution/architecture-notes.md)
inform it without adopting their broader schemas.

Existing guarded files and Stage 01 contracts are unchanged. Review required
logical changes to guarded documents before implementation and register a newly
approved stage baseline when approved. Milestone 4 must use the actual merged
workflow design, including its lifecycle rules, rather than infer them here.

Navigation and Atlas distinguish the pending PR from accepted Current implementation.
Official `app/docs/langfuse-local.md` and `app/docs/langfuse-connection.md`
document the implemented local deployment and project check.
Each implementation checkpoint must provide maintained setup/configuration or
troubleshooting guidance for the supported behavior; the personal playground has
its own learning README when created.

## Principle assessment

| Principles | Application |
|---|---|
| 1, 3: approval and no drift | Agreed milestone direction; detailed proposal remains reviewable; no guarded edits or early context implementation. |
| 2, 6: security and configuration | External settings and key references; sanitized diagnostics; no secret payloads. |
| 4, 9, 10: learning, scope and local-first | Four visible checkpoints, self-hosted first, real workflows last. |
| 5: isolated integration | Langfuse-specific code stays inside its integration; no speculative event bus. |
| 7, 8: quality and evidence | Independent offline tests, explicit live checks and Sharon's manual UI gates; no unrun success claims. |
| 11, 13: preservation and sandbox | Existing examples untouched; requested playground remains outside application checks/releases. |
| 12, 14, 15: records and status | Canonical stage documents, discovery/Atlas updates, explicit pending implementation and verification. |
