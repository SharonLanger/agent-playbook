# Architecture Atlas

Open **[index.html](index.html)** from a local checkout in your browser. No server or installation is needed. GitHub displays HTML source; download/checkout the folder first. Markdown guide links open separately in your editor or repository viewer.

- **Current** starts at repository ownership and zooms into current application responsibilities. It uses main `a4264ac` (PR #35 merged, PR #34 runtime preserved) for runtime paths. Approved future integration boundaries are explicitly labeled. The workflow-contract package is approved design; PR #40 is implemented and under review, with lazy-import/error/test follow-up pending. Its unmerged runtime is not presented as the merged baseline.
- **Explorations** preserves candidate roles, executions, shared events, adapters, tools and deferred harness ideas. These may never be adopted. They are not approved architecture or a request to create all candidate files.
- **Reviewer run** switches to Explorations and walks through one candidate invocation.
- **Full file structure** searches and expands the selected view's inventory. Current excludes personal and historical sandbox contents; candidate paths are based on the older PR #34 snapshot `30c8d96` and are historical possibilities.
- **Detailed guide** links the canonical contract and full agent/event research notes. Diagrams support pause/play and zoom; motion is illustrative, not live execution.

PR #34 is accepted and merged at `96cb1f8`. Current paths and sandbox exclusions reflect that implementation. Temporary review task/helper removal is approved; standard application checks remain.

## Authority and maintenance

Read [design instructions](../AGENTS.md), the [guarded design contract](../governance/design-contract.md) and [guard register](../governance/guarded-files.md). The Atlas is a projection, not a second architectural authority. Approved design, implemented behavior and exploration are distinct.

When adding a responsibility: identify its governing decision; consult [relevant explorations](../explorations/README.md); explain repository → component → subcomponent → file placement; get approval for guarded changes; implement within scope; update canonical documents, catalog, public docs and progress; verify. Routine helpers do not require a new architecture block.

1. Update the authoritative Markdown first within the approved scope.
2. Update `catalog.json`: hierarchy, concise summaries, status, source paths, snapshots and file inventories. Current paths must reflect the recorded implementation revision. Add meaningful scenario views to `template.html` and label their status.
3. Run `python designs/atlas/build.py` from the repository root.
4. Run `python designs/atlas/build.py --check`. Commit the catalog/template, source documents and generated `index.html` together.
5. Review semantic accuracy and approval evidence. The check detects broken hierarchy/references, missing registered guards, sandbox inventory leakage and stale generated output. It cannot prove that an agent read instructions or that a design is approved.

The builder uses Python's standard library. It reads only explicit document/diagram references; it never traverses app/examples. It does not run application gates. Diagram authors must also follow [the diagram convention](../diagrams/AUTHORING.md).

[Approval/change record](../refactors/atlas/README.md) · [Verification](../refactors/atlas/verification.md) · [Third-party notices](THIRD-PARTY-NOTICES.txt)
