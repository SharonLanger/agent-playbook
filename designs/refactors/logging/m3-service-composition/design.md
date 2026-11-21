# Logging M3 — local service control

Status: **concrete revised design proposed for Sharon's approval**. Sharon approved the three command groups and actions on 2026-11-21 and confirmed in the current instruction that an explicit `logs --start` starts VictoriaLogs even when workflow logging is disabled, without editing YAML. The aggregate `services --start` selects by effective enabled settings. This is design only; runtime implementation and M3 acceptance have not started.

## Boundary and decision record

M3 adds explicit checkout-only service control to the existing `agent-playbook` CLI. Normal `run` and `dev-run` never start or require Docker. Existing Compose projects, service names, named volumes, images, retention and loopback bindings stay in place: logging project `agent-playbook-logging-smoke` and Langfuse default project `observability`. The only broader Docker/project naming work belongs to [issue #56](https://github.com/SharonLanger/agent-playbook/issues/56). The earlier migration/secrets-consolidation proposal and its three review rounds remain historical in [reviews/status.md](reviews/status.md); this revised contract does not migrate volumes or Langfuse deployment secrets. The selected `secrets.file` continues to hold application/project keys, while existing ignored `app/tooling/observability/.env` holds Langfuse infrastructure values. No guarded architecture/principle change is proposed in this design-only PR.

| Command | Start | Status | Stop |
|---|---|---|---|
| `agent-playbook services` | Start each locally managed component whose effective `integrations.logging.enabled` or `integrations.langfuse.enabled` is true. If neither is enabled, print both skipped and exit 0 without Docker. | Report logging and Langfuse separately, with enabled/disabled selection and actual readiness; a disabled but running service remains visible. | Stop both local projects regardless of enabled flags, in reverse start order. |
| `agent-playbook logs` | Start VictoriaLogs even if workflow logging is disabled; do not change YAML. | Show only VictoriaLogs container and read-only `/health` readiness. | Stop only the logging project. |
| `agent-playbook langfuse` | Preserve the existing local manager's start behavior. | Preserve existing status behavior. | Preserve existing project-scoped stop behavior. |

Only these three actions are added to `logs` and `services`. Existing `langfuse --logs/--follow/--open/--check/--env-file` remain supported. `langfuse --check` remains a Docker-free project connection check and returns 3 when disabled. `--config PATH` selects YAML for `services --start/--status`; `services --stop` does not load YAML. `--env-file PATH` on `services` selects the existing Langfuse Compose settings for actions involving Langfuse and is forwarded unchanged; it is irrelevant to logging. `logs` has no configuration or env-file selector because its local Compose settings are fixed. Installed releases continue to reject development commands with exit 2.

## Placement and configuration ownership

Extend `app/src/agent_playbook/cli/parser.py` and `commands.py` with `services` and `logs`, and `cli/development.py` with checkout-only script mappings. Put a small aggregate coordinator at `app/tooling/services.py` and a VictoriaLogs helper at `app/tooling/logging/manage.py`. Reuse `app/tooling/observability/manage.py` for Langfuse, `app/tooling/logging/compose.yaml` for VictoriaLogs and the existing read-only `agent_playbook.observability.adapters.otel_logging.connection.check_connection` with `LoggingSettings(enabled=True)` for the fixed local `127.0.0.1:9428` endpoint. The coordinator invokes component helpers as isolated subprocesses using the active app interpreter; it does not implement Compose itself. No workflow runner or provider SDK change.

Add `load_service_selection(path: str | None)` in `app/src/agent_playbook/config/loader.py`, returning validated logging/Langfuse enable booleans. Refactor the existing loader's selected YAML, sibling local overlay, `secrets.file` parser and process-environment merge into shared internal helpers; no second YAML or dotenv parser. Selection precedence remains base YAML → sibling local YAML → selected secrets file → process environment, including `AGENT_PLAYBOOK_LOGGING_ENABLED` and `AGENT_PLAYBOOK_LANGFUSE_ENABLED`. Require literal YAML booleans and existing `true/false` environment syntax; malformed config or selected secrets file returns sanitized exit 2 before any aggregate start. The selection API deliberately does not resolve Langfuse project keys or validate unrelated workflow settings: those are not needed to start a local service. Thus logs-only aggregate selection is possible without Langfuse keys. Keep `load_configuration` and normal workflow validation unchanged. A hosted Langfuse URL or nondefault logging endpoint does not rewire the local Compose ports; status reports local service readiness only, and the public guide directs users to the existing connection checks for actual application routing.

The coordinator never writes YAML or the secrets file. Explicit component actions do not consult integration enabled flags. Aggregate status loads selection for enabled/disabled labels but still inspects both projects if selection fails; it prints selection unavailable and exits 2 after reporting actual states. Aggregate stop and component stop/status never require application YAML or secrets. No hidden service prerequisite is added to workflow execution.

## Compose identity, data and secret safety

The logging helper calls `docker compose --project-directory <absolute app/tooling/logging> -p agent-playbook-logging-smoke -f <absolute app/tooling/logging/compose.yaml> ...`. This matches the file's current top-level project name and preserves `agent-playbook-logging-smoke_logs-data`; explicit `-p` prevents an ambient `COMPOSE_PROJECT_NAME` from creating an alternate logging stack. It uses `config --quiet`, `up -d`, `ps --all --format json`, and `down` without `-v`. Keep its existing 7-day retention, fixed IPv4 loopback port 9428, pinned image and bridge network. An old manual Compose invocation using the file without a project override targets the same project and volume.

Langfuse actions continue through its existing helper and `--project-directory app/tooling/observability`, `--env-file` default/selection, six-service Compose definition, five named volumes and URL/port rules. Its project is `observability` by default; an existing explicit `COMPOSE_PROJECT_NAME` continues to select that project's stack. The aggregate coordinator forwards that environment to Langfuse but forces logging's fixed project independently. Neither component receives the other's credentials. Do not print Compose config, subprocess environments, secret values or unredacted service logs.

Before Langfuse `--start` creates a new ignored `.env`, check the chosen project's containers and five expected named volumes. If the file is missing but any already exist, return exit 2 with restore-original-file guidance; never generate replacement infrastructure keys over retained encrypted data. The same guard applies through `services --start`. Existing `setup.py` generation remains for a genuinely fresh project. Do not inspect personal secret values during design or tests. Existing custom `--env-file` users must provide that path for aggregate Langfuse operations; the guide documents this explicitly. `down` retains all named volumes. No `down -v`, volume removal, project rename or migration occurs.

## Exact operations and bounded outcomes

From the repository root after `python3 app/tooling/bootstrap.py`:

```sh
app/.venv/bin/agent-playbook services --start
app/.venv/bin/agent-playbook services --status
app/.venv/bin/agent-playbook services --stop
app/.venv/bin/agent-playbook logs --start
app/.venv/bin/agent-playbook logs --status
app/.venv/bin/agent-playbook logs --stop
app/.venv/bin/agent-playbook langfuse --start
app/.venv/bin/agent-playbook langfuse --status
app/.venv/bin/agent-playbook langfuse --stop
```

Use `services --start --config /absolute/path/application.yaml` for another selected YAML. If Langfuse uses a custom private Compose file, add `--env-file /absolute/path/private.env` to aggregate start/status/stop as well. Logging actions always use the fixed local Compose project. The original direct `python3 app/tooling/observability/manage.py` UI-only path remains supported before bootstrap.

Start order is logs then Langfuse; stop order is Langfuse then logs. Aggregate start attempts each enabled component even if the sibling fails; never tears down a successful sibling. Every component prints one of ready, skipped, stopped, unhealthy, unavailable or failed, with its project name and local URL when known. Health checks prove readiness, not record ingestion. Repeat start reconciles the same project; repeat stop is successful and retains data. For aggregate status, exit 0 when every **enabled** component is ready; disabled components are still reported and do not affect the exit (including when stopped). With neither enabled, exit 0 after reporting both physical states. Exit 1 if any enabled component is non-ready; exit 2 on invalid selection. This selection-aware status does not hide a disabled component that is still running. Component status retains 0 ready, 1 non-ready, 2 invalid local settings. For start, exit 0 if all selected components succeed or none selected; exit 2 on configuration/Compose-settings errors, otherwise 1 on any operational/health failure. Aggregate stop returns 0 if both stop, else 1. Invalid CLI combinations exit 2 without touching Docker.

Use one monotonic deadline of 720 seconds for each component start, including Docker engine readiness/optional existing Mac launch, `config --quiet`, `up -d`, each `ps` refresh, HTTP health request and polling. Each subprocess/HTTP timeout is clipped to the remaining budget; if none remains, fail without another call. Use existing 90-second Mac engine launch maximum within this budget; status and stop have 60-second per-component caps and bounded subprocesses. Coordinator gives each selected component its own 720-second cap and reports both; total aggregate start is bounded by two caps plus small coordinator overhead. Ctrl-C stops waiting and returns 1 without implicitly stopping a healthy project. Do not surface raw Docker output that may contain credentials. Existing Langfuse management behavior is retained except for this bounded-deadline and missing-.env safety guard.

## Acceptance and documentation boundary

[Tests](test-cases.md) specify Docker-free default tests, opt-in Compose validation and Mac acceptance separately. Implementation updates `app/docs/cli.md`, `app/docs/logging.md`, `app/docs/langfuse-local.md`, `app/docs/configuration.md`, the tooling logging README and relevant indexes. They document the distinct meanings of workflow export enablement and explicit local service start, current secret owners, project names, flags, exits and persistence. Preserve existing Stage 02 acceptance and issue #56. Update logging discovery/Atlas with a proposed status now and shipped status only after evidence. M2's remaining failure/shutdown LG-10 check stays open until actual Mac evidence is recorded.
