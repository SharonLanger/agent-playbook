# Round 1 independent test coverage review

Role: test gap reviewer. Configured model: gpt-6.2-sol (served ID unavailable). Candidate: b1c5ede0b6603208109e9f985176d717585800db. Verdict: **CHANGES REQUIRED**. Static review; no runtime/Docker/Mac tests.

| ID | Severity | Expected versus observed |
|---|---|---|
| TG-M3-01 | High | MC-01–03 need Docker-free ordinary tests, opt-in Compose probe, four selection states and independent survival. |
| TG-M3-02 | High | MC-04/06/12 need manifest/context/race, interruption/rollback and same physical-volume record/trace evidence. |
| TG-M3-03 | High | MC-05–07 need parser round-trip, remapped references, ambient dotenv and secret leakage fault paths. |
| TG-M3-04 | Medium | MC-08 needs exact deadlines/order/aggregation and invalid-config no-mutation assertions. |
| TG-M3-05 | Medium | MC-09/11 need direct pre-bootstrap and hosted check contracts plus cli.md. |

Evidence: [candidate tests](https://github.com/SharonLanger/agent-playbook/blob/b1c5ede0b6603208109e9f985176d717585800db/designs/refactors/logging/m3-service-composition/test-cases.md) and existing Langfuse CLI/public guides. MC-10 suitable; MC-12 artifact/live distinction retained. All findings carried to round 2.
