# Setup and management action items

Requested requirements; implementation and exact command contracts await design approval.

| ID | Action | Completion evidence |
|---|---|---|
| ACT-01 | Separate Langfuse and logging Compose definitions; top-level include entry point; leave room for future application/service includes | Each component and combined model validate/start; stopping logs does not stop Langfuse |
| ACT-02 | Preserve existing deployment identity during Compose reorganization | Existing Langfuse project, volume names, secrets and data survive migration and stop/start; no volume deletion |
| ACT-03 | Clear newcomer prerequisites and installer/setup flow | Docker install/launch instructions, CPU/OS suitability, engine-ready check, Compose minimum, tested-version table, resources/ports, image pull and actionable failures |
| ACT-04 | Logging CLI with existing action-flag style | Proposed agent-playbook logs --start/--stop/--status/--open/--check/--logs [--follow]/--help; invalid combinations rejected |
| ACT-05 | Separate availability from end-to-end verification | --check reports prerequisite/service/UI results separately; explicit smoke action writes a unique synthetic record through the actual app-output/collector path and queries it back with a timeout; no false success from HTTP health |
| ACT-06 | One setup/install entry point for selected components or all | Exact spelling undecided; idempotent image/settings preparation; bounded startup; no automatic Docker Desktop installation or destructive reset |
| ACT-07 | Integrate discoverable setup/check instructions | Update official setup/config/troubleshooting guides and entry points when implemented; normal offline quality gates must not require running Docker |
| ACT-08 | Demonstrate replacement | Same application log call/schema reaches an alternative supported sink by changing collector/deployment configuration; no workflow/context edits; record UI/query/data-migration differences |
| ACT-09 | Review exact artifacts/licenses and bounded delivery | Pin versions/digests, review notices, test file permissions, rotation, concurrent writers, buffering/retry limits and shutdown |

Compose include documentation specifies Compose 2.20.3+. This is the feature floor, not a tested project Docker Desktop/Engine minimum. Establish the latter from a pinned implementation probe. Do not equate Docker CLI availability with a running engine.

Existing agent-playbook langfuse --check is a read-only connection check; preserve its semantics. Suggested logs --check --smoke (or a separate --smoke action) must clearly disclose its synthetic write. Exact spelling remains open. Component --logs means container diagnostics; --open opens application-log search UI.

Aggregate/component operations must share one deliberate project identity. Running component Compose files independently with implicit different project names must not silently create duplicate stacks or fresh data volumes. Profiles/service targeting and installed-release versus checkout support require concrete design.
