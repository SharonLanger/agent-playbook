# PR 46 test coverage follow-up — draft

- Project: `system-one-harness`
- Source: https://github.com/SharonLanger/system-one-harness/pull/46
- Feature: `f-01-offline-test-suite`
- Status: Draft for user review; no change to the approval status of `design.md`.
- Inspection baseline: PR head `4ce5d9cc314286224c21f5debb0a0c85e89f3cc1` and playbook review-02.

## Purpose and scope

Close the most important test gaps identified during PR 46 review without turning this PR into a storage redesign or a migration of all deferred experiments. The central result should be credible coverage at two connected depths: real flow with real blocks and scripted Laya; and real hook/CLI entry through serialization, protocol output and exit behavior. Unit tests still cover focused decisions and failure paths.

This is a proposed follow-up scope, not an approved deviation from the existing draft design. The user will decide which items must land in PR 46 and which can land in the next PR before implementation is treated as complete.

## Behavioral test layers

| Layer | Keep real | Replace or isolate | Main assertion |
| --- | --- | --- | --- |
| Unit | One meaningful decision or contract | Unrelated collaborators | Return value, error, or call contract; test important branches rather than one test per method. |
| Flow integration | Flow, action and method-selection blocks, validation and TypeScript extraction | Laya responses via scripted fake; in-memory session store where relevant | Context/Noop/Failure and meaningful extracted content, plus scripted-call consumption. |
| Hook/CLI system | Actual entry point, dispatch, flow, blocks, serializer and process outcome | Real Laya/network; test-specific output paths and injected storage/logging boundaries | Exact stdout/stderr protocol and exit status, alongside session behavior across invocations. |
| Persistence contract | Production file-backed session store | Only external dependencies; unique temporary directory | Save/reopen/transaction, malformed data, and cooperating concurrent updates. Reading the written file is allowed here when it is the contract under test. |

The existing `tests/integration/flows/test_real_blocks_offline.py` exercises real blocks but enters at the flow. `tests/system/hooks/test_offline_session_lifecycle.py` covers session behavior but directly calls dispatchers. Existing gateway tests replace both decision blocks. Preserve those useful tests and add the missing connected path; do not relabel a dispatcher test as full end-to-end coverage.

## Proposed implementation

1. Inventory current CLI/hook tests and map successful context, Noop, Failure, malformed input, timeout, and protocol behavior to existing tests. Add focused unit tests only where a meaningful branch or contract is uncovered. Do not create a test merely for each method name.
2. Add a test-only entry-point launcher that installs scripted Laya before the real gateway/CLI loads. Use the current injection points; do not add production test flags or replace the action and selection blocks. Fail on unexpected or unconsumed fake responses.
3. Run the complete prompt-to-context path through the real entry point, real blocks and TypeScript extraction. Cover: successful context; unsupported/ambiguous request; invalid or failing Laya response; missing source or extraction failure; repeated prompt suppression; PostCompact followed by new enrichment; and independent sessions. Split scenarios where necessary for readable failure diagnosis.
4. Assert exact public serialization, stdout/stderr separation, and exit behavior at the entry point. Check internal events through returned values or a test-owned in-memory/structured channel. A subprocess test must inject its dependencies and paths in the child process; parent monkeypatches alone do not cross that boundary.
5. Give each test a unique temporary directory using pytest `tmp_path`. Redirect session-state and any required log output, including child-process output, into that directory. Do not hand-name files after tests, manually delete prior-run files, or let a test write application output into the checkout. Existing dedicated file-persistence tests remain active and use temporary directories.
6. Stop using generated output files as the result oracle in ordinary scenarios that this work touches. Assert returned Context/Noop/Failure, public CLI output, or captured events. It is valid to read authored source and JSON fixtures and to test JSON parsing/serialization into objects. Keep direct file readback in dedicated storage-contract tests. Do not delete a test to satisfy this rule; preserve its behavior with an equivalent assertion.
7. Run focused unit, flow integration, system, Python full suite, TypeScript tests, and repository hygiene in CI. Record commands, counts, skips, and exact commit. Verify that the new end-to-end scenario actually executed; a green command alone can hide conditional skips.

## Acceptance checks

- At least one system test begins at the real hook/CLI process boundary and reaches the real decision blocks and TypeScript extractor with scripted Laya, then checks serialized output and exit status.
- Flow integration tests cover both positive and negative behavior without using generated files as their result oracle.
- The session lifecycle is verified across invocations; subprocesses receive unique temporary state paths. Persistence contract tests still cover real file-store behavior.
- JSON fixture reading and JSON-to-object parsing tests remain active, or are added if an inventory shows the behavior is missing. No experiment or existing test is deleted as a shortcut.
- A coverage table records each acceptance behavior, the test that proves it, and any explicit gap. CI passes on the updated PR head.

## Explicit deferrals and decisions

- Full network and write-denial enforcement across every test process remains a documented gap for a subsequent scope decision. This proposal still requires tests to use isolated temporary output paths; it does not claim that path redirection proves sandbox enforcement.
- SQLite migration, the debug-log redesign and replacement of the file-store implementation are separate work. Do not create a broad storage abstraction just for these tests; use the existing session-store injection where it suffices.
- The 105 named deferred experiment-derived checks are not required to become 105 active tests in PR 46. Keep their inventory and map relevant harness behavior to direct scenarios over time. Do not delete experiments or deferred tests without an explicit separate decision.
- The original `design.md` remains Draft 1. Before claiming the feature conforms to an approved baseline, approve an exact design revision or document an approved scope change. This document itself does not grant that approval.
