# Offline test coverage and CI — implementation brief

- Project: `system-one-harness`
- Feature: `f-01-offline-test-suite`
- Source repository: https://github.com/SharonLanger/system-one-harness
- Foundation: merged PR 46; main baseline `c7331b6288f5200c8b446ccb1747e521b01bc0dd`.
- Purpose: one self-contained brief for the next implementation session.
- Execution was requested in the conversation. This brief records that scope; it does not retroactively mark the original `design.md` approved.

## Outcome

Deliver meaningful unit, flow-integration and real-process end-to-end coverage, with automatic GitHub Actions checks on every PR. Make individual check status, test counts, failure logs and downloadable reports easy to locate from a phone. Existing tests stay active. No experiment migration or deletion belongs in this implementation.

## Start and work boundaries

Read repository instructions and this brief. Fetch current main, verify PR 46 is merged, create a feature branch and inspect the baseline test results. Reuse existing tests and shared fakes. Work through the steps below without stopping for routine implementation choices. Commit to the feature branch and open a source-repository PR; never push to main or merge a PR. If source behavior must change materially, explain the defect and proposed correction rather than weakening a test to produce a pass.

The implementer role in the playbook is currently a placeholder. Execute this concrete brief directly as a coding task; do not claim the placeholder role or Markdown alone runs an orchestration engine.

## Agreed test and storage boundaries

- Test meaningful behavior and failures, not one mechanically mocked test per method.
- Unit tests may mock individual collaborators. Integration tests keep the flow, blocks, validation and extraction real and replace the external model boundary with explicit scripted responses.
- Keep the existing memory session store for same-process scenarios. Do not build a large fake database.
- For actual subprocess persistence, give each test a unique pytest `tmp_path` directory and pass its paths into every child process. Do not hand-name shared output files after tests or manually delete files from a previous run.
- Dedicated session-persistence tests may write and read temporary files to prove durability, corruption handling and transactions. Keep them until SQLite replacements exist.
- Reading authored source and JSON fixtures is allowed and necessary. Preserve or add tests for JSON-to-object parsing, nested values, Unicode, malformed input and duplicate keys where the public contract rejects them.
- Ordinary scenario results should be asserted through returned values, public output or captured events. New tests must not read generated reports/logs as their oracle. A broad migration of existing logging tests is deferred with the debug redesign.
- Python parent monkeypatches do not propagate to child processes. Install the scripted external dependencies and temporary paths inside the test-only launcher before loading the real entry point. Avoid production test-mode flags.

## Step 1 — inventory and focused unit tests

Map existing unit and CLI/hook tests before adding duplicates. Keep their useful coverage. Add missing input/serialization cases: nested and Unicode JSON, empty and false values, malformed/duplicate keys, missing input file, public Context serialization, and empty output for Noop/Failure. Check expected exception type/code and exact decoded value, not only whether a call returned.

Keep mock scope narrow. A mocked dispatcher can prove CLI argument forwarding, but cannot prove the whole flow works. Label each test according to what is actually real.

## Step 2 — connected flow integration

Use real action and method-selection blocks plus real TypeScript source extraction and scripted Laya. Cover successful context and negative cases: unsupported action, ambiguous/no selected method, absent file, empty request, no callable candidates, invalid model response, model failure, source disappearing during extraction, and output-budget rejection. Assert meaningful result reason/stage and ensure all scripted responses were consumed. Check that failed/no-op scenarios do not emit enrichment payloads.

Do not force existing experiment report/replay infrastructure into the harness. Record which behavior is covered by which test and distinguish deliberately deferred experiment-only contracts.

## Step 3 — public CLI/hook end-to-end tests

Start fresh child processes at the actual CLI and gateway entry points. Keep the default dispatchers, flow, real decision blocks, serializer and TypeScript extractor active. Replace only external Laya loading and redirect persistent session state to a test-specific temporary directory. Capture diagnostic records in memory; transfer test evidence through a structured channel separate from public stdout.

Verify:

| Case | Required observation |
| --- | --- |
| Valid prompt | One valid serialized context response containing actual extracted source; correct event name and exit status. |
| Repeated prompt in same session | No repeated context from a fresh process. |
| PostCompact then prompt | Compaction produces no context; next prompt may enrich again. |
| Different session | Independent session can enrich. |
| Unsupported/ambiguous/missing/empty input | No context, expected reason, no unnecessary model calls. |
| Invalid or failing Laya response | Controlled failure with no context; exact stage and expected call count. |
| Source/extraction failure and output budget | No context and correct failure/no-op classification. |
| Malformed public JSON | Input error and zero model calls. |
| Model/library stdout and file-descriptor noise | Public stdout remains valid protocol; noise is confined to stderr. |

Keep existing dispatcher lifecycle tests. They provide a useful lower-level diagnostic when a process test fails. Keep existing storage transaction/concurrency tests; a memory fake does not prove those contracts.

## Step 4 — automatic and visible CI

The baseline already runs Python, TypeScript and hygiene on PRs. Extend it rather than adding a duplicate workflow.

- Use standard GitHub-hosted Ubuntu runners and no paid service or real model credentials.
- Run on every `pull_request`, on main pushes, and allow manual dispatch.
- Show separately named checks for Python unit, integration, end-to-end, remaining existing tests, and TypeScript build/tests. Keep the remaining active root and block-runtime tests collected; do not lose them by running only the three new folders.
- Build the TypeScript helper before Python suites that use it; use the existing pinned npm lockfile.
- Use read-only repository permissions, bounded job timeouts, dependency caches and cancellation of superseded runs from the same PR. One failed suite must not cancel evidence from the others.
- Produce JUnit XML, readable count summaries and downloadable reports on success or failure. Missing reports or empty suites must never look like a pass. Preserve the test command's failing exit code.
- Keep repository-hygiene checks active. Use short artifact retention and avoid duplicate PR/push runs.
- Document the phone navigation: PR → Checks → named job → test step; workflow Summary and Artifacts for counts and XML. State that branch/ruleset enforcement is separate from having a workflow.

This is continuous integration. Package publishing, releases, deployments, license selection and paid infrastructure are separate work.

## Step 5 — verify and deliver

Run the new focused tests, then the complete active Python and TypeScript suites and repository hygiene. Record exact commands, counts, skipped tests and the tested commit. Investigate failures; distinguish introduced failures from baseline or environment problems. Do not silently skip or delete tests. If the environment cannot execute a check, report that limitation and use real GitHub CI evidence before claiming success.

Verify the new suite selection covers all active tests without duplicates. Verify summary parsing with successful, failed, skipped, empty and missing report inputs. Inspect GitHub Actions results after opening the PR, fix actionable failures, and link the actual run so the user can inspect it.

The PR should include test code, CI configuration, and a concise coverage map plus result-viewing instructions in `tests/README.md`. Its description must identify what is real versus scripted in the end-to-end tests and record validation and remaining limitations. No claim of complete feature coverage is justified solely by a test count.

## Completion criteria

- All intended new unit, flow and process scenarios execute; no new hidden skips.
- Existing active tests remain collected and no experiments or tests were deleted.
- Ordinary new test oracles use behavior, not generated reports; real persistence is isolated per test.
- PR checks run automatically and visibly separate Python and TypeScript results.
- CI report artifacts and summaries are available, with exact commit evidence.
- A branch PR is ready for the user to review, with any remaining failure or uncertainty stated plainly.

## Explicit next work

Full operating-system network/write-denial enforcement remains deferred. Temporary paths and scripted loading reduce accidental side effects but do not prove a complete sandbox.

SQLite and debug-log redesign are later features. Keep the file store's existing contract tests until replacements exist.

After harness test coverage is established, plan a separate experiment-repository migration. Inventory and copy all experiments, authored inputs, cases and relevant documentation; preserve history/provenance as appropriate; validate the destination and reference/dependency changes; then remove the migrated content here as a separately reviewed change. Another agent may own that migration. No deletion is authorized by this brief, and a green suite alone does not establish that every experiment's behavior is preserved.
