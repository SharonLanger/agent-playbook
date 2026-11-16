"""Example-local configuration: called before importing CrewAI."""

import os
import tomllib
from pathlib import Path
from typing import cast


def configure() -> bool:
    with Path(__file__).with_name("settings.toml").open("rb") as stream:
        document = tomllib.load(stream)
    if set(document) != {"crewai"}:
        raise ValueError("Expected only the crewai settings section")
    raw = document["crewai"]
    if not isinstance(raw, dict):
        raise ValueError("CrewAI settings must be a table")
    settings = cast(dict[str, object], raw)
    names = {"usage_telemetry_enabled", "tracing_enabled", "suppress_flow_events"}
    if set(settings) != names:
        raise ValueError("Invalid CrewAI settings keys")
    for key in names:
        if type(settings[key]) is not bool:
            raise ValueError(f"{key} must be a boolean")
    for env, key, invert in (
        ("CREWAI_DISABLE_TELEMETRY", "usage_telemetry_enabled", True),
        ("CREWAI_TRACING_ENABLED", "tracing_enabled", False),
    ):
        value = os.environ.get(env)
        if value is not None and value.lower() not in {"true", "false"}:
            raise ValueError(f"{env} must be true or false")
        enabled = bool(settings[key])
        os.environ[env] = (
            value.lower()
            if value is not None
            else str(not enabled if invert else enabled).lower()
        )
    return bool(settings["suppress_flow_events"])
