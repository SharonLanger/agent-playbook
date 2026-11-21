"""Validated integration settings; workflow policies stay with their workflow."""

from ipaddress import ip_address
from typing import Literal
from urllib.parse import urlsplit

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)


class CrewAISettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    usage_telemetry_enabled: bool
    tracing_enabled: bool
    show_framework_events: bool


class LangfuseSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    enabled: bool = False
    base_url: str = "http://localhost:3000"
    environment: str = "local"
    public_key: SecretStr | None = None
    secret_key: SecretStr | None = None

    @field_validator("base_url")
    @classmethod
    def valid_base_url(cls, value: str) -> str:
        try:
            parts = urlsplit(value)
            valid = (
                parts.scheme in {"http", "https"}
                and parts.hostname is not None
                and parts.port != 0
                and parts.username is None
                and parts.password is None
                and parts.path in {"", "/"}
                and not parts.query
                and not parts.fragment
                and not any(char.isspace() for char in value)
            )
        except ValueError:
            valid = False
        if not valid:
            raise ValueError("base_url must be an HTTP(S) origin without credentials")
        return value.rstrip("/")

    @field_validator("environment")
    @classmethod
    def valid_environment(cls, value: str) -> str:
        if (
            not value
            or len(value) > 64
            or not all(char.isalnum() or char in "_-" for char in value)
        ):
            raise ValueError("environment must be a short label")
        return value

    @model_validator(mode="after")
    def required_keys(self) -> "LangfuseSettings":
        if self.enabled and (self.public_key is None or self.secret_key is None):
            raise ValueError("enabled Langfuse requires project keys")
        return self


class LoggingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    enabled: bool = False
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    endpoint: str = "http://127.0.0.1:9428/insert/opentelemetry/v1/logs"

    @field_validator("endpoint")
    @classmethod
    def local_endpoint(cls, value: str) -> str:
        try:
            url = urlsplit(value)
            valid = (
                url.scheme == "http"
                and ip_address(url.hostname or "").is_loopback
                and url.port is not None
                and 1 <= url.port <= 65535
                and url.path == "/insert/opentelemetry/v1/logs"
                and url.username is None
                and url.password is None
                and not url.query
                and not url.fragment
                and not any(c.isspace() for c in value)
            )
        except ValueError:
            valid = False
        if not valid:
            raise ValueError("endpoint must be a local HTTP OTLP logs endpoint")
        return value


class IntegrationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    crewai: CrewAISettings
    langfuse: LangfuseSettings = LangfuseSettings()
    logging: LoggingSettings = LoggingSettings()


class SecretsSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    file: str

    @field_validator("file")
    @classmethod
    def valid_file(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("file must name a nonempty path")
        return value


class ApplicationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    integrations: IntegrationSettings
    secrets: SecretsSettings
    workflows: dict[str, object] = Field()
