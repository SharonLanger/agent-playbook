# Workflow contract: second-review test-quality handoff

Status: **Q1–Q4 implemented on PR #40; verification evidence below; pending review.**
Requested by Sharon on 2026-11-13. This document records the second independent review and its implementation follow-up. It does not authorize merging either PR.

Implementation update on PR #40: Q1–Q4 corrections below are in place and their negative controls failed on the intended assertions. The completion table near the end records current evidence. The review findings below describe the historical handoff at `f61683c`.

## Start here and preserve the current work

- Design: [PR #38](https://github.com/SharonLanger/agent-playbook/pull/38), `docs/workflow-contract-design`.
- Implementation: [PR #40](https://github.com/SharonLanger/agent-playbook/pull/40), `feat/workflow-contract`.
- Reviewed implementation: [`f61683c8e2a089b2dc4f008d193dd83618322adf`](https://github.com/SharonLanger/agent-playbook/tree/f61683c8e2a089b2dc4f008d193dd83618322adf).
- Verified application/release source: `9f75544c47c1b2356a547f54a634c00262edbdc0`. Changes from that commit to the reviewed head were documentation only.
- Governing acceptance: [design.md](design.md), [test-plan.md](test-plan.md), and the A1–F6 matrix in [review-follow-up.md](review-follow-up.md#test-matrix-to-close).

Refresh both branch heads. Incorporate the latest design branch into the existing implementation branch without resetting it. Preserve PR #40's runtime fixes, test additions and per-ID evidence mapping when reconciling overlapping documents. The older follow-up contains historical instructions for I-1–I-4; those fixes are already implemented at the reviewed head. This document is the current work list for the remaining four gaps, not a request to redo the refactor.

This pass should primarily change tests and evidence. If a corrected test reveals an actual runtime defect, report the reproduction and make only the narrow fix needed to satisfy the existing approved contract. Raise an architectural conflict before changing that contract.

## What the review established

The independent review passed Pyright, Ruff lint/format, all **314 tests**, and Atlas checks at `f61683c`. Lazy dependency imports, constructor-error classification and alias/phase diagnostics behaved as designed. Existing real CrewAI flow/state/step scenarios remain present.

The reviewer independently rebuilt a wheel from the hash-checked application snapshot, embedded source commit `9f75544`, installed its locked dependencies in isolation and ran the installed verifier. All registered built-ins, both configured aliases and representative failures passed. The wheel SHA-256 matched the implementation agent's reported artifact exactly: `b4fb6593f02fc000b15f99fcc5262a531e0296e27f1fe3d554bcd2f9b1b12326`.

That independent artifact check did not rerun the original Git clean-check/archive release entrypoint. PR #40 separately records the implementer's clean release build. Python socket/DNS auditing is not an OS network sandbox; Linux checks do not establish Mac/PyCharm behavior. No old-release/new-YAML compatibility was tested or requested.

Four maintained tests can pass without proving their stated requirement. Temporary in-memory review probes demonstrated the weaknesses below; those probes changed no repository files and are not maintained regression coverage. These are gaps in the evidence, not proof that the current production implementation violates all four contracts.

## Work and risk

| ID | Existing requirement | Gap to close | Review severity | Approximate effort |
|---|---|---|---|---|
| Q1 | E3: reject invalid input before flow construction/kickoff | Observe the prohibited work directly | Medium | 45–90 minutes |
| Q2 | C6: configuration precedes the first framework import | Make the subprocess environment deliberately conflicting and assert both startup settings | Medium | 45–90 minutes |
| Q3 | D4: reject invalid YAML in each file independently | Remove unrelated fixture defects and verify the intended rejection | Medium | 60–120 minutes |
| Q4 | B2: every failing boundary stops later calls | Inject an actual exception from a callable, then assert cause and stopping point | Low | 45–90 minutes |

Allow additional time for the full gate, reconciliation and evidence updates. These are planning estimates, not timing guarantees. Production-change risk is low if the pass remains tests/documentation only; Q2 and Q3 require care because process state and multiple validation layers can hide an ineffective test. None requires context/Langfuse or a new lifecycle abstraction.

## Q1 — prove invalid input cannot construct or start a flow

Current test: [`test_invalid_input_never_constructs_or_kicks_off`](https://github.com/SharonLanger/agent-playbook/blob/f61683c8e2a089b2dc4f008d193dd83618322adf/app/tests/workflows/test_wrappers.py#L100) in `app/tests/workflows/test_wrappers.py`.

**Observed weakness:** the test only checks an input exception, FAILED/PREPARE state, and a later exception from execute. It never observes the concrete flow constructor or kickoff. A review probe changed WF-01 preparation to construct and run the real flow first, then reject the invalid input; this maintained test still passed.

Implement the following:

1. Preserve all existing invalid-input cases across WF-01, WF-02 and WF-03. Add the concrete flow target to the parameter data where needed rather than branching on workflow IDs in production.
2. Patch the concrete flow class at the location used by the wrapper's deferred import. Use a constructor spy/mock whose returned flow has a separately observable `kickoff` mock. For this input-rejection unit test, no real business work should execute.
3. Construct the wrapper and invoke its real public `prepare(invalid)` method. Keep the real input validation and ABC lifecycle in the test; do not mock `_prepare` on the normal success-under-test path.
4. Assert `WorkflowInputError`, FAILED status, PREPARE failure phase, and that the recorded cause is the caught input error. Explicitly assert that the flow constructor and kickoff were never called. Keep these assertions after the raised-exception context so an eventual input rejection cannot hide earlier work.
5. Replace the broad `pytest.raises(Exception)` for the subsequent execute call with `WorkflowOrderError`. Check that this rejected call leaves the failure record intact and still causes no constructor/kickoff call.
6. Retain the separate real-wrapper integration tests. Mocks here prove the input boundary; they do not replace real CrewAI execution evidence.

**Acceptance:** every invalid-input case detects premature construction, even if kickoff is never reached, and detects work attempted before the eventual input exception. Validate the test instrumentation with a temporary negative control that moves flow construction before validation. A second control may attempt kickoff before rejection using the harmless mock. The strengthened test must fail on its no-call assertion, not on an unrelated setup error. Restore the production implementation afterward.

Do not add a duplicate test with the same weak assertions. Strengthen the existing test or replace it with an equivalent clearer parameterized test and update E3's mapping.

## Q2 — prove the runner applies startup settings before importing CrewAI

Current test: [`test_real_runner_import_order_and_unused_flows_in_fresh_process`](https://github.com/SharonLanger/agent-playbook/blob/f61683c8e2a089b2dc4f008d193dd83618322adf/app/tests/application/test_followup_boundaries.py#L203).

**Observed weakness:** `-I` isolates Python startup behavior but the child still inherits environment variables. The parent test setup already supplies `CREWAI_DISABLE_TELEMETRY=true`. The import guard only checks that one value. A review probe replaced runner assembly with configuration loading alone, skipping `configure_crewai`; this maintained test still passed.

Implement the following:

1. Keep a fresh subprocess and real runner/assembly/configuration code. Before importing application modules, deliberately seed `CREWAI_DISABLE_TELEMETRY=false` and `CREWAI_TRACING_ENABLED=true` in that child. This conflicts with the maintained offline YAML, which requests telemetry and tracing disabled.
2. Neutralize inherited `AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED` and `AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED` overrides, either removing them in the child or explicitly setting both to `false`. Keep event output disabled too. Do not let the user's shell decide this test's expected settings.
3. Install the import guard before any application/framework import. At the first attempted framework import, including the pinned distribution's `crewai`/`crewai_core` module boundary, assert **both** `CREWAI_DISABLE_TELEMETRY == 'true'` and `CREWAI_TRACING_ENABLED == 'false'` before delegating to the real import. Record that the guard was reached so a test which never imports the framework cannot pass vacuously.
4. Preserve the assertion that building the lightweight class registry imports no CrewAI framework or concrete flow modules. Retain the unused WF-02/WF-03 import guards and the final `sys.modules` checks when running WF-01.
5. Assert the real WF-01 result and a successful subprocess exit. Include captured output only as failure diagnostics; retain a finite timeout.

**Acceptance:** normal execution passes from deliberately wrong initial framework settings. A temporary bypass of `configure_crewai` must fail at the first import guard; changing only tracing setup must also be detected. The guard must fail **before** framework initialization under the conflicting values, so proving the test does not enable telemetry or require a service/network connection. A test that only verifies final environment values after execution does not establish ordering.

Keep this fresh-process integration test separate from runner unit tests. No production-only test switch, import framework, optional dependency profile or new environment setting is required.

## Q3 — make every YAML rejection test fail for its intended reason

Current test: [`test_yaml_parse_rejects_keys_and_tags_in_both_files`](https://github.com/SharonLanger/agent-playbook/blob/f61683c8e2a089b2dc4f008d193dd83618322adf/app/tests/config/test_workflow_matrix.py#L148).

**Observed weakness:** for base-file cases the test prepends a fragment containing `workflows:` to a fixture which already contains `workflows:`. The merge-key case therefore fails on a duplicate root key. It still passed when the explicit merge-key rejection was disabled. Some local-file cases provide useful coverage; do not describe or delete the whole matrix as worthless.

Implement the following:

1. Build each malformed document from an otherwise valid full base configuration or a valid local overlay. The base must contain valid integrations and exactly one root `workflows` key, except in a case explicitly testing a duplicate root workflows key. Keep the companion base/local file valid.
2. Do not assemble base documents by blindly prepending fragments to `offline.yaml`. Use a test fixture builder with one insertion point under the existing workflows mapping, or explicit complete YAML strings. Duplicate-key fixtures must remain raw YAML text; normal dictionaries cannot represent duplicates.
3. Cover base and local files independently with named parameter cases: root duplicate; nested duplicate, including an unused workflow config; merge key in an unused block; complex/non-string key; malformed YAML; and unsupported Python tag. Prefer an inert unsupported tag such as `!!python/tuple` rather than a payload that invokes a shell command. These tests must never run arbitrary external work if a loader regresses.
4. Supply a matching valid control for each fixture shape: removing the single intended defect must allow configuration loading. Keep unknown-entry/settings errors out of loader-focused controls; unused entries can remain raw when appropriate under the selected-only validation contract.
5. Add or retain small `StrictLoader` unit assertions for the intended parser/constructor error category and safe reason, such as duplicate key, merge key or invalid key. This distinguishes the actual guard being exercised even if another downstream schema would also reject the value. Do not make the public diagnostic print parser internals to satisfy a test.
6. Keep public `load_configuration` integration assertions for both files. They must raise `ConfigurationError` and avoid raw YAML values/source snippets. The public loader intentionally redacts parser detail and suppresses its cause, so its generic error alone cannot prove which guard fired.

**Acceptance:** temporarily allow YAML merge keys through the loader; the merge-specific test must fail because the forbidden merge is accepted or the expected merge rejection is absent. The root/nested duplicate tests must similarly detect removal of duplicate detection. In every case, failures must identify the intended behavior, not an unrelated duplicate root block or an unknown application field.

Keep layered tests where they prove distinct contracts: a loader unit test can prove the specific guard, while the public test proves classification/redaction. Consolidate redundant parameter cases only if their unique base/local, nesting and defect coverage remains explicit in D4's mapping.

## Q4 — inject a real failure and prove downstream calls stop

Current test: [`test_failure_stops_before_success`](https://github.com/SharonLanger/agent-playbook/blob/f61683c8e2a089b2dc4f008d193dd83618322adf/app/tests/application/test_followup_boundaries.py#L142).

**Observed weakness:** `setattr(workflow, f'_{boundary}', original)` installs a `ValueError` object in place of a callable hook. Calling it raises `TypeError`, not the intended exception. The test accepts any `WorkflowExecutionError` and does not assert cause or downstream calls. Existing `test_runner_contract.py` tests already provide some useful stopping assertions; preserve and reuse that coverage.

Implement the following:

1. Replace exception-as-method assignment with a callable mock using `side_effect=original`, or a typed hook which raises that exact exception. Use `patch.object`/scoped patches so restoration is automatic. Do not patch final production method definitions to evade static checks.
2. Choose a clear layer: for isolated runner ordering tests, mock public workflow methods and collaborators; for ABC failure bookkeeping, use real public methods with injected hook failures. Do not duplicate the complete lifecycle matrix just to repair B2.
3. Track assembly, registry, selection, construction and the workflow public calls. Assert the expected successful prefix and that every later collaborator/method is uncalled. Construction failures and invalid JSON must leave all lifecycle methods uncalled. JSON decoding occurs **after** wrapper construction in the approved sequence.
4. For injected ordinary errors, assert the exact outward category/phase/selected alias and `failure.value.__cause__ is original`, not merely `isinstance(..., ValueError)`. Where a real lifecycle wrapper is exercised, check its recorded failure phase/cause as well.
5. Keep legitimate configuration/selection/input cases distinct: their category stays exit 2. Do not invent an original injected cause for real malformed-JSON validation; assert the actual validation boundary and absence of subsequent calls instead.
6. Assert that no successful `RunResult` is constructed on failure; a constructor spy on the runner's result boundary is suitable. Preserve safe outward error checks without exposing injected private text.

Use the runner's current sequence when defining the expected suffix:

| Failure point | Calls that must not occur afterward |
|---|---|
| Assembly | Registry, selection, construction, prepare, execute, validation, serialization, success result |
| Registry | Selection and all later calls |
| Selection | Construction and all lifecycle/result calls |
| Construction | All lifecycle/result calls |
| JSON decoding | All lifecycle/result calls; construction has already succeeded |
| Prepare | Execute, output validation, serialization, success result |
| Execute | Output validation, serialization, success result |
| Output validation | Serialization and success result |
| Serialization | Success result |

**Acceptance:** the injected ValueError is the actual causal exception. A temporary change that continues to a downstream method after an earlier failure must make the stopping assertion fail. Replacing the hook with a noncallable exception object must no longer accidentally satisfy the intended-cause assertion. Existing constructor-classification tests may supply the construction row if their no-later-call assertions are sufficient; reference them explicitly rather than duplicating tests solely to increase the count.

## Test quality and replacement rules

- Judge a test by the behavior its assertions protect, not its name, existence or contribution to the total count.
- Strengthen the four named tests first. Delete or consolidate a weak duplicate only after a maintained replacement proves every distinct requirement it used to claim. Record the old-to-new mapping and reason.
- Retain useful real CrewAI integration coverage, boundary values, alias/default/override scenarios, failure classification and strict typing. Do not replace all integration tests with mocks.
- Use one-defect fixtures and explicit assertions. Broad `raises(Exception)` is insufficient where the contract names an error category. No unconditional xfail, skipped cases, swallowed assertion errors or weakened requirements to obtain green results.
- For Q1–Q4, demonstrate sensitivity with the focused negative controls described above. Run each control in isolation, verify the expected assertion fails, and restore the code/patch before the final gate. Record the changed behavior and observed failing assertion. Do not count collection errors, missing dependencies, timeouts or unrelated failures as evidence.
- No mutation-testing framework, new dependency or permanent production failure toggle is required. Keep useful shared fixture helpers small and local to maintained tests. Do not commit deliberately broken production variants.
- Recheck the A1–F6 mapping for the tests touched by this pass and any nearby consolidated duplicates. This is a focused correction, not a request to redesign every test or invent new product requirements.

## File placement, authority and documentation impact

The permanent plan belongs at `designs/refactors/workflow-contract/review-test-quality.md`. Tests stay in their existing owning folders; shared YAML fixtures stay in `app/tests/fixtures/`. Implementation evidence belongs with this refactor and in PR #40, not in `app/docs/`.

| File/surface | Expected change |
|---|---|
| `app/tests/workflows/test_wrappers.py` | Q1 constructor/kickoff observations and specific order-error checks |
| `app/tests/application/test_followup_boundaries.py` | Q2 subprocess isolation and Q4 correct failure injection |
| `app/tests/application/test_runner_contract.py` | Extend/reuse collaborator stop assertions if needed for Q4 |
| `app/tests/config/test_workflow_matrix.py` | Q3 single-defect YAML matrix and controls |
| Existing loader tests / `app/tests/fixtures/` | Only small loader-specific assertions or independent fixtures needed for Q3 |
| `review-follow-up.md` on PR #40 | Preserve A1–F6 history; correct E3/C6/D4/B2 mappings to maintained assertions |
| This document, refactor README and `designs/progress.md` | Revision-specific completion evidence and remaining limitations |
| Atlas catalog/index/README | Current review status and discoverable handoff; rebuild generated output |
| `app/src/`, `app/tooling/`, dependencies, YAML defaults | No planned behavior changes; narrow defect fix only if the stronger tests expose one |
| `app/docs/` | No change for tests-only work: supported commands, outputs and configuration do not change |

Sharon requested this plan and suggestions for replacing ineffective tests. It clarifies existing approved acceptance within existing component boundaries. Companion guarded edits only register/link this follow-up and reconcile current review status; they do not change the ABC, runner order, YAML semantics, lifecycle, error vocabulary or orchestration ownership. Preserve every existing guard. Charter, principles, architecture and project structure require no changes.

Principles assessment: explicit scope/guards, reproducible gates, evidence, traceability and honest status are directly addressed. Privacy/offline tests preserve security and local-first behavior. CrewAI and external configuration boundaries remain intact. Learning material and historical evidence remain. No new provider, migration or future-stage feature is introduced. The exploration index was consulted; observability/agent/harness proposals introduce no requirement for this test-only follow-up. `app/examples/` and historical `sandbox/` remain excluded from reading, tests and maintenance.

## Implementation sequence and verification

1. Read root/design instructions, governance, governing package and this handoff. Refresh PR refs, record the starting implementation SHA and reconcile the design branch. Do not overwrite the maintained test mapping with the older design-branch version.
2. Run the baseline standard gate and record its actual result. The previous 314-pass result belongs to `f61683c`, not automatically to a new head.
3. Implement Q1–Q4, strengthening/replacing tests as described. Run the focused tests and their negative controls. Restore every control before final verification.
4. Run the full standard gate after the final test edits. No new test-count minimum is required; document a justified reduction if duplicates were consolidated.
5. Update per-ID evidence, this document's completion table, refactor status/progress and PR #40's description. Rebuild/check Atlas and run whitespace/diff checks.
6. For a tests/docs-only change, retain the pinned earlier release evidence with an explicit no-runtime-change comparison. A fresh full release is not required solely because assertion quality improved. If production/package/tooling behavior changes, run the relevant source verifier and clean isolated current-release gate on a committed source revision, including every registered built-in and both aliases. Do not claim a new release was verified if only old evidence was reused.
7. Commit and push the changes to PR #40. Report exact final SHA, commands/outcomes, Q1–Q4 sensitivity evidence, replaced tests and limitations. Leave both PRs open and unmerged for review.

Suggested commands from a normal checkout with the project's existing environment:

```bash
cd app
./.venv/bin/python -m pytest tests/workflows/test_wrappers.py tests/application/test_followup_boundaries.py tests/application/test_runner_contract.py tests/config/test_workflow_matrix.py
./.venv/bin/python -m tooling.checks check
cd ..
python3 designs/atlas/build.py
python3 designs/atlas/build.py --check
git diff --check
```

Include any additional loader test module modified by Q3 in the focused run. For behavior-affecting changes only, from `app/` run the maintained `./.venv/bin/python tooling/verify_runtime.py dev-run` and `./.venv/bin/python -m tooling.release` using the normal clean-checkout/pinned-dependency procedure. Do not change versions or dependency pins merely to repair tests.

## Completion evidence — PR #40

| Item | Maintained test node IDs | Behavior/assertions proved | Negative control and intended failure | Verified revision/result |
|---|---|---|---|---|
| Q1 / E3 | `tests/workflows/test_wrappers.py::test_invalid_input_never_constructs_or_kicks_off` (11 invalid inputs) | Real `prepare` rejects, records FAILED/PREPARE and exact cause; patched deferred-import flow constructor and kickoff have zero calls before/after `WorkflowOrderError` | Temporarily constructed WF-01 flow before input validation; the constructor no-call assertion failed with one call; restored source | Focused cases passed; final gate below |
| Q2 / C6 | `tests/application/test_followup_boundaries.py::test_real_runner_import_order_and_unused_flows_in_fresh_process` | Child seeds telemetry disabled=false and tracing=true; first intercepted CrewAI import sees telemetry disabled=true and tracing=false; guard ran; registry/unused flows remain lazy; real WF-01 succeeds | Temporarily bypassed `configure_crewai`, then separately skipped only tracing assignment. Each run failed the corresponding first-import guard assertion before framework initialization; restored both files | Focused case passed; final gate below |
| Q3 / D4 | `tests/config/test_workflow_matrix.py::test_yaml_parse_rejects_keys_and_tags_in_both_files` (7 defects × base/local) | Each otherwise valid file has one defect and a matching valid control; `StrictLoader` gives the intended safe reason, public load returns a redacted error; includes unused blocks and inert Python tag | Temporarily disabled merge-key rejection; the expected-reason assertion failed. Separately disabled duplicate detection; root and unused-nested duplicate cases failed at `pytest.raises(yaml.YAMLError)`; restored loader | Focused cases passed; final gate below |
| Q4 / B2 | `tests/application/test_followup_boundaries.py::test_failure_stops_before_success` (9 boundaries) | Callable collaborators fail with exact cause and phase; recorded calls stop at the failing boundary, `RunResult` is never called, invalid JSON never prepares | Temporarily called `execute` from failing `prepare`; exact call-prefix assertion failed because of the extra `execute`; restored test | Focused cases passed; final gate below |

Q3 revealed one narrow production diagnostic defect: merge-key nodes were rejected as generic invalid keys before the explicit merge-key branch. `StrictLoader.construct_mapping` now reports `YAML merge keys are unsupported`. Public configuration errors remain redacted. No orchestration or package boundary changed. The former Q4 exception-object assignment was replaced by callable failure injection; the other three named tests were strengthened in place. The A1–F6 mapping remains in [review-follow-up.md](review-follow-up.md#pr-40-maintained-test-mapping).

Verification at application commit `4775cbea7b3b86dda76de015cbfd282e43df6cf9`: the focused four-module suite passed **119 tests**; `cd app && ./.venv/bin/python -m tooling.checks check` passed Pyright (0 errors/warnings), Ruff lint and format, and **315 tests**. The negative controls above were temporary and restored before this gate. `cd app && ./.venv/bin/python tooling/verify_runtime.py dev-run` passed WF-01/02/03, both configured aliases with defaults and overrides, an execution-failure exit, and zero Python socket/DNS attempts. `cd app && UV_CACHE_DIR=/workspace/.uv-cache ./.venv/bin/python -m tooling.release` repeated the full gate on the clean commit, built the wheel, installed hash-checked locked dependencies, passed `uv pip check` for 138 installed packages, and passed the isolated installed verifier for the same built-ins, aliases and failure. `release.json` records `verified: true`, source commit `4775cbea7b3b86dda76de015cbfd282e43df6cf9`, wheel SHA-256 `150b5d67638642232931b54ac838751fa967edb25c6d1e6cb8451b4f8a3f3fb8`, requirements SHA-256 `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840`, and lock SHA-256 `5bb830f9eaf61fb9b67d3d6c6cf07a2084279cb64fa03a26968cb36e4ec36d04`.

`python3 designs/atlas/build.py --check` and `git diff --check` passed after the evidence update. The installed verifier compares the source and installed expected outputs for all registered built-ins and both aliases. No historical regression scenario was removed; tests, checks and the release exclude personal `app/examples/`. The public configuration guide already states that merge keys are rejected and errors hide source values, so the more specific internal loader reason needs no public guide change. The release is local and untracked. Python socket/DNS auditing is not an OS network sandbox; Linux verification does not establish Mac/PyCharm behavior or compatibility between an older installed release and the new YAML. Context/Langfuse, optional packaging, children and recovery remain separate.

Also record: baseline/final gate results; any old-to-new test mapping; no unresolved failures; Atlas/whitespace checks; whether production files changed; which release evidence applies; and exact environment limitations. A test name without its relevant assertion is not sufficient evidence. Keep historical review findings available after marking them resolved.

## Copyable instruction for the next agent

> Continue PR #40 on feat/workflow-contract. Read the latest PR #38 design package, especially designs/refactors/workflow-contract/review-test-quality.md. Incorporate the updated design branch while preserving the implemented I-1–I-4 fixes and existing A1–F6 mapping. Implement Q1–Q4: prove invalid input causes no flow construction/kickoff; prove both startup settings are applied before the first CrewAI import from a conflicting child environment; fix YAML fixtures so each rejection tests its intended defect; and fix exception injection plus exact-cause/downstream-call assertions. Strengthen or replace ineffective tests, consolidating duplicates only with explicit preserved coverage. Demonstrate each corrected test detects its stated regression. Update the evidence mapping/docs/Atlas, run the full gate and applicable release checks, then push to PR #40 and report the final SHA, evidence and limitations. CrewAI keeps orchestration; do not add context/Langfuse, optional packaging, children or recovery. Do not merge either PR.
