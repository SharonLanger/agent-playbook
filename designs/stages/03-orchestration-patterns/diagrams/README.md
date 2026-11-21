# Approved diagram reference

Sharon approved all eight diagrams in the conversation on 2026-11-15 and requested this exact diagram at the top of each recipe README. [approved-preview.html](approved-preview.html) preserves the original graph definitions, node labels, topology and selector; only a standalone page/theme wrapper was added for portable viewing.

This is a visual design reference, not recipe code or execution evidence. Diagram order maps to C01–C08. User-facing recipe assets must be portable SVGs beside each recipe, following [diagram authoring](../../../diagrams/AUTHORING.md), with readable layout, correct edges/labels, reduced motion and static fallback. Preserve the accepted design; do not replace it with a different graph.

Preview verification from the originating turn: JavaScript syntax passed; all eight selections were exercised at two widths with a DOM smoke check and node-boundary checks (16 cases). Browser screenshot verification was blocked by the environment's Chromium socket restriction. No Dashmotion pipeline or runtime Flow test was run for this preview. Implementers must render and inspect the final delivered SVG assets and report actual checks.

C05's sibling outcome was explicitly left “To verify”; native behavior must be observed on CrewAI 1.15.40 and honestly annotated. C02 is best-after-all, C06 counts all five outcomes before applying threshold, and loops are bounded normal workflow routing. These meanings are approved; no automatic cancellation or exception recovery is implied.
