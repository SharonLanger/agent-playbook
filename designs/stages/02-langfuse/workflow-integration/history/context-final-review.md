# M4.1 — final design-session review

Date: 2026-11-14. Reviewer: root design session. Status: **PASS for the M4.1 runtime/design contract; documentation integration completed; PRs #43/#44 merged with Sharon’s authorization.** This is an independent final review, not user acceptance or merge authorization.

## Revisions and scope

- Implementation: [draft PR #44](https://github.com/SharonLanger/agent-playbook/pull/44), `feat/m4-1-context`, targeting `docs/workflow-observability-planning`.
- Approved design/base: `11bba581291c1b166973848ea8db6a9e2a142413`, including Sharon's G01–G08 authorization supplied in the handoff.
- Reviewed runtime/test candidate: `16c1580e96bd36945fa96b6ecfa8f9a563d53913`.
- Published implementation head: `9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2`.
- Target inspected: `9aaf31e4b0e6345ed7162da765f37dbe94167f4b`.
- Rounds remain **2/3**. This final review does not restart the cap or authorize implementation changes.

I inspected the [approved-base-to-candidate diff](https://github.com/SharonLanger/agent-playbook/compare/11bba581291c1b166973848ea8db6a9e2a142413...16c1580e96bd36945fa96b6ecfa8f9a563d53913), actual changed runtime and test code, the approved context contract/cases, G01–G08 amendments, and permanent review evidence. The [candidate-to-published-head comparison](https://github.com/SharonLanger/agent-playbook/compare/16c1580e96bd36945fa96b6ecfa8f9a563d53913...9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2) changes only five review/status Markdown files. Runtime and tests are unchanged.

## Findings and disposition

### FINAL-DOC-01 — duplicate D30 when combining the documentation streams

Priority: medium, documentation integration. **Open; no fix applied.**

The [target decisions table](https://github.com/SharonLanger/agent-playbook/blob/9aaf31e4b0e6345ed7162da765f37dbe94167f4b/designs/stages/02-langfuse/workflow-integration/decisions.md) defines D30 as the accepted requirement to attach correlation_id to workflow-associated observations and future logs. The [implementation branch](https://github.com/SharonLanger/agent-playbook/blob/9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2/designs/stages/02-langfuse/workflow-integration/decisions.md) adds a heading also named D30 for M4.1 approval and implementation status.

Keeping both unchanged gives one decision ID two meanings. A text merge can retain this ambiguity without a conflict marker. Preserve both decisions and their approval/history; retain the established correlation D30 references and give the implementation approval entry an unambiguous new identifier or a non-numbered dated approval heading. Check incoming references when integrating. This is not a context schema or runtime defect and requires no speculative application change.

### Known integration blocker — current target conflicts

GitHub reports PR #44 not mergeable at the inspected heads. The [orchestrator trial-merge addendum](https://github.com/SharonLanger/agent-playbook/blob/9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2/designs/stages/02-langfuse/workflow-integration/reviews/context/round-02/orchestrator.md#target-branch-refresh-addendum--2026-11-14) identifies content conflicts in Atlas catalog/output, workflow-integration README, requirements and repository-updates. Preserve M4.1 approvals/evidence and M4.2 correlation/planning material. Rebuild generated Atlas from reconciled sources rather than selecting one HTML side. Recheck links, IDs, statuses, Atlas freshness and whitespace afterward.

I did not perform another merge trial or modify either PR. Documentation-only integration must retain proof that the reviewed runtime/tests are unchanged. A runtime/test correction requires the remaining review round under the existing plan; this review does not authorize a fourth round.

### Runtime and approved design

No required runtime or M4.1 contract finding.

- Frozen keyword-only dataclasses match the approved fields. UUID4 correlation is created only when omitted; nested dataclass replacement preserves correlation/workflow identity and isolates agent fields.
- The runner creates context after selection, inside CONSTRUCTION. Factory, Workflow ABC, wrappers and all three actual Flows retain the same reference. Config/import ordering, input validation before Flow construction, existing lifecycle and error causes are preserved.
- Private Flow storage avoids business-state and ordinary model serialization. CrewAI's separate execution_context remains untouched.
- No Langfuse instrumentation, logger, provider handle, trace-ID allocation, agent runtime or dependency change was introduced.
- The six round-1 gaps are addressed by actual round-2 assertions, including real runner-to-Flow reference checks, scheduled router/listener execution and negative paths. Existing test migrations still exercise their intended behavior.
- G01–G08 are bounded dated amendments covered by the handoff's explicit approval. The three approved milestone files change only their approval/status headers, not their implementation/test contracts.

## Independent verification

Created a separate review snapshot from the candidate's GitHub files; verified Git blob SHA-1 values for **61 selected source/config/test/fixture files**, including required package markers. Neither PR, its branch, nor its working files were changed.

Python 3.13.5; CrewAI 1.15.40; Pydantic 2.12.5; Langfuse 5.2.0; pytest 8.4.2. A dedicated review interpreter used the existing research environment's dependency packages and the exact candidate source. This was a targeted verification environment, not a fresh hash-locked installed-release reproduction.

From the snapshot's app directory, with writable isolated HOME/XDG directories:

```text
python -m pytest -q tests/context/test_models.py tests/application/test_context.py tests/workflows/test_context.py tests/application/test_followup_boundaries.py
...........................................                              [100%]
43 passed in 8.66s
```

An initial reviewer-created snapshot omitted the existing tests/workflows package marker and failed collection with a duplicate test-module name. After restoring that exact candidate file and verifying all 61 blob hashes, the unchanged candidate tests passed as above. This was a snapshot preparation error, not a candidate defect.

Reviewed, not independently repeated here: Pyright/Ruff/full **380-test** gate, offline runtime inventory, installed wheel/release verification and prior Atlas checks. The [round-2 test-gap report and CTX-17 addendum](https://github.com/SharonLanger/agent-playbook/blob/9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2/designs/stages/02-langfuse/workflow-integration/reviews/context/round-02/test-gap.md) maps CTX-01–17 and reports artifact hash, isolated installed import and release inventory. Release source `2e5d76dde2ec76b5a7ecae8ea0094286838229a9` lies in the verified report-only delta. I did not independently obtain or hash the released wheel.

No live Langfuse, Mac/PyCharm or external-user-secrets bootstrap test was performed. These do not establish missing M4.1 tracing behavior: tracing is explicitly later. The context tests and source review do not claim SDK active-scope or cross-process propagation.

## Preservation and next step

This review is stored on the separate M4.2 discussion branch, outside the implementing Codex's files. No code, approved baseline, previous review report, PR metadata or merge state was changed. No personal examples or historical sandbox content was read or run. Public guides and Atlas are not modified by this isolated review note; the implementation's workflow guide is accurate, while shared integration/status reconciliation remains explicitly pending.

Applicable principles: approval/traceability and truthful status are preserved by the pinned contract and separate record; secrets/configuration/provider boundaries are unchanged; tests provide actual-runtime evidence; scope stays incremental and local; history and sandbox isolation are preserved. The observability exploration remains deferred rather than being used to introduce a broker or runtime abstraction.

**Recommendation:** accept the reviewed M4.1 runtime implementation once Sharon is satisfied with this review; resolve and verify the documentation integration before a separately authorized merge. M4.2 drafting can continue against this context contract. No context redesign is needed by the findings above.

## Integration disposition — 2026-11-14, iteration 35

Sharon accepted M4.1 and authorized documentation reconciliation and merging PRs #43/#44. FINAL-DOC-01 is resolved by retaining correlation D30 and using a dated unnumbered approval heading. Both conflicting documentation streams are preserved and Atlas regenerated. Runtime/tests are unchanged; merge result is pending at this pre-merge checkpoint. The earlier review remains revision-specific history.

## Confirmed merge — 2026-11-14

PR #43 merged as c8f129ee8c978067bf576b0ab563bfab74c9d6fe; PR #44 merged as 942e59344c429454263319e783ea76ad297b7ea6. GitHub confirmed both. Application tree 0789b6bfd7ffe2248afbe9b3cd735cb908125571 is identical to reviewed head 9392b39. Documentation integration findings are closed. M4.1 is accepted and merged; M4.2 is design-only.
