"""Bounded, read-only authentication check for a configured Langfuse project."""

from dataclasses import dataclass
from typing import Literal

import httpx

from agent_playbook.config.models import LangfuseSettings
from langfuse import Langfuse
from langfuse.api import LangfuseAPI
from langfuse.api.core.api_error import ApiError

ConnectionStatus = Literal["ok", "skipped", "auth_failed", "unreachable", "failed"]


@dataclass(frozen=True)
class ConnectionResult:
    status: ConnectionStatus
    base_url: str


def create_client(
    settings: LangfuseSettings, *, tracing_enabled: bool = False
) -> Langfuse:
    assert settings.public_key is not None and settings.secret_key is not None
    return Langfuse(
        public_key=settings.public_key.get_secret_value(),
        secret_key=settings.secret_key.get_secret_value(),
        base_url=settings.base_url,
        environment=settings.environment,
        timeout=5,
        tracing_enabled=tracing_enabled,
    )


def check_connection(settings: LangfuseSettings) -> ConnectionResult:
    """Check project-scoped API access; create no observations."""
    if not settings.enabled:
        return ConnectionResult("skipped", settings.base_url)

    assert settings.public_key is not None and settings.secret_key is not None
    try:
        # A Langfuse client caches its tracing resource manager by public key.
        # A disabled preflight client would poison a later exporting client.
        with httpx.Client(timeout=5) as transport:
            api = LangfuseAPI(
                base_url=settings.base_url,
                username=settings.public_key.get_secret_value(),
                password=settings.secret_key.get_secret_value(),
                httpx_client=transport,
            )
            projects = api.projects.get()
        if not projects.data:
            return ConnectionResult("auth_failed", settings.base_url)
        return ConnectionResult("ok", settings.base_url)
    except ApiError as error:
        status: ConnectionStatus = (
            "auth_failed" if error.status_code in (401, 403) else "failed"
        )
        return ConnectionResult(status, settings.base_url)
    except httpx.TransportError:
        return ConnectionResult("unreachable", settings.base_url)
    except Exception:
        # SDK messages may contain credentials, URLs or response bodies.
        return ConnectionResult("failed", settings.base_url)
