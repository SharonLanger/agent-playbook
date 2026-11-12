# External configuration — review and verification

Sharon approved external YAML, separate integration/workflow ownership, settings
independent of release versions, documented environment overrides, and initialization
before CrewAI imports. Configuration code/design/learning remain in PR #30. General
principles and AGENTS compliance instructions are independently reviewable in PR #31.

## Principle assessment

| Principle | Application and evidence |
|---|---|
| Explicit approvals | Implements the configuration proposal approved in this conversation; the folder and stage documentation now record that decision. General protected wording is isolated in PR #31. |
| Security from the start (PR #31) | Safe YAML loading, typed validation, private error output, ignored local overrides and external credentials; no credential fields or secrets introduced. Active settings are excluded from wheels/releases. No claim of comprehensive secret scanning. |
| No design drift | Stage architecture and guarded structure describe the approved `configs/` boundary and startup contract. |
| Learning first | Configuration guide explains hierarchy, precedence, startup and a PyCharm exercise; code guide points beginners to concepts before CLI internals. |
| Isolated integrations | CrewAI environment mapping lives in `config/crewai.py`; workflow steps do not read integration settings. |
| External configuration | Required typed integration settings come from YAML/local/environment sources. WF-03 retains `PASS_THRESHOLD` in its own code. |
| Reproducible gates | PyYAML is explicitly pinned to the already locked 6.0.3; dependency lock/export and clean-commit release behavior remain. Tests use an offline fixture instead of user preferences. |
| Evidence over claims | Executed results and limitations appear below; historical Stage 01 findings retain their original scope. |
| Incremental scope | No configuration server, automatic reload, speculative workflow configuration framework, provider credentials or future-stage SDK work. |
| Local-first | Shared defaults disable telemetry/tracing. Users may enable them; offline claims apply only to the disabled configuration. |
| No silent migration | Historical sandbox and prior playbook semantics are untouched; old release argv behavior is preserved. |

The charter already requires independently configurable workflows; no duplicate
charter change was needed. Tests alone do not establish this assessment: file
placement, secret boundaries and approved design scope were reviewed separately.

## Verification

Verified on Linux x86_64 with Python 3.13.5, CrewAI 1.15.40, Pydantic 2.12.5,
PyYAML 6.0.3 and uv 0.13.6. Application version remains 0.1.0.

| Check | Observed result |
|---|---|
| Full release quality gate | Pyright 0 errors; Ruff lint/format pass; **116 tests passed** |
| Configuration tests | Nested local overlays, explicit path/environment precedence, env references, reload, invalid/missing/unknown fields, private errors and safe YAML tags pass |
| Startup ordering | Fresh subprocess verifies settings applied before CrewAI import; invalid config imports no framework; changed startup settings in an initialized process fail clearly |
| Clean committed release | Wheel built, hashed and installed with locked production requirements; 138 runtime packages consistent |
| Installed runtime probe | WF-01, WF-02 and both WF-03 routes pass; invalid input exits 2; zero audited Python socket/DNS attempts |
| Same installed release, edited external file | Additional framework output appears after changing `show_framework_events`; result remains `[Hello, workflow!]`; no rebuild or version bump |
| Installed file selection | Direct invocation without a selector fails with configuration exit 2; source launcher succeeds with default and explicit shared paths from outside the checkout |
| Source isolation | Temporary source-only message edit changes dev-run output; installed release still returns the original message; edit restored |
| Packaging | Wheel: 21,502 bytes, 54 entries; no active/local YAML, `.env`, test or tooling files |
| Legacy argv boundary | Launcher adds no new CLI options to a bare old-release invocation; explicit config paths remain separate argv entries |

The verified local release source commit is
`f7a640b6591725154c0aae08cd8ff62108a6f18c`. The local checkout is reconstructed for
verification, so the GitHub commit SHA differs. Runtime Python sources and settings
are compared with the uploaded tree; documentation-only updates followed the release.
Historical measurements in findings.md describe the earlier 17 KB wheel, not this build.

- Wheel SHA-256: `a5e57a22484a14d1bb2de91075a185ca062b1adfc68588f8aa9f9fcec45ea20c`.
- Requirements SHA-256: `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840`.
- Lock SHA-256: `5a234572faa5c3f13ddd8587f3f6f45a989d98ebece6d6fcca68e56b03c1207a`.

Production requirements are unchanged: PyYAML was already in CrewAI's locked closure
and is now explicitly declared because the application imports it directly.

## Practical limits

- Each invocation reloads files; a running process does not hot-reload.
- A reused Python process cannot change CrewAI startup telemetry/tracing after import;
  it receives a clear restart error. Per-flow event display may vary between calls.
- A shared file can be rejected by an older release with a different schema.
- Direct installed invocations need `--config` or `AGENT_PLAYBOOK_CONFIG`; source
  launchers pass the external path automatically. No active settings are bundled.
- The network probe observes Python socket/DNS audit events, not all possible native
  network behavior. Enabling real telemetry export is outside this offline verification.
- Stage 01 has no token/path fields. Future integrations must explicitly introduce
  validated secret references and local paths; unused infrastructure was not added.
- Linux verification does not certify macOS PyCharm UI behavior.
