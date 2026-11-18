# M3 acceptance cases

Status: proposed test plan for Sharon's approved M3 behavior. Exact tooling command spellings, schema and migration mechanics must be completed before runtime implementation. Use stable IDs below; do not report mocks as live Docker evidence.

| ID | Scenario and observable acceptance | Level |
|---|---|---|
| MC-01 | Validate each component's resolved Compose model and shared entry behavior. Names are act-logs and act-langfuse; pinned images, loopback host bindings, logging retention and isolation remain intact. No duplicate stack from alternate entry paths. | Offline/config + live |
| MC-02 | Start logging only, Langfuse only, both, neither using integration enabled settings. Disabled components are not started; normal workflow execution never starts Docker. Logs-only operation does not require disabled Langfuse credentials. | Focused tooling tests + live |
| MC-03 | Stop either component while the other stays usable. Stop works after its enabled setting becomes false. Repeated start/stop is predictable; no down -v or volume deletion. | Focused tooling tests + live |
| MC-04 | Existing deployment transitions to new Docker names with the same volumes and secrets. Existing records/traces remain readable after stop/start. Detect already-running old/new stacks and avoid concurrent writers. Conflicting/ambiguous storage mapping stops with actionable guidance, not empty replacement storage. | Migration fixtures + live |
| MC-05 | Shared YAML/local/environment precedence and secrets.file selection use the existing loader. Non-secret deployment settings belong in YAML; tokens/passwords use named references to the shared file. Unrelated keys and values survive setup/migration. No second parser/store or implicit discovery. | Offline real-loader tests |
| MC-06 | Migrate documented legacy Langfuse .env values without regeneration or destructive overwrite. Identical entries are idempotent; conflicting entries require resolution before mutation. Missing/unreadable/invalid files fail safely. Current VictoriaLogs has no artificial credential requirement. | Synthetic file tests |
| MC-07 | Only the selected component's required values reach its deployment. Credentials never appear in argv, normal diagnostics, reports, tracked files or test failure output. Use synthetic sentinels; do not read real user secrets. | Offline transport/process tests |
| MC-08 | Unavailable Docker, invalid config, ports occupied and component startup failure produce bounded, actionable status. Report partial success honestly; do not shut down a healthy unrelated component or implicitly retry workflow work. Define exact timeout/exit behavior in completed design. | Offline faults + live where applicable |
| MC-09 | Existing Langfuse management/check behavior retains its documented user contract or explicit migration guidance. Shared entry point reuses component definitions and health methods; health is not ingestion proof. | Regression + source review |
| MC-10 | Source/package/CLI/file/folder/user path names remain unchanged except Docker naming references. Issue #56 stays separate. No app/examples access, M4 CLI expansion, SDK upgrade or runner behavior change. | Diff review |
| MC-11 | Canonical configuration guide documents shared credentials and current sections; setup/logging/Langfuse docs link there. Guarded shared-config rule and AGENTS.md match the approved scope. Atlas/status and all links reflect actual evidence. | Documentation checks |
| MC-12 | Deliver a copyable Mac .txt guide after implementation: prerequisites/versions, checkout/revision, safe migration, selection, independent and aggregate operations, retained data, expected results, troubleshooting and cleanup. Include LG-10 real M2 workflow correlation query/lifecycle/DEBUG/chained-exception/UI/shutdown inspection. Clearly separate instructions from completed evidence. | Artifact review + manual |

## Concrete assertions for the completed proposal

All offline tests use synthetic files, mock Docker responses and fake volume labels. The exact target names below are proposed test locations; implementation may keep equivalent tests in the same maintained test module with the same IDs in names.

| ID | Proposed maintained check and assertion |
|---|---|
| MC-01 | `app/tests/tooling/test_services_manage.py::test_compose_models`: run each `docker compose -p ... -f ... config --quiet` with synthetic values; inspect `config --format json` safely in a controlled fixture for project names, service/image/port/network/retention/volume targets and no aggregate project. Compare canonical service definitions to pinned source. A real daemon is needed later for binding. |
| MC-02 | `test_selection_matrix`: parameterize enabled logs/Langfuse and explicit/all requests with real loader and synthetic secrets; assert only selected Compose calls. Logs only succeeds with missing Langfuse keys. Workflow runner test asserts no Docker invocation. |
| MC-03 | `test_stop_disabled_and_repeat`: real loader disabled values, repeated start/stop, per-project mock states; assert stop reaches the requested project, no other project down and no `-v`. |
| MC-04 | `test_legacy_volume_mapping`: fixtures for complete legacy, custom project, new, partial, foreign, old/new concurrent and mounted-by-other states; inspect expected source/target and labels; assert no `up` on conflict and same external volume names on migration/repeat. Live Mac: identify old/new project containers and six volume names, verify old records/traces after restart. |
| MC-05 | `app/tests/config/test_loader.py` service-mode cases: base/local/secrets/process precedence, `--config` and environment selector, typed ports/retention, named refs, old YAML defaults, no provider parser, no actual `os.environ` mutation. |
| MC-06 | `test_migrate_legacy_secrets`: existing identical, absent, conflicting, process override, malformed/unreadable/missing, interrupted write and fresh initialization; assert byte-preserved unrelated entries, mode 0600, backup, idempotency and no regeneration of old seven values. |
| MC-07 | `test_compose_environment_isolation`: inject unique secret sentinels and hostile inherited Compose variables; assert Langfuse subprocess receives only its seven values and ports/volume names, logs subprocess receives no Langfuse secrets, argv/stdout/stderr/reports redact sentinels. |
| MC-08 | `test_partial_failure_and_deadlines`: unavailable engine, invalid config, port collision, unhealthy/timeout/interrupt; assert 0/1/2 policy, bounded calls, other healthy component untouched, no implied workflow retry. Live repeat for port collision when feasible. |
| MC-09 | Existing `app/tests/tooling/test_langfuse_manage.py` plus CLI delegation tests: direct script/CLI compatibility, `--check` hosted endpoint without Docker, `--logs/--follow/--open` behavior, legacy `--env-file` migration guidance. Health result is not stored-trace evidence. |
| MC-10 | Diff inspection: only Docker project names change; no source/package/CLI/path rename, app/examples access, M4 CLI or SDK/runner changes. |
| MC-11 | Markdown link/config examples and Atlas freshness checks; review exact four guarded logical additions and public guide consistency with shipped behavior. |
| MC-12 | Review post-implementation Mac `.txt` for exact repo-root commands, versions, backup/migration, four selection states, independent/combined stop, volume/trace persistence, cleanup and M2 LG-10 correlation/query/lifecycle/DEBUG/chained exception/UI/shutdown observations. Mark live steps NOT RUN until Sharon records evidence. |

## Evidence requirements

Map every ID to maintained tests and exact assertions or live/manual evidence. Mark each as PASS/FAIL/NOT RUN/BLOCKED, with revision and environment. Run appropriate local quality checks; ordinary offline checks do not require Docker. Record Docker/Compose versions actually tested and any feature minimum supported by official documentation. Do not substitute successful health/flush for stored records.

MC-04 uses disposable test data for automation; preserving Sharon's actual volumes is checked through the later Mac guide. Never remove or reset real data to make a test pass. Full M3 acceptance and M2 LG-10 remain pending until live evidence exists.
