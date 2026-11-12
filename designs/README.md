# Design workspace

Start with the [target architecture](architecture.md) and its visual collection.
The architecture describes the completed system. The roadmap describes how we build
and learn it. Progress records what has actually been accepted.

| Location | Purpose |
|---|---|
| [project-structure.md](project-structure.md) | Guarded folder ownership, dependency rules and current source layout |
| [architecture.md](architecture.md) | Components, ownership, execution, errors, data and integration boundaries |
| [diagrams/](diagrams/README.md) | Animated SVGs, static SVGs and a local visual viewer |
| [Diagram authoring](diagrams/AUTHORING.md) | When and how future agents use Dashmotion and Animated SVG |
| [learning/](learning/README.md) | Plain-language explanations spanning the whole system |
| [charter.md](charter.md) | Purpose, outcomes and scope |
| [principles.md](principles.md) | Engineering and approval rules |
| [roadmap.md](roadmap.md) | Incremental learning and implementation order |
| [progress.md](progress.md) | Verified state and outstanding acceptance |
| [stages/00-environment/architecture.md](stages/00-environment/architecture.md) | Stage 00 development-foundation end state |
| [stages/00-environment/plan.md](stages/00-environment/plan.md) | Stage 00 substages and acceptance criteria |
| [stages/00-environment/findings.md](stages/00-environment/findings.md) | Executed experiments and limitations |
| [Stage 01 — CrewAI Flows](stages/01-crewai-flows/README.md) | Permanent architecture, learning, workflow contracts, test specification and diagrams; design under review |
| [../AGENTS.md](../AGENTS.md) | Repository operating instructions |

## Viewing diagrams

New and updated visual explanations embed animated SVGs directly in Markdown, including
the Stage 01 architecture and lessons. Static siblings remain available. The optional local
HTML viewers add pause/resume controls without a server, installation or external requests.
Some Markdown viewers suppress SVG animation; the browser viewer remains a fallback.

## Stage documents

Each stage has its own end-state architecture and plan, plus findings and learning
exercises. Detailed future-stage design waits until that stage becomes current.
The historical [sandbox](../sandbox/) is outside the active application architecture.

## Permanent material and handoffs

Stage packages belong permanently in `stages/`, including while their designs are under review.
Keep lessons, examples, diagrams and findings with their stage for future contributors and agents.
Approval changes document status, not retention or location.

`temporary/` is reserved only for disposable agent-to-agent handoffs. Transfer any lasting
knowledge into permanent documents before deleting a handoff. Handoff cleanup must not remove
stage designs or learning material.
