# Logging M3 implementation review status

Approved design, test cases and plan: `c4e0951bd87c81e627d58127841494d4812732ab`, approved by Sharon on 2026-11-21. Implementation base/target: main `46e9062d1fbedefbc04240c280d12001cfdea0ac`. Branch: `impl/logging-m3-service-control`; draft PR #65. Design PR #57 and overall logging design PR #51 remain open/draft.

**Current disposition after Sharon's one additional focused M3-D03 correction/review: BLOCKED.** The newly frozen code/test candidate is `df64582af4e3accb4b0747e3c1b44a429d541a6b`. Both independent reviewers assessed that same SHA and returned CHANGES REQUIRED: the design reviewer reproduced a failed `docker logs --follow` diagnostic reaching stderr before the CLI knows the subprocess failed; the test reviewer found that path absent from maintained tests. See [additional M3-D03 review](additional-m3-d03/status.md). The new authorization used **1/1** round; the earlier three-round history below remains intact. The PR is not ready for Mac verification or merge.

## Earlier three-round implementation review — historical

**Outcome: BLOCKED after 3/3 authorized implementation rounds.** The final code/test candidate is `912e5bc7289960baf14333427d9f0b2a08cbcd58`. No fourth correction/review round is authorized. M3-D03 remains open: the current Compose settings used to redact `langfuse --logs` may differ from settings held by existing containers, leaving an older credential visible in a service diagnostic. The reviewer reproduced the filter gap with synthetic values; whether a real container emits that diagnostic was not tested. Do not merge or claim M3 acceptance.

| Round | Frozen candidate | Design verdict | Test verdict | Disposition |
| --- | --- | --- | --- | --- |
| [01](round-01/orchestrator.md) | `319950acba1beabc36e9c3ed5dcac8126bffa1be` | [CHANGES REQUIRED](round-01/design-drift.md) | [CHANGES REQUIRED](round-01/test-gap.md) | D01–03, TG01–04 sent to coder |
| [02](round-02/orchestrator.md) | `d3b53850bb839b4ef7d070f2242715acedba233b` | [CHANGES REQUIRED](round-02/design-drift.md) | [CHANGES REQUIRED](round-02/test-gap.md) | D01/TG01–04 closed; D02/D03 and TG05 sent to coder |
| [03](round-03/orchestrator.md) | `912e5bc7289960baf14333427d9f0b2a08cbcd58` | [CHANGES REQUIRED](round-03/design-drift.md) | [PASS](round-03/test-gap.md) | D02/TG05 closed; D03 remains open; stop at cap |

One coder and two independent reviewers assessed each same-round frozen SHA. Coder, design reviewer and test reviewer configured model IDs were `gpt-6.2-sol`; serving IDs were unavailable. The orchestrator's exact serving model ID was unavailable in this session (identified as GPT-6 by the host). Reports were added only after all three code/test candidates were frozen; compare the final candidate with the published report-only head to confirm no code or test change.

## Acceptance evidence map at final candidate

| ID | Evidence and status |
| --- | --- |
| SC-01 | Parser, release rejection, direct-script help, disabled Langfuse check and ancillary actions in `test_cli_tasks.py`, `test_development.py`, `test_langfuse_manage.py`: offline PASS. |
| SC-02 | `test_service_selection.py`, `test_service_cancellation.py`: four combinations, loader precedence, caller-relative selectors, malformed input and bounded selection: offline PASS. |
| SC-03 | `test_service_cli_integration.py`, `test_service_managers.py`: explicit logs start despite disabled export, aggregate skip and byte-preserved configuration: offline PASS. |
| SC-04 | Same CLI integration and selection matrix: key-free logging lifecycle and retained workflow key validation: offline PASS. |
| SC-05 | `test_service_managers.py`, `test_service_cli_integration.py`: fixed logging project, Compose identity precedence, collision, repeat start and retained volumes: offline PASS. |
| SC-06 | `test_service_cli_integration.py`, `test_service_selection.py`: disabled-running status, invalid selection and stop order/continuation: offline PASS. |
| SC-07 | `test_service_cancellation.py` and manager budget tests: real POSIX shortened outer start/status/stop timeout, Ctrl-C, descendant cleanup, TERM/KILL order, no implicit down: offline PASS. |
| SC-08 | `test_service_managers.py`, `test_langfuse_manage.py`: asset inventory, identity, guarded initialization and current-config redaction: offline tests PASS; **M3-D03 historical-container redaction remains open**. |
| SC-09 | Maintained tests use fake Docker/synthetic settings: PASS. Separate opt-in Compose v2.40.3 syntax, project-name matrix and synthetic redaction: PASS. |
| SC-10 | Live Mac lifecycle, ingestion/readback, trace and physical-volume acceptance: **NOT RUN**. |
| SC-11 | Workflow dispatch isolation and explicit service/export independence in CLI integration and existing application tests: offline PASS. |
| SC-12 | Public/tooling docs, indexes, Atlas and diff inspected: PASS for recorded scope; Mac SC-10 and M2 LG-10 remain NOT RUN. |

Final candidate gate: `CREWAI_STORAGE_DIR=/workspace/scratch/m3-crewai-tests-round03 app/.venv/bin/agent-playbook check` passed Pyright (0 errors/warnings), Ruff lint/format (125 files) and 553 pytest tests in 82.84 seconds. It ran outside the sandbox under automatic approval because a standalone LanceDB open stalled in the default sandbox. Focused default-sandbox suite: 118 passed. `python3 designs/atlas/build.py --check` and `git diff --check` passed. Opt-in daemon-free Compose script passed on v2.40.3 with synthetic values; no live Docker stack was started. Live Mac SC-10 and M2 LG-10 are NOT RUN. No app/examples or real secret values were accessed.
