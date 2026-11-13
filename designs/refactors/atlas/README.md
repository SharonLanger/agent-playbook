# PR #35 — Atlas and design-governance change record

Status: logical scope explicitly approved by Sharon on 13 November 2026; implementation in this draft PR awaits merge review. Do not merge automatically. The permanent viewer is now [designs/atlas](../../atlas/README.md); optional reasoning lives in [explorations](../../explorations/README.md). Earlier proposal patches are superseded by these approved edits, not retained as competing instructions.

## Approved logical changes per guarded file

| Guarded file | Addition/change | Removal or consequence |
|---|---|---|
| charter.md | Maintained official documentation and Atlas; personal-sandbox boundary; requested research kept non-binding | Replaces blanket future-document prohibition with explicitly requested exploration; purpose/stage scope and approved initial integrations preserved |
| principles.md | Mandatory discovery/placement/maintenance; honest statuses; docs and sandbox ownership | Logical per-file approval replaces mandatory line-by-line presentation; explicit approval still required |
| architecture.md | Clearly labels approved target; links current implementation evidence and optional agent/event ideas | Does not adopt candidate role/event/harness layouts; Langfuse remains approved initial tracing |
| project-structure.md | Permanent governance/Atlas/explorations ownership; correct docs/tests/sandbox boundaries; current-versus-pending #34 paths | Removes maintained examples-test ownership; does not pretend #34 is merged or promote future runtime folders |
| governance/design-contract.md (new) | Guarded mandatory seven-step flow, authority, approval and maintenance rules | No agent self-approval; applies across repository via root instructions |
| governance/guarded-files.md (new) | Minimum protection register, including historical Stage 00/01 and catch-all for other approved content | Omission, moves, generated summaries and stale headings cannot remove existing guards |

All previously guarded files stay guarded. Stage designs/contracts are not rewritten. Sharon approved logical changes, not a mandatory line-by-line presentation; reviewable diffs remain. Approval of this process does not approve implementation of reviewer/event/harness explorations.

## Supporting changes

Root AGENTS explicitly requires designs/AGENTS and the guarded contract for work anywhere in the repository. The nested instructions list the required reading and flow. This is a mandatory repository constraint, not a claim that every client automatically loads nested instructions. Progress records approval, revision-specific evidence and pending integration; roadmap retains stage sequence; the designs index provides discovery.

The permanent offline Atlas has Current/Explorations views, architecture zoom levels, a candidate reviewer walkthrough, source references and searchable file trees. A standard-library builder checks references/hierarchy/guards and generated freshness. Detailed prior research is indexed under explorations with status and unresolved questions.

Public documentation removes sandbox-specific guides/index entries and states the maintained product-doc boundary. Product commands are unchanged. Internal `app/docs/refactor-review.md` exists only in pending PR #34; move it to its owning designs/refactors folder during coordination rather than inventing or deleting a file absent from this base.

## Integration with #34

Main runtime snapshot remains `6f16508`; #34 head `59c6fff` is open and its latest sandbox isolation follow-up is unverified. Keep this PR's governance and documentation changes when resolving overlap. After #34 merges, refresh project structure, progress, catalog/current paths and affected public docs together. Do not restore personal-sandbox dependencies or use older verification to certify the new head.

[Verification](verification.md)
