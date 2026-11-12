# Independent workflow sandboxes

Sharon approved separate, directly runnable examples after accepting and merging PR #30.
The entry point is [Workflow experiments — start here](../../../../app/examples/workflows/README.md).
Read that index, then open an example's run.py in PyCharm with app/.venv/bin/python.

## Scope and ownership

Eight independent learning folders live under app/examples/workflows, the existing
checkout-only examples boundary. They use no application runner, workflow registry,
CLI dispatch, shared example helpers, real agents or Langfuse integration. All example
assets, tests and configuration stay with that example; only navigation and the test
collection command are shared. The existing integrated WF-01/02/03 remain unchanged.
These are authorized experiments, not a revision of the protected Stage 01 baseline or
an implementation of future stages. Project structure and principles are not edited.

The first four examples teach sequence/data passing, method references versus strings,
router labels, and the deliberate name collision Sharon explored. The next four adapt
the official CrewAI routing-patterns page: bounded loop, nested join, chained routers,
and combined routing/join/persistence. The last replaces upstream model work with a
fixed Python calculation and explicitly restores SQLite state in a second flow instance.

## Principle review

| Principle | Evidence in this change |
|---|---|
| Explicit approvals | User requested this separate examples PR after reviewing the self-contained design. |
| Security from the start | No secrets/model credentials; telemetry/tracing defaults off; generated SQLite ignored inside example 08. |
| No design drift | Existing runtime contracts and protected files unchanged; experiments stay in the approved examples boundary. |
| Learning first | README per example, editable input, direct run.py, source attribution and animated trigger graphs. |
| Isolated integrations | Direct CrewAI API use is the object of these experiments; no runtime provider integration or shared abstraction is introduced. |
| External configuration | Each folder has settings.toml plus validated environment overrides, loaded before framework imports; workflow inputs are separate JSON. |
| Reproducible quality gates | Existing dependency pins retained; Test/Check collect the colocated example tests; strict checks include examples. |
| Evidence over claims | Copied-folder subprocess tests check behavior; observed order is not presented as a general scheduling guarantee. |
| Incremental scope | No Langfuse, agent SDK, retry service or production recovery implementation; routing/persistence remain isolated experiments. |
| Local-first | Runs use local installed dependencies and deterministic Python; turning on telemetry/tracing can enable network activity. |
| No silent migration | Historical sandbox and existing runtime workflows remain unchanged. |

## Evidence and limits

The initial 14 cases passed in 122.72 seconds. They cover exact sequence/data, ordinary
return values versus router labels, both routing outcomes, collision behavior, bounded
loop termination, nested conditions, all three order routes, and persisted state restoration.
Two further collision variants change only the ordinary return payload or only the method
name. Tests copy one entire example to a temporary location and launch its run.py from a
different working directory with PYTHONPATH cleared; they do not invoke the application CLI.
The installed interpreter/dependencies are shared intentionally.

Each example contains HTML with pause controls, an embedded animated SVG and a static SVG.
Dashmotion's pinned renderer/checker produced 24 final artifacts with zero violations.
Edge-label bounding boxes were checked numerically for overlap after positioning labels
near their owning source/target. Standalone SVGs remove SMIL dots, retain CSS dashed-edge
motion gated by reduced-motion preferences, and carry a dark background. Animation is
illustrative. It neither measures execution timing nor proves concurrency. The collision
diagram shows the default score-80 path; the nested condition's 'either' box is a logical
condition, not a Python method. MIT notices travel with each folder.

All 41 relative Markdown links in the example collection resolve; all 16 SVGs parse.
Runtime import inspection found no dependency on agent_playbook, tooling or other examples.
An offline uv wheel build produced 54 entries / 21,540 bytes; inspection confirmed it
contains no example code, tests, TOML/JSON input, diagrams or SQLite database. This was a
wheel packaging check, not another full release/install certification.

The official 1.15.40 Flow page and the skills routing guidance differ in their descriptions
of or_. The latter reports tests on 1.15.22/23. These examples test our installed 1.15.40;
they do not claim behavior across all versions. Terminal calls lists are maintained by
our code and are not causal tracing. macOS PyCharm button behavior and animation rendering
in Sharon's Markdown viewer remain user review items.

Final full gate: Pyright 0 errors; Ruff lint and formatting passed; **132 tests passed in 221.20 seconds**, including all 16 example cases. Both collision mutations passed: changing only the returned payload preserved revise; changing only the method name removed that trigger.
