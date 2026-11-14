# Connect the application to a Langfuse project

Application settings belong in `app/application.yaml`. Project credentials belong
in an external private file. Docker's `app/tooling/observability/.env` holds
separate infrastructure credentials; do not put project keys there.

## Create the private credentials file

- Create the directory if it does not exist.

```sh
mkdir -p "$HOME/.config/agent-playbook"
```

- Restrict access to your user.

```sh
chmod 700 "$HOME/.config/agent-playbook"
```

- Create the file if needed, preserving any existing contents.

```sh
touch "$HOME/.config/agent-playbook/secrets.env"
```

- Restrict access to the file.

```sh
chmod 600 "$HOME/.config/agent-playbook/secrets.env"
```

- Prepare the application environment from the repository root if needed.

```sh
python3 app/tooling/bootstrap.py
```

- Start Langfuse if using the local service and it is not already running.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

Hosted endpoints do not require Docker. The [local setup guide](langfuse-local.md)
covers first-time account, organization and project creation.

## Copy the project keys

- Open your Langfuse instance: `http://localhost:3000` for the default local setup.

- Select your project.

- Open **Project Settings → API Keys**.

- Create a key pair if you do not already have both values.

The secret key is shown once. If it is unavailable, create a replacement pair.
See Langfuse's [API key location guide](https://langfuse.com/faq/all/where-are-langfuse-api-keys).

- Open `~/.config/agent-playbook/secrets.env` in your editor.

- Save these two entries with your actual values replacing the placeholders.

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-placeholder
LANGFUSE_SECRET_KEY=sk-lf-placeholder
```

The enable switch, base URL and environment belong in YAML, not in this credentials
file. More integrations can add their credentials to the same file later.
Never put actual key values in shared YAML, documentation or chat.

## Configure the application

- Open `app/application.yaml`.

- Confirm its general, top-level secrets section points to your file.

```yaml
secrets:
  file: ~/.config/agent-playbook/secrets.env
```

This setting applies to all integrations. It is already present in the supplied
configuration. `~` expands to your home directory. Relative paths resolve beside
the selected base YAML file, independently of your terminal's working directory.
The path is required, and the file must exist and be readable. An empty file is
allowed when no enabled integration requires credentials.

- Set `integrations.langfuse.enabled` to `true` in your configuration.

- Confirm the existing URL and environment match your instance.

```yaml
integrations:
  langfuse:
    enabled: true
    base_url: http://localhost:3000
    environment: local
    public_key: {env: LANGFUSE_PUBLIC_KEY}
    secret_key: {env: LANGFUSE_SECRET_KEY}
```

Edit the existing block; preserve the CrewAI and workflow settings. The supplied
shared YAML defaults to disabled. To keep personal setting changes out of Git,
put a partial override in the ignored `app/application.local.yaml` instead:

```yaml
integrations:
  langfuse:
    enabled: true
```

The loader reads YAML, then the selected credentials file, then resolves the key
references. No secrets-file export is needed in the terminal or PyCharm.
`AGENT_PLAYBOOK_SECRETS_FILE` no longer selects the file. If you previously exported
Langfuse enable/URL/key overrides, remove them from that shell or IDE to use your
YAML and credentials file; process environment values still take precedence.

## Verify the connection

- Run the project check from the repository root.

```sh
app/.venv/bin/agent-playbook langfuse --check
```

- Confirm that it reports successful project authentication.

```text
Langfuse project authentication succeeded at http://localhost:3000.
```

The loader checks the required path, file syntax and required keys without printing
credential values. The checker then authenticates with your project; it creates
no traces. Exit 0 means success, 3 means disabled/skipped, 2 means invalid
configuration, and 1 means authentication or connection failure.

## Send your first trace

- Leave the local service running and follow the [hands-on guide](langfuse-hands-on.md).

The exercise sends synthetic arithmetic traces and verifies readback. Ordinary
application workflows remain uninstrumented. The [configuration guide](configuration.md)
describes file syntax, precedence and alternate YAML selection.

## Stop when finished

- Stop the local service when you no longer need it.

```sh
app/.venv/bin/agent-playbook langfuse --stop
```

Named volumes, project settings and previous traces are preserved. Your YAML and
private credentials file remain ready for the next run; no terminal export is needed.
