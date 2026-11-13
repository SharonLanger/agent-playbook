# Workflow contract implementation plan

Status: **Plan only. Do not begin implementation until Sharon explicitly authorizes it.**

## Scope and authorization record

On 13 November 2026 Sharon accepted the workflow ABC/registry/YAML direction, required strict input/output validation and error boundaries, then explicitly added shared lifecycle statuses with final public methods and abstract underscore hooks. He authorized updating the design documents and the Stage 01 restriction. His latest instruction is to report readiness without beginning implementation.

One refinement resolves the heterogeneous typing boundary: serialization reads the instance's stored validated result instead of accepting a result parameter. The exact config defaults and strict YAML rules in design.md are implementation proposals within the requested design, available for review here.

No application implementation, dependency changes, release build, workflow execution, recovery mechanism or Langfuse integration is authorized by this documentation task.

## Milestones after approval

Estimates are focused engineering time for one developer familiar with the project, including tests/review fixes. They are planning ranges, not elapsed-day commitments. Work is sequential where contracts depend on earlier decisions.

| Milestone | Change and observable gate | Estimate | Main risk and control |
|---|---|---|---|
| 0 | Approve package; apply reviewed guarded changes; record baseline check result | 0.25–0.5 day | Low: stale source/design; refresh main and preserve other work |
| 1 | ABC, lifecycle/status/errors and typed result; isolated contract tests and strict typing pass | 0.5–1 day | Medium: generic variance or incorrect transition/failure; prove with rich result and transition matrix |
| 2 | YAML selected-entry validation, strict loader, registry and factory; config/import-order tests pass | 0.75–1.5 days | Medium: configuration precedence and early imports; dedicated fixtures/subprocess checks |
| 3 | Wrap all three existing flows and adapt runner/CLI; real workflow regression matrix passes | 0.5–1 day | Medium: changed error classification/output text; preserve old scenarios and step behavior |
| 4 | Full gate, current-release verification, official guides and manual review instructions | 0.5–1 day | Medium: source/release mismatch or missed fixture; isolated current build and same CLI cases |

Total planning range: **2.5–5 focused developer days**, rounded. No time is allocated for children, recovery, old-release compatibility or observability. Milestones are reviewable checkpoints, not a requirement to create five PRs. Prefer one focused implementation PR unless separation demonstrably reduces integration risk.

## Guarded change manifest

The complete code design must be approved before implementing it. No charter/principles change is needed. Approval to document is not permission to silently apply every future guarded change.

| Guarded file | Exact logical change | Consequence and approval state |
|---|---|---|
| stages/01-crewai-flows/architecture.md | Preserve historical behavior; replace the blanket no-base-class restriction with a narrow successor allowance for this ABC/registry; retain no custom engine/plugins/container rule | Explicitly authorized in this conversation; documentation clarification included now |
| architecture.md | Refine application-facing workflow ownership: ABC transitions/validation/serialization, factory/registry selection, runner depends on ABC; CrewAI retains all step orchestration | Proposed for final approval; currently unchanged |
| project-structure.md | Update application/workflows/config responsibility descriptions to match file-structure.md; preserve all other component and sandbox boundaries | Proposed for final approval; currently unchanged |
| governance/guarded-files.md | Register the approved workflow-contract design and its file/test contracts once final approval is recorded; retain every existing entry | Proposed for final approval; currently unchanged |
| governance/design-contract.md | No procedural change | Existing process already supports this refactor |
| Stage 01 file-structure.md and test-plan.md | Add concise successor references once approved; retain historical layout and original flow acceptance scenarios | Proposed; do not rewrite history as if wrappers already existed |
| Stage 01 plan and individual workflow contracts | Preserve computations, inputs, routing and historical acceptance | No behavior change required; use successor references only if approval review identifies a conflict |
| charter.md and principles.md | No change | Purpose, CrewAI ownership, strict typing and approval discipline still apply |

An inspectable docs-only diff accompanies the authorized Stage 01 edit. The design package stays proposed until final review; it does not grant itself guarded-baseline status.

## Design and public documentation impact

- Add this permanent five-file package and link it from designs/README.md.
- Record design-only progress and the pre-Langfuse ordering without claiming runtime work.
- Add Atlas navigation to the package, labeled proposed/unimplemented; retain current runtime descriptions. Rebuild/check generated output.
- Public app/docs guides remain accurate for current behavior and are unchanged now. Update configuration, workflows, CLI, troubleshooting and their navigation in the implementation PR.
- No new architectural diagram is required: the existing component ownership remains. Tables specify the lifecycle; the indented tree explains proposed placement.
- Personal examples and historical sandbox are untouched. No new CI service or dependency is introduced.

## Principle assessment

| Principle | Application to this design |
|---|---|
| 1 Explicit approvals | Narrow Stage 01 authorization recorded; remaining guarded manifest awaits review |
| 2 Security | Safe YAML and redacted errors; no credentials or raw exception payload export |
| 3 No drift | Current implementation separated from proposed successor; CrewAI ownership retained |
| 4 Learning first | Explain public final methods versus abstract hooks; observable manual gates |
| 5 Isolated integrations | Wrapper handles CrewAI boundary; no Langfuse/provider client added |
| 6 External configuration | App-root YAML and selected workflow schemas; established overlay/env rules preserved |
| 7 Quality gates | Strict Pyright, Ruff, pytest and current release checks remain required |
| 8 Evidence | Documentation checks and future application tests recorded separately |
| 9 Incremental scope | Children, recovery, context and agent integration are deferred explicitly |
| 10 Local first | Deterministic workflows remain runnable without model/service credentials |
| 11 No silent migration | Historical stage material retained; no sandbox migration |
| 12 Traceability | Governing documents, placement, contracts and per-file changes recorded |
| 13 Sandbox isolation | No access or testing dependency on personal examples |
| 14 Official documentation | No runtime guide changes before support exists; exact future guide impact listed |
| 15 Honest status | Proposed design is not presented as implemented, verified or merged behavior |

Governing sources: root/design AGENTS, charter, principles, architecture, project structure, roadmap/progress, governance contract/register and Stage 01 architecture/plan. Observability exploration and relevant agent-execution notes were consulted for the separation of execution evidence, telemetry projection and runtime clients; detailed agent-event/harness machinery is not adopted.

## Langfuse and context handoff

The next agent can work on local Langfuse setup independently, then integrate against the approved workflow contract after this refactor.

- Application assembly creates shared clients/connections. Later run context supplies them and correlation metadata to each workflow; workflows should not each initialize independent Langfuse clients.
- Central public lifecycle methods are the future observation points. Keep subclass hooks focused on workflow work.
- Record phase start, successful end and failure once. A workflow is fully complete after validation and serialization, not merely after kickoff.
- Keep lifecycle failures distinct from configuration/selection/JSON failures that may occur before a wrapper exists. An outer run observation must also cover those rejected attempts.
- Preserve exception cause for local debugging; export only deliberately redacted diagnostics.
- Workflow wrapper phases and CrewAI step/agent spans are different levels. Later agent integration must use its own execution boundary/CrewAI evidence, without making wrapper status control agent scheduling.
- Context owns transient logger/client/connection objects. Typed CrewAI state owns business data that future persistence may need.
- Workflow ID (configuration selection) is not run identity. Decide correlation with the existing CrewAI execution identity at the context stage; avoid introducing duplicate unrelated IDs here.
- Decide exporter failure/flush policy, secret redaction and SDK pin compatibility in the Langfuse design. No logger backend, event bus, observer interface or empty context placeholder is added now.

## Deferred feature requests

| Feature request | Future questions and acceptance |
|---|---|
| Configurable composite/child workflows | Input mapping, sequential/parallel semantics, output aggregation, child validation timing, errors and trace relationships. CrewAI must own orchestration. Not part of this refactor. |
| Recovery/resume | Verify pinned CrewAI persistence/checkpoint behavior; persist needed state; interrupt and resume a real run; test which completed work repeats and side-effect idempotency. Wrapper enum is not a checkpoint. |
| Reuse/reset and async/concurrent invocation | Define a deliberate policy if required; current instances represent one attempt and concurrent calls on one instance are unsupported. |

These are feature-request records, not claims that GitHub issues have been filed or implementation scheduled.

## Documentation verification

The docs-only update must pass Atlas reference/hierarchy/guard/freshness checks, links for the new package, and a changed-file scope review. Check that all lifecycle transitions and public/hook names agree across documents and the living record.

No runtime tests or type checks are claimed for this documentation-only change. Their concrete acceptance cases are in test-plan.md. Final review and explicit go-ahead remain the only user gates before implementation; failed technical gates during implementation must be resolved without hiding them behind casts, weakened tests or unapproved scope changes.

### Checks completed for this documentation update

Validated the staged documentation snapshot against main a4264ac. Atlas build and --check passed (references, hierarchy, registered guards, sandbox boundary and generated freshness). Local document-link checks found 44 valid relative links; Markdown fences and docs-only path scope passed. Lifecycle method coverage was checked across the design and test plan. No application tests, Pyright run, release build or browser visual verification was performed for this documentation-only update.
