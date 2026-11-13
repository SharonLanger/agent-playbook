# Architecture Atlas — review package

Status: draft proposal. This is a separate documentation PR based on main; PR #34 is being handled independently. Future runtime ownership uses its explicitly labeled snapshot. No future runtime code is implemented.

## Read and review

1. [Sandbox and official documentation policy](documentation-and-sandbox-policy.md): Sharon’s current constraints and gaps in older wording.
2. [Architecture placement protocol](architecture-placement.md): how agents move from purpose and high-level ownership to a file.
3. [Architecture guide](architecture-guide.md): components, events, adapters, reviewer/verifier scenarios and research.
4. [File structure](full-file-structure.md): candidate paths; personal examples contents are excluded.
5. [Exact governance proposal](governance-proposal.patch): proposed principle/structure/public-index edits against the recorded main snapshot. Review and reconcile with #34 before applying; it has not been applied to guarded files.

## Open the interactive atlas

After checking out this PR, open `designs/refactors/atlas/architecture-atlas.html` in a browser. On macOS, from the repository root:

```sh
open designs/refactors/atlas/architecture-atlas.html
```

No server, installation or external assets are required. GitHub shows HTML as source; use a local checkout or download this directory. Architecture blocks drill into owners; breadcrumbs return upward. The Reviewer run tab explains a concrete invocation; Files searches the proposed hierarchy; Detailed guide contains the complete explanation. Diagram controls select motion and zoom. Static and animated SVGs and standalone viewers are in `diagrams/`.

## What this PR changes

Adds this review package, links it from designs/README.md, and adds the directly requested sandbox/public-docs instructions to AGENTS.md. It does not alter sandbox contents, application code, quality-gate configuration or PR #34. Existing test/gate cleanup is a separate coordinated task; this PR does not claim it is complete.

Public documentation impact: no supported runtime behavior changes in this PR. Internal architecture review belongs here. PR #34’s refactor-review.md should move into its own design/refactor directory in the thread handling that PR.

The Markdown authorities govern design. The atlas illustrates them and clearly labels proposals. See [verification](verification.md) and [third-party notices](THIRD-PARTY-NOTICES.txt).
