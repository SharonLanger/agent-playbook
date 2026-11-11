# Design Inventory

This folder is the documentation and learning source for the Agent Playbook project.

| File or folder | Purpose | Status |
|---|---|---|
| [charter.md](charter.md) | Project learning purpose, scope and selected tools | Proposed protected baseline |
| [architecture.md](architecture.md) | Target system components, boundaries and diagrams | Proposed protected baseline |
| [principles.md](principles.md) | Guardrails, approval rules, modularity and configuration | Proposed protected baseline |
| [roadmap.md](roadmap.md) | Provisional stages and learning progression | Editable |
| [progress.md](progress.md) | Verified progress, experiments, evidence and findings | Editable |
| [stages/](stages/) | Stage-specific architecture, plans, learner explanations and findings | Create when each stage begins |
| [../AGENTS.md](../AGENTS.md) | Agent operating instructions and protected-file change protocol | Root instructions |

## Stage documentation convention

Only the **current stage** gets a detailed design. Create `stages/NN-name/architecture.md`, `plan.md`, `findings.md`, and learner-facing `learning/` materials as needed. Review and explicitly approve its design before implementation, then guard it against unapproved edits. Future stages remain roadmap entries.

The corresponding executable project belongs in [../app/](../app/) once Stage 00 is approved.

The older experimental playbook is preserved in [../sandbox/](../sandbox/), outside this design's authority.
