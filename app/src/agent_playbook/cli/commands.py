"""Parse commands and present application outcomes."""

import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.application.results import (
    WorkflowExecutionError,
    WorkflowInputError,
)
from agent_playbook.application.runner import run_workflow
from agent_playbook.cli.development import run_development
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.releases.selection import run_release


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
            "--workflow", help="Workflow ID: wf-01 (default), wf-02 or wf-03."
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
    check_parser = commands.add_parser(
        "check", help="Run all checks, or selected checks."
    )
    for name in ("types", "lint", "format"):
        check_parser.add_argument(
            f"--{name}", action="store_true", help=f"Check {name} only (combinable)."
        )
    commands.add_parser(
        "format", help="Apply formatting fixes to source, tooling, examples and tests."
    )
    release_parser = commands.add_parser(
        "release", help="Build and verify the current committed version."
    )
    release_parser.add_argument(
        "--output", help="Unused output directory (relative to your current directory)."
    )
    version_parser = commands.add_parser(
        "version", help="Show version, or bump the checkout patch version."
    )
    version_parser.add_argument(
        "action",
        nargs="?",
        choices=("patch",),
        help="Update TOML and lockfile; review and commit before release.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        if args.action == "patch":
            return run_development("version", ["patch"])
        print(f"agent-playbook {version('agent-playbook')} (source: {SOURCE_COMMIT})")
        return 0
    if args.command == "run":
        if SOURCE_COMMIT != "development":
            if args.release_version and args.release_version != version(
                "agent-playbook"
            ):
                parser.error("This release can run only its own version.")
            return present_workflow(args.workflow, args.workflow_input, args.config)
        forwarded: list[str] = []
        if args.workflow is not None:
            forwarded.extend(["--workflow", args.workflow])
        if args.workflow_input is not None:
            forwarded.extend(["--input", args.workflow_input])
        if args.config is not None:
            forwarded.extend(["--config", args.config])
        return run_release(args.release_version, forwarded)
    if args.command == "dev-run":
        if SOURCE_COMMIT != "development":
            parser.error("dev-run requires a source checkout.")
        return present_workflow(args.workflow, args.workflow_input, args.config)
    if args.command == "check":
        flags = [
            f"--{name}" for name in ("types", "lint", "format") if getattr(args, name)
        ]
        return run_development("check", flags)
    if args.command == "release":
        return run_development(
            "release",
            ["--output", str(Path(args.output).resolve())] if args.output else [],
        )
    if args.command in ("test", "format"):
        return run_development(args.command)
    parser.error("Unknown command")


def present_workflow(
    workflow_id: str | None = None,
    raw_input: str | None = None,
    config_path: str | None = None,
) -> int:
    """Map input and execution failures separately; presentation belongs to the CLI."""
    try:
        result = run_workflow(
            "wf-01" if workflow_id is None else workflow_id,
            raw_input,
            config_path=config_path,
        )
    except ConfigurationError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2
    except WorkflowInputError as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2
    except WorkflowExecutionError as error:
        print(f"Workflow failed: {error}", file=sys.stderr)
        return 1
    print(f"[{result.workflow_id.upper()}] result: {result.output}")
    return 0
