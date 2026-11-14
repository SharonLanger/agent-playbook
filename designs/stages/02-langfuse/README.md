# Stage 02 — Langfuse milestones

Status: **M1–M3 local setup and mock-trace exercise accepted by Sharon on Mac on 2026-11-14; PR #36 merged as `44d6919`. Delivery readback has a recorded limitation; M4 remains deferred.**
Milestone 1's fixed checkpoint remains available; see
[findings](findings.md) and the [local operation guide](../../../app/docs/langfuse-local.md).
Milestone 2 adds a project connection check, and milestone 3 adds the explicit
mock playground. Milestone 4 remains deferred and unimplemented.

## Start here

M4 planning now has a [permanent workflow-integration workspace](workflow-integration/README.md): current requirements, decisions, CrewAI research and the pending repository-update checklist. PR #43 now includes a [detailed M4.1 context draft](workflow-integration/01-context-design.md), separate test cases and a capped implementation/review plan. Sharon reports sending the M4.1 authorization at 11bba58 to Codex; implementation evidence/final review remain pending. M4.2 preliminary design is active, including shared correlation metadata. The earlier PR #36 milestone/branch policy below records M1–M3; M4 uses the separate milestone PR direction in the new workspace.

Latest: [local acceptance and remaining limitation](acceptance-2026-11-14.md),
[approved main reconciliation](main-reconciliation.md),
[the original review](review-2026-11-13.md),
[the follow-up resolution](resolution-2026-11-13.md) and the
[CLI plan / Codex handoff](verification-simplification-plan.md).
Sharon approved the six conflict resolutions. Main's workflow refactor and the
Langfuse branch are combined; verification is recorded in the reconciliation
file. R1/R3 delivery reporting and R4 status prose have been corrected on this
merged implementation; the helper and six double-dash CLI actions are implemented.
Earlier Linux live-stack verification hit a `vfs` disk limit. Sharon has now
confirmed local project access, visible mock traces and normal stop/start
persistence on Mac. Bounded delivery readback returned unconfirmed for one visible
trace; that limitation remains open. Real workflow/context integration remains later.

Read [the four milestones and local checkpoints](milestones.md), then
[configuration and ownership](architecture.md) and the
[playground/manual exercise](smoke-plan.md).
Implementing agents must follow [verification before handoff](verification.md).
The [M1 brief](implementation-handoff.md) covers setup and its port follow-up.
The [M2/M3 handoff](connection-playground-handoff.md) and
[combined current verification guide and historical milestone files](user-verification.md) record their scope and
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
refactor merges is superseded by this milestone separation. PR #36 is merged; its earlier planning and review checkpoints remain historical.

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

Navigation and Atlas now record merged M1–M3 separately from deferred workflow/context integration.
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
| 12, 14, 15: records and status | Canonical stage documents, discovery/Atlas updates, implemented PR follow-up, local acceptance and explicit remaining limitations. |

