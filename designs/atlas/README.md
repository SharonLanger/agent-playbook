# Architecture Atlas

Open **[index.html](index.html)** from a local checkout in your browser. No server or installation is needed. GitHub displays HTML source; download/checkout the folder first. Markdown guide links open separately in your editor or repository viewer.

- **Current** starts at repository ownership and zooms into merged application responsibilities. The runtime structure PR #34, workflow design PR #38 and workflow implementation PR #40 are merged; Sharon accepted Stage 01 after those merges. I-1–I-4 and Q1–Q4 verification remains attached to application revision `4775cbe`, where the 315-test gate and isolated release passed. Stage 02 was accepted and closed through [Stage Design PR #47](https://github.com/SharonLanger/agent-playbook/pull/47). Its [stage index](../stages/02-langfuse/README.md) links the merged setup, context and tracing evidence. Approved future integration boundaries are explicitly labeled.
- **Explorations** preserves candidate roles, executions, shared events, adapters, tools and deferred harness ideas. These may never be adopted. They are not approved architecture or a request to create all candidate files.
- **Reviewer run** switches to Explorations and walks through one candidate invocation.
- **Full file structure** searches and expands the selected view's inventory. Current excludes personal and root sandbox contents. The PR #59 documentation migration is merged. Explorations preserves historical paths and candidate ideas, including old shared-learning and root-sandbox paths from the [pre-migration main snapshot](https://github.com/SharonLanger/agent-playbook/tree/cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4).
- **Detailed guide** links the canonical contract and full agent/event research notes. Diagrams support pause/play and zoom; motion is illustrative, not live execution.

Current runtime paths and sandbox exclusions reflect the merged runtime. The [project refactor record](../refactors/project-refactor/learning-sandbox-migration.md) retains the documentation migration evidence for merged PR #59. The Atlas status labels distinguish implemented responsibilities, approved future boundaries and exploratory proposals; file inventory labels identify completed stage records and historical review evidence.

## Authority and maintenance

Read [design instructions](../AGENTS.md), the [guarded design contract](../governance/design-contract.md), the [guard register](../governance/guarded-files.md) and the [stage and milestone working method](../governance/stage-milestone-workflow.md). The Atlas is a projection, not a second architectural authority. Approved design, implemented behavior and exploration are distinct.

When adding a responsibility: identify its governing decision; consult [relevant explorations](../explorations/README.md); explain repository → component → subcomponent → file placement; get approval for guarded changes; implement within scope; update canonical documents, catalog, public docs and progress; verify. Routine helpers do not require a new architecture block.

1. Update the authoritative Markdown first within the approved scope.
2. Update `catalog.json`: hierarchy, concise summaries, status, source paths, snapshots and file inventories. Current paths must reflect the recorded implementation revision. Add meaningful scenario views to `template.html` and label their status.
3. Run `python designs/atlas/build.py` from the repository root.
4. Run `python designs/atlas/build.py --check`. Commit the catalog/template, source documents and generated `index.html` together.
5. Review semantic accuracy and approval evidence. The check detects broken hierarchy/references, missing registered guards, sandbox inventory leakage and stale generated output. It cannot prove that an agent read instructions or that a design is approved.

The builder uses Python's standard library. It reads only explicit document/diagram references; it never traverses app/examples. It does not run application gates. Diagram authors must also follow [the diagram convention](../diagrams/AUTHORING.md).

[Approval/change record](../refactors/atlas/README.md) · [Verification](../refactors/atlas/verification.md) · [Third-party notices](THIRD-PARTY-NOTICES.txt)
