# Workflow contract test plan

Status: **Approved test specification. PR #40 includes the follow-up coverage mapped in [review-follow-up.md](review-follow-up.md#pr-40-maintained-test-mapping); its final release evidence remains in progress.**

Preserve existing regression scenarios. Add focused tests for the new contract without replacing real CrewAI integration coverage with mocks. Application fixtures must not read, import or depend on app/examples.

## 1. Shared ABC and lifecycle unit tests

Use a small deterministic concrete test workflow with injectable hook failures.

The tested public sequence is `prepare()`, `execute()`, `validate_output()` and `serialize_output()`; corresponding underscore hooks supply only the workflow-specific behavior.

- Cannot instantiate a subclass missing any required hook.
- Constructor initializes CREATED, no failure and no validated result.
- Each public method exposes its in-progress status inside the hook and its success status after return.
- Complete sequence reaches COMPLETED. Kickoff/hook execution occurs once.
- Parameterize wrong-order calls across all statuses: no hook runs; status and original failure record stay unchanged.
- Repeat prepare/execute/validation/serialization and call them after COMPLETED/FAILED: reject without reset, retry or duplicate work.
- Re-enter the same method from its hook: reject while in progress.
- Every hook raising an ordinary exception produces FAILED with the correct phase and original cause; later hooks do not run.
- KeyboardInterrupt/SystemExit propagate unchanged; they are not reported as invalid input or swallowed.
- Two instances have independent status, failure, validated results and mutable domain state.
- Reading result before validation fails. A valid None result is distinct from no validated result.
- Nested typed result survives without stringification; serialization reads that same validated result and can fail separately.
- Type-check a concrete rich-result workflow, covariance through the heterogeneous registry, final override prohibition and hook signatures. Keep expected-error checks isolated from the normal passing type gate; do not weaken strict settings or add Any/casts.

## 2. Runner unit tests with other components mocked

Mock assembly, selection/factory and workflow public methods. Do not use CrewAI for this layer.

- Exact public call order and argument forwarding; serializer takes no caller-supplied result.
- Returned RunResult holds the validated object and the serialized presentation separately.
- Failure at each boundary prevents every subsequent call and never returns success.
- A ValueError or WorkflowInputError originating during execute remains an execution failure.
- Explicit input rejection during prepare maps to exit category 2; unexpected prepare/setup defects map to category 1.
- Configuration/selection failure occurs before workflow steps; invalid JSON does not call prepare.
- No output type checks or workflow-ID branches in the runner: a test-only rich-result implementation works through the same path.
- Preserve causal chain, workflow identity and phase. Safe public errors do not reveal private input/config values.
- Replace the old unknown-ID-before-configuration test with shared-configuration-first and selected-ID validation tests. Do not remove unrelated error coverage.

## 3. Registry and factory tests

- Every built-in implementation is concrete, satisfies the constructor contract and creates a Workflow instance.
- Stable keys resolve real classes; class name and module path are not YAML inputs.
- Unknown, missing or disabled selected ID fails clearly; unknown implementation fails before prepare/kickoff.
- Two IDs selecting shared_state with different defaults instantiate independent objects of the same class.
- New configured alias runs without modifying the runner, parser choices or workflow ID Literal.
- An invalid unused entry, unknown unused implementation and unused implementation-specific invalid settings do not block a valid selected entry.
- Do not resolve configuration-specific unused implementations or construct unused wrappers. Lightweight wrapper classes may be imported for the explicit registry; unused concrete flow/dependency modules must remain unloaded.
- Fresh-process test proves integration configuration precedes any CrewAI import. Keep current import-order regression protection.

## 4. Configuration tests

Cover each case in the design's configuration table:

- Missing workflows versus empty mapping versus null/list/scalar.
- Missing/empty/null implementation config and defaults; unknown shared fields versus unknown selected entry/settings fields.
- Strict booleans and integers; reject numeric strings and bool-as-int.
- Duplicate keys at root and nested levels in both base/local files, including unused workflow blocks.
- Unsafe tags, merge keys, malformed YAML, invalid mapping keys and unreadable files.
- Selected config defaults validate before request overrides; valid overrides win; invalid explicit values do not fall back.
- File-path and local/environment precedence remain unchanged. Reload changes on the next invocation.
- Empty local mapping retains inherited entries; disabled overlay prevents selection; explicit null errors when selected.
- Diagnostics preserve field/type information and avoid values or YAML source snippets containing secrets.

Update maintained offline fixture configurations for the new required workflows block. Do not rely on the user's application.local.yaml.

## 5. Real workflow and wrapper regression scenarios

Keep existing flow/state/step tests; make only justified setup/import/assertion changes. Execute real decorated CrewAI flows in integration tests; do not manually invoke listeners to imitate kickoff.

| Workflow | Input/configuration | Expected result and behavior |
|---|---|---|
| WF-01 | absent input and empty JSON object | native/display `[Hello, workflow!]`; ordered steps |
| WF-01 | any input field | input failure, no steps |
| WF-02 | defaults 3, 2, 4 | native 20; display "20"; history [3, 5, 20] |
| WF-02 | initial 10, increment -2, multiplier 3 | native 24; display "24"; history [10, 8, 24] |
| WF-02 | zero/negative values and allowed boundaries | exact arithmetic/history; no accidental bool acceptance |
| WF-02 | outside -1000..1000, extra fields, numeric strings, bool | input failure, no steps |
| WF-02 alias | configured defaults 10, -2, 3 | 24 without request input; request initial 2 gives 0 |
| WF-03 | default 80; scores 60 and 100 | pass; only accept branch |
| WF-03 | scores 0 and 59 | needs_work; only revise branch; successful exit |
| WF-03 | -1, 101, numeric string, bool, unknown field | input failure, no steps |
| WF-03 alias | configured default score 59; request score 60 | needs_work by default; pass with override; threshold unchanged |

For each workflow, verify wrapper failure classification, invalid output and serialization failure using focused injections. For WF-02, inject add failure and assert multiply never runs. Preserve repeated independent run tests and route exclusivity.

Changing RunResult.output from display text to a typed value intentionally changes affected runner assertions. Preserve the old CLI text assertions using serialized_output. This is contract adaptation, not permission to weaken regression expectations.

## 6. CLI, offline and current-release tests

- Default WF-01, explicit WF-02/03, arbitrary configured alias, valid inputs and existing successful text.
- Exit 2 for configuration/selection/input; exit 1 for execution/output/serialization; exit 0 for valid needs_work.
- Raw arguments including spaces/quotes remain individual argv values; no shell interpolation.
- Current source and newly built current release agree. No old-release/new-config compatibility matrix.
- The release verifier covers every registered built-in implementation, exercises deferred imports, and leaves the release unverified if any supported case fails.
- Preserve isolated interpreter flags, no editable/source import leakage, production dependency closure and dedicated offline settings.
- Maintain the fresh-process offline audit; describe it accurately as Python socket auditing, not an OS network sandbox.
- Keep normal check/test/lint/type/release gates and existing test collection; exclude personal examples.

## Acceptance and evidence

Before changing code, record the baseline full-gate result. After implementation, run targeted tests once changes are complete, then the standard full gate and relevant current-release verification. Fix failures; do not delete regressions to obtain green results.

Record commands, revision, outcomes and limitations. Sharon's manual gate should show default WF-01, WF-02 with two inputs, both WF-03 routes, a YAML alias and representative input/execution failures. No Langfuse server or real agent is required for this refactor.

Documentation-only verification is recorded separately in the implementation plan; it does not stand in for any test above.
