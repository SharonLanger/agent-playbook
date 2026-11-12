# Agent Playbook — Agent Instructions

This repository has one active design workspace in `designs/` and an executable project in `app/`. `sandbox/` contains historical experiments and must not be changed without a separate request.

## Read before working
1. Read `designs/README.md` for the document inventory.
2. Read `designs/charter.md`, `designs/architecture.md`, `designs/principles.md`, `designs/roadmap.md`, and `designs/progress.md`.
3. Read `designs/project-structure.md`; it is the guarded authority for code placement and dependency boundaries.
4. For an active stage, read its approved architecture and plan before implementation.
5. For diagrams and visual explanations, read `designs/diagrams/AUTHORING.md`: Dashmotion is the default; Animated SVG handles timed/narrated walkthroughs.

## Governance
- Charter, target architecture, and principles are proposed baselines until explicitly approved. Once approved, they are protected.
- Each current stage's architecture and committed design must be explicitly approved and locked **before** implementation.
- Never change protected text without presenting **each exact added, edited, or deleted line** and obtaining explicit user approval beforehand.
- Stop when a proposed implementation contradicts the target or locked stage design. Experiments may explore alternatives without silently changing baselines.
- Progress, learning explanations, and findings may evolve with verified evidence. Distinguish hypotheses from observations.

- The approved project structure is protected. Follow its change rules before moving component boundaries.

## Documentation retention
- Keep stage designs, plans, lessons, examples, findings and diagrams permanently under `designs/stages/<stage>/`, including during review. Follow `designs/README.md` to locate them.
- Reserve `designs/temporary/` only for disposable agent-to-agent handoffs. Preserve lasting decisions in permanent documents before deleting a handoff. Never delete stage material as part of handoff cleanup.

## Engineering
- Keep external integrations isolated behind explicit contracts/adapters. Configure provider endpoints, credentials, and environment-specific settings externally; never commit secrets.
- Prefer deterministic regression tests and strict static checking; record actual verification results, not unverified success claims.
- No GitHub Actions CI is required for now. When Stage 00 defines the local quality-check command, run it before declaring code changes ready and document it in `README.md` and `app/README.md`. Never claim tests ran if they did not.
- Keep implementation-facing plans distinct from learner-facing Markdown under stage `learning/`. Use Mermaid for static diagrams and self-contained animated SVG where movement clarifies behavior, with a static fallback. Verify rendered assets where possible.
- Do not create detailed designs for future stages ahead of their turn.

## Status
Stage 00 has been accepted by the user. The approved structure refactor prepares for Stage 01; Stage 01 behavior still requires its own approved design. See `designs/progress.md` for current acceptance and open PRs. The top-level architecture describes the target system; stage architectures describe incremental end states. Review architecture changes through their PR; do not infer implementation completion from target diagrams.
