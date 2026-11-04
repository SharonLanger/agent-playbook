# Maintaining This Repository

Keep role instructions in `agents/`, coordination instructions in `workflows/`, and project-specific rules in `projects/`.
Keep the orchestrator limited to launching agents and following explicit workflow routes; pass specialist instruction paths without reading or pasting their contents.
Do not turn examples or placeholders into finalized behavior without a requested change.
Files marked `UNIMPLEMENTED` do not define runnable roles or workflows.

Use exact project folder names (for example, `system-one-harness`). Feature folders use `f-<number>-<slug>`, numbered within each project with at least two digits and a lowercase slug of at most three words. Design lookup and saving instructions are in `agents/designer.md`.
