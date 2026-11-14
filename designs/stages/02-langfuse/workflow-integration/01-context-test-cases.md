# M4.1 — test cases

Status: **DRAFT FOR REVIEW — required cases proposed; none claimed implemented or passed.** Version 1, 2026-11-14.

[Design](01-context-design.md) · [Implementation/review procedure](01-context-implementation-plan.md) · [Shared requirements](requirements.md)

## Acceptance rules

These stable CTX IDs are the test reviewer's checklist. A case may map to several pytest nodes, and one parametrized test may satisfy several cases. Map actual nodes and assertions after implementation; a filename or passing suite count alone is insufficient. Retain existing relevant tests where they already prove a case instead of duplicating them.

All cases below are mandatory for M4.1. A blocked, skipped, xfailed, missing or weakly asserted required case is not PASS. Changing/removing a case requires Sharon's decision, not a coder/reviewer shortcut. Later Langfuse/UI/agent features are explicitly excluded below; their absence is not a test gap in this milestone.

Use maintained fixtures and configured offline settings. Never read, import or scan app/examples/. Exercise real context classes and actual integration boundaries; mock only the boundary needed to inject a controlled failure or inspect arguments. Do not replace both sides of propagation and then claim the real path works. No Docker or live Langfuse requirement.

## Context identity and scope

| ID | Scenario and setup | Required observable assertions | Requirement / likely owner |
|---|---|---|---|
| CTX-01 | Construct two independent real ExecutionContext instances without correlation_id | Each has a nonempty canonical UUID4 string; values differ; root agent fields are None. Use known workflow/run input values so identity domains are not confused. This protects the project's generation policy, not a statistical UUID-quality test | R30; tests/context/test_models.py |
| CTX-02 | Explicitly supply an existing correlation_id to two contexts with different workflow/run values | Supplied correlation value remains unchanged; workflow_run_id stays distinct; neither object changes the other. This tests the data contract only, without implementing nested workflows | R30/D01; tests/context/test_models.py |
| CTX-03 | Call the real for_agent for reviewer A1, coder B1 and reviewer A2 from one parent | Distinct outer and observability objects; same correlation/workflow/run values; correct agent labels and distinct supplied invocation IDs; parent still has both agent fields None; no sibling is overwritten | R04/R16/R21/R24/R30; tests/context/test_models.py |
| CTX-04 | A helper receives an agent child, calls another helper, then returns; repeat with a helper raising an exception caught by its caller | Both helpers see that exact child reference and identity; parent/sibling remain unchanged after normal return and after failure; exception is not swallowed by context code | R03/R04/R24; tests/context/test_models.py |
| CTX-05 | Try ordinary assignment to correlation_id and workflow/agent identity on actual frozen objects | Assignment is rejected and original values remain. Cover outer and inner protection once; do not test every dataclass-generated method or claim protection against deliberate object.__setattr__ bypass | D24/D27; tests/context/test_models.py |

CTX-03 must detect regeneration during derivation, dropped inherited fields and accidental mutation. Use nondefault supplied IDs so passing by accidentally rebuilding defaults cannot satisfy it. Do not assert exact random UUID values; deterministic identity assertions can use explicit values. No real agent object/client is needed for these cases.

## Construction and real workflow propagation

| ID | Scenario and setup | Required observable assertions | Requirement / likely owner |
|---|---|---|---|
| CTX-06 | Invoke the public runner twice in one process for the same configured ID, then a configured alias | Each invocation constructs a different root context and fresh correlation/workflow_run_id; the configured ID, including alias, appears in observability.workflow_id; root agent fields are None; no import-time/shared cached context | R01/R30; tests/application/test_context.py |
| CTX-07 | Observe context through real construct_workflow and create_workflow, using real Workflow subclasses | Both helpers forward exactly the provided object into constructor/ABC property; no copy or fallback. Cover every registered wrapper constructor with valid config. Update existing registry/constructor tests rather than removing their assertions | R02/D19; tests/application/test_context.py and existing test_workflow_registry.py |
| CTX-08 | Through normal runner/factory/wrapper preparation, capture each maintained Flow for WF-01/02/03 | Flow.context is wrapper.context and the runner-supplied reference. Test all three to catch a missed constructor/super/prepare forwarding call. Preserve framework tracing/display and typed initial-state arguments | R02/R03; tests/workflows/test_context.py |
| CTX-09 | Execute decorated methods with real CrewAI kickoff, including WF-03 scores 80 and 40 | A start and listener can read the expected Flow.context; the router and selected terminal listener see the same context; unselected branch is absent; normal results remain. Do not claim access merely by calling an undecorated helper directly | R03/R28 foundation; tests/workflows/test_context.py |
| CTX-10 | Serialize the actual maintained Flow model and its state before/after execution | Our context, correlation/workflow/agent fields and private storage are absent from state and ordinary Flow model serialization; Flow.context still returns the original object. CrewAI's existing execution_context field may remain present with its unchanged default; do not confuse it with ours | R23/privacy; tests/workflows/test_context.py |
| CTX-11 | Retain earlier context reference while a second wrapper/Flow runs; inspect the first afterward | Original context and original state/result remain separate; second execution cannot rebind the first. Cover success followed by success and a failure in the second run | R01/R04/D24; tests/application/test_context.py or test_context.py under workflows |

For CTX-06/08, use a recording wrapper/constructor spy that delegates into the actual implementation, or equivalent direct identity observations. Do not add a production global capture list or change RunResult merely to make tests convenient.

For CTX-09, test-only subclasses can assert context inside decorated overrides and then delegate to the real method; preserve the framework's decorators and method graph. An equivalent transparent spy is acceptable only if the test still executes the actual scheduled method and would fail if production context storage/forwarding disappeared. At least one real run of each maintained Flow must be covered by CTX-08 and existing behavior tests. Do not replace the implementation with a lookalike fixture that independently installs its own context.

For CTX-10, inspect relevant keys/value absence, not a huge framework-model snapshot. Keep business outputs as the existing explicit contracts. Private attributes are not a promise about generic pickling or arbitrary framework cloning; those are outside acceptance.

## Regression, isolation and delivery

| ID | Scenario and setup | Required observable assertions | Requirement / existing owner |
|---|---|---|---|
| CTX-12 | Existing invalid-input cases and configuration/selection failures; add a context-construction failure at its new boundary | Existing invalid inputs still never construct/kick off a Flow. Assembly/registry/selection failures do not construct context. An unexpected context-construction exception keeps the CONSTRUCTION message/category and exact cause; later phases do not run | R01/R02; test_wrappers.py, test_followup_boundaries.py, test_context.py |
| CTX-13 | Existing ABC ordering, single-use, hook failure, result typing and runner error cases with required context supplied | Lifecycle ordering/terminal guards, rich native result, serialization and exact exception cause/category remain. A missing context argument must not accidentally replace the intended injected failure and make a weak test pass | Existing approved workflow contract; test_contract.py, test_runner_contract.py, test_followup_boundaries.py, test_typing_contract.py |
| CTX-14 | Fresh-process import/configuration and isolated context-module import | Existing configuration-before-CrewAI and unused-flow import checks still pass. Importing/constructing/deriving context alone loads no CrewAI/Langfuse/OTel integration and performs no network calls; use an import/network guard if needed, without expanding app/tests/conftest.py's framework setup into a false claim | R01/R23 and locality principle; existing followup tests plus context subprocess case |
| CTX-15 | Existing offline runtime verifier and CLI regression inventory | Real maintained workflows and aliases, configured defaults/overrides, both route results and controlled failure retain outputs and exit categories; zero Python socket/DNS attempts in the existing verifier. No new identity printing, keys, service startup or tracing side effect | Existing test_offline_runtime.py and tooling/verify_runtime.py |
| CTX-16 | Run strict maintained quality gate and context-focused tests | Pyright, Ruff lint/format and pytest pass under the pinned environment; no Any/casts/blanket ignores to hide the new constructor/property types; existing negative typing tests still fail for their intended reasons. Record collected nodes for CTX-01–15 | Principle 7; tooling.checks |
| CTX-17 | Build and verify a clean committed application release using existing tooling | Wheel includes context/models.py; isolated installed invocation imports it and executes the existing workflow inventory. Existing release manifest/hash/verification checks pass; do not run only editable source and call this installed evidence | Existing packaging gate; tooling.release/verify_runtime |

CTX-12 can patch the runner's imported ExecutionContext constructor with a callable that raises a known exception; assert that exact cause. Tests must not pass because a fake constructor forgot the new context parameter. Existing Q1–Q4 test-quality obligations remain in force.

CTX-14's context-only subprocess should start before importing pytest application conftest or CrewAI. It verifies the new module's dependency boundary. Existing offline tests verify the application, which already uses CrewAI. Neither test should be described as an OS-level network sandbox.

CTX-16 includes documentation checks: Atlas freshness, changed-document links and git diff whitespace. CTX-17 runs once on a candidate that otherwise passes the two reviews; repeat only if a change invalidates that evidence or a failure requires a fix. No version bump is required solely for this milestone. If existing release tooling requires a fresh version or another repository condition, report it and follow the existing policy rather than silently changing unrelated release rules.

## Test mapping and review evidence

Every round's test-gap report must contain all CTX-01–17 rows:

| Case | Exact pytest node or documented gate | Assertion/evidence location | Outcome | Gap/finding ID |
|---|---|---|---|---|
| CTX-01 … CTX-17 | Fill with actual nodes/commands | File:line and tested SHA/output reference | PASS / FAIL / MISSING / WEAK / BLOCKED / NOT RUN | Stable T-number or none |

No placeholder table counts as a completed report. Include selected parameters where behavior differs. The reviewer must read the relevant assertions and inspect what was executed, not trust the coder's mapping. Existing tests count only if they still exercise the intended boundary after the signature changes.

Before readiness, targeted checks that are not included in the full gate must have their own results. The release result may initially be NOT RUN while reviewers evaluate a candidate; overall readiness remains pending until CTX-17 passes and its evidence is appended for that same candidate. A report-only commit can follow code review if the runtime/test files are proven unchanged; record both SHAs.

Do not require a mutation-testing framework. Use a small temporary negative control only when an assertion's ability to catch a plausible regression is unclear; restore changes and keep the check isolated from the reviewed candidate. Test presence, coverage percentages and large repeated full-suite runs are not substitutes for meaningful assertions.

## Explicitly outside these test cases

No Langfuse ingestion/UI assertions, trace/span parentage, SDK flush/outage behavior, instrumentor installation, model cost/score tests, logger storage/viewer tests, real agent execution, subprocess context transport, retries, persistence/resume or concurrent use of one Workflow instance. Those belong to later milestones. Application context isolation is not evidence that SDK active scope or process propagation works.

The maximum-three-round rule and required coder/design-drift/test-gap/orchestrator reports are in the [implementation plan](01-context-implementation-plan.md). They are not new application runtime tests or a framework to implement.
