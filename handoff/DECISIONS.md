# Decisions, Rationale and User Preferences

This is a **conversation-context snapshot** for a new Work chat. It is not a new approved design. Do not merge this PR.

## Primary objective and pedagogy
- User is an experienced backend engineer: Java, Spring Boot, C#, TypeScript and Node.js. They are not learning programming from scratch; explain Python by contrasting type systems, IDE/compiler behavior, packaging, dependency management, runtime and execution semantics.
- Learning is the primary objective. Build a working reusable application gradually, not a maximal platform quickly.
- **Exactly one principal new concept/task per substage.** Finish a small, observable experiment, then progress. The user wants to pull, inspect, execute and debug each substage personally.
- The user prefers candid technical pushback, concise explanations, explicit assumptions and evidence. Do not inflate scope or claim an experiment is a benchmark.
- For Pyright, demonstrate wrong method arguments, return values and optional values, see errors in tooling, repair and rerun. Distinguish PyCharm's native inspections from external Pyright diagnostics; Pyright editor integration should be verified rather than assumed.
- Use learner-facing Markdown separate from implementation-facing stage architecture and plan; diagrams via Mermaid and animated SVG only when useful. Document findings with observed results.

## Stage 00 choices
- **PyCharm** is the Python IDE. WebStorm was mentioned mistakenly; it is not a Stage 00 requirement.
- **uv** for Python version/environment/dependencies and a committed lockfile. **Pyright strict** for static checks; don't add mypy. **Ruff** for lint/format; **pytest** for deterministic regression tests.
- One setup script/entry point is critical: previous SOH setup was fragmented and frustrating. It must prepare Python environment, dependencies, CLI and checks as those are introduced, remain idempotent, and fail visibly. Subordinate internal helpers are acceptable; the user invokes one command.
- The **application CLI** is added in **0.2**, not 0.1. Planned commands: `agent-playbook run`, `test`, `check`, `version`, introduced one at a time. `test` and `check` are developer-oriented and should fail clearly if invoked without development tools. Build/publish need not be in the release CLI.
- Stage 00.1 only needs a runnable `main()`, the bootstrap, PyCharm setup and git hygiene. Do not add Pyright, pytest, Ruff, CLI framework, CrewAI or Langfuse yet.
- Git ignores must include `.idea/`, `.venv/`, caches, generated build outputs, local secrets; commit `pyproject.toml`, lockfile and configuration that belongs in source control.
- No GitHub Actions CI for now. Local quality gate will be introduced at 0.6.
- Avoid adapters/interfaces and elaborate package architecture until needed by real integration stages.

## Development versus release
- The user values Java/TypeScript-like build discipline and predictable deployment. Separate **development mode** (live source, PyCharm debugging) from **release mode** (installed versioned artifact).
- Python Wheels are packaging artifacts, not compiled Java-like binaries; static checks do not prevent all runtime errors.
- Release build runs quality gates first, builds a Wheel, records source commit and SHA-256 of artifact, installs in a clean non-editable environment, and executes installed code rather than source-tree imports.
- Demonstration: after building, modify source and prove that an isolated installed release retains its behavior. A version label alone does not prove artifact byte identity; independently verify SHA-256. Embedded version/commit metadata is useful but self-reporting alone is not integrity proof.
- Project-specific version convention inspired by SemVer: `MAJOR.MINOR.PATCH`; major `0` throughout learning, minor = stage number, patch = verified substage/release iteration. First Stage 00 verified release `0.0.1`; Stage 01 `0.1.0`; stable platform `1.0.0` only when separately justified. Do not publish a release for every temporary experiment.

## Technology roadmap and architectural rationale
- **CrewAI Flows** chosen as Python workflow orchestrator, partly due to green status on the company's allowed tooling list. **Not in Stage 00**; first installation and simple deterministic Flow in Stage 01.
- **Langfuse** selected for traces/observability in Stage 02. Start with useful traces, avoid duplicative dashboards and telemetry frameworks.
- Later: branching/parallelism/state and deterministic workflow tests; independently learn Claude Agent SDK/Codex SDK execution/session semantics; integrate real SDK agents behind replaceable boundaries only when justified.
- Other agent frameworks (e.g. LangGraph, Temporal, Paperclip) are not part of the approved initial plan. Do not introduce CrewAI Crews or unnecessary extra frameworks just because they exist.
- External providers, secrets, endpoints and integrations should be configurable and isolated behind explicit contracts when they actually become necessary. Local-first where useful, but not a blanket offline-only requirement for this repo.
- The user prefers TypeScript generally but chose Python for this CrewAI learning sandbox. Maintain strict type discipline.
- Open-source inventory request: user wants a stage-by-stage inventory of chosen tools, links, license, language, local execution and approval-list status where known. A dedicated `designs/tech-stack.md` was recommended in conversation, but **not confirmed created**. Treat as backlog, not Stage 00.1 scope.

## Governance and PR workflow
- Root `AGENTS.md` and `designs/` define project rules. Target architecture/charter/principles were originally proposed; do not assume they are protected unless explicitly approved. Stage 00 architecture and plan were reviewed and PR #15 merged as the agreed Stage 00 baseline.
- Each substage gets a separate branch and PR. User wants to pull and check locally before merging implementation PRs. No automatic merge without explicit approval.
- Protected approved docs require exact line-by-line proposed diff and user approval before editing. Experimental findings and progress can evolve with evidence.
- Stage process: Learn → design end-state and acceptance criteria → approve/lock → experiment → implement → verify/document. Don't pre-design distant stages in detail.
- Distinguish what has actually been executed from code that merely looks correct. Record exact verification and limitations.

## Prior System One Harness (SOH) context relevant here
- SOH was a separate hackathon/agent-harness experiment with hooks, small-model routing, token budgets and recovery. It is **not** the implementation target of this project.
- Its setup became messy and fragmented, motivating the single bootstrap command.
- Its benchmarking and failure experience motivated an evidence-first approach and avoidance of claims unsupported by observed tests.
- Old agent-playbook role/workflow experiments have been preserved in `sandbox/`; they are historical, not the current app.

## Future design interests (not Stage 00 scope)
- Understand orchestration hierarchy, agent loop, hooks, sessions, recovery, role/permission boundaries, logging and traces, deterministic workflow simulations.
- Build a genuinely useful, modular, replaceable workflow platform incrementally, with future SDK agent integration and observability.
- Strong interest in learning how agent runtime and AI platform engineering map onto established backend/distributed-systems engineering.
- The user wants each new chat to recover durable state from GitHub, not rely on inaccessible prior conversation text.
