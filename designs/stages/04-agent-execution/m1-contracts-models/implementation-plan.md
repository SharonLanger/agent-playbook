# S04.M1 implementation plan — draft, no handoff

**Entry gate:** Sharon approves the same pinned revision of [design.md](design.md), [test-cases.md](test-cases.md) and this plan after the open choices and any guarded amendments are resolved. The exact approval reference and SHA are pending.

## Planned work order

1. Confirm current main and Stage 04 records, actual package/import locations and guarded ownership changes. Present any needed architecture or structure amendment before implementation.
2. Implement the three separate abstract behavioral contracts and the callback type. Keep provider-specific types inside eventual adapters.
3. Implement the five frozen event models/union, result/status types and the approved request/settings/permission data. Validate only the agreed boundary semantics.
4. Add focused contract tests for the [acceptance cases](test-cases.md) in maintained `app/tests/`. Verify types with the repository's normal static checker. Keep the fake integration for M2.
5. Run the required local quality gate and document the actual revision and results, including anything blocked. Open a separate focused implementation PR against main, including the approved design commit link.

## Handoff and review

Once approved, freeze the governing documents and pin their full SHA for the implementer. An orchestrator assigns one coder and two independent reviewers for design drift and test gaps at the same implementation candidate SHA. Preserve reports for each used round and the three-round limit under [handover rules](../../../governance/codex-handover-rules.md). The design session then reviews the actual candidate for Sharon. Technical verification, Sharon's acceptance and implementation merge remain separate. If a new requirement arises during implementation, record it as a follow-up or explicitly pause and approve a new baseline.

**Not started:** no source files, executable tests, dependencies or runtime fixtures are created by this design PR. Exact Python model shapes, paths and test commands remain subject to the M1 design review.
