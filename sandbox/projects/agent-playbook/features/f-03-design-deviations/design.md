# f-03-design-deviations — Record and resolve material design deviations

- Project: `agent-playbook`
- Source repository: https://github.com/SharonLanger/agent-playbook
- Status: Draft; not approved for implementation.
- Revision: Draft 1
- Inspection baseline: `9c674a76ee2dec04e5f05e5bdd6b8c564e761c86`
- Feature identifier: `f-03-design-deviations`

## Problem and intended outcome

The initial designer can write a design but cannot yet evaluate deviations during implementation. Extend that same role to record proposed changes while preserving the user's approved baseline.

## Scope and approach

A deviation request identifies the project, feature, approved baseline revision, relevant code revision, evidence, proposed change, alternatives, and impact. The designer classifies its impact and writes a decision record. It performs no code changes.

Store records beside design.md as deviation-001.md, deviation-002.md, and so on. Each record identifies the exact baseline, requested change, rationale, behavior/test impact, status (proposed, approved, or rejected), decision authority, and evidence of the decision. Retain the original proposal and decision history; new information must not erase earlier decisions.

The baseline's approved content remains unchanged. Only a bottom section linking deviation records may be appended. The designer is the single writer of that link section within a run. Readers follow only approved deviations; discovering a link does not grant approval.

The planner may approve only implementation adjustments covered by an explicit delegation from the user. With no delegation, a material change remains proposed and returns to the user. Changes to requirements, scope, public behavior/API, security assumptions, or acceptance criteria require the user's decision. Ordinary implementation choices do not need deviation records.

No default blanket delegation is introduced. Implementation may resume only after the required decision is available. At completion, outcome.md describes the delivered result and accepted deviations while retaining the baseline and records.

## Acceptance criteria

- Deviation records identify what changed, why, and who authorized it.
- The approved baseline body is preserved; the only baseline diff is the permitted link section.
- Proposed or rejected records never become effective requirements.
- Delegated decisions stay within recorded authority; missing authority requires a user decision.
- Records and links do not overwrite another deviation or silently conflict.
- A later reader can reconstruct the baseline plus the accepted changes.
- The outcome document distinguishes implemented changes from remaining proposals.

## Verification scenarios

| Scenario | Expected behavior |
| --- | --- |
| Internal helper adjustment with no design impact | Remains an implementation choice; no unnecessary approval cycle. |
| Alternative implementation within explicit delegated authority | Planner records the reasoning, approval, and delegation reference. |
| Same proposal without delegation | Record proposed; obtain the user's decision before dependent implementation. |
| Proposed extra required public field | Treat as a potential contract change, not as minor because only one field was added. |
| Rejected or undecided deviation linked from the design | Reader sees it but does not implement it. |
| Existing deviation number or concurrent proposal | Recheck existing records and coordinate numbering; do not overwrite. |
| Conflicting approved deviations | Surface the conflict and obtain a resolving decision; do not choose silently. |
| Feature completion | Compare outcome with baseline and accepted records; preserve history. |

Verify baseline preservation with an actual before/after diff, rather than relying on the designer's claim. Use a disposable approved example with explicit test delegation to exercise decisions; do not label a real unapproved design approved for convenience.

## Delivery sequence and dependencies

Use the implementer handoff from f-02 to define deviation inputs. Extend agents/designer.md and the README, exercise the authority and preservation cases, and save an outcome record. No separate replanner agent or workflow engine is introduced.

## Open decisions

For each real run, the user must define any delegated decision boundary they want. In its absence, the planner records a recommendation and the user decides. Automated write protection and distributed locking remain future work.
