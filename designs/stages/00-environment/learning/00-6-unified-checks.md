# 00.6 — Unified checks

After the same bootstrap and activation, run:

```sh
agent-playbook check
```

Order: Pyright → Ruff lint → Ruff format verification → pytest. The command stops
at the first failure and returns a nonzero status. Missing developer tools are an
error, not a skipped check. Bootstrap now invokes this same command.

Repeat one earlier type, formatting or behavior mutation and see the corresponding
step fail. Undo it and rerun. No files are auto-fixed by the gate.
In PyCharm run module `agent_playbook.cli`, parameters `check`, interpreter app/.venv.
No GitHub Actions CI; this is the local gate required before release building.
