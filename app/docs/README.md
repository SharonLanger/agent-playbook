# User documentation

This is the maintained official product documentation for new and existing users. Start here to run or configure Agent Playbook. Internal reviews, handoffs and temporary proposals belong in designs. Changes to supported behavior or user-relevant architecture must update affected guides, navigation and links in the same PR.

| Guide | What you will learn |
|---|---|
| [CLI and releases](cli.md) | Commands, local service management, source versus installed runs, checks and releases |
| [Configuration](configuration.md) | Which settings file is loaded, local/environment overrides, external secrets files, CrewAI controls and PyCharm examples |
| [Application logging](logging.md) | Configure local OTLP diagnostics, use context helpers and explicitly check service health |
| [Langfuse connection](langfuse-connection.md) | Store project keys outside the repository and explicitly check project authentication |
| [Langfuse hands-on](langfuse-hands-on.md) | Authenticate, run synthetic traces, inspect steps and verify local persistence |
| [Running workflows](workflows.md) | Choose supported integrated workflows, provide input, read results and understand native tracing limits |
| [Troubleshooting](troubleshooting.md) | Resolve interpreter, configuration, workflow, check and release problems |
| [Local Langfuse UI](langfuse-local.md) | Install Docker, start and troubleshoot the optional self-hosted service |
| [Mock trace playground](../examples/langfuse/README.md) | Explicitly send editable synthetic arithmetic runs and inspect them in the UI |

## Setup and learning

- [Application setup](../README.md): bootstrap and the project interpreter.
- [Stage 01 learning guide](../../designs/stages/01-crewai-flows/learning/00-reading-the-code.md): understand the integrated workflows and read their code.
- [Target architecture](../../designs/architecture.md) and [current progress](../../designs/progress.md): distinguish the intended system from what is implemented.

The shared file is `app/application.yaml`; its user guide is here.
Component ownership notes stay beside source code, and detailed stage lessons stay with
their stage. This index links them rather than duplicating the same explanation.


Configured workflow IDs and defaults are documented in [configuration](configuration.md#configured-workflows); lifecycle errors are covered in [troubleshooting](troubleshooting.md#workflow-selection-or-phase-failure).
