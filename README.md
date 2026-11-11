# Agent Playbook

A gradual Python learning project for agent orchestration. Current branch: **00.6 — Unified checks**.

Stages 00.1 and 00.2 are accepted and merged. 00.3–00.7 are prepared as a sequential
PR stack at the user's request; review and merge one at a time, starting at 00.3.

From repository root (macOS/Linux):

```sh
python3 app/scripts/bootstrap.py
source app/.venv/bin/activate
agent-playbook run
agent-playbook test
agent-playbook check
```

[App setup and checks](app/README.md) · [Progress](designs/progress.md) ·
[Design inventory](designs/README.md) · [Historical sandbox](sandbox/)

Read AGENTS.md before changes. Protected baselines remain unchanged. No GitHub
Actions CI. Adds one fail-fast check command: Pyright, Ruff lint, Ruff format verification, then pytest.
Numbered sections show each tool's diagnostics. The final summary distinguishes
PASS, FAIL and NOT RUN; later checks do not run after a failure.
