# Round 2 — coder correction report

Role: coder. Date: 2026-11-14. Implementation PR: [#44](https://github.com/SharonLanger/agent-playbook/pull/44), branch `feat/m4-1-context`, target `docs/workflow-observability-planning`. Implementation base and approved M4.1 design: `11bba581291c1b166973848ea8db6a9e2a142413`. Frozen round-2 code/test candidate: `16c1580e96bd36945fa96b6ecfa8f9a563d53913`. This report is a later report-only delta. Round count is 2/3; round 1 remains preserved.

## Corrections to every round-1 finding

| Finding | Correction and actual assertion | Files / test node |
|---|---|---|
| T-001, CTX-04 | The inner helper now raises on the failure path. Both helper observations are checked by object identity for normal and failure paths; failed child, parent and sibling identities remain unchanged. | `app/tests/context/test_models.py::test_children_and_nested_helpers_preserve_parent_and_siblings` |
| T-002, CTX-05 | Assigning to a derived child's `agent_run_id` raises `FrozenInstanceError` and the original value remains. | `app/tests/context/test_models.py::test_ordinary_assignment_is_rejected` |
| T-003, CTX-08 | Through the real runner, factory and each maintained wrapper, a spy delegates to the actual Flow constructor and retains the actual object. Each real kickoff/result is checked; `flow.context is` the runner factory argument for WF-01/02/03. | `app/tests/application/test_context.py::test_runner_context_reaches_each_real_flow` |
| T-004, CTX-10 | Nondefault correlation, workflow/run and agent values are checked for absence from Flow model dump and business state before/after execution, along with application field/key names; CrewAI's separate `execution_context` field is retained. | `app/tests/workflows/test_context.py::test_real_flow_keeps_context_out_of_business_state_and_serialization` (four parameters) |
| T-005, CTX-11 | A second real Flow is constructed, then its kickoff raises an injected exception. The first Flow's exact context reference, state value and result remain intact; existing success/success and later failed prepare checks remain. | `app/tests/workflows/test_context.py::test_consecutive_flows_keep_original_context_and_result` |
| T-006, CTX-12 | The existing assembly/registry/selection failure matrix now spies on `ExecutionContext` and asserts no construction in each of those three earlier failure paths. Its original cause/category/order checks remain; the separate context-construction failure case still checks exact cause/category. | `app/tests/application/test_followup_boundaries.py::test_failure_stops_before_success` (assembly/registry/selection); `app/tests/application/test_context.py::test_context_construction_failure_has_existing_boundary` |

No round-1 design-drift finding required a production fix. The entire M4.1 production and guarded diff from round 1 remains unchanged. G01–G08 retain Sharon's approval reference from his implementation instruction at the approved design revision. No dependency, CLI, YAML, SDK instrumentation, logger, agent runtime, personal examples or public guide change was introduced in round 2. The existing official workflow guide and progress/Atlas updates remain on the implementation branch. Their review is still pending final candidate review.

## CTX-01–17 mapping and checks

CTX-01/02: `tests/context/test_models.py::test_fresh_identity_and_explicit_reuse`; CTX-03/04: `test_children_and_nested_helpers_preserve_parent_and_siblings`; CTX-05: `test_ordinary_assignment_is_rejected`; CTX-06: `tests/application/test_context.py::test_runner_fresh_roots_and_alias`; CTX-07: `test_factory_forwarding` for three IDs plus maintained registry tests; CTX-08: `test_runner_context_reaches_each_real_flow` and direct real Flow cases; CTX-09: `tests/workflows/test_context.py::test_scheduled_decorated_paths_can_read_context` for scores 80/40; CTX-10: `test_real_flow_keeps_context_out_of_business_state_and_serialization` for four parameters; CTX-11: `test_consecutive_flows_keep_original_context_and_result`; CTX-12: boundary matrix plus construction-failure test and maintained invalid-wrapper tests; CTX-13: maintained contract/runner/typing suites; CTX-14: context-only subprocess plus maintained import-order cases; CTX-15: maintained offline runtime and CLI inventory; CTX-16: focused/full gate and documentation checks below; CTX-17: **NOT RUN**, pending both independent reviews and orchestrator's clean installed release gate on this exact candidate.

- Python 3.13.5; pinned CrewAI 1.15.40/Pydantic 2.12.5; no lockfile change. Tests ran from `app/` with writable `/workspace/.home` HOME/XDG values and granted network permission for CrewAI's version-check path. No external Langfuse service was used.
- `./.venv/bin/python -m pytest -q tests/context/test_models.py tests/application/test_context.py tests/workflows/test_context.py`: **exit 0, 17 passed** on the final test tree.
- Same command with `tests/application/test_followup_boundaries.py` added: **exit 0, 43 passed** before the final identity-only assertion refinement (which was then covered by the 17-case run and full gate).
- `./.venv/bin/python -m tooling.checks check`: **exit 0** on the final test tree; Pyright 0 errors/warnings, Ruff lint/format passed, pytest **380 passed in 35.35s**. Existing negative typing test remained collected.
- From repository root: `python3 designs/atlas/build.py --check` and `git diff --check`: **exit 0**. No changed Markdown in this candidate; prior round's 173 checked relative links, zero missing, remain applicable.
- Clean installed release: **NOT RUN**, by plan's review-before-release sequence. Mac/PyCharm and live Langfuse are not M4.1 automated evidence.

Both independent reviewers must inspect this exact candidate and entire approved diff, including retained round-1 files. A code/test correction after their reviews would require round 3; report-only updates would not.

### Same-candidate verification addendum — 2026-11-14

After committing the frozen candidate, I reran `./.venv/bin/python -m tooling.checks check` from `app/` on the unchanged application tree at `16c1580e96bd36945fa96b6ecfa8f9a563d53913` (report-only commits followed it). Exit 0: Pyright 0 errors/warnings, Ruff lint/format passed, pytest **380 passed in 36.05s**. This confirms the final assertion refinement was included; the earlier 35.35s result is retained as historical same-tree evidence.
