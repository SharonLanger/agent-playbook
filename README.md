# Agent Playbook

A local-first learning project for CrewAI orchestration, Langfuse observability, and later agent runtimes.

## Where to find things

- [Design inventory](designs/README.md) — target architecture, charter, principles, roadmap, progress, and future stage learning assignments.
- [Executable Python project](app/) — created incrementally beginning with Stage 00; source code, configuration and tests will live here.
- [Historical sandbox](sandbox/) — previous experiments and original agent instructions, preserved unchanged.

## How to work

Read [AGENTS.md](AGENTS.md) before making changes. Design baselines require explicit approval before being locked or modified. Stage 00 has not been designed or implemented.

## Local checks

No GitHub Actions CI is planned for now. During Stage 00 we will define a single repeatable local quality-check command for Pyright, Ruff and pytest and document how to run it from a terminal or a PyCharm/WebStorm run configuration. **No runnable check command exists yet.**
