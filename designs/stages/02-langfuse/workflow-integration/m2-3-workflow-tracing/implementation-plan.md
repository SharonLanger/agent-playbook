# Combined runner + CrewAI tracing — implementation plan

Version 2, 2026-11-15. **REVIEW DRAFT; not a runnable implementation authorization.**

Read [Codex handover rules](../../../../governance/codex-handover-rules.md) first, then the [design](design.md), [tests](test-cases.md), [requirements](../requirements.md), [decisions](../decisions.md), [research](../research/crewai-langfuse.md) and [discussion](../history/runner-design-discussion.md).

## 1. Before handoff

The originating design session records the accepted PAYLOAD-01 policy and approval of the exact three-file revision and applicable RUN-G01–08 logical amendments, and delivers the filled outgoing prompt from the standing rules. Do not manufacture approval from this draft. M4.1 is accepted/merged and its contract stays unchanged.

Refresh current main and repository instructions. Record design SHA, main SHA, implementation base/target and intervening differences. PR #47 is a continuing documentation workspace: do not base runtime changes on its local scratch checkout or merge it early. Implementation branch should start from refreshed main; read the approved design at its pinned PR revision. Include only implementation-required approved documentation amendments in the implementation PR, not unrelated ongoing planning.

## 2. Coder work

1. Confirm supported dependency closure against current main and apply the tested instrumentor pin with the lockfile.
2. Locate existing settings/initialization, runner and CLI cleanup entry points. Reuse native setup; add only concrete small helpers where necessary. Keep once-only instrumentation and one provider.
3. Add the native runner scope and three-field propagation around existing lifecycle. Preserve M4.1 creation/forwarding and current errors. No manual Flow-step instrumentation.
4. Add final CLI flush in finally after scopes close; preserve workflow error precedence. Use native exporter behavior, no custom queue/retry/cache.
5. Implement RUN cases against actual maintained workflows and test fixtures. No production agent/sample workflow needed.
6. Apply only approved guarded amendments; update supported public guides and stage status without claiming acceptance prematurely.
7. Run required focused/full/release/documentation checks. Record unrun/blocked live acceptance honestly.

The coder report must explain each new helper in terms of application wiring. A helper that merely recreates a Langfuse span/event API is design drift.

## 3. Reviews and corrections

Use one coder and two separate independent reviewers. Design reviewer checks the exact approved design, native-SDK minimality, scope, guards, runtime behavior and documentation. Test reviewer maps RUN-01–20 to implementation/assertions/evidence and assesses gaps/false confidence. Freeze one candidate SHA for both.

Store reports under this milestone's reviews/ directory:
- status.md
- round-01/implementation.md
- round-01/design-drift.md
- round-01/test-gap.md
- round-01/orchestrator.md

Create equivalent round-02/03 directories only if needed. Consolidate findings and send corrections to coder. Both reviewers recheck the corrected candidate. Maximum three total rounds, then STOP if unresolved. Keep prior findings/reports; no reset after handoff.

## 4. Return and acceptance

Publish the implementation PR as draft/open/unmerged unless separately instructed otherwise. Return the exact fully populated final-review handoff format from the standing rules, with immutable report links, approved contract, base, candidate/head comparison, all rounds and test evidence, remaining manual acceptance and risks.

The originating design session reviews the actual diff/evidence. Its review does not replace Sharon's acceptance or merge authorization. Documentation PR #47 remains MERGE LAST, including after this implementation PR merges. Reconcile final results into it without discarding ongoing work.

## 5. Current next step

The design session supplies a pinned copyable implementation instruction. Sharon forwarding that instruction explicitly authorizes this design/test/plan and the listed narrow RUN-G01–08 amendments. Record that instruction as the approval reference; do not infer approval merely from this document's existence. Once implementation starts, keep this contract unchanged until the returned output is reviewed; record later changes in a separate follow-ups.md. Use the standing rules' required return report.
