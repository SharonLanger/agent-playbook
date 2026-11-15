# Project Charter

Status: **GUARDED.** Governed by [design contract](governance/design-contract.md).

Purpose and scope of the target application.

## Purpose
Learn open-source agent orchestration incrementally by designing, experimenting, implementing and verifying a real, reusable local-first engineering environment.

## Learning and engineering outcomes
- Understand CrewAI Flows through deterministic, inspectable exercises.
- Observe executions through Langfuse before introducing real agent SDKs.
- Progress toward independently configurable, testable workflows and interchangeable external integrations.
- Build a small shared execution foundation and common harness in Stage 04; keep advanced harness capabilities open for Stage 06+. Detailed milestone designs require separate approval.

## Scope and boundaries
- Selected orchestration framework: **CrewAI Flows (Python)**.
- Selected initial tracing/observability backend: **Langfuse**.
- Python code should use strict static checking, formatting, linting, and deterministic regression tests.
- Real Claude/Codex agent execution is deferred until orchestration and observability have been learned independently.
- No fixed final-product acceptance checklist. Future-stage implementation commitments follow the roadmap, including its specific Stage 04 foundation exception. Explicitly requested research and POCs may be preserved as non-binding explorations; they are not project goals or implementation authorization.
- Existing playbook experiments remain historical and separate. `app/examples/` is Sharon’s personal sandbox, accessed only for explicitly requested work.
- Maintain an understandable architecture and accurate official product documentation. Keep implementation evidence, approved design and optional explorations distinct.
- Langfuse remains the approved initial tracing choice while alternatives are investigated; exploration alone does not replace that decision.

## Governance
Target architecture and principles are controlled after approval. Approve the stage boundary first, then draft, review and explicitly lock each milestone design before its implementation. Stage 04 foundation milestones may progress early under the narrow [roadmap exception](roadmap.md#sequencing-and-approval); real SDK prerequisites remain unchanged. Experiments may suggest changes but never silently change approved baselines.


Changes to guarded meaning require Sharon’s explicit approval of the logical change per file; all existing stage protections remain. See the [guarded-file register](governance/guarded-files.md).
