# Design workspace

Start with [AGENTS.md](AGENTS.md) and the [guarded design contract](governance/design-contract.md), then the core documents below. Open the [permanent Atlas](atlas/README.md) for Current and Explorations views.
The architecture describes the completed system. The roadmap describes how we build
and learn it. Progress records what has actually been accepted.

| Location | Purpose |
|---|---|
| [PR quality and local versions](refactors/pr-ci/README.md) | Accepted implementation in #64, design closeout and remaining public activation checks in #62 |
| [Workflow contract refactor](refactors/workflow-contract/README.md) | Completed and accepted ABC lifecycle and YAML contract; [A1–F6 mapping](refactors/workflow-contract/review-follow-up.md) and [Q1–Q4 test corrections](refactors/workflow-contract/review-test-quality.md) retain revision-specific evidence |
| [Runtime structure refactor](refactors/2026-11-12-runtime-structure/README.md) | Accepted runtime refactor record, exploratory future-tree proposal and revision-specific verification evidence |
| [Logging M3 contract](https://github.com/SharonLanger/agent-playbook/tree/c4e0951bd87c81e627d58127841494d4812732ab/designs/refactors/logging/m3-service-composition) | Approved service-control baseline, candidate status in [progress](progress.md#logging-m3-implementation-candidate--2026-11-21) |
| [Project refactor](refactors/project-refactor/README.md) | Stage document structure, existing-stage alignment and the learning and sandbox migration in draft PR #59 |
| [project-structure.md](project-structure.md) | Guarded folder ownership, dependency rules and current source layout |
| [architecture.md](architecture.md) | Components, ownership, execution, errors, data and integration boundaries |
| [diagrams/](diagrams/README.md) | Animated SVGs, static SVGs and a local visual viewer |
| [Diagram authoring](diagrams/AUTHORING.md) | When and how future agents use Dashmotion and Animated SVG |
| [Architecture walkthrough](architecture-walkthrough.md) | Plain-language example connecting one run to the target architecture and execution diagram |
| [charter.md](charter.md) | Purpose, outcomes and scope |
| [principles.md](principles.md) | Engineering and approval rules |
| [roadmap.md](roadmap.md) | Incremental learning and implementation order |
| [progress.md](progress.md) | Current stage status, accepted work and historical revision-specific evidence |
| [Stage 00 — Development environment](stages/00-environment/README.md) | Accepted foundation; seven substages, learning, plan and evidence |
| [Stage 01 — CrewAI Flows](stages/01-crewai-flows/README.md) | Accepted workflow batch; five substages, contracts, verification and code-reading guides |
| [Stage 02 — Langfuse](stages/02-langfuse/README.md) | Accepted local setup, connection and mock work, execution context and native tracing |
| [Stage 03 — Orchestration patterns](stages/03-orchestration-patterns/README.md) | Accepted standalone CrewAI recipe batch; requirements, decisions and closeout evidence |
| [../AGENTS.md](../AGENTS.md) | Repository operating instructions |

## Viewing diagrams

New and updated visual explanations embed animated SVGs directly in Markdown, including
the Stage 01 architecture and lessons. Static siblings remain available. The optional local
HTML viewers add pause/resume controls without a server, installation or external requests.
Some Markdown viewers suppress SVG animation; the browser viewer remains a fallback.

## Learning

The [system-wide walkthrough](architecture-walkthrough.md) connects the diagrams to one concrete run. The [target architecture](architecture.md) defines the system boundaries. For stage exercises and code-reading guides, start with [Stage 00 learning](stages/00-environment/learning/) and [Stage 01 learning](stages/01-crewai-flows/learning/), or open the relevant stage index above.

## Stage documents

For new stages, follow the [stage layout](governance/stage-milestone-workflow.md#1-shared-workspace-and-ownership). Keep stage-specific learning and research with their stage when there is material to retain. The [exploration index](explorations/README.md) tracks cross-cutting research and POCs as non-binding material. Each stage README is the entry point for its milestone status, next action and the original stage architecture, plans and evidence.

Future implementation baselines wait for their stage except for the scoped Stage 04 foundation exception in [roadmap.md](roadmap.md#sequencing-and-approval).
The [root sandbox](../sandbox/README.md) holds historical references and draft ideas outside active application work.

## Stage, refactor and milestone working process

Read the [stage, refactor and milestone working method](governance/stage-milestone-workflow.md) before planning a stage, independent refactor or milestone. Calling work a refactor triggers its [startup procedure](governance/stage-milestone-workflow.md#independent-refactors): `refactors/<slug>/`, requirements and decisions, optional research/learning, and either one root design/test/plan package or milestone folders. The same approval, freeze, review and design-PR closeout gates apply. It defines shared requirements and decisions, the milestone/status table and next action in the stage README, milestone folders and incremental approval. Before delegating implementation, read the [Codex handover rules](governance/codex-handover-rules.md) for the Sol roles, independent reviews, three-round cap, permanent reports and handoff templates. Existing approved packages retain their established layout.

## Permanent material and handoffs

Stage packages belong permanently in `stages/`, including while their designs are under review.
Keep lessons, examples, diagrams and findings with their stage for future contributors and agents.
Approval changes document status, not retention or location.

`temporary/` is reserved only for disposable agent-to-agent handoffs. Transfer any lasting
knowledge into permanent documents before deleting a handoff. Handoff cleanup must not remove
stage designs or learning material.


## Mandatory reading and discovery

Read charter, principles, architecture, project structure, roadmap and progress, then the applicable approved stage design. Consult the [exploration topic index](explorations/README.md) for relevant earlier reasoning. Follow the [guarded-file register](governance/guarded-files.md); historical protection survives stale headings and moves.

- [Permanent Atlas](atlas/README.md): maintained Current/Explorations navigation.
- [Design contract](governance/design-contract.md): mandatory placement, approval and maintenance flow.
- [Explorations](explorations/README.md): optional research, not project commitments.
- [Atlas change record](refactors/atlas/README.md): approval scope and verification for #35.

Official product documentation lives in app/docs; internal/refactor review material belongs here. Personal examples are not a source to inspect during architectural discovery.
