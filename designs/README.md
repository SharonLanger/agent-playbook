# Design workspace

Start with the [target architecture](architecture.md) and its visual collection.
The architecture describes the completed system. The roadmap describes how we build
and learn it. Progress records what has actually been accepted.

| Location | Purpose |
|---|---|
| [project-structure.md](project-structure.md) | Guarded folder ownership, dependency rules and current source layout |
| [architecture.md](architecture.md) | Components, ownership, execution, errors, data and integration boundaries |
| [diagrams/](diagrams/README.md) | Animated SVGs, static SVGs and a local visual viewer |
| [learning/](learning/README.md) | Plain-language explanations spanning the whole system |
| [charter.md](charter.md) | Purpose, outcomes and scope |
| [principles.md](principles.md) | Engineering and approval rules |
| [roadmap.md](roadmap.md) | Incremental learning and implementation order |
| [progress.md](progress.md) | Verified state and outstanding acceptance |
| [stages/00-environment/architecture.md](stages/00-environment/architecture.md) | Stage 00 development-foundation end state |
| [stages/00-environment/plan.md](stages/00-environment/plan.md) | Stage 00 substages and acceptance criteria |
| [stages/00-environment/findings.md](stages/00-environment/findings.md) | Executed experiments and limitations |
| [../AGENTS.md](../AGENTS.md) | Repository operating instructions |

## Viewing diagrams

Markdown embeds static SVGs for reliable viewing in PyCharm and GitHub. Each has
an animated sibling. Open `diagrams/index.html` in a browser to browse the moving
diagrams and pause/resume them. It needs no server, installation or external requests.
Some Markdown viewers suppress SVG animation; use the local browser viewer in that case.

## Stage documents

Each stage has its own end-state architecture and plan, plus findings and learning
exercises. Detailed future-stage design waits until that stage becomes current.
The historical [sandbox](../sandbox/) is outside the active application architecture.
