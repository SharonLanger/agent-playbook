# Architecture diagrams

Open **index.html** from this folder in a browser to view the animated collection.
Use its Pause motion button or Static view button. All assets are local; no network,
fonts, JavaScript libraries or setup steps are required. Reduced-motion preferences
hide moving markers automatically; static labels and arrows remain complete.

| View | Static | Animated |
|---|---|---|
| Target system | [SVG](01-system.svg) | [SVG](01-system.animated.svg) |
| One workflow run | [SVG](02-execution.svg) | [SVG](02-execution.animated.svg) |
| Execution observation | [SVG](03-observability.svg) | [SVG](03-observability.animated.svg) |

The dots indicate direction, not timing or live status. The system view's links
show responsibility/dependency relationships; only the execution view describes
routing. Static variants are embedded in architecture.md for reliable Markdown
preview. Use the local viewer for motion; Markdown viewers may suppress animation.

Static SVGs were rendered and visually inspected. SVG structure, variant parity,
reproducible generation and viewer JavaScript syntax were checked. Interactive
browser verification is still pending: Chromium could not launch in the authoring
environment. Check tab switching, Pause motion, Static view and reduced-motion
behavior when opening the gallery locally.

## Updating

Edit `render.py` and run `python3 designs/diagrams/render.py` from repository root.
It regenerates both SVG variants from the same nodes/edges. Regenerate the viewer
with `python3 designs/diagrams/build_viewer.py`. Both use the standard library only.
Keep architecture.md and its explanatory tables consistent with diagram changes.
