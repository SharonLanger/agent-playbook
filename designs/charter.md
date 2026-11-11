# Charter — Proposed Protected Baseline

Status: **DRAFT / AWAITING EXPLICIT APPROVAL**

## Purpose
Learn open-source agent orchestration incrementally by designing, experimenting, implementing and verifying a real, reusable local-first engineering environment.

## Learning and engineering outcomes
- Understand CrewAI Flows through deterministic, inspectable exercises.
- Observe executions through Langfuse before introducing real agent SDKs.
- Progress toward independently configurable, testable workflows and interchangeable external integrations.
- Keep future directions open, including harness engineering, without committing to their designs today.

## Scope and boundaries
- Selected orchestration framework: **CrewAI Flows (Python)**.
- Selected initial tracing/observability backend: **Langfuse**.
- Python code should use strict static checking, formatting, linting, and deterministic regression tests.
- Real Claude/Codex agent execution is deferred until orchestration and observability have been learned independently.
- No fixed final acceptance checklist or detailed future-stage designs yet.
- Existing playbook experiments remain historical and separate.

## Governance
Target architecture and principles are controlled after approval. Current stage design is drafted, reviewed, explicitly approved, and then locked before implementation. Experiments may suggest changes but never silently change approved baselines.
