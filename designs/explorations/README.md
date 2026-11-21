# Exploration topic index

These are optional research, POCs and preserved reasoning. They can be superseded or abandoned. They are neither roadmap promises nor authority to implement. Approved decisions remain in the guarded charter, principles, architecture, project structure and stage contracts. This index does not claim to contain every past chat.

| Topic / search terms | Read | Status and open question |
|---|---|---|
| Agent roles, coder, reviewer, verifier, Claude, Codex, events, normalization, capabilities | [Agent execution](agent-execution/README.md) | Exploration: contract size, native evidence, controls and role-specific handlers remain undecided |
| Logging, tracing, Langfuse, exporters, alternatives | [Observability](observability.md) · [Stage 02 milestone index](../stages/02-langfuse/README.md) · [Workflow-integration package and research](../stages/02-langfuse/workflow-integration/README.md) | Stage 02 accepted and merged via #47. M1–M3, M4.1 and combined M4.2 + M4.3 delivered. The eight-case CrewAI probe is research evidence; final application and local acceptance are in the stage records. The separate [application logging refactor](../refactors/logging/README.md) is complete. |
| Harness, tools, hooks, permissions, prompts | [Harness](harness.md) | Deferred exploration; avoid treating proposed paths as approved abstractions |

Before introducing a module, consult relevant topics and record which reasoning you reused, rejected or extended. Link new research here with its status, sources and unresolved questions. Promotion requires explicit approval and an update to the affected guarded decision; moving a file does not approve it.

The [roadmap](../roadmap.md) now places the basic shared harness/fake foundation in Stage 04 and native SDK integration in Stage 05. Advanced harness features remain optional exploration. This stage-level direction does not promote every exploratory schema or candidate folder to an approved implementation contract.
