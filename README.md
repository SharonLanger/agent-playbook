# Agent Playbook

A gradual Python learning project for agent orchestration. Stage 00.1–00.7 are
merged. Stage 00 is accepted. Stage 01 implements three deterministic CrewAI workflows
with separate code, tests and learning guides.

Before the first run, [create the external credentials file](app/docs/configuration.md#general-secrets-file). It may be empty while integrations are disabled. Its path is already configured in `app/application.yaml`. The supplied YAML enables Langfuse; if you have not configured project keys yet, [disable it in a local override](app/docs/configuration.md#langfuse-settings) before bootstrap.

From the repository root, prepare the application:

```sh
python3 app/tooling/bootstrap.py
```

The [app setup](app/README.md) explains the environment. The optional [local Langfuse setup](app/docs/langfuse-local.md) needs Docker only for a local trace UI, not for ordinary workflows or a hosted endpoint. **All CLI commands and
release rules are in [app/docs/cli.md](app/docs/cli.md).**
[Runtime configuration](app/docs/configuration.md) covers shared YAML and environment overrides. For Langfuse project keys and the read-only authentication check, see the [Langfuse connection guide](app/docs/langfuse-connection.md).

**[Start learning Stage 01](designs/stages/01-crewai-flows/learning/00-reading-the-code.md)**

[Design inventory](designs/README.md) · [Progress](designs/progress.md)

Project layout: [guarded project structure](designs/project-structure.md).


The proposed runtime structure cleanup and completed-system file tree are documented
in the [refactor review](designs/refactors/2026-11-12-runtime-structure/README.md).

Native runner tracing uses the configured Langfuse destination. Framework events are visible by default so the pinned CrewAI integration records Flow and step observations; see [workflow tracing behavior and limits](app/docs/workflows.md#native-workflow-tracing). Local acceptance remains pending.
