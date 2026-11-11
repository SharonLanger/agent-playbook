"""Stage 00.2: a minimal command-line interface."""

import argparse

from agent_playbook.__main__ import main as run_main


def main() -> None:
    parser = argparse.ArgumentParser(prog="agent-playbook")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="Run the existing Python entry point.")
    args = parser.parse_args()
    if args.command == "run":
        run_main()


if __name__ == "__main__":
    main()
