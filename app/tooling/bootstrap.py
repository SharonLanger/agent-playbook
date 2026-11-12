"""Prepare Stage 00.7 from any working directory using Python 3.10+."""

import os
import subprocess
import sys
import venv
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tooling.toolchain import UV_VERSION, pinned_uv, private_uv_path

APP = Path(__file__).resolve().parents[1]


def run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    print("+ " + " ".join(map(str, command)), flush=True)
    subprocess.run(command, check=True, cwd=APP, env=env)


def main() -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError("Bootstrap requires Python 3.10+ with venv/ensurepip.")

    # Reuse only the pinned uv; otherwise provision it without changing global tools.
    uv = pinned_uv(APP)
    if not uv:
        tools = APP / ".bootstrap-tools"
        scripts = tools / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        uv = str(private_uv_path(APP))
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(tools)
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "uv==" + UV_VERSION,
            ]
        )

    # Keep setup pointed at this checkout, even from an activated foreign venv.
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env["UV_PROJECT_ENVIRONMENT"] = str(APP / ".venv")
    pin = (APP / ".python-version").read_text().strip()
    run([uv, "sync", "--locked", "--python", pin], env=env)
    python = APP / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    cli = python.parent / (
        "agent-playbook.exe" if os.name == "nt" else "agent-playbook"
    )
    run([str(cli), "dev-run"], env=env)
    run([str(cli), "check"], env=env)
    print("Ready. PyCharm interpreter: " + str(python))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print("Bootstrap failed: " + str(error), file=sys.stderr)
        sys.exit(1)
