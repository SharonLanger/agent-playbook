# M4.2 + M4.3 — round 02 revision and continuation

2026-11-15. Approved direction: Sharon accepts visible framework output, native workflow input/output capture, readable names, and continuation under the SDK-first constraint. Latest instruction: “we must use LangFuse SDK before we decide to do something ourselves” and prepare the next Codex handover. This document is the narrow amendment to the original contract, not a fresh review cycle. The implementation team stopped after round 01 and has not begun round 02.

## Baseline and reading order

- [Original design](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/design.md)
- [Original RUN-01–20 test cases](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/test-cases.md)
- [Original implementation plan](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/implementation-plan.md)
- [Requirements](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/requirements.md), [decisions](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/decisions.md), [research](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/research/crewai-langfuse.md).
- [Standing handover rules](https://github.com/SharonLanger/agent-playbook/blob/7915feb3c2a55f613fb65835109b8b758099de9f/designs/governance/codex-handover-rules.md).
- Implementation PR #50: impl/m4-2-3-native-tracing to main; published head 95c1b8fd7c175643ebb26a1c4d74638ff9702234. Round-01 candidate 4df1a434c37cfff0b20d8b719bbb6841ea0e9e33. Read its follow-ups and all round-01 reports.
- Stage Design PR #47 stays draft/open. Original baseline ab3fab459c97eed44cc0b202402e559a827a71cf remains immutable history. Main reconciliation at 7915feb changed no handed-off stage contract.

Read this amendment together with the original files; it takes precedence only for the explicit changes below. Pin this document's published commit in round-02 reports.

## Revised design and scope

1. SDK FIRST is mandatory. Native context managers provide observation lifetime/exception handling; native propagation, instrumentor and flush provide tracing. Only minimal application wiring and native SDK update calls are authorized. No broker, custom span/event engine, monkeypatch, custom exporter, output interception or generic state serializer. If a requested result needs custom infrastructure, stop that part and explain why; do not implement it speculatively.
2. Visible CrewAI framework output is accepted for this integration. Set the committed application default show_framework_events to true and align relevant integration fixtures. Preserve explicit external overrides and document that false currently suppresses automatic Flow spans with OpenInference 1.1.25. Do not silently override a user's false value. No extra configuration flag is requested. CrewAI cloud telemetry/tracing stay disabled; Langfuse uses its configured local destination. This supersedes preservation of quiet console presentation only, not business results or exit/error behavior.
3. Record real workflow business input and final output on the existing outer runner observation using native SDK fields. Use the parsed input mapping only after workflow preparation/validation succeeds; attach validated JSON-compatible output through the existing serialization boundary. Do not record raw invalid JSON as validated input. An omitted input may be represented as an empty mapping; this does not pretend to contain resolved defaults or initial state. Never pass ApplicationSettings, execution context, credentials, complete Workflow/Flow objects or arbitrary state to the exporter. No hardcoded score/fields or per-workflow tracing implementation. Failure must not fabricate a successful output.
4. Prefer stable readable Flow/step names through supported native naming facilities, preserving UUIDs as identity metadata. Inspect actual installed APIs before choosing the minimal assignment. Do not rewrite spans or build a naming processor. If native support is insufficient, report this separately for deferral rather than adding a custom workaround.
5. Public project identifier: Sharon accepts a public key appearing as SDK metadata. Identify the exact field and origin before narrowing the test. Only the confirmed public identifier is exempt; secret keys, configuration objects and unrelated settings remain forbidden. Record this narrow payload-policy amendment in the relevant docs. Do not broadly remove payload checks.
6. Visible framework output showed an update notice. Determine whether ordinary runs initiate an external update check and use a supported native disable switch if available. Do not use ad hoc network monkeypatches or silently relax local-only requirements. If no supported remedy exists, report the concrete tradeoff for Sharon; do not assume approval.
7. Keep the existing schema, tracing version pins unless a separately justified change is needed, and CLI finally-based flush. Future API invocation is a later scope, not a server implementation now. No arbitrary initial/final state snapshots are required in this revision.

## Acceptance amendment

Retain RUN-01–20 and report each honestly. Do not remove failing integration assertions or mock away the integration being accepted. Existing workflow behavior tests need no broad refactor. Their arithmetic/console specifics are not the purpose of this milestone; new checks focus on application tracing and boundaries.

- R2-01: ordinary enabled configuration produces runner/kickoff/executed-step hierarchy with show_framework_events true. Disabled Langfuse still runs normally. Explicit false's known tracing limitation is documented, not mislabeled supported complete tracing.
- R2-02: different real inputs, including scores 59 and 60, appear on the outer observation and match corresponding validated outputs. Input capture is generic and excludes settings/credentials; malformed input has no fabricated validated payload/output.
- R2-03: RUN-13 asserts parent.start <= child.start <= child.end <= parent.end for runner/kickoff/steps, plus external-parent restoration after success and failure. Separate assertions/tests so missing span counts do not hide all restoration evidence.
- R2-04: readable native naming if supported; no UUID display suffix requirement. Identity/correlation remains correct across repeats.
- R2-05: verify automatic descendant payloads, the identified public-key exception and secret exclusion after hierarchy works.
- R2-06: audit normal enabled execution for unintended external connection/DNS attempts; report scope of audit accurately. UI success alone does not prove locality.
- R2-07: full quality gate, installed release and existing regression obligations remain. Independent reviewers must distinguish completed runs from timeouts/interruption.

Manual evidence already supplied by Sharon: after Setup installed the missing OpenInference package, WF-01 returned [Hello, workflow!] with exit 0. Screenshot confirms local Langfuse runner/kickoff/three-step hierarchy; Sharon confirmed identical correlation/workflow-run IDs across descendants. He ran WF-02 and both WF-03 inputs, and described score-60 begin output 60, choose/accept/kickoff output pass. Do not upgrade this to complete RUN-18: explicit branch checks, failure case and new outer input/output/naming checks still need recorded evidence. Automated diagnostic stalls were observed in LanceDB initialization; they prove neither integration pass nor fail. No open-ended performance investigation is requested.

## Implementation and review instructions

Continue on PR #50; inspect current main and repository instructions first. Do not merge #47 wholesale into implementation. Apply this amendment and only the original authorized RUN-G01–08 plus directly necessary stage/config/public-guide/test wording for this revision. For other guarded semantic changes, stop and explain. Preserve main governance and other-stage content; escalate conflicts beyond this scope.

Use one Sol coder and two independent Sol reviewers (design drift and test gaps); record actual models. Begin round 02 of a maximum THREE TOTAL rounds. Diagnostic-only attempts did not consume another round. Preserve round 01 and all open finding IDs. Both reviewers assess the same new candidate, mapping RUN-01–20 and R2-01–07 to assertions/evidence. Keep implementation.md, design-drift.md, test-gap.md and orchestrator.md under reviews/round-02; use round-03 only if necessary. Stop after round 03 if required issues remain.

Update implementation status/follow-ups/public guides and Atlas based on observed results; do not label partial work accepted. Keep this approved revision and original contract frozen while working. New gaps go in follow-ups. No merges or auto-merge.

Return ONE copyable FINAL REVIEW HANDOFF using the standing rules: candidate/head/base and contract SHAs, exact tests/results, both verdicts and report links, N/3 rounds, disposition of every finding, manual checks outstanding, and explicit unmerged state. Return BLOCKED for unresolved requirements; only completed evidence counts as passed.
