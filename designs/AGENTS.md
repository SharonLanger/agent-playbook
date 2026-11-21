# Design workspace instructions

This file applies to work in designs. The root AGENTS.md also requires agents working elsewhere in the repository to load it explicitly.

## MUST read before work

Read [governance/design-contract.md](governance/design-contract.md), [governance/guarded-files.md](governance/guarded-files.md), [README.md](README.md), [charter.md](charter.md), [principles.md](principles.md), [architecture.md](architecture.md), [project-structure.md](project-structure.md), [roadmap.md](roadmap.md) and [progress.md](progress.md). Then read the applicable approved stage baseline and consult relevant topics in [explorations/README.md](explorations/README.md). Reuse already-loaded unchanged revisions within a task; never assume unavailable handoff context contains the rules.

For each stage/refactor design and implementation handoff, including refactors without milestones, read [stage-milestone-workflow.md](governance/stage-milestone-workflow.md) and [codex-handover-rules.md](governance/codex-handover-rules.md). When Sharon calls work a refactor, create or reuse `refactors/<slug>/` under the working method. Keep shared requirements/decisions/history at its root. Put design/test/plan/reviews at that root for one bounded package, or in milestone folders when the scope needs milestones. Create research/learning only when useful material exists; do not invent empty milestones. Verify alignment before drafting and before handoff.

## MUST follow

Identify governing decisions → consult relevant explorations → explain placement → obtain required guarded-change approval → work within scope → update affected design/Atlas/public documentation → verify and record evidence. Follow the contract's required decision record; this is a constraint, not optional advice.

Keep every existing guard, including historical stage baselines with stale headings. Logical changes to guarded files need Sharon's explicit approval before editing. Record its scope. Do not ask again for changes already authorized in the active session; do not expand that authorization to unrelated decisions.

Explorations preserve useful reasoning and alternatives; they are not a roadmap, approved target or implementation instruction. Do not infer adoption from their presence in the Atlas. Approved design remains in the guarded authorities. Do not copy chat claims into progress as verified behavior.

Keep the permanent viewer under atlas/, optional research under explorations/, procedural authorities under governance/, stage material under stages/, and independent refactor designs, requirements, decisions, learning/research and review history under refactors/. Internal or temporary material never belongs in app/docs/. app/examples/ is an excluded personal sandbox: no unrequested access or maintenance.

For new or changed diagrams read diagrams/AUTHORING.md. Maintain Atlas Current/Explorations status, links and generated output. Preserve protected architecture semantics when revising visuals. Run `python3 designs/atlas/build.py --check` and appropriate link/diagram checks after relevant documentation changes. This does not replace application validation when application behavior changes.

Use [progress.md](progress.md) for current stage status and the relevant stage/refactor summaries for milestone detail. Before declaring work ready, reconcile their claims, affected design documents and Atlas against the default branch and actual PR state. Keep earlier evidence clearly historical, and distinguish implemented, verified, accepted and merged.

Use `[Stage XX Design] <stage name>` for the ongoing draft documentation PR and `[Stage XX · MYY] <milestone outcome>` for implementation PRs. Follow the lifecycle and explicit stage-PR merge gate in [stage-milestone-workflow.md](governance/stage-milestone-workflow.md#stage-design-pr-lifecycle). Sequencing is owned by [roadmap.md](roadmap.md#sequencing-and-approval); Stage 04 is the only early-foundation exception.

For independent refactors use `[Refactor Design] <name>` and `[Refactor <name> · M<number>] <outcome>` for milestone implementation; without milestones use `[Refactor <name>] <outcome>`. The Refactor Design PR has the same keep-open, closeout and explicit merge gate. Refactors have no stage number or automatic stage-sequencing dependency, but must respect real dependencies and guarded scope. Existing active workspaces retain their paths and contracts.
