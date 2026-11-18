# M3 plan and Codex handoff

## Authority and approval

Sharon approved the existing M3 behavioral design at `c516c94926af0355e387b3bbb92ac5d6118e7390` on 2026-11-18 and requested a separate M3 PR plus Codex instructions. The design explicitly listed unfinished technical choices. This preparation package records approval accurately and supplies proposed test cases. Follow [Codex handover rules](../../../governance/codex-handover-rules.md) and [stage/milestone workflow](../../../governance/stage-milestone-workflow.md).

Base main: `cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4`. Target main. Continue the separate draft M3 PR; do not merge the design branch wholesale. Design PR #51 remains draft/open. The full ACT rename belongs to issue #56.

## First task: finish the concrete design

Read current repo instructions, guarded authorities and approved design. Inspect actual current configuration loader/models and setup/management code, excluding personal examples and secret values.

Resolve and write concrete choices in this package:
1. Docker project ownership: two independent names versus a single aggregate Compose project. Establish the minimal main entry point that preserves approved independent behavior. Do not assume Compose include preserves two independent project identities. Verify chosen Compose semantics with official docs and a disposable config probe.
2. Exact config-to-Compose bridge: fields, loader reuse, selection behavior, disabled-component credentials, settings-to-container mapping and existing Langfuse compatibility. Avoid designing a full M4 CLI.
3. Existing volume and credential migration: old/new identity mapping, collision detection, no concurrent writers, preserving encrypted Langfuse data, conflict handling, non-destructive repeat execution and recovery instructions. Existing Docker secrets currently live separately from the application's secrets.file.
4. Concrete source paths, commands, schema additions, timeout/exit policy, required public docs and exact guarded logical amendments. Retain all existing project/file/path names; Docker components alone receive the new names.
5. Turn MC-01–12 into concrete checks against those choices and reconcile the implementation order.

Inspect existing owners:
- app/tooling/logging/compose.yaml
- app/tooling/observability/compose.yaml, manage.py, setup.py, README.md and tracked .env.example (never real .env)
- app/src/agent_playbook/config/loader.py, models.py, paths.py
- existing Langfuse CLI delegation and app/tests/tooling/test_langfuse_manage.py
- logging/Langfuse read-only connection checks
- app/docs/configuration.md, logging.md and setup/connection guides.

The user has authorized drafting the shared-configuration principle and AGENTS.md rule. Present exact amendments within the completed design; preserve historical Stage 02 contracts. Do not silently turn an unresolved ownership change into an approved implementation decision.

**Return the completed technical design/test/plan and unresolved policy choices to the originating design session before changing runtime code.** The guarded milestone workflow requires approval of a concrete revision. Do not describe the earlier behavioral approval as approval of subsequently invented migration/schema contracts. No runtime code, Docker data or credentials should be changed during this first task.

## Bounded independent review

Use Sol (gpt-6.1-sol when available) for delegated roles, record actual model IDs. One author/coder prepares the package; two separate reviewers inspect the same frozen candidate: design correctness/drift and test coverage. Maximum three total review rounds for this M3 delegation, including corrections; keep count across later continuation rather than resetting it. Reports under reviews/status.md and round-01/{implementation,design-drift,test-gap,orchestrator}.md; create later rounds only when used. During design completion explicitly label reports as documentation/design review, not runtime implementation PASS.

Once concrete approval is obtained, follow the same governance for coding and same-candidate independent reviews; do not assume unused review rounds grant scope or merge authorization. If the cap is reached, report BLOCKED.

## Concrete design gate and implementation sequence proposal

Freeze this design/test/plan candidate before two independent reviews. Reviewers inspect the same candidate SHA, then report design correctness and MC coverage separately; no runtime PASS can be granted in this phase. Publish reports under `reviews/` and distinguish candidate from report-only head. Do not edit runtime, guarded files or public shipped-behavior guides before Sharon approves this completed contract and each enumerated guarded logical amendment.

Implementation sequence after that approval:

1. Add narrow service-mode loader API and optional `local_service` typed blocks in `app/src/agent_playbook/config/{models,loader}.py`; adapt `app/application.yaml` with safe non-secret defaults and named references. Preserve workflow loader and existing env precedence. Test MC-02/05/06/07 fixtures first.
2. Add `app/tooling/services/manage.py` and private mapping manifest handling. Reuse `app/tooling/observability/{manage,setup,compose}.py/yaml`, `app/tooling/logging/compose.yaml` and `app/tooling/logging/check_services.py`. Force the two project names through `-p`; add external named volume interpolation and selected environment only. Wire direct Langfuse helper and its existing CLI delegation without changing CLI spelling. Validate migration and MC-01/03/04/08/09.
3. Update canonical user configuration, local Langfuse, logging and connection guides, tooling READMEs and `app/docs/cli.md` plus docs discovery. Apply only the separately approved guarded logical additions to principle 6, root AGENTS, architecture and project structure. Update status and Atlas after implementation evidence; preserve Stage 02 history.
4. Run `python3 designs/atlas/build.py --check` and app's maintained `app/.venv/bin/agent-playbook check` and `app/.venv/bin/agent-playbook test` with app/examples excluded. Run disposable `docker compose config --quiet` for both projects and relevant live checks when daemon available. Record exact revision, versions, failures and skips. Create Mac `.txt` in M3 for Sharon's real-data verification, including LG-10. Never use `down -v`.
5. Freeze code/test candidate; one coder and two independent Sol reviewers assess the same SHA, at most three rounds per the handover rules. Reports retained under `reviews/`; no merge or ready-for-review promotion without originating design-session final review and Sharon's later decision.

The current design-stage local probe used Docker CLI 29.9.2 / Compose v2.40.3. A second probe with a synthetic `/tmp/.env` and `COMPOSE_DISABLE_ENV_FILE=1` failed on the required missing `TARGET`, confirming default dotenv suppression in this installed Compose version. `docker compose config` ran without daemon; Docker API access was denied, so no live Docker or Mac acceptance was performed. Official semantics: [project name](https://docs.docker.com/compose/how-tos/project-name/), [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/), [external volume](https://docs.docker.com/reference/compose-file/volumes/), [down](https://docs.docker.com/reference/cli/docker/compose/down).

## Implementation order summary

The five steps above are the complete order. Use the exact proposed commands and migration gate in [design.md](design.md#exact-operator-commands-repository-root-proposal). Do not treat the design-stage reports as implementation evidence.

## Return format

Return one copyable LOGGING M3 — DESIGN COMPLETION HANDOFF first: PR and candidate SHA; behavioral approval revision; completed design/test/plan links; technical decisions and evidence; proposed guarded changes; each reviewer verdict and reports; rounds used; unresolved questions; exact scope for next approval. Clearly state runtime implementation NOT STARTED.

After actual implementation, use the full final-review return template in Codex handover rules. Distinguish candidate/published head, all MC IDs, failed/unrun evidence, models, rounds, branch drift and Mac/manual gap. Preserve M2 LG-10 until demonstrated.
