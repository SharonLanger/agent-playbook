# Logging progress

Updated 2026-11-15. [Repository progress](../../progress.md) owns stage status.

| Area | Design | Implementation / verification | Acceptance |
|---|---|---|---|
| Stack | Direct Python logging / OpenTelemetry / local VictoriaLogs selected as direction | Official-source review; no service run | Concrete version/config approval pending |
| Lifecycle/API | Runner-owned init/cleanup; context + message agreed | No runtime changes | Exact context/error/outage details pending |
| M1 configuration sanity | Design/test/plan drafted | Not started; Docker unavailable in design environment | No approved SHA |
| M2 runner integration | Proposed next outcome | Not started | Not approved |
| CLI/setup/Compose migration | Requirements retained | Not started | Deferred |
| Event/observation capture | Deferred | Not implemented | Not approved |

Design PR #51 remains draft/open. No logging milestone implemented, accepted or merged. Stage 02 remains complete; Stage 03/04 remain independent.

Next: review M1's bounded scope and pinned configuration, approve its concrete revision, then implement the smoke check in a separate PR. Production outage policy is not required to demonstrate M1 but is required for M2.
