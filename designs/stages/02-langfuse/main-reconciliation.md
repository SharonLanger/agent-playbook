# PR #36: approved main reconciliation

Sharon approved resolutions 1–6 on 2026-11-13 after reviewing the YAML,
configuration models and strict-loader differences. This reconciles PR head
`cc620df7270ec3d26f695ba656b68a75e5d4e82b` with main
`53764abeb9402d596ee26bef19872fc2ebd7d888`. PR #36 remains draft and unmerged.

## Applied resolutions

- Application YAML retains the workflow registry and default-disabled Langfuse
  settings as separate configuration sections.
- Models retain main's required workflow field plus Langfuse settings/validators;
  all required imports are combined.
- Loader retains main's StrictLoader and imports both Any and cast, preserving
  duplicate/non-string/merge-key rejection and Langfuse overrides/key resolution.
- Progress retains both dated histories and identifies the current state.
- Atlas retains both inventories without duplicate paths and updates current
  refactor/pending-Langfuse status. HTML is rebuilt from the combined sources.
- Main-only runtime, tests, fixtures, release checks and guarded design files are
  retained verbatim. PR-only Langfuse work is preserved. Version remains 0.1.2;
  SDK 5.2.0 and uv 0.13.6 pins remain unchanged.

## Verification

The combined source was assembled from hash-verified GitHub file versions in an
isolated workspace; normal Git HTTPS authentication was unavailable.
`uv sync --directory app --locked` passed on CPython 3.13.5.
Pyright and Ruff lint/format passed; pytest reported **329 passed**.
The maintained source runtime verifier passed every built-in, both aliases and
both conditional routes, invalid input exit 2, execution error exit 1 and zero
Python socket/DNS attempts. This is not an OS network-isolation guarantee.
Release verification and final GitHub tree/parent evidence will be recorded
before the implementation handoff is declared ready.

## Scope and next agent

This addresses review R2 (main integration), subject to completion of the final
verification above. R1 (SDK lifetime/export), R3 (false delivery-success reporting)
and R4 (remaining stale stage prose) are deliberately not fixed by this merge.
No manage.py, Langfuse CLI action, real workflow/context integration or agent SDK
execution was added. No live Langfuse ingestion, Mac UI or persistence acceptance
is claimed. The four-item original review remains dated evidence.

The next agent should follow steps 2–5 of
[verification-simplification-plan.md](verification-simplification-plan.md), once
Sharon supplies the implementation instruction. The earlier pause to agree on
these six conflicts has been satisfied. Do not redo it or restore the older
branch. Refresh actual refs first; surface any newly introduced conflict before
resolving it. Keep the PR draft and unmerged.

The charter, principles, merged guarded workflow contract and project structure
were consulted. The observability exploration does not approve a broader event
or harness model. This reconciliation changes no guarded meaning beyond taking
main's already approved files verbatim. Public configuration guides retain both
branches' documented settings; no new supported command is introduced here.
