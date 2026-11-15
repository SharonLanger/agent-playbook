# M1 implementation plan

**Draft — not an approved implementation handoff.**

Approval revision: absent. Implementation PR: not opened. Design PR #51 stays draft/open. Main at alignment: 4ed7a318e25653d481705d9cb40c35de9ab649c7; refresh before implementation.

1. Obtain approval of this design, test cases and plan at a concrete SHA. Resolve any changes before coding.
2. Refresh repository instructions/current main and exact dependency lock. Reuse [source notes](../research/2026-11-15-direct-otlp.md), record pinned artifact licenses. Do not upgrade unrelated Langfuse dependencies.
3. In a separate implementation branch/PR, add only the tooling Compose/smoke/README paths specified in [design](design.md), plus the needed aligned dependency and public developer reference. No production wiring.
4. Implement the small synthetic emitter, external local endpoint validation, dedicated provider/handler, bounded cleanup and explicit unconfirmed-delivery output.
5. Run LS-01–04 and appropriate Python checks. If Docker is unavailable, report LS-02 NOT RUN and provide exact local reproduction commands; never mark integrated acceptance complete.
6. Record implementation/review evidence in m1-configuration-sanity/reviews only when it exists. Update package progress and Atlas from actual evidence.
7. Return for final design review and Sharon's acceptance; do not merge either PR automatically.

Follow [Codex handover rules](../../../governance/codex-handover-rules.md) for a future implementation handoff: pinned approved contract, Sol coder and independent design/test reviewers, bounded three rounds and permanent evidence. This planning update does not start that process.

M2 will separately design production helper context, runner cleanup and outage behavior. Setup/management CLI, umbrella Compose migration and distribution remain deferred.
