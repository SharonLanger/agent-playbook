# Check a Langfuse project connection

The explicitly invoked, read-only project authentication check
It sends no traces and does not connect workflows automatically. Start the
[local Langfuse service](langfuse-local.md), create a project in its UI, and copy
that project's public and secret API keys from project settings. These keys are
different from the Docker service secrets in `tooling/observability/.env`.

From the repository root, install the locked application environment:

```sh
python3 app/tooling/bootstrap.py
```

The committed `app/application.yaml` keeps Langfuse disabled. Existing YAML
files without a `langfuse` section also remain disabled. To check your local
project without storing keys in a file or shell history, run in a Bash or Zsh
terminal from the repository root:

```sh
export AGENT_PLAYBOOK_LANGFUSE_ENABLED=true
export LANGFUSE_PUBLIC_KEY="$(python3 -c 'import getpass; print(getpass.getpass("Public key: "))')"
export LANGFUSE_SECRET_KEY="$(python3 -c 'import getpass; print(getpass.getpass("Secret key: "))')"
app/.venv/bin/agent-playbook langfuse --check
```

Expected: `Langfuse project authentication succeeded at
http://localhost:3000.` and exit code 0. The check creates no traces; the list
stays empty. To inspect its exit code immediately, run `echo $?`. A disabled
check returns 3 and says it was skipped; invalid configuration returns 2;
authentication or network failure returns 1 with a safe explanation.

If your UI uses another port, set
`AGENT_PLAYBOOK_LANGFUSE_BASE_URL=http://localhost:PORT` in the shell before
the check, substituting your actual port. HTTPS origins are supported too.
Configuration selection still follows the [application configuration
guide](configuration.md): pass `--config PATH` to `langfuse --check` or set
`AGENT_PLAYBOOK_CONFIG`. A selected YAML file can contain:

```yaml
integrations:
  langfuse:
    enabled: true
    base_url: http://localhost:3000
    environment: local
    public_key: {env: LANGFUSE_PUBLIC_KEY}
    secret_key: {env: LANGFUSE_SECRET_KEY}
```

Merge this block into an existing file; do not replace its CrewAI settings.
For private machine settings, add the block to ignored
`app/application.local.yaml`. Values are loaded from the named environment
variables on each invocation. `AGENT_PLAYBOOK_LANGFUSE_ENABLED`,
`AGENT_PLAYBOOK_LANGFUSE_BASE_URL` and `AGENT_PLAYBOOK_LANGFUSE_ENVIRONMENT`
override corresponding file values. A disabled check needs no keys or service.

When finished, remove keys from this terminal and stop the service safely from
the deployment folder:

```sh
unset LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY AGENT_PLAYBOOK_LANGFUSE_ENABLED AGENT_PLAYBOOK_LANGFUSE_BASE_URL
app/.venv/bin/agent-playbook langfuse --stop
```

The stop preserves named volumes. The checker validates an HTTP(S) origin and
does not print key values, raw SDK errors, or URL credentials. It uses Langfuse
Python SDK 5.2.0 with a five-second request timeout. HTTP health alone does not
prove project authentication; a successful explicit check does.

After a successful check, the optional [personal mock playground](../examples/langfuse/README.md)
can send synthetic traces when explicitly run. Ordinary application workflows
remain uninstrumented.
