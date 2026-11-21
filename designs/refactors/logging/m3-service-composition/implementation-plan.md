# M3 Codex handoff

Start on the design branch of PR #57 with the revised design and test cases and Sharon's explicit disabled-start decision. The historical three rounds exhausted the previous delegation. A new bounded design review begins only on Sharon's instruction.

## Design completion
1. Read repository governance, the existing CLI dispatch, Langfuse management, YAML loader, VictoriaLogs Compose and health checks. Resolve exact entry points, repeat behavior, exit semantics and a complete readiness deadline using those existing owners.
2. Refine design/test/plan, check discovery and Atlas, and list any guarded-file changes requiring approval. Keep historical reviews intact.
3. Use one author and two independent reviewers (design correctness/drift and test coverage), both reviewing the same frozen revision. Cap the newly authorized design review at three rounds. Record reports under a distinct revised-contract path and report actual model IDs, verdicts and remaining findings.
4. Return the frozen contract and evidence to Sharon. Implementation requires approval of that exact design/test/plan revision. Keep PRs draft for her decision.

## Implementation after approval
Wire the three groups to the existing component operations. Add focused offline CLI checks and update the CLI and setup docs. Use a separate implementation PR with a coder and both independent reviewers. Supply one Mac verification text file with copyable commands, expected results, component isolation, persistence and pending M2 checks. Preserve honest live-test status.
