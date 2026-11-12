# Visual guide

Open **[index.html](index.html)** locally in your browser after checking out/downloading this
branch. No server or dependency installation is needed to view it. GitHub displays HTML source;
it does not host the interactive viewer. Markdown uses the static SVG siblings.

| Diagram | Teaches | Animated | Static |
|---|---|---|---|
| Shared architecture | One reusable shell selects one independent workflow | [HTML](00-architecture.html) | [SVG](00-architecture.svg) |
| WF-01 sequence | Return-value passing | [HTML](01-sequence.html) | [SVG](01-sequence.svg) |
| WF-02 state | Value/history after each operation | [HTML](02-state.html) | [SVG](02-state.svg) |
| WF-03 pass | Score 80 follows the pass branch only | [HTML](03-route-pass.html) | [SVG](03-route-pass.svg) |
| WF-03 needs work | Score 40 follows the other valid branch | [HTML](04-route-needs-work.html) | [SVG](04-route-needs-work.svg) |

Pause the background motion when reading. The numbered step notes explain expected values;
they are not synchronized runtime traces. Reduced-motion preferences stop motion.
The architecture illustrates one WF-02 journey; it does not start three workflows together.

## Authoring provenance

These diagrams use Dashmotion's pinned renderer, templates and structural checker, with
project-specific semantic graphs and explanatory notes. See [sources](../sources.md) and
[MIT notices](THIRD-PARTY-NOTICES.txt). The companion Animated SVG video pipeline was not run.
The static siblings remove moving-dot elements and animations while preserving the graph.

For changes, read [the permanent authoring policy](../../../diagrams/AUTHORING.md). Recreate
semantic graph inputs from these workflow contracts in a temporary authoring directory,
then run the pinned Dashmotion `scripts/layout.py <graph.json> --render <output.html>`.
Follow its flow/architecture reference for graph schema. Add local lesson/navigation text,
regenerate static siblings, and rerun `scripts/check_diagram.py` on every final animated file.
Keep the input graphs outside delivered outputs as directed by that authoring workflow.
