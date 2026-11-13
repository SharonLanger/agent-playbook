# User documentation

This is the maintained official product documentation for new and existing users. Start here to run or configure Agent Playbook. Internal reviews, handoffs and temporary proposals belong in designs. Changes to supported behavior or user-relevant architecture must update affected guides, navigation and links in the same PR.

| Guide | What you will learn |
|---|---|
| [CLI and releases](cli.md) | Commands, source versus installed runs, checks, formatting, version changes and releases |
| [Configuration](configuration.md) | Which settings file is loaded, local/environment overrides, CrewAI controls, secrets and PyCharm examples |
| [Running workflows](workflows.md) | Choose supported integrated workflows, provide input and read results |
| [Troubleshooting](troubleshooting.md) | Resolve interpreter, configuration, workflow, check and release problems |

## Setup and learning

- [Application setup](../README.md): bootstrap and the project interpreter.
- [Stage 01 learning guide](../../designs/stages/01-crewai-flows/learning/00-reading-the-code.md): understand the integrated workflows and read their code.
- [Target architecture](../../designs/architecture.md) and [current progress](../../designs/progress.md): distinguish the intended system from what is implemented.

The shared file is `app/application.yaml`; its user guide is here.
Component ownership notes stay beside source code, and detailed stage lessons stay with
their stage. This index links them rather than duplicating the same explanation.


Configured workflow IDs and defaults are documented in [configuration](configuration.md#configured-workflows); lifecycle errors are covered in [troubleshooting](troubleshooting.md#workflow-selection-or-phase-failure).
