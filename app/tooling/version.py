"""Set the application version and refresh its uv lockfile together."""

import argparse
import re
import shutil
import subprocess
import tomllib
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
UV_VERSION = "0.13.6"


def next_patch(current: str) -> str:
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", current):
        raise ValueError("Patch bump requires a MAJOR.MINOR.PATCH version.")
    major, minor, patch = current.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "version", help="New MAJOR.MINOR.PATCH, or patch to increase the current patch"
    )
    args = parser.parse_args()
    if args.version == "patch":
        try:
            current = tomllib.loads((APP / "pyproject.toml").read_text())["project"][
                "version"
            ]
            args.version = next_patch(current)
        except (OSError, ValueError, KeyError, TypeError) as error:
            parser.exit(1, f"Could not read current version: {error}\n")
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        parser.error("Use MAJOR.MINOR.PATCH, for example 0.0.7.")

    private_uv = APP / ".bootstrap-tools" / "bin" / "uv"
    candidates = [shutil.which("uv"), str(private_uv) if private_uv.is_file() else None]
    for uv in candidates:
        if uv is None:
            continue
        try:
            reported = subprocess.check_output([uv, "--version"], text=True).split()
            if reported[1] == UV_VERSION:
                subprocess.run(
                    [uv, "version", args.version, "--project", str(APP)], check=True
                )
                print(
                    "Updated app/pyproject.toml and app/uv.lock. Review and commit "
                    "both files, then run agent-playbook release. No commit, push or build was performed."
                )
                return
        except (OSError, IndexError, subprocess.CalledProcessError) as error:
            parser.exit(1, f"Could not update version: {error}\n")
    parser.exit(1, "uv 0.13.6 was not found; run app/tooling/bootstrap.py first.\n")


if __name__ == "__main__":
    main()
