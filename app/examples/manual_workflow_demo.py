"""Run a small, one-shot batch of the existing workflows through the source CLI.

From the repository root, after the normal app bootstrap:
    app/.venv/bin/python app/examples/manual_workflow_demo.py
    app/.venv/bin/python app/examples/manual_workflow_demo.py --config /path/to/application.yaml

For Langfuse inspection, first start your local server and configure the application
with your project credentials using the normal external settings. Actual workflow
tracing depends on the ongoing runtime integration; traces are not yet guaranteed
on main. This script creates no telemetry itself. Filter by workflow name/ID and
the time of this batch; only normal CLI output can expose additional identifiers.

Parallel runs are independent CLI processes, not parallel branches in a workflow.
Each invocation has a 120-second limit; a failed invocation does not stop the rest.
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]


def run_demo(
    workflow_id: str, data: dict[str, int], config: str | None
) -> tuple[int | None, str]:
    command = [
        sys.executable,
        "-m",
        "agent_playbook.cli",
        "dev-run",
        "--workflow",
        workflow_id,
        "--input",
        json.dumps(data),
    ]
    if config is not None:
        command.extend(["--config", config])
    try:
        result = subprocess.run(
            command,
            cwd=APP_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120,
            check=False,
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired as error:
        output = error.stdout or b""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        return None, output + "\nTimed out after 120 seconds."
    except OSError as error:
        return None, f"Could not launch CLI: {error}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", help="Application YAML; relative to your current directory."
    )
    args = parser.parse_args()
    config = str(Path(args.config).expanduser().resolve()) if args.config else None
    sequential = [
        ("sequence", "wf-01", {}),
        ("arithmetic: (3 + 2) * 4", "wf-02",
         {"initial": 3, "increment": 2, "multiplier": 4}),
        ("route: pass", "wf-03", {"score": 85}),
    ]
    parallel = [
        ("sequence repeated", "wf-01", {}),
        ("arithmetic: (-5 + 2) * 3", "wf-02",
         {"initial": -5, "increment": 2, "multiplier": 3}),
        ("arithmetic: (10 - 10) * 7", "wf-02",
         {"initial": 10, "increment": -10, "multiplier": 7}),
        ("route: needs_work", "wf-03", {"score": 59}),
        ("route: pass at threshold", "wf-03", {"score": 60}),
    ]
    outcomes: list[tuple[str, int | None]] = []

    def show(
        label: str, workflow_id: str, data: dict[str, int],
        result: tuple[int | None, str],
    ) -> None:
        code, output = result
        print(f"\n=== {label} | {workflow_id} | input={json.dumps(data)} ===", flush=True)
        status = code if code is not None else "unavailable (launch error or timeout)"
        print(f"CLI exit: {status}")
        print(output, end="" if output.endswith("\n") else "\n", flush=True)
        outcomes.append((label, code))

    print("Sequential CLI invocations", flush=True)
    for label, workflow_id, data in sequential:
        show(label, workflow_id, data, run_demo(workflow_id, data, config))

    print("\nParallel CLI invocations (at most two at a time)", flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = {
            pool.submit(run_demo, workflow_id, data, config): (label, workflow_id, data)
            for label, workflow_id, data in parallel
        }
        for future in as_completed(pending):
            label, workflow_id, data = pending[future]
            show(label, workflow_id, data, future.result())

    print("\nSummary (CLI exit codes)")
    for label, code in outcomes:
        print(f"  {label}: {code if code is not None else 'unavailable'}")
    return 0 if all(code == 0 for _, code in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
