"""Prepare Stage 00.1 from any working directory using Python 3.10+."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

APP = Path(__file__).resolve().parents[1]
UV_VERSION = "0.13.6"


def run(command, **kwargs):
    print("+ " + " ".join(map(str, command)), flush=True)
    subprocess.run(command, check=True, cwd=APP, **kwargs)


def main():
    if sys.version_info < (3, 10):
        raise RuntimeError("Bootstrap requires Python 3.10+ with venv/ensurepip.")

    # Reuse only the pinned uv; otherwise provision it without changing global tools.
    uv = shutil.which("uv")
    if uv:
        version = subprocess.run([uv, "--version"], check=True, capture_output=True,
                                 text=True).stdout.split()
        if version[1] != UV_VERSION:
            uv = None
    if not uv:
        tools = APP / ".bootstrap-tools"
        scripts = tools / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        uv = str(scripts / ("uv.exe" if os.name == "nt" else "uv"))
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(tools)
        run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
             "uv==" + UV_VERSION])

    # Keep setup pointed at this checkout, even from an activated foreign venv.
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env["UV_PROJECT_ENVIRONMENT"] = str(APP / ".venv")
    pin = (APP / ".python-version").read_text().strip()
    run([uv, "sync", "--locked", "--python", pin], env=env)
    python = APP / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run([str(python), str(APP / "src/agent_playbook/__main__.py")], env=env)
    print("Ready. PyCharm interpreter: " + str(python))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print("Bootstrap failed: " + str(error), file=sys.stderr)
        sys.exit(1)
