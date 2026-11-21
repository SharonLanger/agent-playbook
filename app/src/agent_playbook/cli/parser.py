"""Declare the public command-line interface without importing integrations."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-playbook")
    commands = parser.add_subparsers(dest="command", required=True)
    run_parser = commands.add_parser("run", help="Run the newest installed release.")
    run_parser.add_argument(
        "--version",
        dest="release_version",
        help="Select the newest installed release of this version.",
    )
    dev_parser = commands.add_parser(
        "dev-run", help="Run editable source in the development checkout."
    )
    for workflow_parser in (run_parser, dev_parser):
        workflow_parser.add_argument(
            "--workflow", help="Configured workflow ID (default: wf-01)."
        )
        workflow_parser.add_argument(
            "--input",
            dest="workflow_input",
            help="JSON object: wf-01 {}; wf-02 initial/increment/multiplier; wf-03 score.",
        )
        workflow_parser.add_argument(
            "--config",
            help="External YAML configuration (overrides AGENT_PLAYBOOK_CONFIG).",
        )
    commands.add_parser("test", help="Run pytest in the development checkout.")
    langfuse = commands.add_parser(
        "langfuse",
        help="Manage local Langfuse or check project access (source checkout).",
    )
    actions = langfuse.add_mutually_exclusive_group(required=True)
    for name in ("start", "stop", "status", "logs", "open", "check"):
        actions.add_argument(f"--{name}", action="store_true")
    langfuse.add_argument(
        "--follow", action="store_true", help="Follow --logs until Ctrl-C."
    )
    langfuse.add_argument(
        "--env-file", help="Private Compose settings for local actions."
    )
    langfuse.add_argument("--config", help="Selected application YAML for --check.")
    for command, help_text in (
        ("services", "Manage local services together (source checkout)."),
        ("logs", "Manage local VictoriaLogs (source checkout)."),
    ):
        service = commands.add_parser(command, help=help_text)
        actions = service.add_mutually_exclusive_group(required=True)
        for name in ("start", "status", "stop"):
            actions.add_argument(f"--{name}", action="store_true")
        if command == "services":
            service.add_argument("--config", help="Application YAML for start/status.")
            service.add_argument(
                "--env-file", help="Private Langfuse Compose settings."
            )
    check_parser = commands.add_parser(
        "check", help="Run all checks, or selected checks."
    )
    for name in ("types", "lint", "format"):
        check_parser.add_argument(
            f"--{name}", action="store_true", help=f"Check {name} only (combinable)."
        )
    commands.add_parser(
        "format", help="Apply formatting fixes to source, tooling and tests."
    )
    release_parser = commands.add_parser(
        "release", help="Build and verify the current committed version."
    )
    release_parser.add_argument(
        "--output", help="Unused output directory (relative to your current directory)."
    )
    version_parser = commands.add_parser(
        "version", help="Show version, or bump the checkout version."
    )
    version_parser.add_argument(
        "action",
        nargs="?",
        choices=("patch", "minor", "major"),
        help="Update TOML and lockfile; review and commit before release.",
    )
    return parser
