# S03.M1 — Copyable Codex handoff

Contract revision: 6067fb652f0bffe2fa1f8a0e53f045a421a16f11. The recipe behavior was approved by Sharon; sending the prompt below explicitly authorizes this concrete revision. This file is a pointer and does not alter the pinned package. Stage Design PR #52 remains draft/open.

```text
You are the implementation orchestrator for S03.M1 in https://github.com/SharonLanger/agent-playbook.

I authorize the eight-recipe batch at contract revision 6067fb652f0bffe2fa1f8a0e53f045a421a16f11. This implements the diagrams and behavior I approved in the Stage 03 design conversation on 2026-11-15. Do not expand its scope.

Read and follow:
https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/governance/codex-handover-rules.md

Read these exact files at that revision:
- Design: designs/stages/03-orchestration-patterns/m1-recipe-batch/design.md
  https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/m1-recipe-batch/design.md
- Verification cases: designs/stages/03-orchestration-patterns/m1-recipe-batch/test-cases.md
  https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/m1-recipe-batch/test-cases.md
- Implementation plan: designs/stages/03-orchestration-patterns/m1-recipe-batch/implementation-plan.md
  https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/m1-recipe-batch/implementation-plan.md
- Requirements: designs/stages/03-orchestration-patterns/README.md
  https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/README.md
- Decisions/approval history: designs/stages/03-orchestration-patterns/decisions.md
  https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/decisions.md
- Approved diagram reference: designs/stages/03-orchestration-patterns/diagrams/approved-preview.html
  https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/diagrams/approved-preview.html
Also read the diagram provenance and repository diagram-authoring instructions linked in the package.

Refresh repository instructions and inspect current main. Last inspected main: 4ed7a318e25653d481705d9cb40c35de9ab649c7. Create impl/stage-03-recipe-batch from current main and one PR targeting main titled "[Stage 03 · M1] Standalone CrewAI recipe cookbook". Assess intervening changes; do not merge the design branch into implementation.

Implement all eight together. Move the existing eight example folders into concepts/ without behavioral changes and repair required links. New Python code belongs only inside each recipes/ recipe folder, including temporary verify.py. No application runtime/config/registry changes, dependency upgrades, real agents, logging, Langfuse or recovery features.

Each recipe README starts with its matching approved diagram immediately below the title, then a short practical learning guide. Official documentation links go at the bottom. Preserve the approved diagram topology and meaning; deliver portable SVG assets with each copied recipe.

Include temporary verify.py scripts in the pushed implementation for me to run. Run and document the specified checks, including direct/copy runs and expected failures. Do not add recipes to application gates or run unrelated application regressions. Do not delete temporary scripts at the first handoff. Their deletion happens after my hands-on review, before merge, with evidence preserved.

Use gpt-6.1-sol for one coder and two independent reviewers: design drift, and test-gap/behavior verification. Use Sol for orchestration when selectable; otherwise report the actual orchestrator model. Both reviewers must inspect the same frozen candidate SHA and must not edit it. The behavior reviewer must map every test ID and independently run relevant checks.

Maximum THREE total coding/review rounds. Preserve all findings and reports under designs/stages/03-orchestration-patterns/m1-recipe-batch/reviews/. Stop as BLOCKED if required findings remain after round three; never reset the count. No fictitious PASS or claims for unrun checks.

Freeze the pinned contract. Record new design gaps separately in follow-ups.md and report them; do not edit design/requirements to match your code. Apply only the approved relocation/path repairs; no blanket guarded semantic changes.

Stage Design PR: https://github.com/SharonLanger/agent-playbook/pull/52
Keep it draft/open. Do not enable auto-merge or merge either PR.

Return ONE self-contained final-review handoff using the repository return template: implementation PR, contract/base/candidate/published SHAs, actual models, all round reports/verdicts, test-ID evidence, exact commands for me to run examples and temporary tests, failures/limits, pending cleanup and manual acceptance. Distinguish code candidate from any later report-only commits.

The originating Stage 03 design session will review your actual diff and evidence before we authorize cleanup/merge. Your completion state is READY FOR FINAL REVIEW or BLOCKED, never self-accepted or merged.
```
