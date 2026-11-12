# Verification record

Verified 12 November 2026 on Linux, Python 3.13.5 and pinned uv 0.13.6.
Status: **Draft for Sharon's review; not accepted or merged.**

Tested implementation commit:
[`eb8c3df84268b3ce4b023767ea7172046c390462`](https://github.com/SharonLanger/agent-playbook/commit/eb8c3df84268b3ce4b023767ea7172046c390462).
Its Git tree was verified identical locally and on GitHub before release creation.
The follow-up commit only finalizes this evidence and progress documentation.

## Executed checks

| Check | Result |
|---|---|
| Source review helper, default mode | Passed; explicitly reported release checks NOT RUN |
| Pyright | Zero errors, warnings or information diagnostics |
| Ruff lint and formatting | Passed; 107 Python files |
| pytest | 137 passed; includes tests colocated with all eight independent workflow examples |
| Clean bootstrap from committed source, without an existing venv | Created environment from the pinned lock, ran default WF-01 and full gate; 137 passed in 66.10s |
| Final review helper with `--build-release` | Passed; release builder ran the full gate (137 passed in 66.24s), built and installed the wheel with locked/hash-checked dependencies |
| CLI smoke checks from an unrelated temporary directory | Help, version, console and direct package entry points, custom WF-02 input, invalid command and invalid WF-03 input all passed |
| Source and installed workflow probes | WF-01, WF-02, both WF-03 routes and invalid input checks passed; zero Python socket/DNS attempts |
| Installed identity and import isolation | Version/source commit matched manifest; package imported from the release venv |
| Installed development-command guards | `test`, `check`, `format`, `release`, `version patch` and `dev-run` rejected with exit 2 |
| Release artifact evidence | Wheel, requirements.txt and uv.lock hashes matched the manifest |
| Wheel contents | New application/release modules present; retired runner/selection absent; no tooling, tests, examples or active YAML |
| Source release discovery and launch | `run` selected the newly built release and executed WF-01 successfully |
| Documentation and IDE definitions | 110 relative Markdown targets valid; all 19 shared task XML files parsed |
| Repository checks | `git diff --check` passed; historical sandbox and independent example source files unchanged; proposal preserved byte-for-byte |

The additional regressions cover framework-free CLI imports, early unknown-workflow
rejection, legacy local-YAML detection without data loss, missing-release presentation
and configuration-error exit handling. Existing tests continue to cover workflow
results, routing, fresh state, argv boundaries, config precedence and release behavior.

## Release evidence

| Field | Value |
|---|---|
| Version | `0.1.0` (unchanged) |
| Wheel | `agent_playbook-0.1.0-py3-none-any.whl` |
| Wheel size | 23,373 bytes; this excludes the installed dependency environment |
| Wheel SHA-256 | `735fda7b40affd50cf6d9c349d8f8cc691e9a88b96ac584bd762fd468de6661c` |
| requirements.txt SHA-256 | `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840` |
| uv.lock SHA-256 | `5a234572faa5c3f13ddd8587f3f6f45a989d98ebece6d6fcca68e56b03c1207a` |
| Manifest verified | `true` |

The verification installation is generated under ignored app/dist; binaries are not
committed or published. The final evidence commit changes documentation only, so a
release you build after checkout will record that newer commit and its own wheel hash.

## Reproduce and remaining acceptance

Use [the review guide](../../../app/docs/refactor-review.md) for source-only, build-release
and existing-release commands. The script streams the quality-gate/build output and
returns a nonzero exit when a requested check fails. The existing-release mode is
provided but was not invoked separately; its shared verification path ran after the build.

Automated smoke checks use `tests/fixtures/offline.yaml`, not machine-specific settings.
The audit probe covers Python socket/DNS calls for these paths, not an OS network sandbox.
Dependency installation can use the network. Live telemetry/model integrations were not tested.

macOS/PyCharm buttons and Sharon's local configuration remain manual acceptance work.
Explicit old YAML paths in external scripts/settings must be updated; ignored local
YAML must be moved or merged deliberately. No existing releases or settings are deleted.
