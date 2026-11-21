# Agent Playbook — Agent Instructions

This repository has one active design workspace in `designs/` and an executable project in `app/`. `sandbox/` holds curated historical references and draft ideas and must not be changed without a separate request.

## Mandatory design entry

For every repository task, explicitly load `designs/AGENTS.md`, `designs/governance/design-contract.md` and `designs/governance/guarded-files.md`, including work under app/. Follow their required decision flow: identify governing decisions, consult relevant explorations, explain placement, obtain required approval, maintain affected documents/Atlas and verify. A nested instruction file is not assumed to load automatically.

For stage/refactor planning and implementation handoffs, including a refactor without milestones, also read `designs/governance/stage-milestone-workflow.md` and `designs/governance/codex-handover-rules.md`. These define alignment before design, stage/refactor folders, optional refactor milestones and the bounded independent-review process. When Sharon identifies work as a refactor, create or reuse `designs/refactors/<slug>/` and follow the refactor startup procedure in the working method; do not require him to restate the convention.

## Read before working
1. Read `designs/README.md` for the document inventory.
2. Read `designs/charter.md`, `designs/architecture.md`, `designs/principles.md`, `designs/roadmap.md`, and `designs/progress.md`.
3. Read `designs/project-structure.md`; it is the guarded authority for code placement and dependency boundaries.
4. For an active stage or refactor, read its approved design and plan before implementation.
5. For diagrams and visual explanations, read `designs/diagrams/AUTHORING.md`: Dashmotion is the default; Animated SVG handles timed/narrated walkthroughs.

## Governance
- Charter, architecture and principles are guarded approved baselines. Preserve all existing guards, including approved stage material with stale proposed-status headings. New baselines require explicit approval.
- Approve a stage or refactor's overall boundary first; each milestone's concrete design/test/plan must be explicitly approved and locked **before its implementation**. Later milestone details may remain draft. A refactor without milestones approves its root design/test/plan as one work package. Follow the Stage or Refactor Design PR lifecycle in designs/governance/stage-milestone-workflow.md.
- Never change protected text without explaining the logical additions/removals and consequences for each affected guarded file and obtaining Sharon’s explicit approval beforehand; retain an inspectable diff.
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

## Engineering
- Keep external integrations isolated behind explicit contracts/adapters. The approved M4.2/M4.3 native tracing exception permits direct Langfuse scope/propagation at the application runner and setup at assembly, with concrete setup/flush functions in its adapter; it does not permit provider imports in workflow business steps or weaken agent execution adapter isolation. Configure provider endpoints, credentials, and environment-specific settings externally; never commit secrets.
- Prefer deterministic regression tests and strict static checking; record actual verification results, not unverified success claims.
- Run the local quality gate before declaring code changes ready. The approved [PR CI design](designs/refactors/pr-ci/README.md) requires the same offline checks, Atlas freshness and a clean installed-wheel check for every PR targeting public `main`. Keep hosted jobs dormant while private. Report actual run and protection evidence separately.
- Keep implementation-facing plans distinct from learner-facing Markdown under stage `learning/`. Use Mermaid for static diagrams and self-contained animated SVG where movement clarifies behavior, with a static fallback. Verify rendered assets where possible.
- Future-stage implementation designs await their stage except for the specific Stage 04 foundation exception in designs/roadmap.md; ordinary approval gates and actual dependencies remain. Explicitly requested research and POCs may be recorded under designs/explorations/ as non-binding explorations; they do not authorize implementation or replace the guarded architecture.

## Status and reconciliation

Read `designs/progress.md` for current project and stage status, and the applicable stage/refactor summaries for milestone detail. Before reporting work ready, reconcile those records, relevant design documents and Atlas with the actual implementation and PR state under the guarded design contract. Preserve dated evidence as history. The roadmap describes intended sequencing; the target architecture does not itself establish current implementation.


## Maintained boundaries

- All existing guarded documents remain guarded, including accepted historical stage documents with stale status headings. Follow the guarded-file register; omission or relocation never removes protection. The logical-change approval procedure replaces mandatory line-by-line presentation, not the approval requirement.
- `app/examples/` is Sharon’s personal sandbox. Do not read, search, inspect, run, test, lint, format, import, modify or maintain its contents without a specific request. Exclude it from broad searches and automated application gates. Application tests/fixtures belong in `app/tests/` and must not depend on examples. Explicit user-requested sandbox lint/format remains permitted outside automatic gates.
- `app/docs/` is maintained official product documentation. No internal reviews, temporary notes, handoffs or unapproved proposals belong there. Every change assesses documentation impact and updates affected public guides in the same PR, or records a concrete no-impact reason.
- Maintain `designs/atlas/` as the Current/Explorations view and `designs/explorations/README.md` as the discovery index. Existing approvals govern decisions; the viewer and research do not grant approval.
- Preserve the merged runtime split, app-root YAML and personal-sandbox exclusions. Approved historical stage baselines remain protected.

Deleting the personal examples directory must leave application behavior, collected tests and application coverage unchanged; this is an independence requirement, not an instruction to inspect or delete the sandbox. Detailed role/event/harness proposals remain exploratory.
