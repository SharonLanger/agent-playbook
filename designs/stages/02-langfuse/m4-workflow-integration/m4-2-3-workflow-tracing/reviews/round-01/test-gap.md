# Round 01 independent test-gap review

Author role/model: independent test-gap reviewer, `gpt-6.1-sol`. Frozen candidate `4df1a434c37cfff0b20d8b719bbb6841ea0e9e33`; base `fefe4cc1065642b710a018ecb1088ececde852db`; contract `ab3fab459c97eed44cc0b202402e559a827a71cf`. **Verdict: CHANGES REQUIRED.** No files edited by reviewer.

Findings:

- **TG-01 BLOCKER, OPEN.** RUN-01–04/06/08/15 need automatic maintained Flow hierarchy. Coder's exact-candidate gate is 397 passed/7 failed, including four hierarchy parameters, repeat, real step failure, and enabled subprocess. Assertions correctly fail instead of weakening expectations. References: `app/tests/observability/test_workflow_tracing.py:93,178,201,369`, `app/tests/fixtures/native_tracing_process.py:78`.
- **TG-02 MEDIUM, OPEN.** RUN-13 external-parent restoration assertions occur after a failing 12-span count; RUN-14 automatic payload checks after failing hierarchy counts. Root-only payload checks cannot establish automatic capture safety. References: tracing test lines 93–198.
- **TG-03 MEDIUM, OPEN.** RUN-13 checks each span's `end_time >= start_time` but not that child intervals lie within parent intervals; parent restoration remains blocked. Reference: tracing test lines 123–164.
- **TG-04 MANUAL ACCEPTANCE BLOCKER, OPEN.** RUN-18 has no actual local server/UI/readback evidence for all workflows, branches, failed step, hierarchy and exact correlation.

`T` below means `app/tests/observability/test_workflow_tracing.py`. PASS denotes coder exact-candidate gate evidence unless marked independent. Assertions after a failed earlier assertion are blocked even when present in the source.

| ID | Nodes and meaningful assertions/evidence | Status |
|---|---|---|
| RUN-01 | `T::test_runner_hierarchy_and_exact_identity[wf-01,None]`: result, exact root/kickoff/produce/decorate/finish IDs, trace and parentage | FAIL, TG-01 |
| RUN-02 | Same node: exported metadata JSON equals captured context's three IDs | PARTIAL: root exact, descendants absent |
| RUN-03 | Same node `[wf-02,None]`: result 20 and initialize/add/multiply/finish even for None methods | FAIL, TG-01 |
| RUN-04 | Same node `[wf-03,score=80/20]`: expected accept OR revise, skipped branch absent, outputs | FAIL for both branches, TG-01 |
| RUN-05 | `T::test_lifecycle_failure_root` six phase parameters: classified error/cause, one ended ERROR root | PASS |
| RUN-06 | `T::test_real_step_failure`: failed multiply/kickoff/root, prior success and no finish | FAIL: only root |
| RUN-07 | `T::test_recovered_child_through_runner`; `test_native_recovery_and_agent_isolation`: child ERROR, parent success | PASS synthetic fixture |
| RUN-08 | `T::test_repeat_and_parent_restoration`; enabled fresh subprocess: repeated roots/IDs, same step counts, no duplicates | FAIL before later IDs/parent checks |
| RUN-09 | `T::test_fresh_process_initialization_and_locality[False]`: outputs/errors, no instrumentor/exporting provider/network | PASS |
| RUN-10 | `T::test_native_recovery_and_agent_isolation`: A/tool → workflow → B/tool IDs, exception restoration | PASS synthetic mechanism |
| RUN-11 | `T::test_cli_flush_after_close[None/invalid]`, `test_cli_flush_execution_failure`, `test_setup_failure_needs_no_client`: after-close flush and exit/result | PASS |
| RUN-12 | `T::test_cleanup_failure_preserves_outcome[None/invalid]`: injected cleanup fault preserves computation/error and sanitized diagnostic | PASS simulated |
| RUN-13 | Hierarchy timing/parent assertions, `test_repeat_and_parent_restoration` outer scope after success/error | BLOCKED/WEAK, TG-02/03 |
| RUN-14 | Hierarchy attrs/events/status plus `test_configuration_excluded_from_root_payload` normal/execute-error | Root PASS; automatic BLOCKED |
| RUN-15 | `T::test_fresh_process_initialization_and_locality[True]`: provider, local endpoint, cloud telemetry off, zero audit attempts, 13 spans | FAIL on span count; earlier locality checks partial |
| RUN-16 | Exact-candidate gate: Pyright/Ruff PASS, pytest 397 passed/7 failed; lock/install compatibility recorded | FAIL overall |
| RUN-17 | Existing `tests/tooling/test_release_dependencies.py`, `test_release_completion.py` test release machinery; new installed artifact/hash not established | NOT RUN/blocked by gate |
| RUN-18 | Local server/UI/readback for WF-01/02/03 both routes and failed step | NOT RUN/manual, TG-04 |
| RUN-19 | Existing `tests/application/test_workflow_runner.py`, `test_runner_contract.py`, `tests/cli/test_workflow_commands.py`, Langfuse connection/observations/SDK delivery tests | Supplied gate PASS; independent partial 8 PASS only |
| RUN-20 | Atlas check, whitespace, public docs, permanent reports/mapping | PARTIAL; independent Atlas and whitespace PASS; reports completed after review |

Independent checks: `python3 designs/atlas/build.py --check` PASS; `git diff --check BASE CANDIDATE` PASS. Independent `app/.venv/bin/python -m pytest tests/observability/test_workflow_tracing.py -q` was interrupted after 91.33s with **no tests ran**; no pass/fail evidence. Regression selection was interrupted after 58.61s with **8 passed**, rest unrun. Neither interruption replaces coder's exact-candidate result. No release build or live acceptance run. Excluded personal examples and historical sandbox were not inspected.
