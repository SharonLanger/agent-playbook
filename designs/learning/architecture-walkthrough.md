# Walk through one workflow

Imagine a workflow that validates an input document, asks an agent to analyze it,
and checks that the returned result matches the expected structure. This is an
illustration of the target, not an additional feature commitment.

1. **Start:** you choose the workflow and input through the CLI or PyCharm.
2. **Prepare:** the runner validates configuration and input, creates a run ID, and
   connects the workflow to the chosen executor and observation integration.
3. **Coordinate:** CrewAI follows the definition. A Python validation step runs first.
4. **Execute:** the analysis step calls the agent execution contract. A Claude or
   Codex adapter handles its SDK's invocation and returns a structured outcome.
5. **Decide:** the workflow checks the outcome and takes its explicit next route.
   Invalid results and failed invocations follow declared failure rules.
6. **Observe:** related events form a run/step/agent trace in Langfuse.
7. **Finish:** the runner returns output and run identity, or a visible failure.

[See the execution diagram](../diagrams/02-execution.svg) or open
[the animated viewer](../diagrams/index.html) locally.

## Who makes which decision?

| Question | Owner |
|---|---|
| Which workflow/provider/configuration is selected? | Application setup and runner |
| What step runs next? | Workflow definition executed by CrewAI |
| How is a specific agent SDK called? | Its adapter |
| Which workflow state is passed onward? | Workflow execution |
| Where can I inspect what happened? | Langfuse through the observation integration |

In deterministic tests, an executor supplies fixed results or errors. The workflow
still makes its real routing decisions. This lets tests prove behavior without an
agent's nondeterministic response controlling every test.

Workflow state and an agent's conversation/session are separate. The adapter manages
session details; the workflow keeps the data it needs. Observation connects their
identities so you can understand a run afterward.

The moving dots show direction of communication. They are illustrative and do not
measure time, represent live work, or imply that all providers run simultaneously.
