# Stage 03 requirements

The approved Stage 03 requirements below retain their wording and protection from the [source stage README at `a8d71539`](https://github.com/SharonLanger/agent-playbook/blob/a8d7153965f1006fa0ce8d79697ac21a98e4dfc6/designs/stages/03-orchestration-patterns/README.md#requirements-and-current-scope), including the later R11 cleanup decision. The [stage index](README.md) records acceptance and merge state. The [decision log](decisions.md) retains rationale and superseded choices.

| ID | Requirement | Authority / status |
|---|---|---|
| S03-R01 | A bounded collection of eight useful, permanent, copyable recipes C01–C08. | Batch accepted in U09 |
| S03-R02 | Map existing coverage first. Reuse prior examples, while allowing an existing concept to be composed into a practical recipe. | User clarification; revision-loop recipe explicitly requested |
| S03-R03 | Check the CrewAI behavior being taught using example output and focused temporary verification where useful. No application or trace integration acceptance. | User clarification supersedes the initial application/tracing interpretation |
| S03-R04 | CrewAI remains scheduler and Flow state owner. Label ordinary Python logic honestly; do not invent a new orchestration framework. | Existing architecture; scoped to standalone examples |
| S03-R05 | Logging is separate and not a prerequisite. | Agreed |
| S03-R06 | No real agents, production recovery framework, human approval service or distributed worker platform. Retry/fallback recovery is deferred. | Roadmap boundary and user scope |
| S03-R07 | Agree and implement a complete batch together in one implementation PR, not a separate implementation cycle per recipe. Keep the ongoing Stage Design PR separate and draft/open. | User batch instruction; existing Stage Design lifecycle |
| S03-R08 | Preserve decisions, rationale, sources and pending choices. | Agreed |
| S03-R09 | Organize app/examples/workflows into concepts/ for existing examples and recipes/ for practical compositions. | Explicitly accepted; merged through PR #53 |
| S03-R10 | Each new recipe contains README.md, flow.py, run.py and input.json. README is the learning guide. | Explicitly accepted |
| S03-R11 | No permanent new test files. Retain the eight temporary verify.py scripts through implementation merge; remove them during Stage 03 closeout before marking the stage done and merging design PR #52. Preserve evidence. | U10 / S03-D26 supersedes the original cleanup timing |
| S03-R12 | Direct PyCharm run.py execution and copying a whole recipe folder are primary uses. No imports from another example or application runtime are needed. | Agreed independence goal |

Existing tests in the older concepts are not authorized for deletion by R11; that instruction concerns new recipes and temporary checks.
