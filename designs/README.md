# Design workspace

Start with [AGENTS.md](AGENTS.md) and the [guarded design contract](governance/design-contract.md), then the core documents below. Open the [permanent Atlas](atlas/README.md) for Current and Explorations views.
The architecture describes the completed system. The roadmap describes how we build
and learn it. Progress records what has actually been accepted.

| Location | Purpose |
|---|---|
| [Workflow contract refactor](refactors/workflow-contract/README.md) | Completed and accepted ABC lifecycle and YAML contract; [A1–F6 mapping](refactors/workflow-contract/review-follow-up.md) and [Q1–Q4 test corrections](refactors/workflow-contract/review-test-quality.md) retain revision-specific evidence |
| [Runtime structure refactor](refactors/2026-11-12-runtime-structure/README.md) | Accepted runtime refactor record, exploratory future-tree proposal and revision-specific verification evidence |
| [project-structure.md](project-structure.md) | Guarded folder ownership, dependency rules and current source layout |
| [architecture.md](architecture.md) | Components, ownership, execution, errors, data and integration boundaries |
| [diagrams/](diagrams/README.md) | Animated SVGs, static SVGs and a local visual viewer |
| [Diagram authoring](diagrams/AUTHORING.md) | When and how future agents use Dashmotion and Animated SVG |
| [learning/](learning/README.md) | Plain-language explanations spanning the whole system |
| [charter.md](charter.md) | Purpose, outcomes and scope |
| [principles.md](principles.md) | Engineering and approval rules |
| [roadmap.md](roadmap.md) | Incremental learning and implementation order |
| [progress.md](progress.md) | Current stage status, accepted work and historical revision-specific evidence |
| [stages/00-environment/architecture.md](stages/00-environment/architecture.md) | Stage 00 development-foundation end state |
| [stages/00-environment/plan.md](stages/00-environment/plan.md) | Stage 00 substages and acceptance criteria |
| [stages/00-environment/findings.md](stages/00-environment/findings.md) | Executed experiments and limitations |
| [Stage 01 — CrewAI Flows](stages/01-crewai-flows/README.md) | Completed and accepted stage; permanent architecture, learning, workflow contracts, test specification, diagrams and code-reading guides |
| [../AGENTS.md](../AGENTS.md) | Repository operating instructions |

## Viewing diagrams

New and updated visual explanations embed animated SVGs directly in Markdown, including
the Stage 01 architecture and lessons. Static siblings remain available. The optional local
HTML viewers add pause/resume controls without a server, installation or external requests.
Some Markdown viewers suppress SVG animation; the browser viewer remains a fallback.

## Stage documents

Each stage has its own end-state architecture and plan, plus findings and learning
exercises. Future implementation baselines wait for their stage. Explicitly requested optional research/POCs belong in explorations and must not be mistaken for approved targets.
The historical [sandbox](../sandbox/) is outside the active application architecture.

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
