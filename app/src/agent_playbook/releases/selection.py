"""Select and launch completed local releases."""

import json
import os
import subprocess
import sys
from pathlib import Path


def find_release(requested_version: str | None) -> tuple[Path, str] | None:
    app = Path(__file__).resolve().parents[3]
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
            "agent-playbook release, or run editable code with agent-playbook dev-run.",
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
