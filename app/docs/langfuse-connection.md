# Check a Langfuse project connection

The project check runs only when explicitly requested. It verifies project
authentication without sending traces or connecting workflows automatically.
Use a project API key pair from Langfuse project settings. Those project keys are
different from the Docker service secrets in `app/tooling/observability/.env`.
The pair identifies the Langfuse project and authenticates the explicit
read-only connection check.

## Prerequisites

- Prepare the locked application environment from the repository root.

```sh
python3 app/tooling/bootstrap.py
```

- Start the local Langfuse service only when checking a local endpoint. Hosted endpoints do not need local Docker.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

The expected local URL is `http://localhost:3000`. See the [local service guide](langfuse-local.md) for Docker setup and status commands.

## Create a private project-keys file

Use the external path `~/.config/agent-playbook/secrets.env`. It stays outside
the repository and release artifacts.

- Create the configuration directory.

```sh
mkdir -p "$HOME/.config/agent-playbook"
```

- Restrict the directory to your user.

```sh
chmod 700 "$HOME/.config/agent-playbook"
```

- Create `~/.config/agent-playbook/secrets.env` with your editor and these entries, replacing the obvious placeholders with your project values.

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-placeholder
LANGFUSE_SECRET_KEY=sk-lf-placeholder
AGENT_PLAYBOOK_LANGFUSE_BASE_URL=http://localhost:3000
AGENT_PLAYBOOK_LANGFUSE_ENABLED=true
```

- Open your Langfuse instance in a browser.

For a local instance, use `http://localhost:3000`. For a hosted instance, use
your Langfuse workspace URL.

- Select the project you want to check.

- Open **Project Settings → API Keys**.

- Create a project key pair if you do not already have both values.

See Langfuse's [API key location guide](https://langfuse.com/faq/all/where-are-langfuse-api-keys).
The secret key is shown once when created. If you cannot retrieve an existing
secret value, create a replacement key pair and update the file.

- Copy the public key and secret key into their matching lines in the external file, replacing the placeholders.

Do not paste real key values into chat, source files, or this guide.

- Restrict the secrets file to your user.

```sh
chmod 600 "$HOME/.config/agent-playbook/secrets.env"
```

The parser accepts blank lines, full-line comments beginning with `#`,
unquoted values, and matching single or double quotes. Leading and trailing
whitespace around unquoted values is trimmed. A `#` preceded by whitespace
starts an unquoted trailing comment. Double-quoted values support escaped
backslashes and quotes. Values are literal: the loader never evaluates variable
expansion, backticks or shell command substitution. Malformed lines and duplicate
names fail with a sanitized configuration error. File permissions reduce access
by other local users; they cannot prevent exposure by a compromised account or
process.

## Select the file

- Select the secrets file in the current terminal session.

```sh
export AGENT_PLAYBOOK_SECRETS_FILE="$HOME/.config/agent-playbook/secrets.env"
```

This export applies to commands started from this shell and its child processes.
Repeat it in a new terminal, add it to your shell startup configuration, or set
the same environment variable in the PyCharm run configuration. `~` expands to
the user's home directory. Relative selector paths resolve from the invocation
directory; use an absolute path for a persistent shell or IDE setting.

Process environment values override entries from the selected file, including
explicit empty values. The file can set `AGENT_PLAYBOOK_LANGFUSE_ENABLED=true`,
but project keys alone never enable Langfuse. This application secrets file is
separate from Docker's `app/tooling/observability/.env`, which the application
loader never reads or changes. Without `AGENT_PLAYBOOK_SECRETS_FILE`, no `.env`,
home secrets or Docker settings are discovered automatically.

## Run the read-only check

- Check the selected project from the repository root.

```sh
app/.venv/bin/agent-playbook langfuse --check
```

- Confirm the expected result for your endpoint.

```text
Langfuse project authentication succeeded at http://localhost:3000.
```

Exit code 0 means authentication succeeded. A disabled check returns 3 and says
it was skipped; invalid configuration returns 2; authentication or network
failure returns 1 with a safe explanation. The check creates no traces. For a
hosted endpoint, set `AGENT_PLAYBOOK_LANGFUSE_BASE_URL` in the secrets file to
its HTTPS origin; local Docker is not required.

The selected YAML file can also provide the enabled setting and reference keys
by name. Merge this block into the file you already use; do not replace its
CrewAI settings:

```yaml
integrations:
  langfuse:
    enabled: true
    base_url: http://localhost:3000
    environment: local
    public_key: {env: LANGFUSE_PUBLIC_KEY}
    secret_key: {env: LANGFUSE_SECRET_KEY}
```

`AGENT_PLAYBOOK_LANGFUSE_ENABLED`,
`AGENT_PLAYBOOK_LANGFUSE_BASE_URL` and
`AGENT_PLAYBOOK_LANGFUSE_ENVIRONMENT` override corresponding YAML values. A
disabled integration needs no keys or service. Configuration file selection
still follows the [runtime configuration guide](configuration.md); use
`--config PATH` or `AGENT_PLAYBOOK_CONFIG` to select YAML.

The checker validates an HTTP(S) origin and does not print key values, raw SDK
errors or URL credentials. It uses Langfuse Python SDK 5.2.0 with a five-second
request timeout. HTTP health alone does not prove project authentication; a
successful explicit check does.

## Send your first trace

The authentication check creates no traces. To continue to the mock exercise,
keep the selector active in the same terminal and leave your local service
running. Then follow the official [Langfuse hands-on guide](langfuse-hands-on.md)
to run the synthetic success and failure scenarios and inspect their traces.
They use arithmetic only, with no model calls, tokens or costs. The optional
[personal playground README](../examples/langfuse/README.md) describes its flags.
Ordinary application workflows remain uninstrumented.

## Environment-only alternative

- Set the Langfuse enable override in the current terminal.

```sh
export AGENT_PLAYBOOK_LANGFUSE_ENABLED=true
```

- Prompt for the public key in the current terminal.

```sh
export LANGFUSE_PUBLIC_KEY="$(python3 -c 'import getpass; print(getpass.getpass("Public key: "))')"
```

- Prompt for the secret key in the current terminal.

```sh
export LANGFUSE_SECRET_KEY="$(python3 -c 'import getpass; print(getpass.getpass("Secret key: "))')"
```

- Run the connection check from the repository root.

```sh
app/.venv/bin/agent-playbook langfuse --check
```

Exports apply only to that terminal session and child processes. Repeat them in
another terminal or store the variable names in your IDE's environment settings.

## Clean up when finished

- Remove shell exports when you no longer need them in this terminal.

```sh
unset AGENT_PLAYBOOK_SECRETS_FILE LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY AGENT_PLAYBOOK_LANGFUSE_ENABLED AGENT_PLAYBOOK_LANGFUSE_BASE_URL
```

The private file remains available for later use; unsetting the selector only
stops this shell from selecting it.

- Stop the local service from the repository root if you started it for this check.

```sh
app/.venv/bin/agent-playbook langfuse --stop
```

The stop preserves named volumes and earlier traces. Keep the selected secrets
file outside the repository for later runs.
