# S03.M1 — Recipe cookbook batch

One batch: eight standalone CrewAI recipes plus the agreed concepts/recipes organization.

- [Design](design.md): behavior, placement, diagram/README contract.
- [Verification cases](test-cases.md): temporary scripts, meaningful assertions and user-run/cleanup lifecycle.
- [Implementation plan](implementation-plan.md): branch, roles, three-round cap and final handoff.
- [Approved visual reference](../diagrams/approved-preview.html) and [provenance](../diagrams/README.md).
- [Requirements](../README.md) and [decisions](../decisions.md).
- [Repository handoff rules](../../../governance/codex-handover-rules.md).

Approval: Sharon's 2026-11-15 acceptance of all eight illustrated recipes and explicit request for this Codex handoff (U09). Exact contract SHA is pinned in the outgoing prompt; forward that prompt to authorize its concrete revision.

Implementation: eight recipes delivered on draft [PR #53](https://github.com/SharonLanger/agent-playbook/pull/53), candidate fdb60f3a3964f9620758e7e3f8be03bbe1084711, published head 906e0e5921fae726f37c5bdbb61551578373c908. Both independent implementation reviews passed in round 1/3. [Originating design-session final review](reviews/final-review.md): PASS, no required corrections. Runtime checks passed in the recorded Linux implementation/behavior-review runs; this design session independently inspected source/assets and rendered diagrams but could not rerun CrewAI. Sharon's hands-on acceptance, temporary-check cleanup and both merges remain pending.

Temporary verify.py scripts remain in the implementation branch for Sharon and review, then are removed before merge. Design PR #52 stays draft/open under its own merge gate.
