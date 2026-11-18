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

## Evidence requirements

Map every ID to maintained tests and exact assertions or live/manual evidence. Mark each as PASS/FAIL/NOT RUN/BLOCKED, with revision and environment. Run appropriate local quality checks; ordinary offline checks do not require Docker. Record Docker/Compose versions actually tested and any feature minimum supported by official documentation. Do not substitute successful health/flush for stored records.

MC-04 uses disposable test data for automation; preserving Sharon's actual volumes is checked through the later Mac guide. Never remove or reset real data to make a test pass. Full M3 acceptance and M2 LG-10 remain pending until live evidence exists.
