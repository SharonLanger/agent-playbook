# Agent Playbook

A gradual Python learning project for agent orchestration. Current branch: **00.7 — Wheel release**.

Stages 00.1–00.5 are merged. Stage 00.6 is under review; this 00.7 branch builds
on it. Review and merge one at a time after local acceptance.

From repository root (macOS/Linux):

```sh
python3 app/scripts/bootstrap.py
source app/.venv/bin/activate
agent-playbook run
agent-playbook test
agent-playbook check
agent-playbook version
python app/scripts/release.py
```

[App setup and checks](app/README.md) · [Progress](designs/progress.md) ·
[Design inventory](designs/README.md) · [Historical sandbox](sandbox/)

Read AGENTS.md before changes. Protected baselines remain unchanged. No GitHub
Actions CI. Adds an isolated versioned Wheel release after the local gate, with Git revision and SHA-256 evidence.

Check output uses numbered sections and a PASS/FAIL/NOT RUN summary.
