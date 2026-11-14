# Agent Playbook application

## Setup

Open the **repository root** (`agent-playbook`) as the PyCharm project. First
run bootstrap from the repository root:

```sh
python3 app/tooling/bootstrap.py
```

Then choose **Add Interpreter → Existing environment** and select
`<repo>/app/.venv/bin/python` as the project interpreter. PyCharm's project
interpreter setting is local to your machine; the committed configurations in
[`.run/`](../.run/) use that project interpreter and `$PROJECT_DIR$/app` paths.
After pulling them, the Run menu should show the eighteen shared tasks listed in
the CLI guide, including individual checks, Format, Bump Patch and Release. `Run` selects the latest built release; use `dev-run` for editable code.

Bootstrap provisions the pinned Python and development tools, installs the project
in `app/.venv`, and runs default WF-01 and local quality checks. Run the
same command again to refresh the environment. The prerequisite is Python 3.10+
with `venv` and `ensurepip`; initial provisioning may require network access.

For the optional local trace UI, see [local Langfuse setup](docs/langfuse-local.md). Docker is required for that local service, not for ordinary workflows or a hosted Langfuse endpoint. Configure project keys with the [external secrets file and connection check](docs/langfuse-connection.md); do not put project keys in Docker's `.env`.

## Documentation

[User documentation index](docs/README.md) links the CLI, configuration, workflow-running and troubleshooting guides.

**[Stage 01: verify and read the code](../designs/stages/01-crewai-flows/learning/00-reading-the-code.md)**
starts the learning sessions, with per-workflow guides, expected outputs and test buttons.


**[Runtime configuration](docs/configuration.md)** explains shared YAML, local overrides,
environment settings and using the same configuration across releases.

**[CLI and releases](docs/cli.md)** explains every command, PyCharm configuration,
release selection, build output, exact release paths, and the quality gate.

[Stage 00.7 learning exercise](../designs/stages/00-environment/learning/00-7-wheel-release.md)
· [Verification findings](../designs/stages/00-environment/findings.md)

Project layout: [guarded project structure](../designs/project-structure.md).

Use **Dev Run** for source edits, **Run** for the latest release, and **Check** for all checks. **Bump Patch** updates version metadata; review and commit before **Release**. See the CLI guide for individual checks and **Format**.


## Independent workflow experiments

[Workflow examples — start here](examples/workflows/README.md). Open an example's run.py directly in PyCharm; no CLI selection or release is needed.

