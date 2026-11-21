# Development tooling

Checkout-only Python tools, excluded from the installed application Wheel.
Run scripts using the project interpreter. Working-directory-independent paths
are resolved from each script's location.

| Script | Purpose |
|---|---|
| `bootstrap.py` | Prepare the pinned environment and run checks |
| `checks.py` | Run the quality gate; accepts `check` (default) with selectors, `test`, or `format` |
| `version.py` | Update project and lockfile version together; exact version or `patch`, `minor`, `major` |
| `release.py` | Gate, build, hash and verify an isolated release |
| `verify_runtime.py` | Run all integrated workflow paths with a Python socket/DNS audit probe |
| `verify_wheel.py` | Verify an artifact's SHA-256 hash |
| `services.py` | Select enabled local services and delegate to their checkout-only managers |
| `service_runtime.py` | Shared Docker checks, deadlines and subprocess helpers for service managers |

Usage and CLI commands: [CLI documentation](../docs/cli.md).
The [local Langfuse deployment](observability/README.md) is the Stage 02 milestone 1 service setup.
The [local logging tooling](logging/README.md) provides VictoriaLogs service management and explicit diagnostic/smoke checks.

Daily entry points: `agent-playbook check`, `format`, `version patch`, and `release`. Scripts remain callable directly.
