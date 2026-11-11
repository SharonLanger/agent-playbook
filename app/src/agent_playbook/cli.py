"""Run a selected release or use development commands in the source checkout."""

import argparse
import json
import os
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from agent_playbook.__main__ import main as run_main
from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.development import run_tools


def find_release(requested_version: str | None) -> tuple[Path, str] | None:
    app = Path(__file__).resolve().parents[2]
    candidates: list[tuple[int, str, Path, str]] = []
    for manifest in (app / "dist").glob("*/release.json"):
        try:
            data = json.loads(manifest.read_text())
            release_version = data["version"]
            executable = manifest.parent / "venv" / "bin" / "python"
            installed_cli = manifest.parent / "venv" / "bin" / "agent-playbook"
            if (
                isinstance(release_version, str)
                and (requested_version is None or release_version == requested_version)
                and executable.is_file()
                and installed_cli.is_file()
                and data.get("verified", True) is True
            ):
                candidates.append(
                    (
                        manifest.stat().st_mtime_ns,
                        manifest.parent.name,
                        executable,
                        release_version,
                    )
                )
        except (OSError, ValueError, KeyError, TypeError):
            continue
    if not candidates:
        return None
    _, _, executable, release_version = max(candidates)
    return executable, release_version


def run_release(requested_version: str | None) -> int:
    selected = find_release(requested_version)
    if selected is None:
        detail = f" version {requested_version}" if requested_version else ""
        print(
            f"No installed release{detail} found in app/dist. Build one with "
            "python app/scripts/release.py, or run editable code with agent-playbook dev-run.",
            file=sys.stderr,
        )
        return 2
    executable, release_version = selected
    print(f"Running release {release_version} from {executable.parents[2]}", flush=True)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    return subprocess.run(
        [str(executable), "-I", "-m", "agent_playbook.cli", "run"],
        env=env,
        check=False,
    ).returncode


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
    parser.error("Unknown command")


if __name__ == "__main__":
    sys.exit(main())
