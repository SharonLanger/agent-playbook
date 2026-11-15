# M2 test cases

**Draft.** Use focused tests of our contracts. The SDK's implementation is not ours to re-test.

| ID | Scenario and meaningful assertions | Level / mapping |
|---|---|---|
| LG-01 | Real OTel in-memory export from helper: message, timestamp/severity, five selected identity fields; absent agent fields omitted; supplied context unchanged; optional scalar attributes preserved; conflicting/unsupported extras cannot overwrite identity or break workflow | Offline real SDK; LOG-01/02/03/22 |
| LG-02 | Parent → A → parent → B plus interleaved run contexts: correct IDs, no agent leakage; repeated invocations distinct; DEBUG filtering versus INFO produces expected record set | Offline; LOG-01/02/29 |
| LG-03 | Native exception export from an outer error raised from an inner error: type/message according to pinned SDK, both causes in stacktrace, no locals; one failed runner record for a propagated error; recovered failure followed by successful completion | Offline real SDK/runner; LOG-04/07/28/31 |
| LG-04 | Existing YAML/local/environment precedence for logging and Langfuse required_start; defaults; disabled integrations; malformed YAML/level/endpoint remains configuration failure; nonlocal endpoint rejected | Offline existing config path; LOG-14/24/26/29 |
| LG-05 | For each integration: initialization failure with required_start=true prevents workflow execution; false warns and runs exactly once with failed integration inactive; disabled skips init; no mandatory connectivity probe is called | Offline boundary fault injection; LOG-26 |
| LG-06 | Inject telemetry-only failures in helper emission, trace scope entry/update/exit and flush: business workflow runs once, result unchanged; a separate workflow exception still propagates with original cause/classification; cleanup attempted in either case | Offline real runner plus targeted faults; LOG-07/21/26 |
| LG-07 | Repeated runner calls/CLI exits: no duplicate handlers/records; contexts remain distinct; observations close before cleanup; logger resources removed; shared Langfuse provider not shut down | Offline; LOG-21 |
| LG-08 | Native tracing enabled/disabled alongside logs using SDK test exporters: existing Langfuse scopes/correlation still work; dedicated LoggerProvider does not replace TracerProvider; log-only calls create no trace | Offline coexistence; LOG-03/09/15 |
| LG-09 | Synthetic secret sentinels in settings/authentication failure objects never appear in exported records/terminal diagnostics; no whole-context/settings/input/output dumping; SDK diagnostics do not recurse into the log exporter | Offline exported records and terminal capture; LOG-10/20/24 |
| LG-10 | One maintained fixture run against local M1 VictoriaLogs: query exact correlation/workflow ID; view lifecycle, DEBUG and native chained-exception details; record actual shutdown behavior and pinned versions. Preserve separate offline tests | Opt-in manual/local; LOG-01/04/19/23/30/31 |
| LG-11 | Documented replacement check through the same helpers with SDK in-memory exporter: no workflow/provider imports or schema changes; review OTLP destination isolation; disclose that this is SDK-level interchangeability, not a second database migration test | Offline + source review; LOG-09/15/20/32 |

Use maintained independent fixtures under app/tests, never app/examples. Keep Docker/live checks opt-in. Do not add an exhaustive reliability, throughput, storage or host-egress suite. Exact local post-load UI sorting behavior under LOG-06 must be recorded as supported or a gap; do not build a custom viewer to hide a limitation.

Map every LG ID to an exact test node or manual evidence in implementation review reports. No PASS from a mocked successful send, a flush call count or process exit alone. LG-10 is NOT RUN until service evidence exists. Any safe-payload or native-scope compatibility failure is a concrete implementation gap to resolve, not permission to weaken the design silently.
