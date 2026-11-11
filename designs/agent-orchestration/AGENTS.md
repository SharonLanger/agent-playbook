# Design Workspace Instructions (Draft)

1. Before work, read `charter.md`, `architecture.md`, `principles.md`, `roadmap.md`, and `progress.md`.
2. The charter, target architecture, and principles become protected after explicit user approval. An active stage's architecture and committed design become protected only after their separate approval.
3. Never silently modify protected text. Present the **exact line-level additions, edits and deletions** and obtain explicit user approval **before** applying them.
4. Check proposed changes against the approved target and active stage baselines. Stop and escalate contradictions; do not resolve them by quietly changing the baseline.
5. Learning experiments and findings may evolve without approval if they do not modify protected files or committed design. Experimental results are not approved architecture.
6. Do not start implementing a stage before its design has been reviewed, explicitly approved, and locked.
7. Use configurable integration boundaries; never hardcode provider endpoints, tokens, or environment-specific details. Do not commit secrets.
8. Maintain deterministic regression tests and record verified evidence; do not mark tasks complete based on assertions alone.
9. Keep progress and findings editable, distinguishing hypotheses from verified observations.
10. Never treat Markdown instructions as sufficient technical enforcement: use review and repository controls where available.

This file is a proposal; it does not authorize changing the existing legacy playbook or any protected baseline.

## Stage documentation and learning visuals

- Keep implementation-facing instructions (`plan.md`, approved `architecture.md`) distinct from learner-facing explanations under each active stage's `learning/` directory. Use `findings.md` for observations and experiment evidence.
- Create learning materials when they genuinely clarify a concept, API path, state transition, or experiment; do not generate filler documents.
- Prefer Mermaid for compact static graphs and self-contained CSS-animated SVG assets referenced from Markdown for moving execution/data-flow explanations. SVG assets must work without JavaScript, remote dependencies, or external network calls; verify rendering in a local browser and, where possible, JetBrains Markdown Preview. GitHub rendering may differ.
- Use available diagram skills/tools when applicable, but never claim a specific skill was used unless it was actually available and invoked. Keep an accessible static diagram or written explanation when animation is unsupported.
- Learner-facing documents explain **why and what happens**, with examples and experiments; implementation-facing documents define **what to build and how to verify it**. Both must remain consistent with the approved target and current stage baselines.
- Learning materials and findings are editable during experimentation; approved stage architecture and committed design remain protected.
