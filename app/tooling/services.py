"""Select and manage checkout-only local services in isolated helper processes."""

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import cast

from agent_playbook.cli.service_process import (
    Cancellation,
    OperationCancelled,
    cancellation_signals,
    ensure_active,
    supervise_component,
    supervise_helper,
)

APP = Path(__file__).resolve().parent.parent
AGGREGATE_SECONDS = {"start": 1500.0, "status": 130.0, "stop": 130.0}
COMPONENTS = {"logs": "logging/manage.py", "langfuse": "observability/manage.py"}


def _selection_worker(config: str | None) -> int:
    from agent_playbook.config.errors import ConfigurationError
    from agent_playbook.config.loader import load_service_selection

    try:
        selection = load_service_selection(config)
    except ConfigurationError as error:
        print(f"Service selection unavailable: {error}", file=sys.stderr, flush=True)
        return 2
    except Exception:
        print(
            "Service selection unavailable: could not load configuration.",
            file=sys.stderr,
        )
        return 2
    print(json.dumps([selection.logging, selection.langfuse]))
    return 0


def _select(
    config: str | None, cancellation: Cancellation, deadline: float
) -> tuple[bool, bool] | None:
    argv = [sys.executable, str(Path(__file__).resolve()), "--select"]
    if config is not None:
        argv.append(config)
    with tempfile.TemporaryFile() as selection:
        result = supervise_helper(
            argv,
            APP,
            "Service selection",
            cancellation,
            aggregate_deadline=deadline,
            stdout=selection,
        )
        ensure_active(cancellation, deadline)
        if result == 2:
            return None
        if result == 0:
            selection.seek(0)
            try:
                payload: object = json.loads(selection.read(64))
                if isinstance(payload, list):
                    flags = cast(list[object], payload)
                    if len(flags) == 2:
                        logging, langfuse = flags
                        if isinstance(logging, bool) and isinstance(langfuse, bool):
                            return logging, langfuse
            except ValueError:
                pass
    print(
        "Service selection unavailable: could not read selection result.",
        file=sys.stderr,
    )
    return None


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
            selection = (
                None
                if action == "stop"
                else _select(args.config, cancellation, deadline)
            )
            if selection is None and action == "start":
                return 2
            logging, langfuse = selection or (False, False)
            enabled = {"logs": logging, "langfuse": langfuse}
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
    if sys.argv[1:2] == ["--select"]:
        raise SystemExit(_selection_worker(sys.argv[2] if len(sys.argv) == 3 else None))
    raise SystemExit(main())
