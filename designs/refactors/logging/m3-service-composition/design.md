# M3 draft design — independent local services and shared configuration

Status: **Behavioral design approved by Sharon on 2026-11-18** at source revision `c516c94926af0355e387b3bbb92ac5d6118e7390`. Approval: “The design of m3 is fine with me. Please mark it and create the files in the new m3 PR and let me know what to give the Codex agent.” The listed remaining technical design choices are still unresolved; approval does not supply their missing answers. Complete and review the concrete design/test/plan before runtime implementation. M1 and M2 are merged; M2 live acceptance LG-10 remains NOT RUN.

The active M3 design-completion package is now in [PR #57](https://github.com/SharonLanger/agent-playbook/pull/57), initially pinned at `7c2872e71c3753d9924c9057412ef7130c4bca14`. Continue design/test/plan work there; this file preserves the approved behavior snapshot. PR #51 remains the overall logging design workspace.

## Confirmed behavior

- Docker component names selected: act-logs and act-langfuse. These are the only naming changes in M3.
- Repository, package, CLI, files, folders, user paths and broader documentation renaming are excluded from this design and tracked separately in [issue #56](https://github.com/SharonLanger/agent-playbook/issues/56).
- Each component starts and stops independently. A shared service-management entry point selects components using their integration configuration's enabled property.
- Service management is explicit; normal workflow execution does not automatically start Docker or introduce a health prerequisite.
- Stop remains possible after disabling an integration. Start/stop preserves stored data. Docker component renaming must not silently create duplicate stacks or empty replacement volumes.
- Reuse each component's Compose definition. Exact aggregate/project ownership must be verified; two independent project names must not be represented as already solved by one Compose include.
- Supply Sharon one plain-text Mac verification guide after implementation, containing exact commands, expected results, independent/combined operation, persistence checks and the remaining M2 live logging checks. Keep LG-10 open until actual evidence is recorded before finalizing design PR #51.

## Shared configuration and credentials — confirmed 2026-11-18

All integrations use the selected shared application YAML and its existing local-overlay/environment precedence. VictoriaLogs has a documented section alongside Langfuse and CrewAI: retain the existing provider-neutral integrations.logging section for its application logging settings. Do not introduce a second overlapping integrations.victorialogs configuration or a provider-specific loader.

Non-secret settings belong in shared application configuration. Tokens, passwords and other secret values belong in the same external secrets file selected by secrets.file, already used for Langfuse credentials and available to other integrations. YAML contains named references rather than literal secrets. Future components follow this same rule.

The current default remains ~/.config/agent-playbook/secrets.env. M3 preserves existing project, package, CLI, file and folder names and user paths; any broader naming migration belongs to issue #56. Shared-secret consolidation uses the existing configured secrets.file path.

The selected direct local VictoriaLogs deployment currently requires no credentials. Document this explicitly; do not invent a token/password or add authentication middleware merely to populate the section. If a later approved deployment needs credentials, it uses the shared secrets mechanism.

### Existing infrastructure discrepancy and migration requirement

Current application documentation explicitly separates Langfuse application keys from app/tooling/observability/.env infrastructure secrets. Therefore the requested shared-file policy is a change to deployment configuration ownership, not a description of completed behavior.

Before implementation, inventory only documented key names and setup/management code, never read personal credential values. Specify how existing Langfuse database passwords, encryption keys and other infrastructure credentials are retained in the selected shared secrets file. Do not regenerate existing values, overwrite unrelated entries, or silently resolve conflicting values. Define an explicit conflict/migration procedure.

Compose receives only the values needed by the selected component through the minimal supported bridge from the existing loader. Shared storage of secrets does not authorize injecting every credential into every container. Avoid another independently editable credentials file, custom parser, credential discovery or config registry. Concrete Compose input mechanics and compatibility with existing Langfuse setup remain to be designed and verified.

## Required permanent documentation and guarded amendments

The M3 implementation contract must include these locations and consequences:

| Owner | Required change |
|---|---|
| designs/principles.md, principle 6 | Make the shared application configuration, shared external secrets file and existing loader the required convention for current and future integrations. Preserve workflow-specific configuration ownership and documented environment overrides. |
| AGENTS.md | Require agents adding integrations or deployment tooling to reuse that convention, document configuration keys and secret references in the canonical guide, and preserve existing credentials during migration. Link to principle 6 and the public configuration guide. |
| designs/architecture.md and designs/project-structure.md | Reconcile configuration/deployment ownership where necessary; enumerate any concrete guarded changes before implementation. |
| app/docs/configuration.md | Canonical user explanation: YAML sections, secrets.file, path/precedence, safe placeholder examples, adding future integration credentials, and application versus deployment consumers. Replace the currently separate Docker .env guidance only when migration is implemented. |
| app/docs/logging.md and Langfuse setup/connection guides | Link to the canonical credentials section; explain VictoriaLogs currently needs no credentials and document the supported migration/setup procedure. |
| Setup examples/templates and documentation discovery links | Use placeholders and references only; no real secrets. Document M3 Docker names and behavior; retain existing project, package, CLI and path names. |

Sharon explicitly requested the guarded shared-configuration rule and AGENTS.md guidance, then confirmed shared YAML plus the same secrets file as Langfuse/CrewAI. This draft records that scope. Concrete protected-file amendments must remain inspectable and must not silently rewrite historical Stage 02 acceptance. Public guides must describe shipped behavior; this design draft does not claim migration has happened.

## Remaining design work

1. Resolve Compose aggregation versus independent project identity, preserving existing volumes and preventing duplicate active writers.
2. Define the minimal configuration-to-Compose bridge and its milestone boundary with M4 management CLI.
3. Specify safe consolidation of existing infrastructure secrets, including conflict handling and compatibility.
4. Define service selection, partial startup failures, repeat operations and bounded health reporting using existing checks.
5. Write exact tests and implementation plan, including live Mac verification and M2 LG-10 evidence.

## Change record and verification

Documentation-only addition under designs/refactors/logging/m3-service-composition. No application behavior, shared credential file, approved M1/M2 contract or guarded principle is changed by this draft. Relevant prior requirements are ACT-01–07 in ../action-items.md and the M2 shared configuration contract. No new research recommendation is adopted.

The Atlas currently indexes the logging package and its shared action items; this draft adds no implemented component/status claim or changes to existing Atlas source inputs. Register the complete M3 package in discovery/Atlas with its reviewed design/test/plan. Application tests and Docker acceptance are not run for this draft.
