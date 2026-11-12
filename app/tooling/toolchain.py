"""Find the pinned uv executable without modifying the environment."""

import os
import shutil
import subprocess
from pathlib import Path

UV_VERSION = "0.13.6"


def private_uv_path(app: Path) -> Path:
    scripts = "Scripts" if os.name == "nt" else "bin"
    name = "uv.exe" if os.name == "nt" else "uv"
    return app / ".bootstrap-tools" / scripts / name


def pinned_uv(app: Path) -> str | None:
    """Try PATH first, then the bootstrap copy if PATH is unsuitable."""
    candidates = (shutil.which("uv"), str(private_uv_path(app)))
    for candidate in dict.fromkeys(c for c in candidates if c):
        try:
            reported = subprocess.check_output(
                [candidate, "--version"], text=True, stderr=subprocess.DEVNULL
            ).split()
        except (OSError, subprocess.CalledProcessError):
            continue
        if len(reported) >= 2 and reported[0] == "uv" and reported[1] == UV_VERSION:
            return candidate
    return None
