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
