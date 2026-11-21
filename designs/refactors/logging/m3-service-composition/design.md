# Logging M3 — local service control

Sharon approved these three command groups and their actions on 2026-11-21. Each command begins with `agent-playbook`.

| Group | --start | --status | --stop |
|---|---|---|---|
| services | Start each enabled local component using the effective YAML settings and existing override precedence. If neither is enabled, report that there is nothing to start. | Report each component separately, including disabled components already running. | Stop both managed projects regardless of enabled settings. |
| langfuse | Start Langfuse using its existing CLI behavior. | Show Langfuse status. | Stop Langfuse alone. |
| logs | Start VictoriaLogs alone. | Show VictoriaLogs status. | Stop VictoriaLogs alone. |

Open decision before handoff: when logging is disabled for workflow export, should an explicit `logs --start` still start the local service? Recommended: yes, consistent with the existing explicit Langfuse command. Manual service startup leaves application settings untouched. Only aggregate start selects components by enabled flags.

## Operating behavior

Repeated starts and stops are safe. Stops retain volumes. Target the existing component Compose projects, scoped to this checkout's local deployment. A component failure during aggregate start is reported separately, the other enabled component is attempted, and the command reports failure. Bound readiness waits including subprocess and HTTP calls. Status distinguishes readiness from stored records. Workflow runs keep their independent lifecycle.

Reuse Langfuse's existing management path and options and the VictoriaLogs Compose file and local health check. A logs-only action operates independently of Langfuse keys. Keep the existing local UI origins and ports consistent with actual Compose publication. Use existing application configuration and its external secrets file for integration keys. Langfuse retains its generated, ignored local deployment settings. Docker renaming belongs to [issue #56](https://github.com/SharonLanger/agent-playbook/issues/56). Normal operation needs no reset or migration.

## Evidence and scope

Sharon saw workflow traces and DEBUG records with matching correlation IDs on his Mac using the existing tools. M3 command acceptance and the remaining M2 failure/shutdown verification are pending. Guided setup, doctor and additional logging actions can be designed later. The prior design and its three reviews remain available at [the frozen candidate](https://github.com/SharonLanger/agent-playbook/tree/3c641fe4760adfcd487e6eacdc468bcf44148236/designs/refactors/logging/m3-service-composition).
