"""Set the application version and refresh its uv lockfile together."""

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tooling.toolchain import pinned_uv

APP = Path(__file__).resolve().parents[1]


def next_version(current: str, part: str) -> str:
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", current):
        raise ValueError("Bump requires a MAJOR.MINOR.PATCH version.")
    major, minor, patch = map(int, current.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError("Use patch, minor or major.")


def next_patch(current: str) -> str:
    return next_version(current, "patch")


def update_version(app: Path, uv: str, version: str) -> None:
    """Restore both inputs if uv fails or leaves an inconsistent project lock."""
    files = (app / "pyproject.toml", app / "uv.lock")
    originals = {path: path.read_bytes() for path in files}
    try:
        subprocess.run([uv, "version", version, "--project", str(app)], check=True)
        project = tomllib.loads(files[0].read_text())["project"]
        lock = tomllib.loads(files[1].read_text())
        locked = [p["version"] for p in lock["package"] if p["name"] == project["name"]]
        if project["version"] != version or locked != [version]:
            raise ValueError(
                "Version update did not synchronize project metadata and lock."
            )
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError):
        for path, content in originals.items():
            path.write_bytes(content)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="New MAJOR.MINOR.PATCH, or patch, minor, major")
    args = parser.parse_args()
    if args.version in ("patch", "minor", "major"):
        try:
            current = tomllib.loads((APP / "pyproject.toml").read_text())["project"][
                "version"
            ]
            args.version = next_version(current, args.version)
        except (OSError, ValueError, KeyError, TypeError) as error:
            parser.exit(1, f"Could not read current version: {error}\n")
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        parser.error("Use MAJOR.MINOR.PATCH, for example 0.0.7.")

    uv = pinned_uv(APP)
    if uv is None:
        parser.exit(1, "Pinned uv was not found; run app/tooling/bootstrap.py first.\n")
    try:
        update_version(APP, uv, args.version)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        parser.exit(1, f"Could not update version: {error}\n")
    print(
        "Updated app/pyproject.toml and app/uv.lock. Review and commit "
        "both files, then run agent-playbook release. No commit, push or build was performed."
    )


if __name__ == "__main__":
    main()
