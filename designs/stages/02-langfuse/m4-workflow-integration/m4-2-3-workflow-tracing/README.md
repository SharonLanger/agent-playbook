<a name="m2m3--native-runner-and-crewai-tracing"></a>

# M4.2 + M4.3 — Native runner and automatic CrewAI tracing

## Stage 02 closeout — 2026-11-15

Stage 02 is completed, accepted by Sharon and merged through Stage Design PR #47. Local Langfuse setup/mock work (PR #36), execution context (PR #44), and native runner plus automatic CrewAI tracing (PR #50) are delivered. PR #50 merged at `b08060f0acba74f19bc8a32aedb21316eed149c1`; its reviewed candidate passed 408 tests, static/lint/format checks and installed-release verification. Sharon completed local success, branch, correlation, input/output, readable-name and controlled-failure acceptance. Stage 03 can proceed under its own design approvals.

Application logging is separate work owned by a different agent under `designs/refactors/logging/`, with its own design and implementation PRs. It is outside completed Stage 02 and does not block Stage 03. Earlier logging requirements and research remain historical inputs; this closeout selects no logger, store, viewer or logging architecture and does not create or edit the logging agent’s files.

## Package

- [Design](design.md), [test cases](test-cases.md) and [implementation and review plan](implementation-plan.md) record the approved combined contract.
- The [round-02 amendment](round-02-revision.md) and its [follow-ups](follow-ups.md) record the approved continuation and evidence.
- [Review status](reviews/status.md), the [final review](reviews/tracing-final-review.md) and [local acceptance](reviews/local-acceptance.md) record the two review rounds and completion of RUN-18.

The [M4 workflow-integration workspace](../README.md) indexes shared requirements, decisions, research and history. The [Stage 02 index](../../README.md#canonical-milestone-index) tracks milestone acceptance and merge evidence.

## Historical checkpoints

Earlier records use the package-local label M2–M3 for the combined M4.2 + M4.3 milestone. The statements below describe the original draft and the 2026-11-15 implementation acceptance before Stage Design PR #47 merged.

<a name="current-status--2026-11-15"></a>

### Implementation acceptance before design closeout — 2026-11-15

**Accepted and merged:** M4.2 + M4.3 merged via PR #50 at `b08060f0acba74f19bc8a32aedb21316eed149c1`. RUN-18 is complete on Sharon's local confirmation; 408-test gate and installed release passed. Two review rounds used, with no third round required. PR #47 stays open for stage closeout.

See [final review](reviews/tracing-final-review.md). Earlier planning and pending statements below retain their historical evidence cutoff.

### Earlier checkpoints


This combined package develops the native Langfuse runner observation and automatic CrewAI Flow/step tracing that were previously discussed as M4.2 and M4.3. The revised detailed package is a review draft; application implementation awaits approval of its contract and applicable guarded amendments. PAYLOAD-01 is accepted: native workflow payload capture with mandatory exclusion of configuration and credentials.

### Draft package

- [Design](design.md) — combined tracing scope, lifecycle, identity propagation and accepted payload policy.
- [Test cases](test-cases.md) — proposed RUN acceptance cases; not executed acceptance.
- [Implementation and review plan](implementation-plan.md) — proposed implementation scope and review process.

Shared requirements, decisions, research and history remain in the [workflow-integration workspace](../README.md). This package does not change the accepted M1 context contract.

<a name="active-implementation-freeze"></a>

### Active implementation freeze at handoff

Once Sharon says Codex is working, freeze design.md, test-cases.md, implementation-plan.md and the governing shared requirements/decisions at the handed-off commit until the returned implementation is reviewed here. Do not move or rename them. Put new issues/corrections in a separate follow-ups.md with their handoff status; they do not silently change the coder's contract. Implementation code/tests and round reports may progress normally. See [handover rules](../../../../governance/codex-handover-rules.md#freeze-while-implementation-is-active).

The copyable implementation prompt explicitly authorizes the pinned contract and its narrow RUN-G01–08 changes when Sharon forwards it. Creating this prompt does not claim the coder has started or authorize merging.
