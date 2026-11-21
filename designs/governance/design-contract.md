# Design contract

**Status: GUARDED — approved by Sharon on 2026-11-13 and merged through PR #35.** This contract governs documentation and design changes. Approval of this contract does not authorize implementation of exploratory designs.

## Current status and reconciliation

`designs/progress.md` owns the current project status. Stage/refactor summaries own work-package and milestone detail; findings retain dated evidence; the roadmap owns intended sequencing. Agent instructions link to these records instead of duplicating detailed progress.

Before reporting work ready, check the affected progress summary, stage/refactor summaries, design documents and Atlas against the actual implementation and PR state. Replace superseded current-status statements. Preserve earlier evidence in clearly labeled historical sections.

Record implementation, verification, user acceptance and merge status separately. Identify the branch or revision for unmerged work. Stage completion requires recorded user acceptance.

After performing a merge, or when asked to reconcile a user-performed merge, inspect the resulting default branch and update affected status records. Never describe an anticipated merge as completed.

Update canonical documents before rebuilding Atlas. Run its existing freshness and reference checks, and review the meaning of its status labels. Report any unresolved inconsistency.

## Mandatory entry procedure

Every agent doing repository work MUST follow this procedure. The root AGENTS.md explicitly requires this file and designs/AGENTS.md even when working outside designs. Do not assume a client automatically discovers nested instruction files.

Before editing, read the root instructions, designs/AGENTS.md, this contract, the guarded-file register, designs/README.md, charter.md, principles.md, architecture.md, project-structure.md, roadmap.md and progress.md. Then read the active stage or refactor's approved design and the relevant entries in explorations/README.md. Follow topic links only when relevant; do not bulk-load unrelated research. Reuse documents already read at the same revision in the current task; refresh when the branch or governing files change and after a handoff when their contents are unavailable.

Never inspect app/examples/ as part of this procedure. It is Sharon's personal sandbox and is excluded unless explicitly requested for the specific task.

## Required decision flow

1. **Identify governing decisions.** State the objective, applicable approved boundaries/principles and active-stage authorization. Check actual branch status and progress; an open PR is not merged implementation.
2. **Consult relevant explorations.** Check the topic index for prior reasoning, alternatives and unresolved questions. An exploration may be rejected, superseded or unused; it never overrides an approved decision.
3. **Explain placement.** Follow repository → component → subcomponent → file. Identify responsibility, inputs/outputs, dependencies and failure ownership. A reusable responsibility may warrant a block; ordinary helper functions usually do not.
4. **Check authority.** If the change alters guarded meaning, explain each affected file's logical additions/removals, consequences and risks, then obtain Sharon's explicit approval before editing. Existing session approval authorizes only its stated scope. Approval to explore is not approval to adopt or implement.
5. **Implement within scope.** Resolve conflicts rather than silently choosing a different architecture. Keep application work independent of the personal examples sandbox.
6. **Maintain the record.** Update affected canonical design, Atlas metadata/views, public documentation and progress in the same PR. Record a concrete no-impact reason for each surface that does not need changes. Preserve historical verification evidence and attach new evidence to its revision.
7. **Verify and report.** Run appropriate checks, report actual results and limitations, and distinguish implemented, verified, accepted and merged states.

For read-only advice, perform the relevant reading and reasoning; no write or manufactured documentation change is required. For routine changes within an established boundary, the decision record can be a short paragraph. A new boundary requires a fuller explanation. Do not ask again for approval already given for the same scope.

## Authority and status

| Source | Authority |
|---|---|
| Charter | Purpose and approved scope |
| Principles and this contract | Mandatory engineering and change process |
| Architecture | Approved component responsibilities and relationships |
| Project structure | Approved ownership and placement rules |
| Approved active-stage/refactor designs | Workstream-specific contracts and implementation scope; refactor root packages and milestones have equal protection |
| Roadmap | Provisional sequencing; does not itself approve implementation |
| Progress and findings | Revision-specific evidence and acceptance history |
| Explorations | Non-binding research, alternatives, POCs and discussion notes |
| Atlas | Maintained visual/index projection; no independent approval authority |
| app/docs | Official documentation of supported behavior, aligned with approved design and verified implementation |

Record three distinct concepts: **implemented** (and its evidence), **approved design** (which may await implementation), and **exploration** (not a commitment). Pending PR code must carry its branch/revision and verification status. Do not promote it to Current merely because it exists in a branch. Conflicts between design and behavior must be surfaced; neither undocumented implementation drift nor an old document silently wins.

## Guard preservation and approval

All existing guarded files stay guarded, including accepted historical stages with stale status labels. See guarded-files.md. Protection follows approved content through renames, moves, splits, merges and generated views; moving it to explorations does not revoke approval or protection.

Sharon approves **logical changes per guarded file**: what is added, removed or changed and the consequences. Line-by-line presentation is no longer mandatory; an inspectable diff remains available. Explicit approval is required before editing guarded meaning, removing guard status or changing this process. Historical line-level wording does not unguard historical files; this approved process supersedes that presentation requirement. No agent can grant itself approval.

New approved stage and refactor baselines, with or without milestones, become guarded and must be registered. The register is not an escape hatch: an approved/locked file remains guarded even if accidentally omitted. When evidence of protection is ambiguous, preserve the file and resolve its status before changing it.

## Personal sandbox and official documentation

app/examples/ is Sharon's personal sandbox. Unless specifically requested, agents MUST NOT read, search, inspect, run, test, lint, format, import, edit or maintain its contents. Exclude it from broad searches. Automated tests, coverage, quality gates, setup and release inputs must not depend on it. Maintained application tests and independent fixtures live in app/tests/. Explicit user-requested sandbox lint/format is permitted outside automated gates; this does not authorize routine sandbox inspection or maintenance.

app/docs/ MUST contain maintained official product documentation for new and existing users. Internal refactor reviews, temporary notes, handoffs and unapproved proposals belong in designs with their owner. Every change requires a documentation-impact assessment. Changes to supported commands, defaults, configuration, installation, workflows, outputs/errors or user-relevant architecture require matching guide/index/link updates in the same PR. Purely internal changes can state a specific no-impact reason. Link to canonical definitions rather than creating competing authoritative copies.

## Atlas maintenance and checks

Maintain designs/atlas/catalog.json and its referenced documents; rebuild index.html with build.py whenever relevant ownership, status, links or scenarios change. Current and Explorations are separate views. Scenario walkthroughs such as reviewer runs must carry their status. Consult the guarded Markdown first; the catalog stores navigation and concise summaries, not competing decisions.

The builder checks hierarchy, references, statuses, sandbox boundaries and generated-output freshness without traversing the sandbox. These checks do not prove that an agent read a document, that prose is accurate or that a design was approved. Review must inspect the decision record and approval evidence. The approved [PR CI workflow](../refactors/pr-ci/README.md) runs this same Atlas check on PRs targeting public `main`.

## Required PR record

- Governing documents and relevant decisions; exploration topics consulted or a reason none apply.
- Placement and contracts; stage/scope authorization.
- Guarded changes and the user approval covering them.
- Design, Atlas and public-documentation impact, including justified no-impact cases.
- Checks, observed results, limitations and the exact revision where relevant.

## Stage boundaries and milestone approval

Approve the stage's overall goal, boundaries and dependencies first. Detailed milestones may then be designed and approved incrementally: only the milestone whose design, test cases and implementation plan are explicitly approved at a pinned revision may be implemented under the relevant authorization. Approval of the stage or one milestone does not approve later milestone contracts. Preserve existing locked contracts.

The [roadmap](../roadmap.md#sequencing-and-approval) defines the sole Stage 04 early-foundation exception; it changes sequencing, not these gates. The [stage working method](stage-milestone-workflow.md#stage-design-pr-lifecycle) defines the ongoing Stage Design PR and its separate explicit merge authorization. The [Codex handover rules](codex-handover-rules.md) govern delegated implementation and the frozen handoff window.

## Refactor applicability

When Sharon identifies work as a refactor, apply the [independent-refactor method](stage-milestone-workflow.md#independent-refactors): create or reuse its permanent folder, shared requirements and decisions, and scope-appropriate design/test/plan package. Research and learning are added when needed; milestones are optional, approval and review gates are not. A root package follows the same pinned approval and freeze as a milestone. Refactors are independent of stage numbering but cannot bypass actual dependencies, guarded contracts or stage-owned scope. The Refactor Design PR remains draft/open until its own closeout and explicit merge authorization.
