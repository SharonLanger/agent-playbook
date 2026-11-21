# Stage 02 — Langfuse milestones

## Stage 02 closeout — 2026-11-15

Stage 02 is completed, accepted by Sharon and merged through Stage Design PR #47. Local Langfuse setup/mock work (PR #36), execution context (PR #44), and native runner plus automatic CrewAI tracing (PR #50) are delivered. PR #50 merged at `b08060f0acba74f19bc8a32aedb21316eed149c1`; its reviewed candidate passed 408 tests, static/lint/format checks and installed-release verification. Sharon completed local success, branch, correlation, input/output, readable-name and controlled-failure acceptance. Stage 03 can proceed under its own design approvals.

Application logging is separate work owned by a different agent under `designs/refactors/logging/`, with its own design and implementation PRs. It is outside completed Stage 02 and does not block Stage 03. Earlier logging requirements and research remain historical inputs; this closeout selects no logger, store, viewer or logging architecture and does not create or edit the logging agent’s files.

[Final closeout and remaining limits](closeout.md).

The [repository progress record](../../progress.md#stage-02-closeout--2026-11-15) tracks stage acceptance and project status.

## Canonical milestone index

| Milestone and outcome | Design and approval | Implementation PR | Verification and review evidence | Acceptance | Merge |
|---|---|---|---|---|---|
| M1 — Local Langfuse UI and persistence | [Agreed setup checkpoint](milestones.md#1-langfuse-runs-locally) and [handoff](m1-3-local-langfuse/history/implementation-handoff.md) | [#36](https://github.com/SharonLanger/agent-playbook/pull/36) | [Setup findings](m1-3-local-langfuse/reviews/findings.md#milestone-1-findings) and [local results](m1-3-local-langfuse/reviews/acceptance-2026-11-14.md#observed-results) | Accepted by Sharon on 2026-11-14 | Merged |
| M2 — Explicit project connection check | [Agreed connection checkpoint](milestones.md#2-our-code-can-connect) and [shared handoff](m1-3-local-langfuse/history/connection-playground-handoff.md#milestone-2--connection-only) | [#36](https://github.com/SharonLanger/agent-playbook/pull/36) | [Connection findings](m1-3-local-langfuse/reviews/findings.md#m2-project-connection--2026-11-13) and [local results](m1-3-local-langfuse/reviews/acceptance-2026-11-14.md#observed-results) | Accepted by Sharon on 2026-11-14 | Merged |
| M3 — Editable mock traces | [Agreed playground checkpoint](milestones.md#3-i-can-see-and-change-mock-runs) and [manual exercise](m1-3-local-langfuse/smoke-plan.md) | [#36](https://github.com/SharonLanger/agent-playbook/pull/36) | [Mock findings](m1-3-local-langfuse/reviews/findings.md#m3-editable-mock-playground--2026-11-13) and [readback limitation](m1-3-local-langfuse/reviews/acceptance-2026-11-14.md#remaining-delivery-confirmation-limitation) | Accepted by Sharon on 2026-11-14, with the recorded readback limitation | Merged |
| M4.R — Released-version tracing research | [Workflow-integration research](m4-workflow-integration/research/crewai-langfuse.md) | Research prerequisite | [Coverage and limits](m4-workflow-integration/research/crewai-langfuse.md#coverage-and-limits) | Research evidence only | Recorded in the merged design workspace |
| [M4.1 — Execution context](m4-workflow-integration/m4-1-context/README.md) | [Approved revision `11bba581`](https://github.com/SharonLanger/agent-playbook/blob/11bba581291c1b166973848ea8db6a9e2a142413/designs/stages/02-langfuse/workflow-integration/01-context-design.md) | [#44](https://github.com/SharonLanger/agent-playbook/pull/44) | [Two review rounds](m4-workflow-integration/m4-1-context/reviews/status.md) and [final review](m4-workflow-integration/m4-1-context/reviews/context-final-review.md) | Accepted by Sharon on 2026-11-14 | Merged at `942e59344c429454263319e783ea76ad297b7ea6` |
| [M4.2 + M4.3 — Native runner and automatic CrewAI tracing](m4-workflow-integration/m4-2-3-workflow-tracing/README.md) | [Approved revision `ab3fab45`](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/design.md) and [round-02 SDK-first approval `82b967dd`](https://github.com/SharonLanger/agent-playbook/commit/82b967dda1fbf942cc1067a3539328c74abc303a) | [#50](https://github.com/SharonLanger/agent-playbook/pull/50) | [Two review rounds](m4-workflow-integration/m4-2-3-workflow-tracing/reviews/status.md), [final review](m4-workflow-integration/m4-2-3-workflow-tracing/reviews/tracing-final-review.md) and [local acceptance](m4-workflow-integration/m4-2-3-workflow-tracing/reviews/local-acceptance.md) | Accepted by Sharon on 2026-11-15 | Merged at `b08060f0acba74f19bc8a32aedb21316eed149c1` |

M1–M3 used a single implementation PR at `44d69194f6add6f646795b14f7c3f43c656baeda`. Their original checkpoints preceded the current per-milestone pinning convention. [Stage Design PR #47](https://github.com/SharonLanger/agent-playbook/pull/47) merged last at `4ed7a318e25653d481705d9cb40c35de9ab649c7`.

The [workflow-integration package](m4-workflow-integration/README.md) owns the shared [requirements](m4-workflow-integration/requirements.md), [decisions](m4-workflow-integration/decisions.md) and research for M4. Earlier records use the package-local IDs M1 and M2–M3 for Stage 02 milestones M4.1 and M4.2 + M4.3 respectively.

<a name="start-here"></a>

## Read the stage records

1. [M1–M3 · Local Langfuse](m1-3-local-langfuse/README.md) groups the setup, connection and mock-trace verification with the acceptance record and earlier handoffs.
2. [M4 · Workflow integration](m4-workflow-integration/README.md) leads to the shared requirements and decisions, M4.R research, the M4.1 context package and the combined M4.2 + M4.3 tracing package.
3. [Stage architecture](architecture.md), the [original milestone plan](milestones.md) and the [final closeout](closeout.md) retain the stage-wide contracts, checkpoints and delivery evidence.

## Next action

Stage 02 is closed. Use the milestone packages above to review its deliverables and the [repository progress record](../../progress.md) for subsequent work.

## Historical checkpoints

The 2026-11-15 closeout pointed to [Stage 03](../03-orchestration-patterns/README.md) as the next learning stage. For context and tracing details it directed readers to the merged milestone packages above.

The following entries preserve the stage's original planning, handoff and verification records. Their status and PR instructions describe their recorded checkpoints. [The original milestone plan](milestones.md) remains the source for the agreed historical gates.


<a name="current-acceptance--2026-11-15"></a>

### Implementation acceptance before design closeout — 2026-11-15

M4.2 + M4.3 native workflow tracing is implemented, final-reviewed and accepted by Sharon; PR #50 merged at b08060f0acba74f19bc8a32aedb21316eed149c1. The reviewed candidate is adbba215da77e1e618c3c699e1d84c1ba45c629e: 408 tests, static/lint/format checks and installed release passed. Sharon completed local success, routing, correlation, input/output, readable-name and controlled-failure checks. M1–M3 and M4.1 remain accepted/merged. Stage Design PR #47 stays open for documentation reconciliation and explicit stage closeout. Logging, real-agent cost/usage and scores/evaluations remain deferred. Earlier pending statements below are historical checkpoints, superseded by this acceptance.

### Earlier status and retained history

Status: **M1–M3 local setup and mock-trace exercise accepted by Sharon on Mac on 2026-11-14; PR #36 merged as `44d6919`. Delivery readback has a recorded limitation; M4.1 is accepted/merged; the combined M4.2/M4.3 implementation is unmerged, continuing round 02 under approved SDK-first amendment 82b967d; review and local acceptance remain pending.**
Milestone 1's fixed checkpoint remains available; see
[findings](m1-3-local-langfuse/reviews/findings.md) and the [local operation guide](../../../app/docs/langfuse-local.md).
Milestone 2 adds a project connection check, and milestone 3 adds the explicit
mock playground. M4.1 is implemented, final-reviewed and accepted; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6. M4.2/M4.3 design/test/plan are approved at `ab3fab459c97eed44cc0b202402e559a827a71cf`. The approved round-02 amendment accepts visible framework events to enable automatic tracing, native input/output capture and readable naming; see [follow-up evidence](m4-workflow-integration/m4-2-3-workflow-tracing/follow-ups.md).

### Earlier navigation and handoff — November 2026

M4 planning now has a [permanent workflow-integration workspace](m4-workflow-integration/README.md): current requirements, decisions, CrewAI research and the pending repository-update checklist. PR #43 now includes a [detailed M4.1 context draft](m4-workflow-integration/m4-1-context/design.md), separate test cases and a capped implementation/review plan. M4.1 candidate 16c1580 passed implementation and final review; Sharon accepted it and authorized merging. M4.2 preliminary design is active, including shared correlation metadata. The earlier PR #36 milestone/branch policy below records M1–M3; M4 uses the separate milestone PR direction in the new workspace.

Latest: [local acceptance and remaining limitation](m1-3-local-langfuse/reviews/acceptance-2026-11-14.md),
[approved main reconciliation](m1-3-local-langfuse/history/main-reconciliation.md),
[the original review](m1-3-local-langfuse/reviews/review-2026-11-13.md),
[the follow-up resolution](m1-3-local-langfuse/reviews/resolution-2026-11-13.md) and the
[CLI plan / Codex handoff](m1-3-local-langfuse/history/verification-simplification-plan.md).
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
[playground/manual exercise](m1-3-local-langfuse/smoke-plan.md).
Implementing agents must follow [verification before handoff](m1-3-local-langfuse/verification.md).
The [M1 brief](m1-3-local-langfuse/history/implementation-handoff.md) covers setup and its port follow-up.
The [M2/M3 handoff](m1-3-local-langfuse/history/connection-playground-handoff.md) and
[combined current verification guide and historical milestone files](m1-3-local-langfuse/user-verification.md) record their scope and
exact local checkpoints.

The goal is gradual, visible progress: first an empty working UI, then a connection
check, then editable mock traces, and finally real workflow integration.
Milestones are acceptance checkpoints, not commit counts or mandatory separate PRs.

### Dependency and PR policy

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

### Playground versus verification

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
gate or permission to inspect other examples. See [verification.md](m1-3-local-langfuse/verification.md).

The future CLI diagnostic feature is tracked in
[issue #37 — doctor](https://github.com/SharonLanger/agent-playbook/issues/37).
It does not block the small standalone connection check.

### Authority and documentation impact

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

### Principle assessment

| Principles | Application |
|---|---|
| 1, 3: approval and no drift | Agreed milestone direction; detailed proposal remains reviewable; no guarded edits or early context implementation. |
| 2, 6: security and configuration | External settings and key references; sanitized diagnostics; no secret payloads. |
| 4, 9, 10: learning, scope and local-first | Four visible checkpoints, self-hosted first, real workflows last. |
| 5: isolated integration | Langfuse-specific code stays inside its integration; no speculative event bus. |
| 7, 8: quality and evidence | Independent offline tests, explicit live checks and Sharon's manual UI gates; no unrun success claims. |
| 11, 13: preservation and sandbox | Existing examples untouched; requested playground remains outside application checks/releases. |
| 12, 14, 15: records and status | Canonical stage documents, discovery/Atlas updates, implemented PR follow-up, local acceptance and explicit remaining limitations. |


### Historical M4.1 implementation review — 2026-11-14

Sharon approved the M4.1 package at `11bba581291c1b166973848ea8db6a9e2a142413`
and G01–G08 in his implementation instruction. The data-only context and actual
workflow propagation are being implemented on `feat/m4-1-context` and are not
merged or accepted. [Round status and evidence](m4-workflow-integration/m4-1-context/reviews/status.md)
track the independent design and test reviews. M1–M3 history is unchanged;
Langfuse tracing and automatic CrewAI observations remain separate checkpoints.
