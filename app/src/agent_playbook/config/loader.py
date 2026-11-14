"""Read shared YAML, optional local values and documented environment overrides."""

import os
import re
from collections.abc import Hashable
from pathlib import Path
from typing import Any, cast

import yaml
from pydantic import TypeAdapter, ValidationError
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import ApplicationSettings, SecretsSettings
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
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise ConstructorError(
                    None, None, "YAML merge keys are unsupported", key_node.start_mark
                )
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
_LANGFUSE_OVERRIDES = {
    "enabled": "AGENT_PLAYBOOK_LANGFUSE_ENABLED",
    "base_url": "AGENT_PLAYBOOK_LANGFUSE_BASE_URL",
    "environment": "AGENT_PLAYBOOK_LANGFUSE_ENVIRONMENT",
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


_ENV_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def _parse_secrets_file(path: Path) -> dict[str, str]:
    """Read a strict, non-executing dotenv subset from an explicitly selected file."""
    values: dict[str, str] = {}
    try:
        with path.open(encoding="utf-8") as source:
            for raw_line in source:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                name, separator, raw_value = line.partition("=")
                name = name.strip()
                if not separator or not _ENV_NAME.fullmatch(name):
                    raise ValueError
                if name in values or name == "AGENT_PLAYBOOK_CONFIG":
                    raise ValueError
                value = raw_value.strip()
                if value.startswith(("'", '"')):
                    quote = value[0]
                    end = -1
                    for index in range(1, len(value)):
                        if value[index] != quote:
                            continue
                        preceding_slashes = 0
                        cursor = index - 1
                        while cursor > 0 and value[cursor] == "\\":
                            preceding_slashes += 1
                            cursor -= 1
                        if quote == '"' and preceding_slashes % 2:
                            continue
                        end = index
                        break
                    if end < 0:
                        raise ValueError
                    raw_trailing = value[end + 1 :]
                    trailing = raw_trailing.strip()
                    if trailing and (
                        not raw_trailing[:1].isspace() or not trailing.startswith("#")
                    ):
                        raise ValueError
                    value = value[1:end]
                    if quote == '"':
                        value = re.sub(
                            r"\\([\\\"])", lambda match: match.group(1), value
                        )
                else:
                    value = re.sub(r"\s+#.*$", "", value).strip()
                    if "'" in value or '"' in value:
                        raise ValueError
                values[name] = value
    except (OSError, UnicodeError, ValueError):
        # Do not expose parser exceptions, source lines, or secret values.
        raise ConfigurationError(
            f"Cannot read secrets file {path}; use valid UTF-8 NAME=value lines."
        ) from None
    return values


def _secrets_file_path(value: str, configuration: Path) -> Path:
    """Resolve the configured secrets file relative to the selected YAML."""
    try:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = configuration.parent / path
    except (OSError, RuntimeError, ValueError):
        raise ConfigurationError("secrets.file must name a usable file path.") from None
    return path


def load_configuration(path: str | None = None) -> ApplicationSettings:
    """Reload for each run; never cache files or print resolved setting values."""
    selected = configuration_path(path)
    data = _read(selected)
    local = selected.with_name(f"{selected.stem}.local{selected.suffix}")
    try:
        if local.exists():
            data = _merge(data, _read(local))
        try:
            secrets_data = _mapping(data.get("secrets"))
        except ValidationError:
            raise ConfigurationError(
                "Invalid configuration: secrets.file must name a nonempty file path."
            ) from None
        file_value = secrets_data.get("file")
        if not isinstance(file_value, str) or not file_value.strip():
            raise ConfigurationError(
                "Invalid configuration: secrets.file must name a nonempty file path."
            )
        secrets = SecretsSettings.model_validate(secrets_data)
        secret_values = _parse_secrets_file(_secrets_file_path(secrets.file, selected))
        # Process values, including explicit empty strings, take precedence.
        environment = secret_values | dict(os.environ)
        integration = _mapping(data.get("integrations"))
        crewai = _mapping(integration.get("crewai"))
        for field, variable in _OVERRIDES.items():
            if variable in environment:
                crewai[field] = _boolean(environment[variable], variable)
            elif isinstance(crewai.get(field), dict):
                reference = _mapping(crewai[field])
                name = reference.get("env")
                if set(reference) != {"env"} or not isinstance(name, str) or not name:
                    raise ConfigurationError(
                        f"Invalid environment reference for {field}."
                    )
                if name not in environment:
                    raise ConfigurationError(
                        f"Required environment variable {name} is missing."
                    )
                crewai[field] = _boolean(environment[name], name)
        integration["crewai"] = crewai
        empty: dict[str, object] = {}
        langfuse = _mapping(integration.get("langfuse", empty))
        for field, variable in _LANGFUSE_OVERRIDES.items():
            if variable in environment:
                langfuse[field] = (
                    _boolean(environment[variable], variable)
                    if field == "enabled"
                    else environment[variable]
                )
        for field in ("public_key", "secret_key"):
            if field not in langfuse:
                continue
            reference = langfuse[field]
            if not isinstance(reference, dict):
                raise ConfigurationError(f"Invalid Langfuse {field} reference.")
            parsed = _mapping(cast(object, reference))
            name = parsed.get("env")
            if set(parsed) != {"env"} or not isinstance(name, str) or not name:
                raise ConfigurationError(f"Invalid Langfuse {field} reference.")
            if langfuse.get("enabled", False):
                if name not in environment or not environment[name]:
                    raise ConfigurationError(
                        f"Required Langfuse {field} environment variable is missing."
                    )
                langfuse[field] = environment[name]
            else:
                langfuse[field] = None
        integration["langfuse"] = langfuse
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
