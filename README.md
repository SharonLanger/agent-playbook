# Agent Playbook

A gradual Python learning project for agent orchestration. Current branch: **00.4 — pytest**.

Stages 00.1 and 00.2 are accepted and merged. 00.3–00.7 are prepared as a sequential
PR stack at the user's request; review and merge one at a time, starting at 00.3.

From repository root (macOS/Linux):

```sh
python3 app/scripts/bootstrap.py
source app/.venv/bin/activate
agent-playbook run
agent-playbook test
python -m pyright --project app/pyproject.toml
```

[App setup and checks](app/README.md) · [Progress](designs/progress.md) ·
[Design inventory](designs/README.md) · [Historical sandbox](sandbox/)

Read AGENTS.md before changes. Protected baselines remain unchanged. No GitHub
Actions CI. Adds pytest and a development-only test command; Pyright remains available. No Ruff yet.
