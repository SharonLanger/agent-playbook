# PR #35 verification

Documentation/Atlas scope only. No application runtime, SDK execution, application tests or personal examples were read or executed for verification. No existing stage contract was edited. Runtime snapshot is main `6f16508`; PR #34 is a separate pending change at inspected head `59c6fff`.

## Checks performed on the final documentation change

- Atlas standard-library builder: generation and `--check` pass. It validates reachable hierarchy, allowed view statuses, source/guard references, sandbox inventory exclusion and generated freshness.
- Negative probes reject a current node mislabeled as exploration, a parent cycle and a personal-sandbox file in the inventory. A source-document change invalidates generated freshness; restoring it produces identical output.
- DOM simulation: all 12 Current and 18 Explorations locations render; view switching, breadcrumbs, candidate reviewer status/switch, tree expand/collapse, file search, motion selection and zoom pass without script errors.
- Five Dashmotion diagrams pass the convention's structural checker with zero violations. Ten SVGs parse as XML and contain no scripts. Diagram geometry is unchanged.
- Local Markdown links resolve against the main path inventory plus this change. Sandbox contents are never traversed.
- Existing stage files retain their original blobs; the guard register explicitly preserves them and covers omitted approved content.

Run from a complete repository checkout:

```sh
python designs/atlas/build.py --check
```

Open `designs/atlas/index.html`, toggle Current/Explorations, zoom through Application → Runtime → Execution in Explorations, and open Reviewer run. Inspect the per-view status and source links. Search `event_mapper` in the candidate file tree. Use the linked guarded documents for authority.

## Limitations and merge coordination

Browser rendering was not visually verified: Chromium launch was blocked by the environment's socket restriction. DOM simulation is not a screenshot/layout test. The diagram checker also does not measure text collisions. Approval/read compliance and semantic accuracy require review; the builder cannot establish them.

No new CI job is introduced. The required PR record and explicit local check make the procedure reviewable; they do not guarantee every agent client loads AGENTS automatically.

PR #34's latest examples-isolation follow-up is unverified according to its description. Its older test/release results are not evidence for that new head. Reconcile current paths, public docs and Atlas after #34 integrates; move its internal refactor guide out of app/docs. Keep PR #35 unmerged until Sharon reviews it.
