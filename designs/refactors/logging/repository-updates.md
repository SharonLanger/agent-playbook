# Repository impact and principle assessment

## Placement and authority

Read root/design AGENTS, design-contract, guarded-files, charter, principles, architecture, project-structure, roadmap/progress, Stage 02 architecture/milestones/closeout, stage-milestone-workflow and codex-handover-rules. Consulted observability exploration and agent-execution notes; reuse correlation/log-versus-trace reasoning, not superseded broker/exporter proposals.

Repository → designs → refactors → logging owns this separate package, as requested and already assigned in closeout. Inputs: handover and repository evidence. Outputs: draft requirements/decisions/research/history. No runtime contracts, dependencies or failure ownership change; eventual logging failure policy remains open.

| Surface | Impact |
|---|---|
| Logging package | New canonical workspace for logging discussion; no approved runtime baseline |
| designs/README and exploration index | Add discovery links; preserve other-stage records |
| Atlas catalog/generated HTML | Add exploration-only logging navigation; regenerate |
| Project progress and Stage 02 records | No edit: closeout already records independent logging ownership |
| Guarded authorities | Unchanged; later concrete amendments need explicit approval |
| app/docs | No impact: no supported behavior, command, configuration or installation changes |
| Runtime/dependencies/tests | No change; implementation not authorized |
| Personal examples / historical sandbox | No content access or modification |

## All-principle assessment

| Principle | Assessment |
|---|---|
| 1 Approvals | No guarded meaning changed; concrete implementation approval remains required |
| 2 Security | LOG-10 retains secret exclusion and payload-policy gate |
| 3 No drift | Existing context/native tracing preserved; unresolved choices visible |
| 4 Learning | Research before selection; no fabricated results |
| 5 Integration isolation | Native tracing exception preserved; logging boundary to design |
| 6 External configuration | LOG-14 reuses existing ownership |
| 7 Quality gates | Documentation/Atlas checks now; runtime gate not applicable to unchanged code |
| 8 Evidence | Repository observations separated from handover and unrun research |
| 9 Incremental scope | Separate logging workstream; no new numbered stage |
| 10 Local-first | LOG-08 constrains research |
| 11 No silent migration | Historical files preserved |
| 12 Traceability | LOG/LD/LQ/R IDs and linked records |
| 13 Sandbox isolation | Personal example contents not inspected |
| 14 Documentation | Specific public-doc no-impact reason; design/Atlas navigation maintained |
| 15 Honest status | Draft, reopened and deferred choices labeled |

## Verification

Baseline: main 4ed7a318e25653d481705d9cb40c35de9ab649c7.
Documentation checks PASS: Atlas build and freshness/reference/hierarchy/guard/sandbox checks; 55 relative Markdown links checked against the baseline tree plus new package; whitespace across 9 Markdown files. Application tests, service startup and external product research are NOT RUN; no implementation or user acceptance claimed.

## Follow-up research/documentation update

Added LOG-15–20, LD10–14, action items, dated follow-up and official-source research. No guarded/runtime edits. Later Compose migration must preserve the current observability project/volume identities; future implementation changes public setup/CLI guides, but these design notes do not invent supported commands. Source research completed; runtime probes and exact artifact-license audit not run. Prior verification above describes the initial commit only; new documentation checks accompany this update.

Follow-up checks PASS: Atlas generation/freshness/references/guards; 23 relative links plus fences/whitespace across 10 package files. Research/configuration examples are illustrative and unexecuted.

## Runner / direct OTLP / M1 draft update

Recorded LD15–19 and LOG-21–25; superseded the collector-first recommendation while preserving its dated research. Added M1 design/test-cases/implementation-plan and current direct-OTLP source notes. Runner initialization is agreed direction; exact production context and outage contracts remain open. No guarded file, runtime, dependency or public supported behavior changed. The existing all-principle assessment still applies; M1 supplies its specific assessment.

Verification: Atlas build and --check PASS; 32 relative links in the logging package checked against known repository paths, plus Markdown fences/trailing whitespace PASS. Docker is absent; runtime smoke and application tests NOT RUN (documentation-only update). PR #51 remains draft/open; no concrete milestone approved or implementation started. Shared project/stage status remains accurate and needs no change.

## M2 draft and settled SDK-first choices

Main refreshed to 529fe15895afc8211d833fc2544e98f0d18fb451; intervening Stage 03 changes do not alter the inspected runtime/config/context or governing instructions. Added M2 design/test/plan, LD26/LOG-31/32, source evidence for native exception conversion and a dated alignment record. Current package progress/README and Atlas now distinguish settled choices from draft implementation contracts.

No guarded document changed. M2 lists LOG-G01–06 for review before implementation, including the narrow Langfuse failure-policy follow-on. No public supported behavior changed, so app/docs remains untouched in this documentation PR. All-principle assessment is included in M2; SDK reuse is an explicit acceptance constraint. No application tests or local service checks have run for this update.

M2 documentation verification: Atlas build and --check PASS; 42 relative links across 22 logging-package Markdown files PASS; fences/trailing whitespace PASS. Source evidence only for SDK exception capture. Application/SDK integration tests and Docker smoke NOT RUN. PR #51 remains a draft design workspace.
