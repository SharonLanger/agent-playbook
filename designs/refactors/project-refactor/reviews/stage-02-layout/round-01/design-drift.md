<!-- Permanent evidence for PR #67; candidate ab94509cedf9f01eedaa32a4546ecdfafcc879e5; round 01. -->

# Stage 02 layout migration — design-drift review, round 1

**Verdict: CHANGES REQUIRED.** Reviewer role: independent design-drift reviewer. Model: `gpt-6.2-sol`. Round 1 of a maximum of 3.

[PR #67](https://github.com/SharonLanger/agent-playbook/pull/67) · [candidate `ab94509cedf9f01eedaa32a4546ecdfafcc879e5`](https://github.com/SharonLanger/agent-playbook/commit/ab94509cedf9f01eedaa32a4546ecdfafcc879e5) · base `13bebb0d824cf9b2d1794a0cbff2311fbd99489c`.

## Required findings

| ID | Severity and status | Expected and observed | Required correction |
|---|---|---|---|
| DD01 | Medium · open | Atlas summaries should identify completed work and date older statuses. `designs/atlas/catalog.json:4368`, `:4373`, `:4378` and `:4383` present the M2/M3 handoff and user verification checkpoints as requested work, the 2026-11-13 review findings as open, and the CLI plan as pending. The relocated records lead to the accepted and merged PR #36 and the documented follow-up. At `:4404` Atlas describes the retained M4 requirements snapshot as current even though its status predates combined tracing approval. At `:4424`, `:4429` and `:4434`, it labels the approved M4.1 design, test cases and implementation plan as drafts while their adjacent status labels explicitly record approval and merge. | Label the M1–M3 entries as historical checkpoints, describe the M4 requirements as retained with stable IDs and deferrals, and describe the M4.1 design, cases and plan as the approved package. Preserve the original stage documents, dated review verdicts and remaining delivery-readback limitation. Regenerate and recheck Atlas. |
| DD02 | Medium · open | The project-refactor alignment record should preserve the PR #59 snapshot and distinguish it from the new layout. `designs/refactors/project-refactor/stage-alignment.md:11` pairs a live link to the renamed M4 package with present-tense instructions that map M4.1 and M4.2 + M4.3 to the removed `m1-context/` and `m2-3-workflow-tracing/` folder names. The dated relocation note at `:24`–`:26` supersedes location retention but omits the renamed subpackages. | Identify the two old names in the existing table as the PR #59 mapping, and add links to both current M4 milestone packages in the dated Stage 02 note. Keep the earlier approved contracts and evidence intact. |
| DD03 | Low · open | The retained Stage 02 `#start-here` anchor should take readers to the current reading order. In `designs/stages/02-langfuse/README.md:59`, it lands at a historical pre-closeout navigation section that describes pending planning; the current reading order starts at `:28`. | Keep the same anchor string and move it immediately above the current `Read the stage records` heading. Preserve the earlier navigation text under its historical heading. |

## Acceptance mapping

| Criterion | Disposition | Independent evidence |
|---|---|---|
| S2L-01 | PASS | Direct GitHub compare shows one commit ahead of base, 62 detected renames and the mapped M4.1 README as one remove/add pair. The 67 mapped sources have distinct destinations, four root paths remain, and only the M1–M3 README is net new. All 67 original local Git blob hashes match the pinned map. |
| S2L-02 | PASS | M1–M3 remain grouped with PR #36. Root and package navigation keep M4.R, M4.1 and combined M4.2 + M4.3 global identities, with M4.1 and combined tracing reviews under their approved milestones. The shared repository checklist sits under M4 history. |
| S2L-03 | PASS | Compared protected Stage 02 architecture/milestone records, six M4 milestone contract files and workflow-contract cross-references after canonicalizing relative link targets. Only mapped link changes remain, and the guard register carries six current paths with original approvals intact. Original absolute URL multisets match for each mapped file. Actual README diffs preserve past status, approval/merge evidence and historical aliases. No review verdict is rewritten. |
| S2L-04 | PASS | All 13 probe files and the adjacent research report compare byte-for-byte. The candidate preserves the eight-case/44-span results as historical research. |
| S2L-05 | CHANGES REQUIRED | Checked mapped-relative targets for twelve protected or public-doc files and inspected old/raw path usage in scoped files. Pinned paths and dated historical paths retain provenance. The old `#start-here` fragment resolves but points to the historical plan, covered by DD03. Full relative-link and anchor coverage belongs to the independent test-gap report. |
| S2L-06 | CHANGES REQUIRED | `python3 designs/atlas/build.py --check` passed independently against the candidate snapshot. Catalog diff is confined to Stage 02 paths and framing, but human-readable labels require DD01. |
| S2L-07 | PASS | Remote compare shows eleven external paths, all within the allowed navigation, register, Atlas and migration-note surfaces. The public Langfuse guide has a single mapped evidence-link repair. The alignment note needs the navigation clarification in DD02. |
| S2L-08 | CHANGES REQUIRED | Root and package README entries start with accepted closeout and provide the correct package/evidence links. DD01–DD03 record remaining current-navigation issues. GitHub search constrained to open draft PRs returned #67 with the frozen candidate in its description. |

## Checks and limits

- GitHub compare of the complete base and candidate SHAs, GitHub PR search `repo:SharonLanger/agent-playbook is:pr is:open is:draft 67 in:number`, and local `git` blob hashing implemented with `hashlib.sha1` over blob headers and bytes. The remote compare and publication manifest agree on scope. Local changed blobs match the candidate manifest, whose remote tree verification was recorded by the orchestrator.
- Independent Python comparisons of map uniqueness, Stage 02 file inventory, original and candidate blobs, absolute URL multisets and mapped href semantics. Inspected the actual per-file unified diffs, preserved approvals and verdicts, root and package README navigation, dated alignment note, and Atlas catalog labels. No expanded scope or product contract change found.
- From the candidate snapshot, `python3 designs/atlas/build.py --check` reported PASS for references, hierarchy, guards, sandbox boundary and freshness. The check confirms generated output and does not determine whether status prose is current.
- Reviewed the available scoped snapshots and the exact GitHub comparison. Outside stages supplied only Atlas dependencies. Personal examples were not accessed. Application tests, live traces, release builds and probe execution were outside this documentation-only review. No candidate edits, publication or merge performed by the reviewer.
