# Stage 00 — Learning and Implementation Plan

Status: **PROPOSED / NOT APPROVED / NO IMPLEMENTATION STARTED**

## Learning approach
For an experienced Java/C#/TypeScript developer: explain Python differences only where they affect the exercise. Use short learner-facing Markdown notes, examples and hands-on failures rather than a general Python course. Store these in `learning/` as the stage proceeds; record actual observations in `findings.md`.

## Substages

### 0.1 — One-command environment and runnable application
Learn just enough about Python, virtual environments, uv, package installation, `pyproject.toml` and PyCharm execution. Create one bootstrap entry point that sets up the entire environment, installs the CLI and dependencies, and verifies readiness. Provide a deterministic `main()` reachable via `agent-playbook run`. Verify repeated setup succeeds. Ignore `.idea/`, `.venv/`, caches, secrets and build artifacts.

### 0.2 — Strong static typing
Configure Pyright strict. Create a small typed class with methods and tests that make Java/TypeScript parallels clear. Intentionally introduce incorrect argument types, return types and optional-value misuse; verify type checking fails and restoring correct code passes. Show PyCharm inspections and the independent Pyright command.

### 0.3 — Deterministic testing and quality gate
Add pytest and Ruff. Exercise a passing test, deliberate regression, lint violation and formatting failure. Implement `agent-playbook test` and `agent-playbook check`, with the latter running Pyright strict, Ruff lint, Ruff format verification and pytest. Fail fast with nonzero exit status. Provide a single repeatable local check entry point, with PyCharm run instructions. No CI.

### 0.4 — CrewAI dependency sanity
Add a compatible, pinned CrewAI dependency and verify imports/version without an LLM request or a workflow. Re-run all checks. Do not add agent orchestration behavior yet.

### 0.5 — Versioned build and isolated release
Build a Wheel only after the quality gate passes. Install into a clean, non-editable environment and execute `agent-playbook run` and `agent-playbook version`. Record release version, Git commit and SHA-256 artifact hash. Modify development source after building and demonstrate that the isolated installed artifact still exhibits its original behavior. First verified release convention: `0.0.1`.

## Acceptance criteria
- Clean checkout can be prepared with one documented bootstrap command.
- PyCharm can run the main entry point; terminal CLI also works.
- Strict typing, lint, formatting and tests run with one check command; deliberate defects are detected.
- CrewAI is importable with no model/API credentials or network inference required.
- Release Wheel is installable in isolation and its content hash can be verified.
- Tests and commands are documented; observed evidence recorded in findings and progress.
- All relevant work conforms to approved target architecture and principles.

## Explicit exclusions
No real CrewAI Flow, Langfuse tracing, Claude/Codex agent, workflow dashboard, deployment infrastructure or GitHub Actions CI.

## Approval gate
User reviews exact Stage 00 architecture and plan. After explicit approval, lock both documents and only then begin substage 0.1 implementation. Any changes to locked text require exact line-level prior approval.
