"""Explicit read-only Langfuse project connection check."""

import argparse

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration
from agent_playbook.observability.adapters.langfuse.connection import check_connection


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="selected application YAML file")
    args = parser.parse_args(argv)
    try:
        settings = load_configuration(args.config).integrations.langfuse
    except ConfigurationError as error:
        # ConfigurationError messages are constructed from safe paths/names only.
        print(f"Invalid Langfuse configuration: {error}")
        return 2

    result = check_connection(settings)
    if result.status == "ok":
        print(f"Langfuse project authentication succeeded at {result.base_url}.")
        return 0
    if result.status == "skipped":
        print("Langfuse is disabled; no connection attempted.")
        return 3
    if result.status == "auth_failed":
        print(f"Langfuse project authentication failed at {result.base_url}.")
    elif result.status == "unreachable":
        print(
            f"Langfuse is unreachable at {result.base_url}; check the service and URL."
        )
    else:
        print(f"Langfuse connection failed at {result.base_url}.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
