# PR #35 — Atlas and design-governance change record

Status: logical scope explicitly approved by Sharon on 13 November 2026; [PR #35](https://github.com/SharonLanger/agent-playbook/pull/35) is merged. The permanent viewer is [designs/atlas](../../atlas/README.md); optional reasoning lives in [explorations](../../explorations/README.md). The sections below retain the approved change record and integration checkpoint for PR #35. Earlier proposal patches are superseded by those approved edits, not retained as competing instructions.

## Approved logical changes per guarded file

| Guarded file | Addition/change | Removal or consequence |
|---|---|---|
| charter.md | Maintained official documentation and Atlas; personal-sandbox boundary; requested research kept non-binding | Replaces blanket future-document prohibition with explicitly requested exploration; purpose/stage scope and approved initial integrations preserved |
| principles.md | Mandatory discovery/placement/maintenance; honest statuses; docs and sandbox ownership | Logical per-file approval replaces mandatory line-by-line presentation; explicit approval still required |
| architecture.md | Clearly labels approved target; links current implementation evidence and optional agent/event ideas | Does not adopt candidate role/event/harness layouts; Langfuse remains approved initial tracing |
| project-structure.md | Permanent governance/Atlas/explorations ownership; correct docs/tests/sandbox boundaries; accepted #34 paths | Removes maintained examples-test ownership; records #34 as merged or promote future runtime folders |
| governance/design-contract.md (new) | Guarded mandatory seven-step flow, authority, approval and maintenance rules | No agent self-approval; applies across repository via root instructions |
| governance/guarded-files.md (new) | Minimum protection register, including historical Stage 00/01 and catch-all for other approved content | Omission, moves, generated summaries and stale headings cannot remove existing guards |

All previously guarded files stay guarded. Stage designs/contracts are not rewritten. Sharon approved logical changes, not a mandatory line-by-line presentation; reviewable diffs remain. Approval of this process does not approve implementation of reviewer/event/harness explorations.

## Supporting changes

Root AGENTS explicitly requires designs/AGENTS and the guarded contract for work anywhere in the repository. The nested instructions list the required reading and flow. This is a mandatory repository constraint, not a claim that every client automatically loads nested instructions. Progress records approval, revision-specific evidence and pending integration; roadmap retains stage sequence; the designs index provides discovery.

The permanent offline Atlas has Current/Explorations views, architecture zoom levels, a candidate reviewer walkthrough, source references and searchable file trees. A standard-library builder checks references/hierarchy/guards and generated freshness. Detailed prior research is indexed under explorations with status and unresolved questions.

Public documentation removes sandbox-specific guides/index entries and states the maintained product-doc boundary. Product commands are unchanged. The internal app/docs review guide was removed in #34; it remains removed. The temporary review helper and task are removed with Sharon’s approval.

## Integration with #34

Main `96cb1f8` includes accepted PR #34. Reconciliation preserves all runtime, test, quality-gate and packaging blobs, except the explicitly removed temporary review helper and task. The internal app/docs review guide and temporary handoff were already deleted by #34.

[Verification](verification.md)
