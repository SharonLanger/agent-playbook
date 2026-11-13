# Architecture placement protocol

Status: proposed workflow for review. Existing guarded documents remain authoritative; future Atlas components are candidates, not approved implementation.

Before adding or relocating a responsibility:

1. Read the charter, principles, architecture, project structure and active stage design. Identify the goal, constraints and authorized scope.
2. Start at the repository boundary: design, runtime, developer tooling, tests or official user documentation. `app/examples/` is excluded unless Sharon explicitly requests a specific task there. Do not read it to discover placement.
3. Zoom into the owning component and then its subcomponent. State what responsibility it owns and which existing boundary supports that choice.
4. Define inputs, outputs, contracts and allowed dependencies before choosing a class or filename. Reuse an existing owner where its responsibility fits.
5. If no boundary fits, propose the missing responsibility and exact guarded-document changes. Do not silently create a new architectural layer.
6. Check roadmap/stage authorization. This user-requested future atlas does not authorize implementing future stages.
7. Assess public documentation impact for every change. Update affected official guides in the same PR, or give a concrete reason why no public documentation changes are needed.
8. Update design navigation and relevant behavioral checks. The HTML must agree with the Markdown authorities; it cannot approve a boundary.

## Placement record

Use a short paragraph for ordinary additions; a table for a new boundary:

| Field | Required explanation |
|---|---|
| Purpose | Charter objective and relevant principles |
| Placement | Repository → component → subcomponent → file |
| Contract | Inputs, outputs, dependencies and failure ownership |
| Stage | Current implementation or explicitly requested future proposal |
| Documentation | Guides changed, or a specific no-impact reason |
| Verification | Appropriate checks and actual evidence |

Example: a Claude event mapper is runtime execution integration, under `app/src/agent_playbook/execution/adapters/claude/event_mapper.py`. It maps native messages to execution events and must not import reviewer domain models. Reviewer reactions belong under `agents/reviewer/`.

## Enforcement

AGENTS.md directs agents to this process. PR review requires the placement and documentation-impact records. Automated link checks and import-boundary checks can support review when introduced, but cannot prove that documentation is complete or that ownership is correct. No new automated enforcement is implemented in this documentation PR.
