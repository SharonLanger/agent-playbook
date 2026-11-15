# Engineering Principles

Status: **GUARDED.**

Rules for developing and evolving the application.

1. **Explicit approvals:** Before editing guarded meaning, explain the logical additions/removals and consequences for each affected file and obtain Sharon’s explicit approval. Retain an inspectable diff; line-by-line presentation is not mandatory. All existing guards remain, including historical stages and approved content moved elsewhere.
2. **Security from the start:** Never commit secrets or expose them in logs or release artifacts. Keep credentials external, use safe defaults, and avoid shortcuts that would require a security redesign later.
3. **No design drift:** Implementation must conform to both the approved target architecture and the active stage's approved architecture. Conflicts pause implementation.
4. **Learning first:** Each stage includes learn, design, approval/lock, experiment, implementation, verification, and findings. Experiments are permitted without silently altering baselines.
5. **Isolated integrations:** Put each external provider behind a small, explicit interface/adapter. Workflow logic must not depend directly on provider-specific clients. Approved native Langfuse instrumentation may directly use the SDK at the reviewed application runner/assembly boundaries; configuration and resource policy remain centralized in the Langfuse adapter. This tracing exception does not relax agent execution adapter isolation.
6. **External configuration:** Keep third-party integration settings in configuration files, with documented environment overrides and startup validation. Keep workflow-specific settings separate; these may be named constants or workflow configuration.
7. **Reproducible quality gates:** Strict static typing (Pyright), lint/format checks (Ruff), deterministic tests (pytest), and pinned dependencies (uv) form the development foundation.
8. **Evidence over claims:** Record actual test results, known limitations, and observed behavior. Never mark unverified work complete.
9. **Incremental scope:** Commit to stage implementation designs when their stage becomes current, except for independently approved Stage 04 foundation milestones under the narrow [roadmap exception](roadmap.md#sequencing-and-approval). Actual dependencies and milestone design/implementation gates still apply; this grants no exception to other future stages or real native integration. Explicitly requested future research/POCs may be documented as non-binding explorations; they are not roadmap commitments. The roadmap is provisional and may be revised deliberately.
10. **Local-first:** Support local development and configurable service deployment; do not assume that using a remote model is offline.
11. **No silent migration:** Preserve historical playbook files and semantics during the proposed sandbox migration; do not delete or rewrite history without review.


12. **Mandatory design traceability:** Follow the [design contract](governance/design-contract.md): load governing documents, identify decisions, consult relevant explorations, explain placement and contracts, obtain required approval, maintain records, verify and report. New files are not placed by convenience alone.
13. **Personal sandbox isolation:** `app/examples/` is Sharon’s sandbox. Agents access it only for a specific explicit request. Application tests, fixtures, coverage, setup, gates and releases must be independent of it. Explicit user-requested sandbox lint/format is allowed outside automated gates.
14. **Maintained official documentation:** `app/docs/` contains public product guides only. Every change assesses documentation impact; update affected guides, links and Atlas/design records in the same PR or give a specific no-impact reason. Surface discrepancies between approved design and implementation.
15. **Honest design status:** Distinguish implemented/verified behavior, approved design awaiting implementation and non-binding explorations. Atlas/catalog content cannot approve a decision. Preserve prior reasoning and revision-specific evidence without presenting either as a current promise.
