# Agent Playbook — Work Chat Handoff

> **TEMPORARY CONTEXT TRANSFER. DO NOT MERGE THIS PR.** Read these files, use them as context, and then close the PR when the handoff is complete. The contents are a snapshot, not an implementation proposal or a replacement for the authoritative documents on `main`.

## Receiving agent: first actions
1. Read **this entire file**, then `handoff/DECISIONS.md`, then `handoff/HISTORY.md`. They are all part of this PR's branch, not `main`.
2. Read the actual authoritative repository files from `main`: `AGENTS.md`, `designs/README.md`, `designs/charter.md`, `designs/principles.md`, `designs/architecture.md`, `designs/roadmap.md`, `designs/progress.md`, `designs/stages/00-environment/architecture.md`, `designs/stages/00-environment/plan.md`, and `designs/stages/00-environment/findings.md`.
3. Inspect the **live** `stage/00-1-python-environment` branch and compare it to `main`. Do not assume files mentioned in an interrupted write exist.
4. Continue **only Stage 00.1** on its existing branch. Implement, inspect and verify the single bootstrap command, Python environment, runnable main, PyCharm instructions, Git ignores and basic reproducibility. Create a separate implementation PR for user review. **Do not merge that implementation PR without explicit user approval.**
5. Explain how the user can pull the branch, open it in PyCharm, run the bootstrap, and execute `main()`. Report actual tests executed versus unverified items.
6. **Do not merge this handoff PR.** Once the receiving agent has loaded these documents, the user can close it. It is not an architectural change request.

## Current state (snapshot at handoff)
- Repository: `SharonLanger/agent-playbook` (private).
- `main` after design PR #15: `7662a8488aee978d7536802fac76eb6413ee49ea`.
- PR #8: merged after relocating its three draft feature designs into `sandbox/`.
- PR #13: merged initial repo foundation and historical-content move to `sandbox/`.
- PR #14: merged simplified root structure (`designs/`, root `AGENTS.md`, historical `sandbox/`).
- PR #15: merged Stage 00 architecture and plan. These are the approved stage baseline; do not silently change them.
- Stage 00.1 branch **exists**: `stage/00-1-python-environment`. At handoff inspection it contained **only three new app files**: `app/.python-version`, `app/.gitignore`, `app/pyproject.toml`. The previous agent's batch of file-creation operations was interrupted; other intended files were **not verified present**. There is no confirmed Stage 00.1 implementation PR or successful setup execution.
- This handoff branch is intentionally independent of the implementation branch.

## What we're building
A gradual, hands-on Python learning environment for agent orchestration, built with engineering rigor and a single setup entry point. Current stage is a foundation, **not** an agent workflow. Eventually CrewAI Flows will orchestrate workflows, Langfuse will provide observability, and later real agent SDKs may be integrated.

## Stage 00 scope — one new concept per substage
- **0.1**: Python environment + uv, one bootstrap entry point, runnable `main()`, PyCharm, `.gitignore`.
- **0.2**: Minimal `agent-playbook run` CLI; extend same bootstrap to expose it.
- **0.3**: Pyright strict, typing experiments.
- **0.4**: pytest and `agent-playbook test`.
- **0.5**: Ruff lint and format.
- **0.6**: Unified `agent-playbook check` gate.
- **0.7**: Build Wheel, install isolated release, `agent-playbook version`, Git revision and SHA-256 evidence.
- **Stage 01**: first CrewAI Flow, including its installation. **No CrewAI dependency in Stage 00**.
- **Stage 02**: Langfuse tracing.
- Future stages: advanced workflows, agent SDKs, integration, exploratory expansion. Only current stage gets detailed design.

## Important operating rules
- One branch and PR **per substage**, based on latest `main`.
- No implementation until the relevant approved stage design is respected; no unapproved edits to protected baselines.
- One user-facing bootstrap command to install/configure **everything needed so far**. No fragmented manual setup.
- No GitHub Actions CI. Local reproducible quality checks when introduced.
- Historical `sandbox/` must not be modified.
- Don't pre-install future-stage tools or introduce premature abstractions.
- Never claim tests or installs passed unless actually executed.

## Handoff versus authority
This handoff records conversation intent and observed state. The receiving agent must use repository documents and live GitHub state as the authoritative source for implementation, and flag any contradictions. This PR is temporary and **must not be merged**.
