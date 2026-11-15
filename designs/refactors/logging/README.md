# Application logging design

**DRAFT — research/requirements workspace; no implementation approval.**

Logging is an independent follow-on related to completed Stage 02, not a new stage or a prerequisite for Stage 03/04. Sharon requested this workspace on 2026-11-15. Placement matches [Stage 02 closeout](../../stages/02-langfuse/closeout.md) and [repository progress](../../progress.md).

## Reading order

1. [History and alignment](history/2026-11-15-kickoff.md)
2. [Requirements / initial specs](requirements.md)
3. [Decisions and open questions](decisions.md)
4. [Proposed research](research/README.md)
5. [Progress](progress.md)
6. [Repository impact and verification](repository-updates.md)

## Candidate outcomes — not approved milestones

| Outcome | Prerequisite | Boundary | Status |
|---|---|---|---|
| Correlated application records | Agree API, schema and outage policy | Context inheritance, useful errors and agreed recording destination | Proposed |
| Search and inspect records | Select storage/viewer | Query before loading; bounded results and client-side filtering; no custom viewer | Proposed; may combine with first outcome |
| Automatic observation/event capture | Explicit scope and supported mechanism demonstrated | Selected records only; no tracing broker or blanket duplication | Deferred |

Once boundaries are agreed, create each milestone's README, design, test-cases and implementation-plan together under the [working method](../../governance/stage-milestone-workflow.md). No empty milestone/review scaffolding or invented PASS reports now. Follow [handover rules](../../governance/codex-handover-rules.md) when preparing an approved implementation handoff.

Keep this design PR open for iteration; merge only when Sharon explicitly requests it. No runtime changes, auto-merge or backend adoption are authorized.

Next: select a bounded research task, starting with R01–R03. No new external research has been performed.
