# Logging M2 — pinned implementation handoff

Copy the block below to the implementing Codex. Approved behavior: Sharon's 2026-11-16 confirmation of the context/message/optional-field logging contract and separate approval of LOG-G01–06, including guarded Stage 02 follow-ons. Contract revision: caeb1637bd9aa611447703f4c19c38becacfe412.

```text
You are the implementation orchestrator for Logging M2 in https://github.com/SharonLanger/agent-playbook.

Read designs/governance/codex-handover-rules.md at https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/governance/codex-handover-rules.md and follow it.
Approved contract revision: caeb1637bd9aa611447703f4c19c38becacfe412.
Approval reference: Sharon's 2026-11-16 "everything you just said ... let's do it" for the M2 logging behavior and his following explicit approval to continue and change guarded Stage 02 files under LOG-G01–06.
Read these files at that revision:
- Design: designs/refactors/logging/m2-application-logging/design.md — https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/m2-application-logging/design.md
- Test cases: designs/refactors/logging/m2-application-logging/test-cases.md — https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/m2-application-logging/test-cases.md
- Implementation plan: designs/refactors/logging/m2-application-logging/implementation-plan.md — https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/m2-application-logging/implementation-plan.md
- Requirements: designs/refactors/logging/requirements.md — https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/requirements.md
- Decisions: designs/refactors/logging/decisions.md — https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/decisions.md
- Guarded amendments: designs/architecture.md, designs/project-structure.md, designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/{design,test-cases,implementation-plan}.md — all at caeb1637bd9aa611447703f4c19c38becacfe412. LOG-G06 guard registration is on the subsequent documentation commit; inspect it on docs/logging-design.
- M1 implementation dependency: draft PR #54 https://github.com/SharonLanger/agent-playbook/pull/54. Sharon observed a local smoke record and matching correlation after the bridge correction, but did not inspect every field. Do not claim complete schema acceptance.

Refresh repository AGENTS/governance/current main; last observed main was 50e8dcc9c84d120fb06df8ecda29f016431a356c. Implementation target: main. Start the separate M2 implementation branch from the current main plus the exact needed M1 changes, or use PR #54 as a temporary dependency base and clearly document the stacked PR/rebase plan. Preserve unrelated branch edits and assess intervening changes. Do not assume M1 is merged.
Implement only Logging M2 scope in the pinned design: context-based helpers, existing config ownership, dedicated OTel logging setup and scoped cleanup, useful runner/infrastructure diagnostics, native exception details, explicit reusable Langfuse/VictoriaLogs read-only connection checks and a small opt-in checks script. Preserve native Langfuse, business exception semantics and low-code SDK reuse. No M3/M4, broker, custom queue/retry/transport/serializer, automatic event duplication or app/examples access. Apply only LOG-G01–06 approved guarded amendments; do not rewrite historical Stage 02 records.
Use Sol for all implementation roles and record actual model IDs. Delegate one coder plus independent design-drift and test-gap reviewers. Both review the same candidate SHA. Keep reports under designs/refactors/logging/m2-application-logging/reviews, at most three rounds total. Preserve findings and failed/unrun evidence.
Map every LG-01–12 to real test/manual evidence. Keep Docker live LG-10 opt-in, report NOT RUN when unavailable. Run relevant repository checks and public docs/Atlas verification honestly. Open a separate draft implementation PR; do not merge.
Design workspace PR #51 https://github.com/SharonLanger/agent-playbook/pull/51 remains draft and open. Do not merge it or enable auto-merge.
Return ONE complete copyable final-review handoff using the rules' return template. The originating logging design session reviews the actual diff/evidence before Sharon's separate acceptance/merge decisions.
```
