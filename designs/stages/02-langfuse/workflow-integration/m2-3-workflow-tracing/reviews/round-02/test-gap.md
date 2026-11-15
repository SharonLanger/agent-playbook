# Round 02 independent test-gap review

Author role/model: independent test-gap reviewer, `gpt-6.1-sol`. Frozen candidate `adbba215da77e1e618c3c699e1d84c1ba45c629e`; original contract `ab3fab459c97eed44cc0b202402e559a827a71cf`; approved amendment `82b967dda1fbf942cc1067a3539328c74abc303a`. **Verdict: CHANGES REQUIRED solely for outstanding manual RUN-18.** No candidate files edited.

Findings: **TG-01 BLOCKER RESOLVED** by approved visible-framework default and passing exact automatic hierarchy tests. **TG-02 MEDIUM RESOLVED**: success/error external-parent restoration now has separate reachable nodes and automatic payload checks execute after passing hierarchy assertions. **TG-03 MEDIUM RESOLVED**: each child's full interval is asserted inside its parent's interval. **TG-04 MANUAL ACCEPTANCE BLOCKER OPEN**: Sharon's screenshot and runs provide partial local evidence, but explicit selected/skipped branches, failed step, outer input/output and readable names need local UI/readback. One nonblocking precision weakness remains: `test_real_step_failure` identifies its three ERROR spans by count; exact error names would improve diagnosis, though normal hierarchy cases and combined assertions give substantial evidence.

`T` = `tests/observability/test_workflow_tracing.py::`. H1–H4 are exact independently collected parameters of `T::test_runner_hierarchy_and_exact_identity`: H1 WF-01/None; H2 WF-02/None; H3 WF-03/score 60/pass; H4 WF-03/score 59/needs_work. “Gate PASS” below is coder's exact-candidate 408-pass full gate, not this reviewer's independent runtime execution.

| ID | Exact nodes and meaningful assertions | Status/evidence |
|---|---|---|
| RUN-01 | T H1: unchanged result, exact five observations, root/kickoff/three-step parentage, unique IDs/one trace | Gate PASS |
| RUN-02 | T H1–H4: each exported root/descendant has exact captured three context IDs | Gate PASS |
| RUN-03 | T H2: result 20, initialize/add/multiply/finish, six observations including None-return methods | Gate PASS |
| RUN-04 | T H3/H4: score 60 accept or 59 revise, exact executed set and skipped branch absent | Gate PASS |
| RUN-05 | `T::test_lifecycle_failure_root[CONSTRUCTION/INPUT/PREPARE/EXECUTE/VALIDATE_OUTPUT/SERIALIZE_OUTPUT]`: classification/cause, ended ERROR root, no successful output or invented early validated input | Gate PASS |
| RUN-06 | `T::test_real_step_failure`: original failure cause, three ERROR observations, prior success, finish absent | Gate PASS; precision weakness above |
| RUN-07 | `T::test_recovered_child_through_runner`, `test_native_recovery_and_agent_isolation`: failed child, successful root | Gate PASS, synthetic fixture |
| RUN-08 | `T::test_repeat_invocations`, `test_fresh_process_initialization_and_locality[True]`: fresh IDs/traces, 12 and 13 expected spans, no duplicates/shutdown | Gate PASS |
| RUN-09 | `T::test_fresh_process_initialization_and_locality[False]`: unchanged output/error, no instrumentor/exporting provider/network | Gate PASS |
| RUN-10 | `T::test_native_recovery_and_agent_isolation`: A/tool and B/tool isolated, checkpoint/root free of agent fields, restoration | Gate PASS, synthetic mechanism |
| RUN-11 | `T::test_cli_flush_after_close[None-0]/[invalid-2]`, `test_cli_flush_execution_failure`, `test_setup_failure_needs_no_client`: after-close flush and preserved exits/errors | Gate PASS |
| RUN-12 | `T::test_cleanup_failure_preserves_outcome[None-0]/[invalid-2]`: simulated flush fault preserves outcome and sanitized diagnostic | Gate PASS, simulated |
| RUN-13 | T H1–H4: parent.start <= child.start <= child.end <= parent.end; `test_external_parent_restoration[None]/[invalid json]`: original parent restored success/error | Gate PASS |
| RUN-14 | T H1–H4: automatic attrs/events/status/resource/scope; exact public-key field; `test_configuration_excluded_from_root_payload[normal/EXECUTE]`: root success/error secret bans | Gate PASS; arbitrary business-input secrets not promised redacted |
| RUN-15 | `T::test_fresh_process_initialization_and_locality[True]`: shared native provider/instrumentor, configured loopback, CrewAI cloud off, native version check off, zero Python connect/DNS | Gate PASS; Python-level audit only |
| RUN-16 | `cd app && .venv/bin/python -m tooling.checks check`; `uv pip check` | Gate PASS: Pyright/Ruff, 408 pytest, 151 compatible packages |
| RUN-17 | Existing release dependency/completion tests plus actual clean release and installed commands/fixture | Gate PASS: verified 0.1.3 wheel, hash/install/inventory/failure/offline check; release result supplied after reviewer cutoff and recorded by coder/orchestrator |
| RUN-18 | Local UI/readback for all workflows/branches/failure/correlation and new outer input/output/names | PARTIAL MANUAL; TG-04 OPEN |
| RUN-19 | Existing application runner/contract, CLI and Langfuse mock/auth/SDK regression nodes in full suite | Gate PASS; framework-visible output is approved amendment |
| RUN-20 | Atlas/whitespace/link checks, public guides, round reports and complete mapping | Independent Atlas/whitespace PASS; 141 links coder PASS; reports published after review |

| Amendment | Exact mapping | Status |
|---|---|---|
| R2-01 | T H1–H4; `test_committed_framework_default`, `test_explicit_quiet_override_is_preserved`, fresh disabled process | Gate PASS |
| R2-02 | T H3/H4 score 59/60 actual input/final output; H1/H2 omitted mapping; six lifecycle failures absent fabricated output/input | Gate PASS |
| R2-03 | T H1–H4 full nested timing; `test_external_parent_restoration[None]/[invalid json]` separate | Gate PASS |
| R2-04 | T H1–H4 native kickoff/step names and `flow_id`; repeat identity test | Gate PASS, UI manual |
| R2-05 | T H1–H4 automatic payload and exact public-key scope exception; root success/error payload cases | Gate PASS |
| R2-06 | Fresh enabled/disabled process audit before import through shutdown, native version switch seeded opposite | Gate PASS, Python-level scope |
| R2-07 | RUN-16/17/19 plus installed release/offline runtime verifier | Gate PASS; release result arrived after reviewer cutoff |

Independent checks: exact candidate HEAD; `python3 designs/atlas/build.py --check` PASS; `git diff --check fefe4cc adbba215` PASS; isolated writable HOME/XDG `timeout 20 .venv/bin/python -m pytest tests/observability/test_workflow_tracing.py --collect-only -q` collected **28 nodes in 0.34s**, exit 0. No heavy runtime rerun while installed release ran. Prior restricted-sandbox LanceDB hangs are environment failures, not integration outcomes. Linux/Python connect/DNS and in-memory delivery do not establish OS-wide isolation, Mac/PyCharm behavior or live ingestion. Personal examples and historical sandbox were not inspected.
