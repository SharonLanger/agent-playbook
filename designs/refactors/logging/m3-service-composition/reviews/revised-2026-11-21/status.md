# Revised M3 design reviews — 2026-11-21

Sharon confirmed explicit `logs --start` while workflow logging is disabled and authorized a **new**, maximum-three-round design review. Historical proposal reviews in the parent `reviews/` remain intact and are not counted again. Runtime implementation NOT STARTED; SC-01–12 runtime/live acceptance and M2 LG-10 NOT RUN.

| Revised round | Frozen design/test/plan candidate | Design correctness/drift | Test coverage | Disposition |
|---|---|---|---|---|
| 1/3 | d96dc81b960e4296446c068646f30acb349417a3 | CHANGES REQUIRED | CHANGES REQUIRED | Corrected in round 2; reports retained |
| 2/3 | 877e86a2dce24c21102d881c8bca025e7b59bf53 | CHANGES REQUIRED | CHANGES REQUIRED | Corrected in round 3; reports retained |
| 3/3 | 407e0c417b4fd8da108135446afe707d1f067569 | CHANGES REQUIRED | CHANGES REQUIRED | **BLOCKED; cap reached** |

Both independent reviewers were configured as `gpt-6.2-sol`; served model metadata was unavailable. Author/orchestrator exact served model ID was unavailable. Each pair reviewed the same frozen SHA and made no edits. Later report/status commits change no design, tests, plan or runtime code.

Open: RD-03 and TG-SC-05. Outer CLI timeout/interrupt termination of the coordinator process group does not reach a component started in its own group. Explicit nested group cleanup and a test that forces the outer 1500/130-second timeout with a live nested child are required. All other revised findings were closed in reviewed documents. No fourth round without Sharon's explicit new decision. This candidate is **not approved for runtime implementation**.

Evidence: Atlas build and freshness PASS on reconciled current-main snapshot (main 46e9062d1fbedefbc04240c280d12001cfdea0ac). Synthetic daemon-free Compose v2.40.3 project-name probe showed default `observability`, file override `from-file`, and shell override `from-shell`. Application tests, live Docker/Mac and LG-10 NOT RUN. PR #57 and design PR #51 remain draft/open; neither merged.
