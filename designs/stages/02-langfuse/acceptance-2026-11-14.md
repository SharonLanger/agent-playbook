# Local Langfuse acceptance — 2026-11-14

Status: **Local setup and mock-trace exercise accepted by Sharon on Mac; PR #36 remains unmerged.**

## Scope and revision

Sharon pulled PR #36 after YAML-selected secrets support was pushed at
`b80b22bd91281ed798aaf745f950007c82c92b44`. He created the local project,
used his own credentials and inspected the explicitly invoked mock example.
This is user-reported live evidence, distinct from the managed Linux test gate.
The local Docker Desktop/Engine/Compose versions were not captured in this session.

## Observed results

| Check | Evidence and result |
|---|---|
| Local service and project access | Sharon opened the local UI and created his account, organization/project and project keys. |
| Credential configuration | External credentials file selected through top-level YAML `secrets.file`; Langfuse enable, base URL and environment stay in YAML. Keys are not recorded here. |
| Live synthetic ingestion | The example's root `mock-wf-02` and `initialize`, `add`, `multiply`, `finish` observations appeared, with default result 20. |
| Trace inspection | Sharon opened the trace tree/timeline/graph, enabled the Trace ID column and filtered one trace ID to show its related observations. |
| Persistence | Sharon stopped and restarted the local service and confirmed his project and earlier traces were still visible. |
| Acceptance | Sharon said the setup was working and authorized merging after his planned enable/version push and pre-merge record reconciliation. The enable/version push is now recorded below; the merge remains pending. |

## Remaining delivery-confirmation limitation

One run printed `delivery: unconfirmed` even though Sharon found that run in the UI.
This proves visible ingestion for that run, but not reliable bounded API readback.
The cause was not diagnosed: query delay, timeout and request failures remain
possibilities, not established explanations. The script must retain its honest
unconfirmed status when readback cannot establish delivery. No retry/replay change
was made. Investigate before treating command-line delivery confirmation as reliable.

Specific deliberate add/multiply failure UI scenarios were not independently
confirmed in this conversation; earlier offline fixtures retain their own evidence.
No real workflow, agent, model call, automatic tracing or offline replay was added.
M4 remains deferred for its separate workflow/context integration design.

## Agent verification and governance

At application revision `b80b22b`, the maintained gate passed 363 tests, Pyright
with zero errors/warnings, Ruff lint and Ruff formatting. The command from `app/`
was `env -u ALL_PROXY -u all_proxy NO_PROXY=localhost,127.0.0.1,::1 .venv/bin/python tooling/checks.py check`.
The proxy adjustment applied only to the managed runner. No real project keys or
service were used by that gate. Sharon subsequently pushed `dafeaedf82df9497700f523a460d9055decafd82`: Langfuse
enabled in shared YAML and application/lock version 0.1.3. This pre-merge update
preserves that push and aligns first-installation docs with the enabled default.
The complete maintained gate was rerun against that shared-default/version
revision: 363 tests, zero Pyright errors/warnings, Ruff lint and formatting passed.
Earlier release evidence remains historical; no 0.1.3 release artifact was built
by this documentation reconciliation.

This record follows the design contract and existing config/tooling/adapter owners.
The observability exploration remains non-binding. The user authorized factual
pre-merge status reconciliation; stage architecture changes are limited to its
status header, with approved milestone boundaries and all contracts retained.
Stage 01/PR #40 already records completed acceptance; old review findings remain
historical. Official product guides already document current behavior, so this
acceptance-only update does not change their instructions. Progress, stage entry,
verification status and Atlas are reconciled together. No whole-Stage-02 completion
or merge is claimed while M4 and the merge itself remain pending.

## Final local-state test correction

The later test-only commit `0a5bf882358b760d92452329c8c56fc0224618b1`
fixes `test_fresh_checkout_status_and_stop_without_settings` by selecting a fresh
`tmp_path` deployment directory. Previously it observed the real checkout's
ignored Docker settings, explaining why Sharon's configured Mac differed from
the clean managed checkout. Production behavior is unchanged.

After fetching that exact test revision, the targeted command
`app/.venv/bin/python -m pytest -q app/tests/tooling/test_langfuse_manage.py::test_fresh_checkout_status_and_stop_without_settings`
passed: **1 passed**. The earlier 363-test gate remains pinned to `dafeaed`;
no new full-suite result is claimed for this test-only follow-up.

## Next-agent boundary

After an explicitly authorized merge, reconcile the resulting main revision and
merge state in progress and Atlas. The next agent should read the governing
documents, this acceptance record and the actual merged workflow contract before
reviewing logging/context design. Existing research is not implementation approval.
Real workflow tracing, context propagation, logging schema and telemetry-outage
policy remain separate design work. This session does not implement them.
