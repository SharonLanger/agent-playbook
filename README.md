# Agent Playbook

A local-first learning project for CrewAI orchestration, Langfuse observability,
and later agent runtimes.

## Where to find things

- [Design inventory](designs/README.md) — target architecture, charter, principles and roadmap.
- [Executable Python project](app/README.md) — Stage 00.1 setup and PyCharm instructions.
- [Progress](designs/progress.md) — current state and remaining validation.
- [Historical sandbox](sandbox/) — previous experiments, preserved unchanged.

## Try Stage 00.1

Requires Python 3.10+ with venv/ensurepip. From the repository root:

```sh
python3 app/scripts/bootstrap.py
app/.venv/bin/python app/src/agent_playbook/__main__.py
```

The first command prepares the environment and runs a sanity check. The second
runs main independently. Windows commands and PyCharm setup are in
[app/README.md](app/README.md).

## How to work

Read [AGENTS.md](AGENTS.md) before making changes. Protected baseline changes
require explicit approval. Stage 00.1 is implemented for review; user acceptance
and merge are pending. No later substage is implemented.

## Local checks

Stage 00.1 uses bootstrap and independent execution as smoke checks. Pyright,
pytest and Ruff arrive in later substages; the unified check command arrives in
00.6. No GitHub Actions CI or application CLI exists yet.
