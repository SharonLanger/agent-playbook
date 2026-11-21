# M2 implementation plan

**Approved M2 behavior and LOG-G01–06 on 2026-11-16; pin this concrete revision for the implementation handoff.**

Inspected main: 529fe15895afc8211d833fc2544e98f0d18fb451. Design PR: [#51](https://github.com/SharonLanger/agent-playbook/pull/51), draft/open. Approved design SHA: none. M1 PR #54 is draft and unmerged; Sharon observed the smoke record and matching correlation locally after the bridge-network fix. Remaining field-level inspection was consciously deferred.

## Work order

1. Review design/tests/plan together; pin the concrete revision; LOG-G01–06 were approved by Sharon on 2026-11-16. Confirm M1 artifact versions. Refresh main and instructions before implementation; preserve unrelated Stage 03/04 work.
2. Extend config/models.py and loader.py with LoggingSettings and documented overrides (no required_start). Update application.yaml; preserve existing invalid-config behavior and secrets handling. Add LG-04/05 coverage.
3. Add observability/logging.py with thin standard-level helpers, explicit ExecutionContext extraction, optional fields and native exc_info. Add real OTel in-memory export checks LG-01–03. No serializers, traceback construction or custom logger classes.
4. Add observability/adapters/otel_logging/runtime.py using SDK configuration/contextlib lifecycle. Reuse aligned SDK dependencies from M1. Configure endpoint/session isolation, logger propagation and disabled NullHandler behavior.
5. Integrate lifecycle and diagnostic placements in application assembly/runner. Preserve business exceptions and CLI output/exit codes. Use narrow native tracing failure containment for best-effort initialization and runtime warning policy; retain SDK tracing capabilities and automatic CrewAI instrumentation. Do not introduce a broker to make containment convenient.
6. Verify LG-05–09 and LG-11. If a pinned SDK boundary cannot meet the contract with small glue, report exact evidence and revise the draft with Sharon before expanding the implementation.
7. Perform LG-10 using M1, recording actual records and cleanup timing. If Docker is unavailable, return NOT RUN plus concrete reproduction instructions; do not claim integrated acceptance.
8. Apply only approved guarded amendments; update public configuration/usage/troubleshooting docs and discovery links. Add a concise SDK-oriented learning explanation here, not internal review notes in app/docs.
9. Run relevant tests and the repository's existing Python quality gate; keep the default checks independent of Docker and app/examples. Refresh Atlas/status from observed results.

## Handoff and review

Implementation belongs in a separate PR targeting current main, after refreshing main and resolving the M1 dependency without silently assuming it is merged. The plan must be converted into the fully filled immutable-link handoff prescribed by [Codex handover rules](../../../governance/codex-handover-rules.md). No placeholder handoff is ready now.

Follow its Sol orchestrator/coder and independent design-drift/test-gap reviewer roles, same frozen candidate, at most three rounds, and permanent reports under m2-application-logging/reviews. Those reports are created only when reviews run. Return for originating design review; user acceptance and merge are separate. PR #51 remains open until explicitly authorized.

## Exclusions and review emphasis

No custom queue, retry/transport/exception engine, generalized startup framework, Langfuse facade, public API/package delivery, M3/M4 infrastructure, Stage 04 event contract or sandbox edits.

Review code inventory against LOG-32: every new helper must implement context mapping, wiring or required failure containment. Tests target application promises rather than copying SDK behavior. Keep a diff-based record of which guarded additions were actually approved/applied.

LD27 update: add/reuse per-integration read-only check_connection methods and one opt-in app/tooling/logging/check_services.py script using existing validated configuration. Implement LG-12. Do not invoke checks from the runner or add a doctor coordinator/registry now. Required-start settings/overrides are removed from this plan. Later M4 can reuse these methods for CLI diagnostics.
