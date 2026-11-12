# Runtime configuration

Edit [application.yaml](application.yaml) to configure integrations. It is separate
from `pyproject.toml`, which owns the application version, dependencies and build settings.
Changing runtime settings takes effect on the next invocation of the same release:
no version bump or rebuild is needed. There is no background configuration server.

## Files and selection

| File | Purpose |
|---|---|
| `application.yaml` | Shared settings, reviewed and versioned in Git |
| `application.local.yaml` | Optional partial overrides for this machine; Git-ignored |
| `src/agent_playbook/config/` | Python loader, typed validation and CrewAI initialization |

Both `dev-run` and `run` accept `--config PATH`. The file selection order is:

1. Explicit `--config PATH`.
2. `AGENT_PLAYBOOK_CONFIG` environment variable.
3. In the source checkout, `app/configs/application.yaml`, found relative to the
   installed editable package, independently of the terminal's working directory.

The source CLI's `run` passes the selected external path to its installed child.
It does not copy settings into `app/dist` or validate a different release's schema.
When invoking an installed release directly, supply `--config` or set
`AGENT_PLAYBOOK_CONFIG`. Installed packages contain no active configuration file.
Relative explicit paths resolve from the invocation directory; use an absolute
path for a persistent environment variable. Upgrades/builds never rewrite your file.

From the repository root, using the CLI installed by bootstrap:

```sh
app/.venv/bin/agent-playbook dev-run
app/.venv/bin/agent-playbook run
app/.venv/bin/agent-playbook run --version 0.1.0 --config "$PWD/app/configs/application.yaml"
```

To use another shared file for both source and releases, set once in your terminal
or PyCharm run configuration:

```sh
export AGENT_PLAYBOOK_CONFIG="/absolute/path/to/application.yaml"
```

For a selected `name.yaml`, an optional sibling `name.local.yaml` is merged by key.
Local files are partial overrides, not standalone base files. Missing optional local
files are fine; unreadable or invalid existing files fail. Value precedence is:
**shared file → local file → documented environment overrides**.

## CrewAI settings

All three fields are required in the merged configuration; no duplicate defaults
are hidden in Python. The committed base file provides the safe initial values.

| YAML key under `integrations.crewai` | Default | Environment override | Framework mapping |
|---|---|---|---|
| `usage_telemetry_enabled` | `false` | `AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED` | Inverse of `CREWAI_DISABLE_TELEMETRY` |
| `tracing_enabled` | `false` | `AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED` | `CREWAI_TRACING_ENABLED` and flow `tracing` |
| `show_framework_events` | `false` | `AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS` | Inverse of flow `suppress_flow_events` |

Environment booleans accept `true` or `false` (case-insensitive). YAML booleans must
be actual booleans, not quoted strings or numbers. These application overrides take
precedence over file values. The two mapped native CrewAI environment variables
are outputs of initialization, not additional override sources. Framework-wide
controls such as `OTEL_SDK_DISABLED` remain outside our ownership and may still
disable telemetry; we do not force-enable global OpenTelemetry.

Unknown keys, wrong types, missing required values and invalid files fail with
configuration exit code 2 before workflow steps run. Older releases can reject newer
configuration schemas: sharing a file does not guarantee cross-version compatibility.
There is no automatic migration or silently ignored setting.

## Environment references and secrets

A CrewAI boolean may reference a variable by name instead of embedding its value:

```yaml
integrations:
  crewai:
    usage_telemetry_enabled: false
    tracing_enabled: false
    show_framework_events: {env: MY_FLOW_EVENTS}
```

Set `MY_FLOW_EVENTS=true` or `false`; a missing variable is an error. The documented
`AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS` override still wins if both are supplied.
This reference syntax is implemented by our loader, not automatically by YAML.

Stage 01 has no credential or machine-path fields to configure. Future integration
schemas must add those deliberately: keep secret values in environment variables
or a secret store and store only references in shared configuration. Keep local
paths in local overrides. Do not add tokens to YAML, even in ignored files, and do
not commit `.env` files. This loader does not read `.env`; export variables or use
PyCharm's environment-variable settings. Third-party libraries may have their own
`.env` behavior, so keep explicit application settings authoritative.

Errors report locations/types without echoing configuration values or YAML source
lines. Active configuration/local overrides are not bundled into wheels or release
directories. Git history records shared changes; ignored local overrides have no Git
history. These controls are boundaries, not a claim of comprehensive secret scanning.

## Workflow rules stay separate

WF-03's `PASS_THRESHOLD = 60` lives in its `steps.py`; score is per-run input. Neither
belongs under CrewAI. A future tunable workflow can own a separate validated section
or file. This stage adds no unused workflow configuration framework or speculative keys.

## Why initialization order matters

The runner loads/validates configuration, applies CrewAI startup environment settings,
and only then imports flow modules. Python imports can initialize library services,
so applying a setting afterward may be too late. Flow-instance options are also passed
explicitly. Importing the workflow package itself no longer changes the environment.

Each CLI invocation is a new process and reads current files. Within one Python process,
repeated runs may change per-flow event display, but changing telemetry/tracing after
CrewAI has been imported is rejected: restart the process. Direct Python callers must
configure startup before importing CrewAI; prefer the application runner. Help, version,
checks and release selection do not eagerly initialize the framework.

Tests and release verification use a dedicated offline fixture, independent of user
files and environment overrides. Enabling telemetry/tracing for a normal run can enable
network activity; the offline guarantee applies to the documented disabled configuration.

## Try it in PyCharm

1. Run **Dev Run** with the committed file: application step messages appear.
2. Create `app/configs/application.local.yaml` with only
   `integrations: {crewai: {show_framework_events: true}}`.
3. Run **Dev Run** again: additional CrewAI output appears; the workflow result is unchanged.
4. Run **Run** with an already built configuration-capable release: it reads that same file.
5. Remove the local override to return to the shared setting.

No new PyCharm task is required. Existing Run/WF tasks use the default selection;
add `--config` to their parameters only when selecting another file.
