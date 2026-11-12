"""Development-only commands; installed releases have no checkout or dev tools."""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


def tool_label(command: list[str]) -> str:
    if command[0] == "pyright":
        return "Pyright (types)"
    if command[:2] == ["ruff", "check"]:
        return "Ruff (lint)"
    if command[:2] == ["ruff", "format"]:
        return "Ruff (formatting)"
    if command[0] == "pytest":
        return "pytest (tests)"
    return " ".join(command)


def print_summary(labels: list[str], results: list[int | None]) -> None:
    print("\nCheck summary", flush=True)
    for label, code in zip(labels, results, strict=True):
        status = "NOT RUN" if code is None else "PASS" if code == 0 else "FAIL"
        detail = f" (exit {code})" if code else ""
        print(f"  {status:<8} {label}{detail}", flush=True)
    passed = results.count(0)
    skipped = results.count(None)
    failed = len(results) - passed - skipped
    overall = "FAIL" if failed or skipped else "PASS"
    print(
        f"\nResult: {overall} ({passed} passed, {failed} failed, {skipped} not run)",
        flush=True,
    )
    if failed:
        print("Fix the reported failure, then rerun this command.", flush=True)


def run_tools(commands: list[list[str]]) -> int:
    app = Path(__file__).resolve().parents[1]
    if not (app / "pyproject.toml").is_file() or not (app / "tests").is_dir():
        print(
            "Development command requires a source checkout; run its bootstrap.",
            file=sys.stderr,
        )
        return 2
    labels = [tool_label(command) for command in commands]
    results: list[int | None] = [None] * len(commands)
    print("Checks run in order and stop at the first failure.", flush=True)
    print(f"Project: {app}", flush=True)
    for index, command in enumerate(commands):
        if importlib.util.find_spec(command[0]) is None:
            print(
                f"Missing development tool {command[0]}; rerun bootstrap.",
                flush=True,
            )
            results[index] = 2
            print("No checks were started: tool setup is incomplete.", flush=True)
            print_summary(labels, results)
            return 2
    for index, command in enumerate(commands):
        print(f"\n[{index + 1}/{len(commands)}] {labels[index]}", flush=True)
        print("Command: python -m " + " ".join(command), flush=True)
        print("-" * 60, flush=True)
        try:
            result = subprocess.run(
                [sys.executable, "-m", *command], cwd=app, stderr=subprocess.STDOUT
            )
            code = result.returncode
        except OSError as error:
            print(f"Could not start {labels[index]}: {error}", flush=True)
            code = 2
        results[index] = code
        status = "PASS" if code == 0 else f"FAIL (exit {code})"
        print(f"{status}: {labels[index]}", flush=True)
        if code:
            print("Stopping here; remaining checks were not run.", flush=True)
            print_summary(labels, results)
            return code
    print_summary(labels, results)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("check", "test", "format"), nargs="?", default="check"
    )
    for name in ("types", "lint", "format"):
        parser.add_argument(f"--{name}", action="store_true")
    args = parser.parse_args()
    selected = [name for name in ("types", "lint", "format") if getattr(args, name)]
    if selected and args.command != "check":
        parser.error("Check selectors apply only to check.")
    return run_tools(select_commands(args.command, selected))


def select_commands(command: str, selected: list[str]) -> list[list[str]]:
    paths = ["src", "tooling", "examples", "tests"]
    if command == "test":
        return [["pytest", "-q", "tests", "examples/workflows"]]
    if command == "format":
        return [["ruff", "format", *paths]]
    checks = {
        "types": ["pyright"],
        "lint": ["ruff", "check", *paths],
        "format": ["ruff", "format", "--check", *paths],
        "tests": ["pytest", "-q", "tests", "examples/workflows"],
    }
    return [value for name, value in checks.items() if not selected or name in selected]


if __name__ == "__main__":
    sys.exit(main())
