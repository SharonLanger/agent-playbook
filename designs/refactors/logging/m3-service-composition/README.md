# Logging M3 — local service commands

Status: revised concrete design **proposed for Sharon's approval**. Sharon approved the three command groups/actions on 2026-11-21 and confirmed that explicit `logs --start` starts VictoriaLogs even when workflow logging is disabled, without editing YAML. Aggregate `services --start` selects by effective enabled settings. Runtime implementation and M3 acceptance have **not started**.

Read [design](design.md), [revised acceptance cases](test-cases.md) and [implementation plan](implementation-plan.md). The earlier three review rounds cover a superseded, broader proposal and remain intact under [historical reviews](reviews/status.md). The separately authorized revised design review is recorded under `reviews/revised-2026-11-21/`.

PR #57 stays draft. The existing Docker project and volume names remain; renaming belongs to [issue #56](https://github.com/SharonLanger/agent-playbook/issues/56). [Overall logging design PR #51](https://github.com/SharonLanger/agent-playbook/pull/51) stays draft/open. The remaining M2 LG-10 check is pending. No runtime code, Compose data or private credentials are changed by this design work.
