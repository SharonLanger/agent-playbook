"""Parse commands and present application outcomes."""

import logging
import sys
from contextlib import contextmanager
from importlib.metadata import version
from pathlib import Path
from typing import Iterator

from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.application.results import (
    WorkflowExecutionError,
    WorkflowInputError,
)
from agent_playbook.cli.development import run_development
from agent_playbook.cli.parser import build_parser
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.releases.discovery import find_release
from agent_playbook.releases.launcher import launch_release


class _SuppressFrameworkErrorLog(logging.Filter):
    """The CLI emits its classified error instead of CrewAI's raw exception text."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.ERROR


@contextmanager
def _safe_framework_errors() -> Iterator[None]:
    logger = logging.getLogger("crewai.flow.runtime")
    guard = _SuppressFrameworkErrorLog()
    logger.addFilter(guard)
    try:
        yield
    finally:
        logger.removeFilter(guard)


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
        return present_release(args.release_version, forwarded)
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


def present_release(
    requested_version: str | None, arguments: list[str] | None = None
) -> int:
    selected = find_release(requested_version)
    if selected is None:
        detail = f" version {requested_version}" if requested_version else ""
        print(
            f"No installed release{detail} found in app/dist. Build one with "
            "agent-playbook release, or run editable code with agent-playbook dev-run.",
            file=sys.stderr,
        )
        return 2
    executable, release_version = selected
    print(f"Running release {release_version} from {executable.parents[2]}", flush=True)
    try:
        return launch_release(executable, arguments)
    except ConfigurationError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2


def present_workflow(
    workflow_id: str | None = None,
    raw_input: str | None = None,
    config_path: str | None = None,
) -> int:
    """Map input and execution failures separately; presentation belongs to the CLI."""
    from agent_playbook.application.workflow_runner import run_workflow

    try:
        with _safe_framework_errors():
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
    print(f"[{result.workflow_id.upper()}] result: {result.serialized_output}")
    return 0
