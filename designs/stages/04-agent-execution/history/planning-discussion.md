# Planning discussion after revision 12

Recorded 2026-11-14. **Summary of the visible discussion, not a verbatim transcript.** The original two records preserve earlier decisions in full. D27–D32 record the approvals; detailed new milestone recommendations remain review proposals.

## 1. Review Stage 04 alongside Stage 02

Sharon asked to inspect roadmap/design/progress and PR #43, learn its design organization and drift-prevention process, and assess parallel work without changing anything. His intuition was that different subfolders supported parallelism.

Assessment: the contracts/data and design can be developed largely independently, but folder separation is insufficient by itself. Assembly, configuration, context, workflow signatures and shared navigation/Atlas can overlap. Keep these crossings explicit; do not copy or redesign the context track.

## 2. Shared foundation before concrete native providers

Sharon wanted parallel designs and suggested eventual implementation of real ABCs and contracts to expose mistakes early. He explicitly excluded current Stage 02 context/Langfuse concerns from the first foundation work. The first product increment should include the surrounding execution system, basic events/settings/permissions and a fake, while avoiding actual provider integrations and concrete reviewer/coder work.

The broader desired layout and three accepted ABCs stay in force. A proposed delivery split is contracts/models, harness/fake, demo agent and CrewAI demonstration. That is a smaller checkpoint breakdown of the foundation direction, not proof that all schema/behavior choices are complete.

## 3. Deterministic agent and workflow exercise

Coder/reviewer remain practical examples for capability discussions. Sharon suggested one simple deterministic agent, perhaps doing a simple task and sleeping for roughly half a minute, and invoking it through CrewAI by the end of the foundation work.

The first exercise should validate the real path, not merely sleep and return success. DemoAgent should implement the role contract and use the injected harness/fake/mapper path; CrewAI should retain its existing workflow ownership. Task entry, fields, output and timing remain to design. A configurable visible delay with zero/short automated-test delay is a recommendation, not an approved default.

## 4. Proposed global stage allocation

Sharon explored redefining Stage 04 around the execution foundation and Stage 05 around native integration. He later explicitly instructed **not to change the roadmap now** and agreed another global stage might be unnecessary. He clarified later integration is more than the SDK: it includes the actual adapter and related native behavior.

Record this as a working planning direction, keep existing global sequencing untouched, and reconcile before implementation lock. No current-stage change or new global numbering has been approved by creating this package.

## 5. Fake fidelity and reproducibility

Sharon agreed that the fake should reflect real integration and verify mapping. He suggested an input such as five, representing five tool calls, or random numbers selecting event types. Those are exploratory scenario ideas, not a frozen schema.

Recommended baseline: predetermined fake native messages passed through a concrete fake mapper, valid ordered tool-call/result pairing, a predictable result and deliberately controlled failure cases. Optional seeded variation can be considered later. Randomness must not be mistaken for correctness, and fake messages do not prove Claude/Codex behavior or sandbox enforcement.

## 6. Permanent design PR and history

Sharon wanted a design PR similar to #43, organized with one starting README, specifications, decisions, milestone planning and preserved history/research. Every progress iteration must retain decisions, alternatives, reasons and open/answered questions. Read the full current records and check contradictions before changing them.

Earlier instructions prohibited implementation and initially prohibited PR creation. The latest instruction explicitly authorizes creating this draft documentation PR. It does not authorize runtime implementation, dependency selection, roadmap edits, guarded logical changes or merging.

## 7. Milestone boundaries and change order

Sharon added an explicit rule: each milestone needs a boundary, and a boundary change must first be made in the milestone plan and checked against the decision board/specification for contradictions.

Operational interpretation recorded under D32: first record a Pending proposed delta in the plan; inspect all affected agreements; explain any conflict before changing agreed meaning; use the approval actually required for that change; then update effective boundary, decision history, specification and affected detailed designs together. This preserves the existing D07 requirement to notify Sharon before changing agreements. A Pending plan edit is not self-approval.

## 8. Repository comparison at PR creation

Main inspected at d12b5fc2867d3646b6fab2eb71f1447ff177d8c1. PR #43 had advanced to head 11bba581291c1b166973848ea8db6a9e2a142413 and was still draft/unmerged. Its README now describes detailed context/test/review documents. Its organization is useful; its schema and independent-review procedure are not automatically adopted for this execution package.

The package retains C01's execution-event/observability ownership reconciliation and Q37's sequencing question. It also retains D12's logging requirement: excluding logging integration from the foundation does not make a recorder equal to a complete logging deliverable.

## Unresolved work

Initial event/request/result payloads and completion ownership; minimal settings/tool-policy data and unsupported-policy behavior; callback/failure/cleanup/lifetime semantics; exact fake scripts; role task entry/helper organization; eventual context/logging connection; guarded canonical amendments and deliberate stage-sequencing review. These are visible design tasks, not reasons to withhold the authorized draft planning PR.

## 9. Subsequent instruction — merge last and initial events, revision 14

Sharon explicitly requires PR #45 to be the last PR merged after all Stage 04 implementation is merged, keeping designs and milestones here throughout the work. D33 and BC02 record the order. He also accepts the five previously explained event names/basic meanings, asks for clarification of future event categories, and requests file/folder placement. D34 records the limited catalogue approval; payloads, ownership and failure rules remain open. The specification explains placement in execution/events.py and preserves separate interface files. No runtime files or provider implementations were requested.
