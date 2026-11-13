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

## Principle compliance
Before implementation and before marking a PR ready, review the applicable charter,
principles, and approved designs. Record brief evidence of compliance and raise
conflicts before proceeding. Passing tests alone does not establish compliance.

- At design time, check every principle; identify the applicable ones and explain any non-applicable items briefly.
- Before review, compare the actual changes with that assessment. In the PR description or findings, link concrete files, checks, or decisions supporting compliance.
- Resolve conflicts with the user before implementing them; a stage plan cannot silently override a project principle.
- Automate suitable checks where practical, while retaining human review for architectural and security decisions.

## Documentation retention
- Keep stage designs, plans, lessons, examples, findings and diagrams permanently under `designs/stages/<stage>/`, including during review. Follow `designs/README.md` to locate them.
- Reserve `designs/temporary/` only for disposable agent-to-agent handoffs. Preserve lasting decisions in permanent documents before deleting a handoff. Never delete stage material as part of handoff cleanup.

## Personal sandbox and official documentation

- `app/examples/` is Sharon's personal sandbox. Unless explicitly requested for a specific task, do not read, search, inspect, execute, test, lint, format, import, modify or maintain its contents. Exclude it from broad searches and application quality gates. Authorization there is limited to the requested task.
- Do not add tests to examples or make application tests depend on it. Keep maintained tests and independent fixtures in `app/tests/`. Existing exclusions/cleanup must be handled explicitly without inspecting or modifying the sandbox unasked.
- `app/docs/` is maintained official product documentation for new and existing users. Internal review notes, temporary material, handoffs and unapproved proposals belong under `designs/` with their owning stage/refactor.
- Every change requires a documentation-impact assessment. Update affected public guides, commands, configuration, examples within guides, links and indexes in the same PR when supported behavior or user-relevant architecture changes. Otherwise state a concrete no-impact reason. Keep docs consistent with approved design and verified implementation; surface conflicts rather than documenting drift.
- Follow the [architecture placement protocol](designs/refactors/atlas/architecture-placement.md): repository boundary → component → subcomponent → file, with purpose, contracts, stage authorization and documentation impact. Future Atlas boundaries remain proposals until approved.
- Detailed rationale and pending guarded-document alignment: [sandbox and documentation policy](designs/refactors/atlas/documentation-and-sandbox-policy.md). The explicit sandbox restriction supersedes older descriptions of examples as maintained/tested lessons; those descriptions await the separately reviewed alignment patch.

## Engineering
- Keep external integrations isolated behind explicit contracts/adapters. Configure provider endpoints, credentials, and environment-specific settings externally; never commit secrets.
- Prefer deterministic regression tests and strict static checking; record actual verification results, not unverified success claims.
- No GitHub Actions CI is required for now. When Stage 00 defines the local quality-check command, run it before declaring code changes ready and document it in `README.md` and `app/README.md`. Never claim tests ran if they did not.
- Keep implementation-facing plans distinct from learner-facing Markdown under stage `learning/`. Use Mermaid for static diagrams and self-contained animated SVG where movement clarifies behavior, with a static fallback. Verify rendered assets where possible.
- Do not create detailed designs for future stages ahead of their turn.

## Status
Stage 00 is accepted. Stage 01 design (#29), workflow/configuration implementation (#30), principles follow-up (#31), and independent sandboxes (#32) are merged. Sharon reported the examples working and accepted #32 after the diagram-size correction. The sandboxes live in `app/examples/workflows/` and run through their own run.py files, independently of the CLI/application runner. User-facing operating guides live in `app/docs/`; active configuration files remain in `app/configs/`. See `designs/progress.md` for verification evidence and acceptance. The next planned stage is Stage 02 (Langfuse); discuss and approve its design before implementation. Keep completed-stage learning material available. The top-level architecture remains the target system; do not infer future implementation from target diagrams.

