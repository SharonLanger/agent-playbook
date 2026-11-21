"""Opt-in bounded read-only checks using the application's configuration."""

import argparse

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration
from agent_playbook.observability.adapters.langfuse.connection import (
    check_connection as check_langfuse,
)
from agent_playbook.observability.adapters.otel_logging.connection import (
    check_connection as check_logging,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config")
    args = parser.parse_args()
    try:
        settings = load_configuration(args.config)
    except ConfigurationError as error:
        print(f"Configuration error: {error}")
        return 2
    tracing = check_langfuse(settings.integrations.langfuse)
    logs = check_logging(settings.integrations.logging)
    print(f"langfuse: {tracing.status}")
    print(f"logging: {logs.status}; authentication: {logs.authentication}")
    return int(
        any(result.status not in {"ok", "skipped"} for result in (tracing, logs))
    )


if __name__ == "__main__":
    raise SystemExit(main())
