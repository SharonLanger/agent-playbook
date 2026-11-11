"""Application commands, introduced one substage at a time."""

import argparse
import sys
from importlib.metadata import version

from agent_playbook.__main__ import main as run_main
from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.development import run_tools


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent-playbook")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="Run the existing Python entry point.")
    commands.add_parser("test", help="Run pytest in the development checkout.")
    commands.add_parser("check", help="Run typing, lint, formatting and tests.")
    commands.add_parser(
        "version", help="Show installed version and source build metadata."
    )
    args = parser.parse_args()
    if args.command == "version":
        print(f"agent-playbook {version('agent-playbook')} (source: {SOURCE_COMMIT})")
        return 0
    if args.command == "check":
        return run_tools(
            [
                ["pyright"],
                ["ruff", "check", "src", "scripts", "tests"],
                ["ruff", "format", "--check", "src", "scripts", "tests"],
                ["pytest", "-q", "tests"],
            ]
        )
    if args.command == "test":
        return run_tools([["pytest", "-q", "tests"]])
    run_main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
