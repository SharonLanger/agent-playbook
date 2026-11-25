# S04.M1 acceptance cases — draft

These are test-design scenarios for the contracts. Final IDs, expected values and test levels must agree with the approved [design](design.md) and [implementation plan](implementation-plan.md) before handoff.

| Case | Requirement or decision | Observable acceptance |
|---|---|---|
| M1-T01 | D24–D26 | An ordinary incomplete subclass for each of the three ABCs cannot be instantiated; a fully implemented subclass can. |
| M1-T02 | D25/D26 | Static checking rejects incompatible `run`, `map` and callback overrides; an explicit no-op `handle_event` is valid. |
| M1-T03 | D34/D36/D37 | All five accepted event classes can be constructed with their agreed fields and inspected by a concrete handler using the union. A finished event carries the same result object provided to it. |
| M1-T04 | D36–D38 | Missing provider call ID remains absent, unknown tool outcome remains distinct, and no test implies inferred call/result pairing. |
| M1-T05 | Q01/Q02/Q08 | Supported request/result/event values are accepted and agreed invalid values fail in the agreed way. Fill examples after validation policy approval. |
| M1-T06 | Q04/Q26 | Basic settings/permission data represents the approved subset and unsupported requests have an explicit contract-level outcome. Fill cases after policy approval. |
| M1-T07 | C01/Q12 | Static dependency checks or import exercise show the shared contracts have no native provider, CrewAI or Langfuse imports. |

No fake native stream or executed tool is required to satisfy M1. M2 will verify callback order, real mapping, cleanup behavior and successful/failed runs. Native permission effectiveness and provider parity belong to Stage 05. Evidence for this milestone will record exact command, revision, meaningful assertions and limits.
