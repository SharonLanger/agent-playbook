# 00.6 — Unified checks

After the same bootstrap and activation, run:

```sh
agent-playbook check
```

Order: Pyright → Ruff lint → Ruff format verification → pytest. The command stops
at the first failure and returns a nonzero status. Missing developer tools are an
error, not a skipped check. Bootstrap now invokes this same command.

Read the numbered headings `[1/4]` through `[4/4]` to see which tool is running.
Its diagnostics appear below its heading. The final summary uses:

- **PASS**: this check ran and succeeded.
- **FAIL**: this check failed; read its diagnostics above the summary.
- **NOT RUN**: execution stopped before this check; its result is unknown.

For example, passing types and lint does not mean formatting passed. If formatting
fails, tests are NOT RUN. After fixing formatting and rerunning, tests can still
report a different problem. Ruff's own `All checks passed!` describes its lint
section only; use the final `Result:` line to judge the combined command.

Repeat one earlier type, formatting or behavior mutation and see the corresponding
step fail. Undo it and rerun. No files are auto-fixed by the gate.
In PyCharm run module `agent_playbook.cli`, parameters `check`, interpreter app/.venv.
No GitHub Actions CI; this is the local gate required before release building.
