# Sandbox and official documentation policy

Sharon's explicit requirements, recorded 13 November 2026.

## Personal examples sandbox

`app/examples/` belongs to Sharon. Without an explicit request scoped to that directory, agents must not read, search, inspect, execute, test, lint, format, import, edit or maintain its contents. Broad repository searches and quality gates must exclude it. An authorized task there permits only the requested work; it does not make examples part of application maintenance.

Do not add or maintain tests inside examples. Application regression tests and their fixtures belong in `app/tests/`, must be self-contained, and must not depend on mutable examples. Changes or failures in the sandbox must not block application quality gates, builds or releases. Existing tests/integration with gates require an explicit, separately reviewed cleanup; this PR does not inspect or alter sandbox contents. PR #34 is being handled separately.

## Official product documentation

`app/docs/` is Agent Playbook's maintained public documentation for new and existing users. Document supported CLI commands, configuration, setup, workflows, outputs, errors, troubleshooting and user-relevant architecture. State the supported version/scope where behavior differs.

Internal review notes, temporary verification instructions, handoffs and unapproved future proposals belong under `designs/`, in their owning stage/refactor, never under `app/docs/`.

Every change requires a documentation-impact assessment. Changes to supported behavior, configuration, command syntax/defaults, installation, workflows, public contracts or user-relevant architecture must update the affected official guides, examples in those guides, links and indexes in the same PR. Internal changes with no user-visible effect must record why no guide changes are required. Do not add a meaningless documentation edit merely to satisfy a checkbox.

The approved design governs intended behavior; implementation and verified behavior establish what is currently available. Official documentation must reflect those authorities accurately. If they disagree, surface and resolve the mismatch; do not silently turn an implementation bug or an unapproved proposal into documented truth. Keep links to canonical definitions rather than maintaining competing copies. Future architecture stays labeled in designs until approved and implemented as appropriate.

## Existing gap and concrete cleanup

Current main's project-structure table explicitly allows tests in examples. Its docs wording says user-facing but does not prohibit internal material or require change-by-change synchronization. The charter does not define either directory boundary in this detail. AGENTS.md protects historical sandbox material but does not currently give `app/examples/` the requested exclusion.

PR #34's `app/docs/refactor-review.md` is specific to that refactor, not a reusable public refactoring manual. Its intended home is `designs/refactors/2026-11-12-runtime-structure/review.md`. Move it and update its backlinks in the agent/thread handling #34, or a coordinated follow-up after its state is settled. Do not race that PR from this branch. General supported commands belong in the public CLI guide; internal verification instructions remain with the refactor.

## Guarded-document alignment

`governance-proposal.patch` presents exact proposed principle/structure wording against main at 6f16508. It is a review artifact, not an applied patch. Reconcile with the final #34 changes before applying it. The current direct user instructions apply to this work even while older guarded wording awaits that review.

The charter can remain focused on purpose and scope. Put enduring engineering constraints in principles, directory ownership in project-structure, operational instructions in AGENTS.md and public navigation in app/docs/README.md. This avoids duplicating the full policy in every file.
