# S04.M1 acceptance cases — draft

These are test-design scenarios for the contracts. Final IDs, expected values and test levels must agree with the approved [design](design.md) and [implementation plan](implementation-plan.md) before handoff.

| Case | Requirement or decision | Observable acceptance |
|---|---|---|
| M1-T01 | D24–D26 | An ordinary incomplete subclass for each of the three ABCs cannot be instantiated; a fully implemented subclass can. |
| M1-T02 | D25/D26 | Static checking rejects incompatible `run`, `map` and callback overrides; an explicit no-op `handle_event` is valid. |
| M1-T03 | D34/D36/D37 | All five accepted event classes can be constructed with their agreed fields and inspected by a concrete handler using the union. A finished event carries the same result object provided to it. |
| M1-T04 | D36–D38 | Missing provider call ID remains absent, unknown tool outcome remains distinct, and no test implies inferred call/result pairing. |
| M1-T05 | D36/D37/D54; Q01/Q02/Q08 | Unit: construction accepts agreed valid values and rejects wrong types/shape immediately, without a harness. Include text=42 versus valid text, list input versus JSON object/None, and valid nullable/unknown evidence. Assert no silent coercion. Complete request/settings/permission and cross-field matrices after their schemas are agreed. |
| M1-T06 | Q04/Q26 | Basic settings/permission data represents the approved subset and unsupported requests have an explicit contract-level outcome. Fill cases after policy approval. |
| M1-T07 | C01/Q12 | Static dependency checks or import exercise show the shared contracts have no native provider, CrewAI or Langfuse imports. |
| M1-T08 | D54 | Unit: a direct caller attempts invalid model construction; its exception reaches the caller and the success-only continuation is not executed. No replacement object/result is returned. Assert the agreed exception type and safe diagnostic details once those choices are settled. No adapter/harness fixture is needed. |
| M1-T09 | D36/D54 | Unit: reject a non-JSON object nested inside otherwise valid tool input/output during construction; accept a corresponding valid nested JSON value, preserving null/unknown meanings. Do not test only the outer container. Copy/deep-immutability behavior remains a separate unresolved choice. |

M1-T05/T08/T09 specify approved validation behavior. Their exact field matrix and exception assertions must be completed before design lock; this update is not implementation/test execution evidence.

No fake native stream or executed tool is required to satisfy M1. M2 will verify callback order, real mapping, cleanup behavior and successful/failed runs. Native permission effectiveness and provider parity belong to Stage 05. Evidence for this milestone will record exact command, revision, meaningful assertions and limits.
