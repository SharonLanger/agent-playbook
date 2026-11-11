# Stage 00 — Learning and Implementation Plan

Status: **PROPOSED / NOT APPROVED / NO IMPLEMENTATION STARTED**

## Learning approach
For an experienced Java/C#/TypeScript developer: explain Python differences only where they affect the exercise. Use short learner-facing Markdown notes, examples and hands-on failures rather than a general Python course. Store these in `learning/` as the stage proceeds; record actual observations in `findings.md`.

## Progression rule
Each substage introduces **one principal new concept or task**, building on the verified previous substage. Do not bundle several new tools into a single lesson. The bootstrap entry point is created early and extended as needed; there is always one documented setup command, not scattered manual installation steps. Every substage ends with a runnable, observable verification.

## Substages

### 0.1 — Python environment and runnable main
Introduce uv and the virtual environment. Create one bootstrap entry point, a minimal Python `main()`, and PyCharm run instructions. Verify clean and repeated setup and execution. Add Git ignores for `.venv/`, `.idea/`, caches, secrets and build artifacts. No CLI framework, test runner or typing lesson yet.

### 0.2 — Application CLI
Introduce a minimal `agent-playbook run` command invoking the existing `main()`. Extend the **same** bootstrap entry point to install/expose the CLI; verify terminal and PyCharm execution. Avoid adding a CLI framework unless needed.

### 0.3 — Pyright strict typing
Introduce Pyright strict. Use a small typed class and method exercises with Java/TypeScript comparisons. Intentionally break argument types, return types and optional handling, observe diagnostics, then restore passing checks. Explore PyCharm inspections versus Pyright independently.

### 0.4 — pytest
Introduce pytest and `agent-playbook test`. Add a deterministic passing test, introduce a regression, observe failure and restore the passing result. No Ruff yet.

### 0.5 — Ruff
Introduce Ruff lint and formatting checks. Deliberately cause and repair one lint error and one formatting failure. Keep pytest and Pyright behavior unchanged.

### 0.6 — Unified quality gate
Combine **already learned** tools into `agent-playbook check`: Pyright strict, Ruff lint, Ruff format verification and pytest. Require nonzero exit on failure. Provide one documented local check command and PyCharm invocation. No CI.

### 0.7 — Versioned Wheel release
Introduce Wheel packaging and isolated installation. Only build after checks pass. Add `agent-playbook version` for embedded version/source metadata. Record Git commit and SHA-256 hash for the built artifact; verify the hash before clean non-editable installation. Modify development source after building and show the installed release is unaffected. First verified release convention: `0.0.1`.

## Acceptance criteria
- Clean checkout can be prepared with one documented bootstrap command.
- PyCharm can run the main entry point; terminal CLI also works.
- Strict typing, lint, formatting and tests run with one check command; deliberate defects are detected.
- CrewAI is importable with no model/API credentials or network inference required.
- Release Wheel is installable in isolation and its content hash can be verified.
- Tests and commands are documented; observed evidence recorded in findings and progress.
- All relevant work conforms to approved target architecture and principles.

## Explicit exclusions
No CrewAI dependency or Flow, Langfuse tracing, Claude/Codex agent, workflow dashboard, deployment infrastructure or GitHub Actions CI.

## Approval gate
User reviews exact Stage 00 architecture and plan. After explicit approval, lock both documents and only then begin substage 0.1 implementation. Any changes to locked text require exact line-level prior approval.
