# Native CrewAI tracing blocker — 2026-11-15

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
