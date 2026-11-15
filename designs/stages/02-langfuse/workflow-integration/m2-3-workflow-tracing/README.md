# M2–M3 — Native runner and CrewAI tracing

This combined package develops the native Langfuse runner observation and automatic CrewAI Flow/step tracing that were previously discussed as M4.2 and M4.3. The revised detailed package is a review draft; application implementation awaits approval of its contract and applicable guarded amendments. PAYLOAD-01 is accepted: native workflow payload capture with mandatory exclusion of configuration and credentials.

## Package

- [Design](design.md) — combined tracing scope, lifecycle, identity propagation and accepted payload policy.
- [Test cases](test-cases.md) — proposed RUN acceptance cases; not executed acceptance.
- [Implementation and review plan](implementation-plan.md) — proposed implementation scope and review process.

Shared requirements, decisions, research and history remain in the [workflow-integration workspace](../README.md). This package does not change the accepted M1 context contract.

## Active implementation freeze

Once Sharon says Codex is working, freeze design.md, test-cases.md, implementation-plan.md and the governing shared requirements/decisions at the handed-off commit until the returned implementation is reviewed here. Do not move or rename them. Put new issues/corrections in a separate follow-ups.md with their handoff status; they do not silently change the coder's contract. Implementation code/tests and round reports may progress normally. See [handover rules](../../../../governance/codex-handover-rules.md#freeze-while-implementation-is-active).

The copyable implementation prompt explicitly authorizes the pinned contract and its narrow RUN-G01–08 changes when Sharon forwards it. Creating this prompt does not claim the coder has started or authorize merging.
