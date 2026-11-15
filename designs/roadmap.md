# Provisional Learning Roadmap

The roadmap owns intended sequencing and stage boundaries. [Architecture](architecture.md) owns component responsibilities; [progress](progress.md) owns verified current status. Detailed stage and milestone designs remain with their stage owners.

| Stage | Focus | Expected outcome |
|---|---|---|
| 00 | Development environment | Completed and accepted; preserve tooling, local gate and isolated-release evidence |
| 01 | CrewAI Flows | Completed and accepted; preserve deterministic workflows, routing/state and failure-path evidence |
| 02 | Workflow observability | Actual workflow runs have useful correlated traces, hierarchy and honest success/failure reporting |
| 03 | Orchestration patterns | A bounded set of branching, parallel-work, join and failure-propagation scenarios |
| 04 | Agent execution foundation | Shared contracts, small harness, fake adapter/mapper, DemoAgent and deterministic CrewAI integration |
| 05 | Native agent integration | SDK investigation, real adapters/mappers and verified compatible provider integration |
| 06+ | Further capabilities | Individually selected extensions with their own design and acceptance |

## Sequencing and approval

The ordinary incremental sequence remains. **Stage 04 alone has an approved exception:** independently approved shared-foundation milestones may progress before Stages 02 and 03 are complete. Actual dependencies and the ordinary design/implementation gates still apply. This does not authorize every Stage 04 milestone, real SDK work or arbitrary future stages.

Independent contracts/fake work can progress early. Workflow integration must inspect and reuse the actual applicable workflow/context contract and resolve shared dependencies before implementation. Do not invent placeholder workflow IDs or a second context system. Real provider integration remains Stage 05 and retains the charter's orchestration/observability learning prerequisites.

Approve a stage's overall boundary first. Then draft each milestone's design, test cases and implementation plan together, approve and lock its exact revision, and implement only its authorized scope. Later milestone details may remain draft. Verify meaningful outcomes and record Sharon's acceptance separately from tests and merge state. The [stage working method](governance/stage-milestone-workflow.md) owns milestone folders and the Stage Design PR lifecycle; [Codex rules](governance/codex-handover-rules.md) own implementation handoffs/review.

Future-stage descriptions remain high level. Outside the specific exception, implementation commitments wait for their stage. Explicitly requested research/POCs remain non-binding [explorations](explorations/README.md). The roadmap does not itself lock an implementation contract.

## Stage 02 — Workflow observability

- **Starting point:** deterministic workflows, accepted local Langfuse and mock traces; preserve M1–M3 acceptance and subsequent context evidence in the owning stage records.
- **Outcome:** actual workflow runs use shared context, useful correlation and execution hierarchy, with honest success/failure reporting.
- **Evidence:** successful and controlled-failure workflows show expected observations, hierarchy and correlation; independent runs remain isolated; the chosen telemetry-outage policy is tested. Automated results and Sharon's local acceptance are separate.
- **Boundary:** tracing preserves workflow semantics. No real SDK requirement, replay/recovery subsystem, new logger or log store/viewer. Application logging is not required to finish this stage. Detailed tracing contracts remain stage-owned.

## Stage 03 — Orchestration patterns

- **Starting point:** basic deterministic workflows and the agreed observation foundation are available.
- **Outcome:** a small explicitly selected set of branching, parallel-work, joining and failure-propagation patterns is understood and verified.
- **Evidence:** maintained scenarios demonstrate expected outputs, branch/join behavior, controlled failure and isolation between parallel branches/runs; correlated traces support inspection.
- **Boundary:** CrewAI remains scheduler/state owner. Reuse Stage 01 evidence instead of repeating completed learning. Select exact scenarios in stage design; no unlimited complexity catalogue, native-agent dependency, logging prerequisite or durable recovery framework.

## Stage 04 — Agent execution foundation

- **Starting point:** basic workflow infrastructure exists; use the sequencing exception only for independent approved foundation work.
- **Outcome:** owned contracts/events, basic settings/permission data, common harness, fake adapter and concrete fake mapper, one deterministic application agent and a maintained CrewAI demonstration.
- **Evidence:** a repeatable request passes through fake native messages, mapping, shared-event callback and role handling to a result; meaningful success/failure checks and the actual workflow boundary exercise the same foundation.
- **Boundary:** native types remain within integrations. Reuse the shared context/observability contracts when needed. No real Claude/Codex SDK or concrete native mapper, full coder/reviewer product, human approval wait, logging infrastructure, generic event bus or second model/tool loop. The fake does not prove native permission enforcement or parity.
- **Ownership:** detailed milestones, schemas and C01/Q12 execution-versus-observability ownership reconciliation remain with the Stage 04 design owner. Broad roadmap approval does not settle them or approve every draft milestone allocation.

## Stage 05 — Native agent integration

- **Starting point:** the common path works with the fake and the necessary orchestration/observability foundation is accepted.
- **Outcome:** investigate one real provider's SDK/transport/lifecycle, implement its adapter and native mapper, then integrate a second provider to demonstrate interchangeability through the same application/workflow boundary. Claude and Codex are the intended providers.
- **Evidence:** explicit live runs verify the supported settings/permissions, truthful event mapping and failure/lifecycle behavior. Compatible adapters can replace each other without rewriting the shared consumer. Shared deterministic checks and provider-specific acceptance remain distinct.
- **Boundary:** exact versions, SDK surfaces and useful role scenario are detailed-design choices. Compatibility covers only supported capabilities; it does not promise identical outputs, timing, permissions, cancellation, session reuse or cost. No entire multi-role catalogue is required.

## Stage 06+ — Further capabilities

- **Starting point:** the agreed basic system runs with real providers.
- **Outcome:** select useful extensions from observed needs, each with its own bounded goal. Richer hooks, human interaction, session features, roles/workflows and integrations are possible ideas, not commitments.
- **Evidence:** each selected feature has a reviewed design, behavioral evidence, known limitations and user acceptance.
- **Boundary:** the small common harness belongs in Stage 04; only additional/advanced harness behavior belongs here. No universal final product is committed.

## Separate deferred workstream — application logging

Traces meet current needs. Retain the eventual execution-event logging requirement (D12); its delivery is deferred and is not a prerequisite for current tracing/foundation progress. Revisit after Stage 02, potentially alongside Stage 03 if Sharon chooses. This is neither a new numbered stage nor a scheduled commitment, and does not extend the Stage 04 exception.

When selected, define bounded success/failure log records, execution correlation, sensitive-data handling and failure behavior. Format, storage/export, retention and exact coverage remain open. A fake/test recorder is not production logging acceptance.

## Approval and scope record

Source: [PR #46 handover at its published revision](https://github.com/SharonLanger/agent-playbook/blob/07ece47ebdc569b2783cfeaede35271706c95443/designs/temporary/stage-roadmap-handover.md), followed by Sharon's explicit approvals in the PR #48 alignment conversation on 2026-11-15.

- **RM01:** preserve numbering and completed 00–01; accept the broad 02–06+ boundaries above.
- **RM02:** Stage 04-only early-foundation exception, retaining real dependencies and approval gates. This deliberately supersedes blanket sequential applicability only for that scope.
- **RM03–RM04:** logging remains required eventually but is deferred; it is not Stage 02 completion or a current progress gate. Precise later scheduling remains open.
- **RM05–RM06:** #46 originally transferred decisions only. Sharon subsequently authorized applying general roadmap/governance changes in #48; stage-specific files and concurrent Stage 02/04 work remain with their owners.
- **RM07:** preserve decisions, alternatives and open questions; milestone scope changes follow the owning plan-first process. No detailed execution decision is silently changed.
- **RM08:** the original handover did not authorize runtime work or a merge. Sharon separately authorized merging #48 after verification in this conversation; that does not authorize merging any Stage Design PR or implementing a milestone.

Earlier Stage 04 isolated real-SDK study is replaced by the shared foundation; SDK study moves into Stage 05. No extra SDK or logging stage is introduced. Broad approval resolves the sequencing direction, while detailed canonical ownership and milestone locks remain separate work. The original handover and historical stage records are retained.
