# Agent Playbook application

## Setup

Open this repository in PyCharm and select the project interpreter at
`app/.venv/bin/python` after running the bootstrap command once from the
repository root:

```sh
python3 app/scripts/bootstrap.py
```

Bootstrap provisions the pinned Python and development tools, installs the project
in `app/.venv`, and runs the editable example and local quality checks. Run the
same command again to refresh the environment. The prerequisite is Python 3.10+
with `venv` and `ensurepip`; initial provisioning may require network access.

## Documentation

**[CLI and releases](docs/cli.md)** explains every command, PyCharm configuration,
release selection, build output, exact release paths, and the quality gate.

[Stage 00.7 learning exercise](../designs/stages/00-environment/learning/00-7-wheel-release.md)
· [Verification findings](../designs/stages/00-environment/findings.md)
