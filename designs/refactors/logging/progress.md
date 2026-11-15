# Logging progress

Updated 2026-11-15. [Repository progress](../../progress.md) owns stage status.

| Area | Design | Implementation / verification | Acceptance |
|---|---|---|---|
| Stack | Direct standard Python logging / OpenTelemetry / local VictoriaLogs | Official-source and pinned-handler review; no service run | Selected direction; no runtime acceptance |
| API | ExecutionContext + message + optional fields; standard exceptions | No runtime changes | User choices settled (LD22–26) |
| Policy | required_start=true inside each enabled integration; runtime/cleanup warn only; DEBUG and seven-day retention defaults | No runtime changes | User choices settled (LD21/24/25) |
| M1 configuration sanity | Design/test/plan drafted | Not started; Docker unavailable here | No approved concrete revision |
| M2 application logging | Design/test/plan drafted | Not started | Guarded amendments listed, not applied; concrete revision review pending |
| M3/M4 Compose/CLI/setup | Outline retained | Not started | Detailed design pending |
| Automatic event/observation capture | Deferred | Not implemented | Not approved |

PR #51 remains draft/open. No logging milestone implemented, accepted or merged. Stage 02 remains complete. Main inspected at 529fe15895afc8211d833fc2544e98f0d18fb451; intervening Stage 03 work does not alter the logging/context baseline.

Next: review [M2](m2-application-logging/README.md), particularly the small integration boundary and guarded amendment list; approve concrete milestone revisions before implementation. M2's live acceptance depends on M1's local service setup. No handoff has been frozen.
