# Provisional Learning Roadmap

Status: **DRAFT — flexible; no stage designs approved**

| Stage | Focus | Expected learning outcome |
|---|---|---|
| 00 | Development environment | Python tooling, strict checking, reproducible tests and sanity checks; design later |
| 01 | CrewAI Flows | Define and execute deterministic workflows; explore routing/state and non-happy paths |
| 02 | Langfuse | Trace workflow runs, inspect events, errors and execution hierarchy |
| 03 | Advanced orchestration | Branching, parallel steps, state, and increasingly complex deterministic scenarios |
| 04 | Agent execution | Study one real agent's SDK, session and lifecycle independently |
| 05 | Agent integration | Invoke real agents through CrewAI workflow boundaries |
| 06+ | Open exploration | Future harness engineering, reusable configuration, monitoring and other directions |

## Stage protocol
1. Learn enough to propose the current stage.
2. Draft the stage's end-state architecture, interfaces, acceptance criteria and plan.
3. Review with user; obtain explicit approval and lock the stage baseline.
4. Experiment and implement within approved boundaries; log findings.
5. Verify against deterministic tests and stage acceptance criteria; close only with evidence.

Future stage descriptions are intentionally high level. Split, merge or reorder through deliberate roadmap review. A stage architecture is **not** created before the stage becomes current.
