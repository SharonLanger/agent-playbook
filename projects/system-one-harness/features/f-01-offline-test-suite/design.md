# f-01-offline-test-suite — draft design

- Project: `system-one-harness`
- Source repository: https://github.com/SharonLanger/system-one-harness
- Feature identifier: `f-01-offline-test-suite`
- Status: Draft; not approved for implementation.
- Revision: Draft 1
- Source inspection baseline: `f2906a005c9385e49a5e1585828d9b34c489f2b2` (cleanup PR #45)
- Design location: `projects/system-one-harness/features/f-01-offline-test-suite/design.md`

## Problem and intended behavior

Build a clearly organized test suite that verifies individual components and complete harness workflows without calling real Laya.

Existing first-flow tests replace the action and selection blocks, leaving a gap in coverage of the complete flow through real blocks. Logging and session persistence can also create files during tests.

The new suite will:

- Test isolated behavior with mocks where appropriate.
- Exercise real flows, blocks, validation, and source utilities together with scripted Laya responses.
- Test complete hook/CLI behavior, including session history across invocations.
- Capture diagnostic logs and session events in memory by default.
- Exercise actual file persistence only in dedicated tests using temporary directories.

Experiments supply examples of useful harness scenarios only. New tests must not import experiment modules or reproduce experiment report/export infrastructure. Assertions should check returned harness behavior directly.

## Current write boundaries

Source inspection found these writes in normal production hook/flow execution:

| Write | Purpose | Default location |
| --- | --- | --- |
| Session events | Prompt enrichment history and PostCompact events | `logs/session-state/<session-id>.jsonl` |
| Session locks | Protect cooperating read–decide–save operations | `logs/session-state-locks/<session-id>.lock` |
| Debug logs | Gateway, flow, prediction, and source-helper diagnostics | `logs/debug.jsonl` |

The source extraction utilities read project files; hook context is emitted through stdout. No additional application file writes were found in normal flow execution. The explicit `src/live_check.py` readiness utility writes a temporary source file and a requested report; it is outside normal hook execution and this feature's scenario scope.

Relevant production boundaries are `src/hooks/session_state.py`, `typescript-helper/src/session-state.ts`, and `src/log_utils.py`. The existing TypeScript store exposes save/load operations; Python currently owns the cooperating cross-process lock and read–decide–save orchestration.

These findings are from source inspection, not a test run.

## Structure and shared mechanisms

Keep production code under `src/`. Mirror its relevant subdirectories inside each test level:

```text
tests/
├── conftest.py
├── unit/
│   ├── building_blocks/
│   ├── block_runtime/
│   ├── flows/
│   ├── hooks/
│   └── laya/
├── integration/
│   ├── building_blocks/
│   ├── flows/
│   ├── hooks/
│   └── storage/
├── system/
│   ├── hooks/
│   └── cli/
├── support/
│   ├── fake_laya.py
│   ├── memory_session_store.py
│   ├── recording_logger.py
│   └── cli_runner.py
└── fixtures/
    ├── projects/
    └── laya/
```

Create directories only when they contain tests. Retain TypeScript-owned tests in `typescript-helper/test/`. Do not add another `src/` level inside `tests/`.

### Suite responsibilities

| Suite | Real code | Replaced dependencies |
| --- | --- | --- |
| Unit | The method, block, or flow under test | Relevant collaborators needed for isolation |
| Integration | Real flow, blocks, validation, and source utilities | Laya; session storage and logging usually stay in memory |
| System | Hook/CLI entry point through the complete operation | Laya and external infrastructure |

Do not mock simple internal helpers mechanically. Test observable behavior rather than reproducing implementation steps. Offline system tests prove harness behavior under controlled model responses, not real model quality or live SDK compatibility.

### Scripted Laya fake

Use existing `AgentRegistry(loader=..., inspection_provider=...)` injection points. Supply explicit responses, inspection outcomes, and exceptions; record requests; fail unexpected or unconsumed scripted calls. Keep production request/response validation and budget decisions active. Do not recreate prediction logic or implement a second Laya.

### Memory session store

Keep one small test-support implementation holding events per session. Preserve history between scenario invocations and copy data to avoid accidental aliasing. It exists primarily for multi-invocation flow/hook tests; unit tests may mock store operations directly.

Do not emulate filesystem locking, corruption, or SQLite. Use the same session operations as production so replacing the fake later affects shared fixture wiring rather than individual scenarios.

### Recording logger

Capture structured events through the shared logging boundary so lower-level logging cannot escape to disk. Replacing only a flow's logger is insufficient because prediction and source utilities call shared logging directly. Keep the production file logger.

### CLI test runner

Use a test-only launcher that injects dependencies before invoking the real CLI entry point. Do not add production test-mode flags. Parent-process mocks do not propagate to subprocesses. Cross-process persistence scenarios use the real file store in an isolated temporary directory.

### Isolation

Reject real Laya loading, including tokenizer/model inspection paths. Block external network access during offline tests. Run system tests in a write-restricted environment with only designated temporary output locations writable; parent-process mocks alone are insufficient for subprocess isolation.

Authored fixture inputs remain read-only. Any test that needs to modify a source fixture first copies it to a temporary directory. Build artifacts and runtime caches must be prepared or directed to designated locations, separate from application outputs.

## Minimal production changes and compatibility

Introduce an injectable session-store interface around the existing operations:

- Save a session event.
- Read history, evaluate the session decision, and conditionally save under one transaction.

Keep current file persistence as the default. Preserve session isolation, duplicate-enrichment suppression, compaction handling, deadlines, and existing persistence-error behavior. The file implementation continues to own locking and the Python-to-Node bridge.

Add a scoped capture mechanism at the common logging boundary. Existing callers retain their logging API and production behavior. Reset test overrides between tests.

These changes must not alter hook protocol output, CLI arguments, block results, or flow decisions. Avoid a broad storage redesign solely for test support.

SQLite implementation and migration, a generic writer framework, a new logging service, experiment report testing, and experiment-project migration are outside this feature.

## Test plan and acceptance criteria

Required coverage:

- Unit behavior for supported blocks, flow routing, validation, and session decisions.
- A real prompt-to-context chain through real action and method-selection blocks, scripted Laya, and real TypeScript extraction.
- Unsupported requests, ambiguous selection, invalid responses, Laya failures, token-budget rejection, and source/extraction failures.
- First enrichment, repeated enrichment suppression, PostCompact, enrichment after compaction, and isolation between sessions.
- Existing behavior when session storage fails or deadlines expire.
- CLI/hook serialization, stdout/stderr separation, and process exit behavior.
- Dedicated persistence tests for reopening history, malformed stored data, and cooperating concurrent updates.

Acceptance:

- All active offline suites pass without Laya credentials, model downloads, or inference.
- Every new test has one clear suite assignment.
- Scenario tests assert returned behavior; they do not generate experiment reports.
- Tests leave tracked files and authored fixtures unchanged and create no application output in the checkout.
- Actual storage writes occur only in designated temporary directories.
- No test depends on historical run results or experiment imports.
- Existing failures are resolved or explicitly reported; reorganizing tests must not conceal them with new skips.
- Coverage migration records distinguish preserved behavior, newly covered gaps, and experiment-only cases excluded from this feature.
- Shared fakes remain small, test-owned, and independently replaceable; the file store remains the production default.

## Implementation sequence

1. Inventory active production tests and relevant historical scenarios; assign each to a suite and identify coverage gaps. Keep the migration checklist in this feature folder when implementation starts rather than adding placeholder documents now.
2. Add the minimal session and logging injection boundaries with focused regression checks.
3. Add shared fakes and isolation, then implement the complete flow and session-lifecycle scenarios.
4. Reorganize existing tests, repair fixture/import paths, and remove superseded helpers after replacement coverage passes.
5. Run Python and TypeScript suites and repository-hygiene checks; document commands for each suite and the complete offline run.

Do not bulk-enable deferred tests. Do not remove historical cases solely because related unit coverage exists. Experiment-only tooling remains outside the new suite and can move with the experiments later.

The cleanup PR reported one active failure in `test_wrapper_and_shared_entry_return_identical_context`, related to duplicate-session behavior. Reproduce and account for it during implementation; the earlier reported counts are not fresh validation for this feature.

## Assumptions, open questions, and approval

- SQLite is a later feature. The small in-memory store may remain useful after SQLite arrives.
- Production logging remains file-based for now.
- Preserve current production session semantics while making dependencies injectable.
- No open questions block review of this draft.
- Saving this document does not approve implementation. Obtain explicit approval of the identified revision before treating it as the locked design baseline.
- Once approved, preserve the baseline and follow the playbook's deviation-record instructions for proposed changes.
