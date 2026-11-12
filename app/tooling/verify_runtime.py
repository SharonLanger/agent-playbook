"""Run all workflows in a fresh process with outbound network attempts denied.

Used with the installed release's Python (-I), so imports cannot fall back to the
checkout. This guard records even attempts that third-party code catches. It is a
regression probe for these Python workflow paths, not an OS network sandbox.
"""

import contextlib
import io
import os
import sys
from pathlib import Path


def main() -> None:
    attempts: list[str] = []

    def block_network(event: str, _arguments: tuple[object, ...]) -> None:
        if event in (
            "socket.connect",
            "socket.getaddrinfo",
            "socket.sendto",
            "socket.sendmsg",
        ):
            attempts.append(event)
            raise RuntimeError(f"Unexpected network attempt: {event}")

    # Verification uses committed fixture data, never the user's active settings.
    configuration = Path(__file__).resolve().parents[1] / "tests/fixtures/offline.yaml"
    for name in (
        "AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED",
        "AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED",
        "AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS",
    ):
        os.environ.pop(name, None)
    sys.addaudithook(block_network)
    from agent_playbook.cli.commands import main as cli_main

    command = sys.argv[1] if len(sys.argv) > 1 else "dev-run"
    if command not in ("run", "dev-run"):
        raise ValueError("Use run (installed) or dev-run (checkout).")
    cases = (
        ("wf-01", "{}", "[Hello, workflow!]"),
        ("wf-02", '{"initial":3,"increment":2,"multiplier":4}', "20"),
        ("wf-03", '{"score":80}', "pass"),
        ("wf-03", '{"score":40}', "needs_work"),
    )
    for workflow, raw, expected in cases:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = cli_main(
                [
                    command,
                    "--config",
                    str(configuration),
                    "--workflow",
                    workflow,
                    "--input",
                    raw,
                ]
            )
        if (
            code != 0
            or f"[{workflow.upper()}] result: {expected}"
            not in output.getvalue().splitlines()
        ):
            raise RuntimeError(f"Installed workflow contract failed: {workflow} {raw}")
        print(f"PASS {workflow} {raw} -> {expected}")
    output = io.StringIO()
    with contextlib.redirect_stderr(output):
        code = cli_main(
            [
                command,
                "--config",
                str(configuration),
                "--workflow",
                "wf-03",
                "--input",
                '{"score":101}',
            ]
        )
    if code != 2 or "Input error" not in output.getvalue():
        raise RuntimeError("Invalid input did not produce exit 2.")
    if attempts:
        raise RuntimeError(f"Network attempts were observed: {attempts}")
    print("PASS runtime network probe: zero Python socket/DNS attempts")


if __name__ == "__main__":
    main()
