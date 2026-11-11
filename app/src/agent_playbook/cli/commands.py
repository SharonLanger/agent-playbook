"""Parse commands and present application outcomes."""

import argparse
from importlib.metadata import version

from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.application.runner import main as run_main
from agent_playbook.cli.development import run_development
from agent_playbook.releases.selection import run_release


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent-playbook")
    commands = parser.add_subparsers(dest="command", required=True)
    run_parser = commands.add_parser("run", help="Run the newest installed release.")
    run_parser.add_argument(
        "--version",
        dest="release_version",
        help="Select the newest installed release of this version.",
    )
    commands.add_parser(
        "dev-run", help="Run editable source in the development checkout."
    )
    commands.add_parser("test", help="Run pytest in the development checkout.")
    commands.add_parser("check", help="Run typing, lint, formatting and tests.")
    commands.add_parser(
        "version", help="Show installed version and source build metadata."
    )
    args = parser.parse_args()
    if args.command == "version":
        print(f"agent-playbook {version('agent-playbook')} (source: {SOURCE_COMMIT})")
        return 0
    if args.command == "run":
        if SOURCE_COMMIT != "development":
            if args.release_version and args.release_version != version(
                "agent-playbook"
            ):
                parser.error("This release can run only its own version.")
            run_main()
            return 0
        return run_release(args.release_version)
    if args.command == "dev-run":
        if SOURCE_COMMIT != "development":
            parser.error("dev-run requires a source checkout.")
        run_main()
        return 0
    if args.command in ("check", "test"):
        return run_development(args.command)
    parser.error("Unknown command")
