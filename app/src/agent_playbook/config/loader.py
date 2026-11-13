"""Read shared YAML, optional local values and documented environment overrides."""

import os
from collections.abc import Hashable
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter, ValidationError
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import ApplicationSettings
from agent_playbook.config.paths import configuration_path


class StrictLoader(yaml.SafeLoader):
    def flatten_mapping(self, node: MappingNode) -> None:
        if any(key.tag == "tag:yaml.org,2002:merge" for key, _ in node.value):
            raise ConstructorError(
                None, None, "YAML merge keys are unsupported", node.start_mark
            )
        super().flatten_mapping(node)

    def construct_mapping(
        self, node: MappingNode, deep: bool = False
    ) -> dict[Hashable, Any]:
        seen: set[str] = set()
        for key_node, _ in node.value:
            if key_node.tag != "tag:yaml.org,2002:str":
                raise ConstructorError(
                    None, None, "Invalid YAML key", key_node.start_mark
                )
            key = key_node.value
            if key in seen:
                raise ConstructorError(
                    None, None, "Duplicate YAML key", key_node.start_mark
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


_MAPPING = TypeAdapter(dict[str, object])
_OVERRIDES = {
    "usage_telemetry_enabled": "AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED",
    "tracing_enabled": "AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED",
    "show_framework_events": "AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS",
}


def _mapping(value: object) -> dict[str, object]:
    return _MAPPING.validate_python(value, strict=True)


def _read(path: Path) -> dict[str, object]:
    try:
        with path.open(encoding="utf-8") as source:
            value: object = yaml.load(source, Loader=StrictLoader)
        return _mapping(value)
    except (OSError, UnicodeError, yaml.YAMLError, ValidationError):
        # YAML/parser errors can include source lines containing private values.
        raise ConfigurationError(
            f"Cannot read configuration {path}; use a readable YAML mapping."
        ) from None


def _merge(base: dict[str, object], overlay: dict[str, object]) -> dict[str, object]:
    result = base.copy()
    for key, value in overlay.items():
        previous = result.get(key)
        if isinstance(previous, dict) and isinstance(value, dict):
            result[key] = _merge(_mapping(result[key]), _mapping(overlay[key]))
        else:
            result[key] = value
    return result


def _boolean(value: str, name: str) -> bool:
    if value.lower() not in ("true", "false"):
        raise ConfigurationError(f"Environment variable {name} must be true or false.")
    return value.lower() == "true"


def load_configuration(path: str | None = None) -> ApplicationSettings:
    """Reload for each run; never cache files or print resolved setting values."""
    selected = configuration_path(path)
    data = _read(selected)
    local = selected.with_name(f"{selected.stem}.local{selected.suffix}")
    try:
        if local.exists():
            data = _merge(data, _read(local))
        integration = _mapping(data.get("integrations"))
        crewai = _mapping(integration.get("crewai"))
        for field, variable in _OVERRIDES.items():
            if variable in os.environ:
                crewai[field] = _boolean(os.environ[variable], variable)
            elif isinstance(crewai.get(field), dict):
                reference = _mapping(crewai[field])
                name = reference.get("env")
                if set(reference) != {"env"} or not isinstance(name, str) or not name:
                    raise ConfigurationError(
                        f"Invalid environment reference for {field}."
                    )
                if name not in os.environ:
                    raise ConfigurationError(
                        f"Required environment variable {name} is missing."
                    )
                crewai[field] = _boolean(os.environ[name], name)
        integration["crewai"] = crewai
        data["integrations"] = integration
        return ApplicationSettings.model_validate(data)
    except ValidationError as error:
        # Report field names/types only, never input values or secret-bearing context.
        fields = "; ".join(
            f"{'.'.join(str(part) for part in item['loc']) or 'root'} ({item['type']})"
            for item in error.errors(
                include_input=False, include_context=False, include_url=False
            )
        )
        raise ConfigurationError(f"Invalid configuration: {fields}.") from None
