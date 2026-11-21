"""Select and manage checkout-only local services in isolated helper processes."""

import argparse
import sys
import time
from pathlib import Path

from agent_playbook.cli.service_process import (
    OperationCancelled,
    cancellation_signals,
    ensure_active,
    supervise_component,
)
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import ServiceSelection, load_service_selection

APP = Path(__file__).resolve().parent.parent
AGGREGATE_SECONDS = {"start": 1500.0, "status": 130.0, "stop": 130.0}
COMPONENTS = {"logs": "logging/manage.py", "langfuse": "observability/manage.py"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    for action in AGGREGATE_SECONDS:
        actions.add_argument(
            f"--{action}", dest="action", action="store_const", const=action
        )
    parser.add_argument("--config")
    parser.add_argument("--env-file")
    args = parser.parse_args(argv)
    action: str = args.action
    deadline = time.monotonic() + AGGREGATE_SECONDS[action]
    try:
        with cancellation_signals() as cancellation:
            selection: ServiceSelection | None = None
            if action != "stop":
                try:
                    selection = load_service_selection(args.config)
                except ConfigurationError as error:
                    print(
                        f"Service selection unavailable: {error}",
                        file=sys.stderr,
                        flush=True,
                    )
                    ensure_active(cancellation, deadline)
                    if action == "start":
                        return 2
            enabled = {
                "logs": selection.logging if selection else False,
                "langfuse": selection.langfuse if selection else False,
            }
            result = 2 if action == "status" and selection is None else 0
            order = reversed(COMPONENTS) if action == "stop" else iter(COMPONENTS)
            for name in order:
                ensure_active(cancellation, deadline)
                if action == "start" and not enabled[name]:
                    print(f"{name} skipped: workflow integration disabled.", flush=True)
                    continue
                if action == "status":
                    label = (
                        "unavailable"
                        if selection is None
                        else "enabled"
                        if enabled[name]
                        else "disabled"
                    )
                    print(f"{name} selection: {label}", flush=True)
                command = [
                    sys.executable,
                    str(APP / "tooling" / COMPONENTS[name]),
                    f"--{action}",
                ]
                if name == "langfuse" and args.env_file is not None:
                    command += ["--env-file", args.env_file]
                code = supervise_component(
                    command,
                    APP,
                    name,
                    action,
                    cancellation,
                    aggregate_deadline=deadline,
                )
                if code == 2 or action != "status" or enabled[name]:
                    result = max(result, 2 if code == 2 else int(code != 0))
            ensure_active(cancellation, deadline)
            return result
    except OperationCancelled as error:
        print(f"{error} Inspect --status before retrying.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(
            "Service operation interrupted. Inspect --status before retrying.",
            file=sys.stderr,
        )
        return 1
    except Exception:
        print(
            "Service operation failed. Inspect --status before retrying.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
