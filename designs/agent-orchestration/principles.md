# Engineering Principles — Proposed Protected Baseline

Status: **DRAFT / AWAITING EXPLICIT APPROVAL**

1. **Explicit approvals:** Never change an approved protected file without presenting each changed line and receiving explicit approval before editing.
2. **No design drift:** Implementation must conform to both the approved target architecture and the active stage's approved architecture. Conflicts pause implementation.
3. **Learning first:** Each stage includes learn, design, approval/lock, experiment, implementation, verification, and findings. Experiments are permitted without silently altering baselines.
4. **Isolated integrations:** Put each external provider behind a small, explicit interface/adapter. Workflow logic must not depend directly on provider-specific clients.
5. **Configurable environments:** Inject or load configuration for URLs, credentials, provider selection and settings. Use environment variables for secrets and environment overrides; do not commit secrets. Validate required settings on startup.
6. **Reproducible quality gates:** Strict static typing (initial candidate: Pyright), lint/format checks (Ruff), deterministic tests (pytest), and pinned dependencies (uv) are the planned foundation, subject to Stage 00 design.
7. **Evidence over claims:** Record actual test results, known limitations, and observed behavior. Never mark unverified work complete.
8. **Incremental scope:** Design future stages only when they become current. The roadmap is provisional and may be revised deliberately.
9. **Local-first:** Support local development and configurable service deployment; do not assume that using a remote model is offline.
10. **No silent migration:** Preserve historical playbook files and semantics during the proposed sandbox migration; do not delete or rewrite history without review.
