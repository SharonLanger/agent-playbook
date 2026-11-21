# Workflows

This package contains the shared application-facing workflow contract and three
implemented CrewAI workflows.

| Location | Responsibility |
|---|---|
| `contracts.py` | Workflow ABC: prepare, execute, validate output and serialize output |
| `lifecycle.py` | Per-attempt status, phase and failure records |
| `errors.py` | Workflow error types |
| `wf_01_step_sequence/` | Pass a string through sequential steps |
| `wf_02_shared_state/` | Update typed state through arithmetic steps |
| `wf_03_conditional_route/` | Select a score-based branch |

Each workflow owns its `workflow.py` wrapper, `flow.py` and `steps.py`, with
`state.py` and `config.py` where needed. CrewAI owns step orchestration; the
wrapper implements the shared lifecycle and input/output contract. The shared
application registry and factory select and construct the configured workflow.
Agent SDK clients belong in execution adapters, outside workflow business steps.

For commands and inputs, see [Running workflows](../../../docs/workflows.md).
For regression coverage, see [workflow tests](../../../tests/workflows/README.md).
The accepted design and learning sequence are in
[Stage 01](../../../../designs/stages/01-crewai-flows/README.md).

Follow [the guarded project structure](../../../../designs/project-structure.md).
