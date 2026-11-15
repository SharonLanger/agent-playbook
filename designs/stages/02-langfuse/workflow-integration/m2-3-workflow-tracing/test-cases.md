# Combined runner + CrewAI tracing — test cases

Version 2, 2026-11-15. **REVIEW DRAFT**, linked to [design](design.md). Not executed acceptance. Supersedes version-1 RUN meanings; no previous RUN implementation evidence is reused. CTX-01–17 remain unchanged.

Use the actual application runner/factory/ABC with maintained workflows, real pinned SDK/instrumentor and an in-memory exporter. Isolate process-global instrumentation between tests using supported public setup/teardown or subprocess fixtures. Exclude app/examples and historical sandbox. Do not require a live backend for automated offline cases.

| ID | Scenario and required observable assertions |
|---|---|
| RUN-01 | WF-01 through runner: unchanged result; one runner root, one Flow kickoff child and produce/decorate/finish children of kickoff; unique observation IDs and one trace ID; no duplicates |
| RUN-02 | Every RUN-01 observation has exact context correlation_id, workflow_id and workflow_run_id; inspect exported attributes, decoding SDK serialization only in tests |
| RUN-03 | WF-02: unchanged result (20 for defaults), initialize/add/multiply/finish captured even where methods return None; do not require fabricated state history |
| RUN-04 | WF-03 both branches: begin/choose plus accept OR revise as executed; absent branch has no observation; outputs unchanged |
| RUN-05 | Runner failures at construction, input parsing, prepare, execute, output validation and serialization retain existing classification/cause; root ends and records failure; no invented downstream steps |
| RUN-06 | Controlled real Flow step failure: failed step, kickoff and escaping root reflect failure; previously successful steps remain successful; later steps absent |
| RUN-07 | Recovered child failure using a maintained test fixture: child failed, parent successfully completes; no automatic workflow failure inference |
| RUN-08 | Two sequential Python runner invocations in one process: fresh application IDs and separate root traces without an external parent; same correct step count; no duplicate instrumentor/exporters or premature client shutdown |
| RUN-09 | Disabled tracing in a fresh process: unchanged workflow outputs/errors, no exporting client/instrumentation pipeline or telemetry network attempts; test enabled process separately |
| RUN-10 | Native A/tool → workflow checkpoint → B/tool scopes: correlation retained, A/B IDs isolated, root and checkpoints free of agent fields; includes exception restoration. Synthetic mechanism test, not real-agent acceptance |
| RUN-11 | CLI final flush on success and representative workflow exception: called after root closure, original result/exit/error preserved; construction/setup failures before SDK existence do not require impossible flush |
| RUN-12 | Cleanup/export failure: no replacement of original workflow exception; successful computation is not mislabeled a workflow failure; bounded test without production retries |
| RUN-13 | Native span timing/parentage and current context restoration after success/error; existing parent scope is preserved rather than replaced with an invented trace ID |
| RUN-14 | Accepted PAYLOAD-01: inspect attributes, events and status; no complete context/settings serialization or configuration credentials. Do not claim native capture redacts arbitrary input secrets |
| RUN-15 | Locality and startup/import order: SDK and instrumentor share provider, only configured local telemetry target; existing CrewAI cloud telemetry remains off. Identify any framework update lookup separately and verify normal application suppression behavior |
| RUN-16 | Current dependency lock/install check and repository quality gate: Pyright, lint/format and full maintained tests; record commands/results/revision and exclude personal examples |
| RUN-17 | Installed release: relevant existing release/package checks, instrumentor dependency present, installed workflow inventory/commands work; record artifact/version/hash and environment limitations |
| RUN-18 | Local Langfuse acceptance: actual WF-01, WF-02 and both WF-03 paths visible; hierarchy, exact correlation filtering and failed-step behavior verified through UI/readback; flush alone is insufficient |
| RUN-19 | Existing CLI/Python behavior and mock/auth-check regression tests remain passing; no accidental changes to context fields, business state, factory signatures or output text |
| RUN-20 | Documentation/Atlas/link/whitespace checks; README/configuration/workflow/troubleshooting describe actual combined integration; two-reviewer reports and all RUN mappings complete |

For RUN-11, a spy may establish flush ordering, but real SDK export cases must also prove observations close. Do not write redundant tests of SDK internals; target our wiring and version-sensitive integration contracts. RUN-14 verifies the accepted default capture and mandatory configuration/credential exclusion, including automatic capture paths.

The test-gap reviewer maps each ID to exact pytest nodes and meaningful assertions, or to explicit manual acceptance evidence for RUN-18. Never classify missing/skipped/blocked/unrun as PASS. Record initial failures and valid reruns with environment changes. Required manual acceptance can remain blocked awaiting Sharon; do not claim the milestone accepted.

Follow [handover rules](../../../../governance/codex-handover-rules.md): both reviewers use one candidate, maximum three rounds, permanent reports. Review the actual coverage, not just a green total.
