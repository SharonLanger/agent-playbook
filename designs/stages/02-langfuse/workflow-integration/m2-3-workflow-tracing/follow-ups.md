# Native CrewAI tracing follow-ups

## Current round-02 continuation — 2026-11-15

Sharon approved SDK-first amendment `82b967dda1fbf942cc1067a3539328c74abc303a` to original frozen contract `ab3fab459c97eed44cc0b202402e559a827a71cf`. This supersedes the pending-decision status below only for the explicit amendment scope. Round 02 of three is active; earlier findings/evidence remain historical.

Placement stays within the approved boundaries: application runner owns native updates after successful prepare and after validated-result serialization; maintained Flow constructors supply the public native `name` field; centralized CrewAI startup uses native `CREWAI_DISABLE_VERSION_CHECK=true`. No business step imports a provider. Original design/test/plan, shared requirements/decisions and the amendment are unchanged. Relevant observability research was consulted; no custom telemetry mechanism was adopted.

The public identifier is observed on native exported runner spans at `instrumentation_scope.attributes.public_key`. Origin: Langfuse 5.2.0 `LangfuseResourceManager.__new__` creates its scoped tracer with `attributes={"public_key": public_key}`. Tests require the exact field/value, exclude only that scope attribute from the public-key substring ban, and retain secret/configuration bans on attributes, events, status, resources and other scope metadata. No arbitrary input/exception-secret redaction is claimed.

CrewAI 1.15.40 `events/utils/console_formatter.py:69–76` checks `CREWAI_DISABLE_VERSION_CHECK` before its PyPI helpers. Startup sets this native switch; the fresh-process fixture seeds false, audits Python connect/DNS events during import/normal enabled and disabled execution, and asserts the effective switch is true. In-memory export avoids a backend dependency; this does not prove live OTLP ingestion or audit all OS networking.

Environment evidence: writable HOME/XDG alone still timed out after 50 seconds in the sandbox, with no completed test, waiting in LanceDB `Future.result → lancedb.connect → CrewAI UnifiedMemory`. The same focused suite outside the sandbox passed; a standalone elevated native LanceDB connection also succeeded. All environment changes are test-process settings, with no production workaround. Exact commands/results follow when complete.

Remaining manual acceptance: Sharon supplied successful WF-01 exit/output and screenshot hierarchy/correlation, plus WF-02 and both WF-03 runs. This is partial RUN-18 evidence; explicit branch/skipped-branch verification, failure case, final outer input/output and readable naming still require local UI/readback evidence. DD-02/TG-04 remain pending for that reason.

### Round-02 automated checkpoint

Coder model: `gpt-6.1-sol`. The original CLI remains `app/src/agent_playbook/cli/commands.py` with finally-based flush. Source changes remain minimal native wiring; no custom tracing infrastructure, output interception, state snapshots, monkeypatches or dependency/version changes were introduced. Explicit native client project selection is necessary for repeat invocations when tests have multiple SDK clients.

- Test environment prefix: `HOME=/tmp/pr50-r2-home XDG_CACHE_HOME=/tmp/pr50-r2-xdg-cache XDG_DATA_HOME=/tmp/pr50-r2-xdg-data XDG_CONFIG_HOME=/tmp/pr50-r2-xdg-config`. These are isolated writable test directories, outside the sandbox only for native LanceDB startup; they are not committed configuration or a network workaround. The elevated tool invocation used no additional-network permission field, but runs outside the sandbox; Python network audits below qualify locality evidence.
- Sandbox `timeout 50 app/.venv/bin/python -m pytest app/tests/observability/test_workflow_tracing.py -xq -o faulthandler_timeout=25` with that prefix: timed out, zero completed tests; preserved log `/tmp/pr50-r2-focused.log`. Elevated `timeout 80` same focused suite: initial 24 passed in 13.21s, enhanced 26 passed in 12.29s. Intermediate enhanced assertions incorrectly JSON-decoded native string output and omitted explicit SDK client selection; both were fixed before the full passing gate.
- First full gate stopped at Ruff import ordering; corrected. Next gate: 407 passed/1 failed because the new committed-default test depended on a missing user secrets file; corrected to use committed YAML plus the explicit empty-secrets fixture. No acceptance assertion was weakened.
- `cd app && <test environment prefix> timeout 180 .venv/bin/python -m tooling.checks check`: PASS, Pyright zero errors/warnings, Ruff lint/format PASS (109 files), **408 passed in 48.79s**. Hierarchy, exact three-field metadata, score 59/60 input/output, nested runner/kickoff/step timing, independently reachable parent restoration after success/failure, exact native naming/public-key scope field, payload secret exclusion, explicit false and committed true default are asserted.
- Fresh-process enabled/disabled tests passed as part of the full gate. They audit Python `socket.connect`/`socket.getaddrinfo`, retain zero attempts, use the actual assembly/runner/ABC/Flows and native instrumentor, and seed the opposite version-check setting before startup. The enabled fixture substitutes only in-memory export delivery, retaining native initialization/provider/wrappers.
- `cd app && UV_CACHE_DIR=/workspace/.uv-cache uv pip check`: PASS, 151 installed packages compatible. Lock/pins unchanged.
- `cd app && <test environment prefix> timeout 80 .venv/bin/python tooling/verify_runtime.py dev-run`: PASS, maintained built-ins, both configured aliases/defaults/overrides, execution failure exit 1 and zero Python socket/DNS attempts.
- `python3 designs/atlas/build.py --check`, `git diff --check`: PASS. Changed Markdown relative links: 141 checked, zero missing, with personal/historical sandbox targets excluded.
- Main reconciliation: `origin/main` is `b145e3123f8cc2d2f5095d8a1b605bf6fa6f5672`; its filtered diff from original base `fefe4cc1065642b710a018ecb1088ececde852db` has no changes outside excluded personal examples. No personal examples or historical sandbox were inspected; no merge is needed for this runtime scope.

Installed release verification follows the clean candidate commit; no result is claimed here until complete. Independent reviews and remaining local acceptance are separate. DD-01/TG-01 have passing amended behavior; TG-02/TG-03 have reached payload/restoration/timing assertions. Their final dispositions belong to the independent reviews/orchestrator. DD-02/TG-04 still include incomplete local acceptance. Round count remains 2/3, not a new cycle.

## Historical round-01 blocker — 2026-11-15

Status: **BLOCKED; pending contract decision.** The approved design/test/plan remain frozen at `ab3fab459c97eed44cc0b202402e559a827a71cf` on Stage Design PR #47. This note does not amend that contract. The active coder informed the orchestrator; the orchestrator agreed to preserve the failure and stop affected implementation. No alternative below has user approval.

The actual maintained runner with default quiet CrewAI settings produces one native runner root and **zero** automatic Flow/kickoff/method observations. `show_framework_events: false` maps to `suppress_flow_events=True` in the existing wrappers. Released `openinference-instrumentation-crewai==1.1.25` unconditionally skips instrumentation for that value in all three normal Flow wrappers. Its comment treats the flag as an internal-agent marker. CrewAI 1.15.40's event listener explicitly says the flag “only asks for console quiet and can legitimately be set on a caller's own flow.”

Released installed source evidence (line numbers in these pinned wheels):

- `openinference/instrumentation/crewai/_wrappers.py`: `_FlowKickoffWrapper` around 557–568, `_FlowKickoffAsyncWrapper` around 627–633, `_FlowExecuteMethodWrapper` around 693–699.
- `openinference/instrumentation/crewai/__init__.py`: normal wrapper installation around 95–178; no supported option overrides the suppress check. `TraceConfig` controls payload capture, not this selection.
- `crewai/events/event_listener.py` around 360–371 documents console-only meaning.
- Application wrappers retain their approved mapping unchanged. No framework/instrumentor monkeypatch or per-step instrumentation was added.

Affected acceptance: RUN-01/02/03/04/06 and automatic counts in RUN-08/15 fail under the normal actual application path. RUN-05 lifecycle failures, RUN-07 recovered synthetic child, RUN-09 disabled mode, RUN-10 isolation, RUN-11/12 cleanup and RUN-13 restoration can still be assessed independently. RUN-14 automatic payload acceptance and RUN-17 installed complete integration cannot be established while automatic tracing is absent. RUN-16 full quality gate remains failed. RUN-18 live acceptance is unrun, independent of this blocker.

Observed focused tests retain the required expected hierarchy; they are intentionally not xfailed/skipped or weakened to declare runner-only behavior a pass. Earlier fixture errors (missing key references) and environment failures (CrewAI writing to read-only per-user storage) were corrected/rerun separately and are not the integration finding.

Choices requiring a design-session decision and, where necessary, a new pinned approved baseline:

1. Investigate a released instrumentor fix that distinguishes internal Flows from caller Flows while retaining quiet display; requires a dependency change and fresh compatibility evidence.
2. Explicitly accept enabling framework event display, with changed output and separate verification of CrewAI's PyPI update lookup. This changes the preserve-output/settings boundary.
3. Reconsider event-listener mode or a narrow upstream fix, with explicit scope/behavior review. The approved contract selects normal wrappers; switching silently is prohibited.

The team does not choose among these options. Keep PR #47 open, preserve the approved package and three-round history, and return a BLOCKED candidate for review. Logging, context redesign, ad hoc stdout interception and framework monkeypatches are not workarounds authorized by this note.

## Coder verification checkpoint

- Provisioning: `UV_CACHE_DIR=/workspace/.uv-cache uv add 'openinference-instrumentation-crewai==1.1.25' --python /usr/bin/python3.13` and `uv sync --locked --group dev --python /usr/bin/python3.13` succeeded after approved network escalation. The initial sandbox attempts failed on read-only default uv cache and restricted PyPI networking. Existing lock versions remain unchanged; four integration dependencies were added.
- Initial focused fixture attempts failed because CrewAI requires writable per-user credential storage; approved escalated reruns were used. A missing-key-reference test fixture was corrected. These are separate from the pinned-integration blocker.
- Initial full gate: Pyright and Ruff lint/format passed; pytest **394 passed, 8 failed**. Six failures showed missing Flow observations; two audit fixtures incorrectly treated socket creation (including asyncio local socket setup) as a network attempt.
- Corrected audit checks actual Python socket connection/DNS attempts, like the maintained runtime verifier. The intermediate focused rerun still had **14 passed, 8 failed** because a harmless socket creation was still counted; that fixture was corrected again. No framework/network function is monkeypatched.
- Corrected full gate: `cd app && ./.venv/bin/python -m tooling.checks check` — Pyright 0 errors/warnings; Ruff lint/format passed; pytest **397 passed, 7 failed**. Every remaining failure is the automatic Flow integration blocker. Disabled fresh-process execution and CLI succeed without instrumentation or connection/DNS attempts. Enabled fresh-process setup also reaches zero network attempts, three closed independent roots and preserved outcomes, then fails the required 13-observation count.
- `cd app && UV_CACHE_DIR=/workspace/.uv-cache uv pip check`: **151 installed packages compatible**.
- `cd app && ./.venv/bin/python tooling/verify_runtime.py dev-run`: **PASS**, built-ins, both aliases/defaults/overrides, execution failure exit 1 and zero Python socket/DNS attempts.
- `python3 designs/atlas/build.py --check`, changed Markdown links (165 checked with personal/historical sandbox links excluded), and `git diff --check`: **PASS**.
- Installed release RUN-17: **NOT RUN / BLOCKED** by the failed required quality gate; no bypass, artifact or verified-release claim. Live server/UI RUN-18: **NOT RUN**; no accessible configured deployment or acceptance evidence was supplied. Linux automated evidence does not establish Sharon's Mac/PyCharm behavior. Network auditing covers Python attempts, not an OS-level network guarantee.

The actual CLI implementation is `app/src/agent_playbook/cli/commands.py`, reached through `agent_playbook.cli:main`. New `runtime.py` helpers only initialize native SDK/instrumentor resources and attempt delivery; `_run_selected` holds the unchanged lifecycle inside native runner scopes. No generic tracing API, resource registry or manual step instrumentation is introduced. Coder model: `gpt-6.1-sol`.
