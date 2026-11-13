# Workflow contract review follow-up and test-gap plan

Status: **Historical first-review plan and current acceptance matrix. I-1–I-4 are implemented on PR #40 at f61683c; the second review found four remaining test-quality gaps.**

Current next-agent work is [review-test-quality.md](review-test-quality.md), Q1–Q4. Preserve the maintained A1–F6 test mapping already present on PR #40 when reconciling this design branch. The original instructions and baseline evidence below remain historical; they do not require reimplementing completed fixes.
Owner: next implementation agent on PR #40. Requested by Sharon on 2026-11-13.
This file supplements the original [design](design.md), [test plan](test-plan.md) and [implementation plan](implementation-plan.md). It does not replace or weaken their acceptance requirements.

## Start here

- Design PR: [#38](https://github.com/SharonLanger/agent-playbook/pull/38), branch docs/workflow-contract-design.
- Implementation PR: [#40](https://github.com/SharonLanger/agent-playbook/pull/40), branch feat/workflow-contract.
- Reviewed implementation: [b3d279b6826284cd9a0e1aba6f559525e8358f31](https://github.com/SharonLanger/agent-playbook/tree/b3d279b6826284cd9a0e1aba6f559525e8358f31).
- Deferred children/composition: [#39](https://github.com/SharonLanger/agent-playbook/issues/39).

Refresh both PR heads before work. Bring the updated design branch into the implementation branch; preserve PR #40's runtime changes and verification history when resolving overlapping documentation edits. Do not reset the implementation to the design branch. Work in the existing implementation PR; do not merge either PR or rewrite unrelated work.

The current documentation task records the plan only. Sharon will give this file to the implementation agent to execute. The earlier instruction to stop before initial implementation is historical; it does not cancel the already authorized refactor or this requested follow-up.

## Decision: lazy dependency imports now

Sharon chose lazy imports in this refactor, before context/Langfuse integration. Context is not a prerequisite: it will later carry clients, connections and run metadata, while this change controls when Python loads implementation dependencies.

Keep stable implementation keys mapped to actual wrapper classes. It is acceptable to import all lightweight wrapper class modules to build that explicit registry. Defer concrete CrewAI flow modules and implementation-specific runtime dependencies until the selected wrapper prepares. Audit indirect imports through state, input schemas, package initializers and annotations as well as obvious flow imports. Type-only imports may use TYPE_CHECKING and deferred annotations; keep strict Pyright passing.

Unselected entries must not resolve configuration-specific implementations, construct wrappers, initialize clients or import their heavy flow/dependency modules. Unknown unused keys remain inert raw configuration. No dynamic plugin discovery, string import paths, loader framework, context placeholder, optional-package extras, or removal of the required CrewAI dependency is part of this work.

Normal execution loads the selected workflow's dependencies. Release verification explicitly exercises all built-in implementations supported by that release. Both policies are required: lazy imports must not turn a broken built-in into a successfully verified release.

Estimate: roughly half to one focused day for lazy imports and their tests alone. Completing all review gaps takes additional time. True optional dependency packaging and installation profiles are separate future work.

## Review evidence and its limits

At reviewed head b3d279b, the reviewer independently ran the standard gate: Pyright passed, Ruff lint/format passed, and 166 pytest cases passed. Existing flow/state/step regression tests were retained. The approved test plan itself was not weakened in PR #40.

The reviewer also ran 14 temporary probes successfully: concrete-wrapper malformed-output rejection, serialization failure classification, WorkflowInputError during execute, flow-construction ValueError during prepare, WF-03 alias defaults/override, and empty/disabled/null workflow overlays. These probes are not committed regression tests; add equivalent maintained coverage.

Three behaviors were reproduced:
1. Blocking the WF-03 flow module import made a WF-01 CLI run raise an uncaught ModuleNotFoundError. The registry imports wrappers whose top-level imports immediately load every concrete flow.
2. A selected wrapper constructor raising WorkflowInputError produced exit 2 and an input-error message; the approved constructor-defect boundary requires exit 1.
3. Invalid input for a shared_state alias named customer-job reported wf-02 rather than the configured ID and omitted the validation error type.

The first finding was qualified after inspecting release tooling: the existing installed-workflow smoke checks should already catch that deterministic import defect in the release environment. It was not evidence that a broken artifact had passed release verification. Sharon nevertheless chose lazy imports for execution isolation, while retaining exhaustive built-in release verification.

PR #40 records a successful clean current-release build at implementation commit 465a09754dcd3201dbaf925c7b243877141083a8. The reviewer did not independently rebuild that release. These results are historical baseline evidence, not verification of the follow-up changes.

## Required implementation corrections

### I-1: dependency import isolation and setup errors

Keep application assembly before framework initialization. Wrapper modules, their configuration schemas and the class registry must be safe to load without importing concrete flow modules. Move runtime imports to the selected preparation path, accounting for transitive imports and type annotations.

Place registry loading inside an appropriate outer execution-error boundary. An ordinary registry/import/setup defect must produce a safe execution failure with the selected workflow ID and setup phase, preserve its cause, and prevent all subsequent calls. A selected flow import failing during prepare is a PREPARE failure, exit 1. Never swallow the error, silently skip a selected implementation, or create a successful result.

The minimal error vocabulary remains sufficient; no large exception hierarchy is needed. Known shared/selected configuration and selection errors remain exit 2. KeyboardInterrupt/SystemExit remain unconverted.

### I-2: distinguish selection from actual construction

Separate known selection/configuration validation from invoking the selected constructor so a blanket passthrough cannot misclassify a constructor exception.

- Unknown/disabled IDs and invalid selected entries: exit 2 before construction.
- An explicitly raised ConfigurationError for invalid implementation settings: exit 2.
- Unexpected constructor exceptions, including WorkflowInputError, raw ValueError and raw Pydantic ValidationError: execution failure, exit 1, phase construction.
- Prepare converts only input-schema rejection to WorkflowInputError; state/flow construction errors remain execution failures.
- Execute/output validation/serialization classify every ordinary exception as execution failure, regardless of its exception class name.
- Preserve causes and wrap once per meaningful boundary. Do not repeatedly wrap an already classified execution error merely to change its wording.

Retain the factory's ownership of selection and construction. A small local helper or narrow try block around constructor invocation is sufficient; a new service or coordinator is unnecessary.

### I-3: selected identity and safe validation detail

The outer boundary knows the configured workflow ID, including aliases. It must ensure diagnostics identify that selected ID and the actual phase. Workflow-specific validators supply field locations and safe validation error codes/types, without assuming that the configured ID is wf-01, wf-02 or wf-03.

Apply this to selected-entry validation, implementation settings and input. For example, a boolean supplied to customer-job.initial should identify customer-job, PREPARE and initial/int_type without echoing the supplied value. Invalid output/serialization diagnostics must identify their own phases rather than EXECUTE by default.

Keep original exceptions available through causes and WorkflowFailure for local inspection, as applicable. Public CLI messages must not include raw values, YAML source lines or exception payloads. Do not promise that an arbitrary caller printing a complete chained traceback is redacted. No Langfuse export or context work is included.

### I-4: close coverage and status gaps

Implement the matrix below, preserving existing regressions. Reuse an existing test when its assertions prove the requirement; do not create duplicates to inflate the count. Existing state-model or pure-step tests alone do not prove the wrapper/no-kickoff or real-CrewAI behavior explicitly required by the plan.

Update stale current-status statements in the design README/index, implementation plan, Stage 01 successor note, Atlas and progress. Preserve dated historical evidence as history. Update official configuration/workflow/error guides for behavior actually supported after the corrections.

## Test matrix to close

Every ID below needs a concrete test reference and passing evidence before final review. Tests may cover multiple IDs where their assertions genuinely do so. The rows combine retained acceptance scenarios with gaps from the review; they are not a claim that every scenario is currently absent.

### A. ABC, lifecycle and typing

| ID | Required assertions |
|---|---|
| A1 | Parameterize a subclass missing each of the four required hooks; instantiation fails. Merely asserting isabstract(Workflow) is insufficient. |
| A2 | Fresh instance has CREATED, no failure and unavailable result. Result stays unavailable until successful validation; valid None is distinguishable from absence. |
| A3 | Each hook observes its in-progress status; each return has the correct success status. Complete sequence reaches COMPLETED and each hook executes once. |
| A4 | Wrong-order/repeated calls across all statuses run no hook and preserve status/failure. Include a genuinely FAILED instance with an existing failure record and a genuinely COMPLETED instance, not only injected enum values. |
| A5 | Re-entry from each of the four hooks is rejected while in progress. When the hook catches the order error, the outer call can complete; an uncaught order error escaping a hook follows normal outer hook-failure bookkeeping. |
| A6 | Failure in each hook records FAILED, the precise phase and original exception; no later hook runs. Retain already validated result after serialization failure. |
| A7 | KeyboardInterrupt and SystemExit from each phase propagate as the same object, without conversion or ordinary failure bookkeeping. Do not assert a durable terminal status after interruption. |
| A8 | Two instances have independent status, failure, mutable domain state and rich results. Serializer consumes the identical stored validated result; no replacement result argument exists. |
| A9 | Positive strict typing proves concrete nested-result access and covariance through the actual class-registry shape. Isolated negative Pyright checks prove final-method override rejection, incompatible hook signatures and invalid result assignments. Assert the intended diagnostic, not merely a nonzero process exit; exclude expected-error fixtures from the normal passing scan without weakening strictness or using Any/unchecked casts. |

### B. Runner and error boundaries

| ID | Required assertions |
|---|---|
| B1 | Mock assembly, registry, factory and public methods. Assert full order and arguments, including config path, selected ID/settings/config, prepare data, validate_output raw value, and argument-free serialization. Native result identity and serialized text remain separate. |
| B2 | Fail assembly, registry setup, selection, constructor, JSON decoding and each lifecycle phase separately. No later call or successful RunResult is produced. Invalid JSON never calls prepare. |
| B3 | Constructor matrix proves I-2, including WorkflowInputError and raw Pydantic ValidationError versus explicit invalid-config ConfigurationError. Assert category, selected alias, phase and cause. |
| B4 | Explicit input rejection during prepare remains input/exit 2; state/flow construction ValueError or ValidationError is execution/exit 1. WorkflowInputError raised during execute remains execution/exit 1. |
| B5 | Actual wrapper failure records yield exact EXECUTE, VALIDATE_OUTPUT and SERIALIZE_OUTPUT diagnostics; mocks must model the failure record where relevant. Assert safe text, selected alias and preserved cause, not only exception class. |
| B6 | Wrong-order programming failures become execution/exit 1 without invoking the prohibited hook; no reset/retry. Do not collapse a validation/serialization order error into an incorrect phase label. |
| B7 | Register a real deterministic test-only Workflow with a nested typed result and run it through factory/runner using arbitrary YAML selection. Do not substitute a bare Mock for this case. No production workflow-ID/output-type branch is needed. |
| B8 | Retain shared-configuration-before-ID precedence and separate selected-ID validation. Do not restore the obsolete ID-before-configuration assertion or remove unrelated failures. |

### C. Registry, imports and aliases

| ID | Required assertions |
|---|---|
| C1 | Every built-in registry value is a concrete Workflow class with the common constructor; constructing valid instances succeeds. Registry contains classes, never shared instances or import-path strings. |
| C2 | Two aliases select the same class with different defaults and independent mutable state/results. Their per-run overrides do not mutate another alias or a subsequent fresh run. |
| C3 | Invalid unused entry shapes, unknown unused implementation and invalid unused implementation-specific settings do not block a valid selection. Assert unused constructors are not called. |
| C4 | In a fresh subprocess, build the lightweight registry without importing concrete flow modules. Guard imports so an attempted unused flow/dependency import fails loudly; selecting WF-01 must still succeed while WF-02/WF-03 flow modules remain unloaded. Do not rely on already populated sys.modules or pytest's configured process. |
| C5 | Selecting the deliberately blocked implementation produces the safe PREPARE execution error and nonzero CLI result; no unhandled traceback or later step. A separate registry-setup failure is normalized at its outer boundary. |
| C6 | Fresh-process import interception proves the real runner applies CrewAI startup settings before the first framework/selected-flow import. Calling configure_crewai alone is insufficient proof of runner ordering. |

### D. YAML, selected settings and overlays

| ID | Required assertions |
|---|---|
| D1 | Shared catalog missing/empty/null/list/scalar; unknown root/integration fields. Empty catalog loads but any selected ID fails. Retain path-selection, unreadable-file and reload tests. |
| D2 | Selected entry null/list/scalar/empty; implementation missing/null/non-string/empty/whitespace/unknown; selected ID empty/whitespace/unknown; enabled strict true/false versus string/number/null; name omitted/valid versus empty/null/whitespace/non-string; config omitted/empty versus null/list/scalar; unknown selected entry fields. |
| D3 | WF-01 rejects nonempty settings. WF-02/WF-03 defaults cover omitted/empty/partial/invalid defaults containers, unknown config/default fields, strict numeric types, booleans, floats, ranges and boundaries. Validate bad defaults before a request override can mask them. Valid request values win; invalid explicit request values never fall back. |
| D4 | Root and nested duplicate YAML keys in both base/local files, including unused blocks. Unsafe tags, merge keys, malformed YAML and non-string/complex keys are rejected independently before merge. Build otherwise valid fixtures so a test cannot pass because of an unrelated syntax/schema error. |
| D5 | Recursive workflow local overlays; empty local maps retain inherited entries/defaults; enabled:false disables an inherited entry; selected null errors; unused malformed entries remain unvalidated except global YAML syntax/key rules. Environment precedence and next-invocation reload remain intact. |
| D6 | Selected entry/default/input diagnostics include selected alias, phase and field/error type where available; no secret marker or YAML source line appears in public messages. Test both source configuration files and request input. |

### E. Real workflows and concrete wrappers

| ID | Required assertions |
|---|---|
| E1 | Preserve all existing flow/state/step cases and real decorated kickoff. WF-01 absent input and {} return the original text in order; any field is rejected before kickoff. |
| E2 | WF-02 defaults yield native 20/display 20/history [3,5,20]; 10,-2,3 yields 24/history [10,8,24]. Add zero, negative arithmetic and allowed -1000/1000 boundary cases through the real flow with exact history. |
| E3 | WF-02 invalid range/type/extra fields and WF-03 -1/101/string/bool/float/extra fields fail through the wrapper without kickoff/steps. Retain model-level tests as well. |
| E4 | WF-02 alias defaults 10,-2,3 yield 24 and request initial 2 yields 0; fresh runs retain configured defaults. WF-03 alias default score 59 yields needs_work; override 60 yields pass with threshold 60 unchanged. |
| E5 | Real WF-03 kickoff for 0,59,60,80,100 executes only the correct branch exactly once. needs_work remains a successful business result. Preserve terminal-failure regression coverage. |
| E6 | For each concrete wrapper inject prepare/setup, execution, malformed-output and serialization failures; assert phase/category/cause, terminal status and blocked downstream calls. Explicitly reject bool as WF-02 output; verify the actual wrapper validators, not only a shared test workflow. |
| E7 | WF-02 add failure skips multiply and preserves expected partial history. Repeated independent runs and per-instance mutable state remain isolated. |

### F. CLI, installed release and maintained verification

| ID | Required assertions |
|---|---|
| F1 | CLI default, explicit workflows, both configured alias types and JSON overrides retain expected text. Arbitrary IDs need no parser changes. needs_work exits 0; config/selection/input exit 2; construction/import/execute/invalid-output/serialization/order failures exit 1 with no result banner. |
| F2 | Preserve raw argv forwarding with spaces/quotes, explicit configuration paths, isolated interpreter flags and absence of source/editable import leakage. Keep existing release/dependency tests. |
| F3 | Verification cases explicitly cover every built-in implementation supported by the release. Assert coverage agrees with registry keys so adding a class without a verification case fails the gate. Default construction is not enough to test deferred imports: prepare and execute deterministic supported cases. |
| F4 | Inject a broken deferred import in a built-in verification case; verification fails and release remains unverified. No silent skip of an implementation with a missing required package. Retain the existing incomplete-release test and add meaningful linkage to lazy-import verification. |
| F5 | Verify the newly built installed artifact with all built-ins and both alias/default/override scenarios, plus representative failure exits. Source and installed results agree. Persist reproducible commands/evidence; manual observations alone do not replace maintained CLI tests. |
| F6 | Full gate and fresh-process offline audit pass with dedicated fixtures. Current-release dependency closure/hash checks and installed isolation pass. Exclude app/examples entirely. Describe Python socket auditing accurately; do not claim an OS network sandbox. |

## File placement and working order

Use the existing component owners:

| Area | Expected files or locations |
|---|---|
| Lazy dependency loading | Each workflows/wf_*/workflow.py and any transitive import that defeats isolation; application/workflow_registry.py remains a class map |
| Construction/error boundaries | application/workflow_factory.py and workflow_runner.py; shared workflow errors only as needed |
| Diagnostics | Workflow validators/configuration validation and the outer application boundary that knows the selected ID |
| Contract/type tests | tests/workflows/test_contract.py and isolated type fixtures/checks with documented collection rules |
| Wrapper tests | tests/workflows/wf_*/test_workflow.py or equally clear existing workflow test modules |
| Registry/runner/import tests | tests/application/; fresh subprocess helpers use maintained test fixtures |
| Configuration/CLI/release tests | tests/config/, tests/cli/, tests/releases/, tests/tooling/; tooling/verify_runtime.py for maintained installed smoke checks |
| Decisions and evidence | This package, designs/progress.md and Atlas; supported operating instructions in app/docs |

1. Reconcile branches and run the current baseline gate. Preserve any concurrent accepted work.
2. Implement I-1 through I-3 with focused regression tests that reproduce the review findings.
3. Complete matrix coverage, reusing existing tests where adequate. Avoid introducing a second runner, orchestration engine, plugin system or generalized lifecycle machinery.
4. Reconcile design/public docs and generate Atlas from the final canonical files.
5. Run targeted checks, then the full gate and clean current-release verification. A new failure or code change justifies rerunning affected checks; otherwise avoid repeated broad testing.
6. Push the implementation branch and update PR #40's evidence. Leave merge decisions to Sharon.

Keep computations/routing inside CrewAI, preserve strong typing and ordinary interruption behavior, and retain all previously accepted workflow scenarios. Context/Langfuse, actual optional dependency packaging, recovery and children remain separate scopes.

## Documentation and guarded authority

This follow-up was requested explicitly after review, including lazy imports now, constructor classification, diagnostics and all planned test gaps. It clarifies approved contracts within the existing component boundaries; no charter, principle, governance-process or future orchestration change is required.

- The workflow design gains explicit lightweight-wrapper/deferred-flow semantics, the release-verification counterpart, and phase/alias diagnostics.
- The original test plan remains intact and links to this implementation checklist.
- The implementation plan and package/index statuses identify PR #40 and supersede obsolete initial-stop wording.
- The guard register includes the approved package and this follow-up; existing guards remain.
- Atlas describes approved design plus a pending reviewed implementation, without promoting PR #40 to merged behavior.
- This documentation commit changes no runtime behavior, so app/docs changes belong with the actual fixes on PR #40. The implementation agent must update supported import/error/release guidance there.
- Historical Stage 01 computations and tests remain protected; its successor status/reference may be updated precisely within the existing approval.
- Relevant observability/agent-execution explorations were considered only for the existing future context boundary. No exploratory component is adopted.

## Evidence required before asking for another review

Fill this section on the implementation branch; do not mark completion in the documentation-only PR.

- Final implementation commit SHA and current PR base/head.
- Every matrix ID A1-F6 mapped to exact test function/node IDs; note which pre-existing tests satisfy a row. Keep this mapping concise. No row is satisfied merely by a test count or a temporary reviewer probe.
- Exact commands and outcomes for focused tests, negative typing probes, full gate, Atlas/checks and clean release verification.
- Installed artifact commit/version/hashes and deterministic source/installed alias comparisons.
- Confirmation that no unrelated regressions were removed, no tests rely on examples, and CrewAI still owns orchestration.
- Known limitations and any unresolved discrepancy. Linux checks do not establish Mac/PyCharm behavior.
- Updated PR #40 description with current scope and evidence; do not claim ready if required cases remain unimplemented.

## Copyable instruction for the next agent

> Continue PR #40 (feat/workflow-contract). First read root/design instructions and the latest PR #38 workflow-contract package, especially review-follow-up.md. Incorporate the updated design branch without discarding the existing implementation. Implement corrections I-1 through I-4 and satisfy every test-matrix ID A1-F6, preserving existing regressions. Lazy dependency imports are required now; context/Langfuse and actual optional-package installation profiles remain separate. Verify every built-in during release creation despite lazy normal execution. Update docs, Atlas and the per-ID evidence mapping; run the full gate and verify a clean installed current release. Push to PR #40 and report results and limitations. Do not merge either PR.
