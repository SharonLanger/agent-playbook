# Progress and acceptance

Updated 2026-11-12. This file records implemented behavior; architecture.md describes
the target system.

| Work | Verified state |
|---|---|
| 00.1 environment | PR #17 merged after user ran main |
| 00.2 CLI | PR #18 merged after user ran help and run |
| 00.3 Pyright | PR #19 merged; user ran Pyright in PyCharm and observed a type error |
| 00.4 pytest | PR #20 merged; user ran Tests in PyCharm and reported four passing tests |
| 00.5 Ruff | PR #21 merged; local IDE configuration was the latest user task |
| 00.6 local gate | PR #22 merged after user accepted the improved check output |
| 00.7 Wheel release | PR #23 merged after user built a release and accepted 00.7 |
| Shared IDE tasks | PR #26 merged; user restored configurations and accepted Stage 00 |
| Target architecture and visuals | PR #25 merged; diagrams and architecture are in main |
| Stage 01 implementation | PR #30 merged after user acceptance; WF-01/02/03, runtime configuration and release verification |
| Principles and compliance | PR #31 merged; security, external settings and principle-review rules |
| Independent workflow examples | PR #32 merged after Sharon reported everything working, including resized diagrams; 132 tests plus type/lint/format checks passed |

The user authorized preparing 00.3–00.7 sequentially. Their review and merge remain
one at a time. After each predecessor merges, retarget its successor to main and
carry any accepted corrections forward. Later stage branches contain older copies
of progress documents; reconcile them instead of restoring obsolete status text.

## Architecture documentation

The target architecture now separates components, execution/failure flow, and
observation flow. Static and animated SVGs share one generator; a local browser
viewer provides playback controls. PR #25 is merged; browser animation verification
remains pending.

Earlier Stage 00 approval is recorded by merged PR #15. Its architecture/plan still
contain historical approval wording, and its acceptance list retains a CrewAI import
item despite excluding CrewAI. Those protected stage files are unchanged in this
visual-documentation PR; their exact correction requires separate review.

## Next actions

Sharon accepted Stage 00 and approved the pre-Stage 01 folder refactor.
`project-structure.md` records the guarded layout. The refactor separates runtime
components from checkout-only tooling and examples, with reserved future folders.
PR #28 (CLI/tooling refactor) and PR #29 (Stage 01 design) are merged. Sharon approved
implementing all three workflows together and learning them sequentially. Stage 01 code
implements WF-01 sequence, WF-02 typed state and WF-03 exclusive routing, with strict inputs,
shared CLI dispatch and dependency-aware releases. See the permanent Stage 01 findings for
verification evidence and the code-reading guide for the learning order. Sharon accepted the
implementation and independent examples, reporting that everything works. The learning
material remains available for continued experiments; acceptance does not claim every topic
has been studied exhaustively.

The independent examples live in `app/examples/workflows/`, with colocated inputs, settings,
tests and compact diagrams. User-facing configuration instructions live in
`app/docs/configuration.md`; YAML stays in `app/configs/`. Documentation navigation is in
`app/docs/README.md`.

Next: discuss Stage 02 (Langfuse observability), agree on the first visible run/step/error
experiment, and approve its design before implementation. No Stage 02 integration has been built.
