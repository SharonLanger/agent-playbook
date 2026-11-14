"""Explicitly send one editable synthetic arithmetic run to Langfuse."""

import argparse
import time
from uuid import uuid4

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration
from agent_playbook.observability.adapters.langfuse.connection import check_connection
from agent_playbook.observability.adapters.langfuse.observations import (
    LangfuseSession,
    Observation,
)

# Personal playground values: edit these, or use the matching command options.
INITIAL = 3
INCREMENT = 2
MULTIPLIER = 4
FAIL_STEP: str | None = None  # None, "add", or "multiply"
DELAY_SECONDS = 0.0


class SimulatedStepError(Exception):
    """Intentional mock failure, distinct from setup or transport errors."""


def step(
    root: Observation,
    *,
    name: str,
    payload: dict[str, int],
    value: int,
    fail_step: str | None,
    delay_seconds: float,
) -> int:
    observation = root.child(name, payload)
    started = time.perf_counter_ns()
    try:
        if delay_seconds:
            time.sleep(delay_seconds)
        if fail_step == name:
            raise SimulatedStepError(f"Mock {name} step failed on purpose")
        output = {
            "value": value,
            "elapsed_ms": (time.perf_counter_ns() - started) / 1e6,
        }
        observation.finish(output=output)
        return value
    except SimulatedStepError as error:
        observation.finish(error=str(error))
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="selected application YAML")
    parser.add_argument("--initial", type=int, default=INITIAL)
    parser.add_argument("--increment", type=int, default=INCREMENT)
    parser.add_argument("--multiplier", type=int, default=MULTIPLIER)
    parser.add_argument("--fail-step", choices=("add", "multiply"), default=FAIL_STEP)
    parser.add_argument("--delay-seconds", type=float, default=DELAY_SECONDS)
    args = parser.parse_args(argv)
    if args.delay_seconds < 0:
        parser.error("delay must be nonnegative")
    try:
        settings = load_configuration(args.config).integrations.langfuse
    except ConfigurationError:
        print(
            "Invalid Langfuse configuration; check the selected YAML and key references."
        )
        return 2
    result = check_connection(settings)
    if result.status != "ok":
        print(
            f"Langfuse connection is {result.status}; run the connection check first."
        )
        return 1

    run_id = str(uuid4())
    session: LangfuseSession | None = None
    try:
        session = LangfuseSession(settings)
        trace_id, root = session.start_trace(
            run_id=run_id,
            name="mock-wf-02",
            input={
                "initial": args.initial,
                "increment": args.increment,
                "multiplier": args.multiplier,
            },
            metadata={"source": "mock", "workflow_id": "mock-wf-02", "run_id": run_id},
        )
        outcome = "success"
        try:
            initial = step(
                root,
                name="initialize",
                payload={"initial": args.initial},
                value=args.initial,
                fail_step=args.fail_step,
                delay_seconds=args.delay_seconds,
            )
            added = step(
                root,
                name="add",
                payload={"left": initial, "right": args.increment},
                value=initial + args.increment,
                fail_step=args.fail_step,
                delay_seconds=args.delay_seconds,
            )
            multiplied = step(
                root,
                name="multiply",
                payload={"left": added, "right": args.multiplier},
                value=added * args.multiplier,
                fail_step=args.fail_step,
                delay_seconds=args.delay_seconds,
            )
            final = step(
                root,
                name="finish",
                payload={"value": multiplied},
                value=multiplied,
                fail_step=args.fail_step,
                delay_seconds=args.delay_seconds,
            )
            root.finish(output={"result": final})
        except SimulatedStepError as error:
            outcome = f"simulated error: {error}"
            root.finish(error=str(error))
        delivery = session.verify_delivery(trace_id)
        url = session.trace_url(trace_id)
        print(f"run_id: {run_id}\ntrace_id: {trace_id}\noutcome: {outcome}")
        print(f"trace_url: {url or 'unavailable; locate the trace ID in the UI'}")
        print(f"delivery: {delivery.status}")
        if delivery.status == "verified":
            print("Trace is visible through the Langfuse project API; inspect details in the UI.")
            return 0
        print("Trace delivery is unconfirmed; check the service and project settings.")
        return 1
    except Exception:
        print("Trace export failed; check the service and project settings.")
        return 1
    finally:
        if session is not None:
            try:
                session.close()
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
