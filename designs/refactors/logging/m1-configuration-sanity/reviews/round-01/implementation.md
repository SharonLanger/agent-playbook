# M1 implementation evidence — round 01

2026-11-16. Coder: `gpt-6.1-sol`. Branch:
`impl/logging-m1-configuration-sanity`; base/main
`529fe15895afc8211d833fc2544e98f0d18fb451`. Frozen code/test candidate:
`d15a5d3f7dcfd29aaba068db89808c1856b6218d`. The orchestrator committed that
candidate after the coder's uncommitted handoff. The coder performed no commit,
PR action, acceptance or merge.

## Authority and placement

Sharon explicitly authorized M1 implementation at contract
`045f9a0d98ccec1f200af6f80adb7d5eb45e66d5`, supplied by the orchestrator.
Loaded root/design AGENTS, design contract, guarded register, stage/milestone and
handover rules, inventory, charter, principles, architecture, project structure,
roadmap/progress and observability exploration. Read the pinned M1 design,
test-cases and implementation plan, shared requirements/decisions, repository
impact assessment, direct-OTLP/SDK-exception/VictoriaLogs research with `git show`.
The draft labels in those frozen files were preserved; authority comes from the
explicit pinned implementation instruction, not their draft headings.

Repository → app → tooling → logging owns the opt-in synthetic emitter and isolated
service. Inputs are the explicit local endpoint and synthetic identity; output is
one SDK log export attempt and an operator correlation/UI instruction. The tool
owns provider cleanup and leaves actual delivery confirmation to the operator.
This is ordinary tooling placement, with no production dependency on tooling.
LOG-23–25 and LD15/18/19 govern; collector-first research remains superseded.

Changes:

- `app/tooling/logging/compose.yaml`: fixed project identity, pinned single
  VictoriaLogs service, local storage/logging, seven-day retention, loopback
  publication and one internal network.
- `app/tooling/logging/logging_smoke.py`: Python logging → supported contrib
  LoggingHandler → dedicated LoggerProvider/BatchLogRecordProcessor → direct HTTP
  exporter. Validates the endpoint before constructing the exporter; ignores
  environment proxies and refuses redirects. Provider shutdown is in `finally`;
  output explicitly leaves delivery unconfirmed. Resource attributes are supplied
  directly, avoiding ambient resource-attribute injection; exporter headers are
  explicit and empty. No global tracing/root logger instrumentation.
- `app/tooling/logging/README.md` and `app/docs/configuration.md`: exact opt-in
  commands, UI acceptance, versions, retention, prerequisites and limitations.
- `app/pyproject.toml` / `app/uv.lock`: only the missing aligned logging
  instrumentation 0.66b2 added. Parsed before/after lock tables confirm every
  existing package version unchanged.
- `app/tests/tooling/test_logging_smoke.py`: focused LS-03 endpoint rejection and
  real Requests session proxy/redirect behavior with a deterministic adapter.
  These offline checks do not claim export/ingestion success.

No guarded contracts were edited. Personal examples and historical sandbox were
not read, searched, run or changed. Public documentation is updated for the new
developer command. No diagram or new architectural boundary needs an Atlas
change; package/status reconciliation is owned by the orchestrator. Atlas
freshness is separately blocked by the inherited baseline condition below.

Principles: explicit pinned approval and unchanged guards (1/3); synthetic fields,
local validation and no secrets (2/6/10); isolated SDK/tooling reuse (5); focused
checks and exact dependency alignment (7/8); M1-only incremental learning (4/9);
historical material untouched (11); permanent traceable evidence (12/15);
sandbox-independent maintained gates (13); supported developer guide updated
(14). No production logging, M2 checks/runner integration, management CLI,
collector, umbrella Compose, custom retry/queue/transport or viewer introduced.

## Environment and artifact evidence

- Linux amd64; CPython **3.13.5** at `/usr/bin/python3.13`.
- **uv 0.13.6**, **Pyright 1.1.407**, **Ruff 0.14.4**, **pytest 8.4.2**.
- Docker CLI **29.9.2**, API **1.56**; Compose **v2.40.3**. Daemon version/Desktop
  unavailable: default local socket `/var/run/docker.sock` returns permission
  denied. Orchestrator independently found `/run/codex-docker/docker.sock` also
  inaccessible. No image/container/UI run occurred.
- SDK and HTTP exporter **1.45.2**; logging instrumentation **0.66b2**. Installed
  distribution metadata for all three declares `License-Expression: Apache-2.0`.
  VictoriaLogs **v1.54.0** LICENSE retrieved from its pinned upstream raw GitHub
  URL and starts with Apache License Version 2.0. See tooling README for immutable
  project license links. No image-layer/transitive-license certification claimed.

## Commands and results

Commands below run from repository root unless prefixed `cd app`.

| ID / check | Command / observation | Result |
|---|---|---|
| LS-01 | `docker version`; `docker compose version` | Client/Compose versions above; daemon access denied |
| LS-01 | `docker compose -f app/tooling/logging/compose.yaml config` and `config --format json` | PASS; rendered project is `agent-playbook-logging-smoke` |
| LS-01 | Parsed rendered JSON and asserted sole service/image, local volume/logging driver, loopback host IP, sole internal network and `-retentionPeriod=7d` | PASS |
| LS-02 | Actual emit → VictoriaLogs → local UI record after cleanup | **NOT RUN**; daemon unavailable. No substitute integration claim |
| LS-03 | `cd app && .venv/bin/python -m pytest -q tests/tooling/test_logging_smoke.py` | **15 passed**, final focused run 0.32s |
| LS-03 | Invalid scheme/host/credentials/path/query/fragment/port rejected via CLI before exporter construction; default/alternate local ports accepted | PASS in focused checks |
| LS-03 | Actual configured Requests session + deterministic HTTP adapter returning remote redirect, with ambient HTTP/ALL proxy settings | PASS: no proxy supplied to adapter; exactly one local destination; TooManyRedirects before remote request |
| LS-04 | Diff/path/import/Compose review | PASS; only tooling/dependency/docs/focused-check/evidence files, no production or excluded scope changes |
| Dependency lock | `cd app && UV_CACHE_DIR=/workspace/.uv-cache uv lock` | Initial network-restricted attempt failed; authorized network-enabled retry PASS, 155 resolved packages, only logging instrumentation added |
| Environment | `cd app && UV_CACHE_DIR=/workspace/.uv-cache uv sync --locked` with authorized network permission | PASS; 152 packages installed |
| Dependencies | `cd app && UV_CACHE_DIR=/workspace/.uv-cache uv pip check` | PASS; 152 compatible installed packages |
| Entry point | `cd app && .venv/bin/python tooling/logging/logging_smoke.py --help` | PASS |
| Full gate | `cd app && .venv/bin/python -m tooling.checks check` | Static/lint/format PASS after corrections; pytest blocked during collection by read-only user data directory |
| Full gate retry | `cd app && XDG_DATA_HOME=/tmp/agent-playbook-m1-data XDG_CACHE_HOME=/tmp/agent-playbook-m1-cache UV_CACHE_DIR=/workspace/.uv-cache .venv/bin/python -m tooling.checks check` | Pyright 0 errors/warnings, Ruff lint PASS, 111 formatted files PASS; pytest collection blocked by CrewAI credential directory below |
| Atlas | `python3 designs/atlas/build.py --check` | FAIL: `Atlas is stale`; no Atlas source changes in this implementation; orchestrator confirmed inherited baseline limitation |
| Whitespace | `git diff --check` | PASS |

Early local iterations caught and fixed unused import, missing contrib type-stub
diagnostic (narrow import-specific suppression), test adapter override signature
and protected response-content access. All are corrected in the final static and
focused test results above. The first gate encountered three read-only
`/home/agent/.local/share/app` collection errors; XDG redirection resolved those,
leaving one collection error in CrewAI's hardcoded token-manager directory.

Automatic approval review rejected additional write access for the full gate to
`/home/agent/.local/share/crewai`: it would create persistent credential material
outside the authorized workspace. The rejection suggested a temporary HOME or
credential path. This session's developer rules prohibit repurposing HOME, so
the coder did not do that or retry persistent access. Full application tests
remain blocked; no claim that the full gate passed. Orchestrator notified.

## Limits and local completion

The pinned SDK batch processor's `force_flush(timeout_millis=...)` currently
ignores that argument (source TODO #4568) and performs synchronous export. The
probe supplies a five-second exporter timeout and five-second flush request;
SDK shutdown has a default 30-second worker join. These settings are not a strict
whole-process deadline. Reusing these SDK facilities, with honest documented
limits, avoids custom timeout/thread/retry machinery. A successful flush call
does not establish delivery.

Docker Engine 28+ is the source-backed prerequisite for loopback semantics, not a
tested service minimum. Internal network + host loopback publication and UI
compatibility remain unverified on Linux or Sharon's Mac. No durable spool,
outage/rotation/load/disk/security matrix, backend substitution, release build or
Langfuse regression proof is claimed by this M1 check.

When a local daemon is available, run the exact README commands, emit synthetic
data, open `http://127.0.0.1:9428/select/vmui`, query the printed correlation ID,
and inspect message `Logging smoke check`, INFO severity, `workflow_id`,
`workflow_run_id`, and `correlation_id` after script cleanup. Record that actual
LS-02 result separately. Stop the service without deleting its volume. User
acceptance and any merge authorization remain pending.
