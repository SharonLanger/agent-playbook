"""Explicit read-only VictoriaLogs health check; never an ingestion test."""

from dataclasses import dataclass
from urllib.parse import urlsplit

import requests

from agent_playbook.config.models import LoggingSettings
from agent_playbook.observability.adapters.langfuse.connection import ConnectionStatus


@dataclass(frozen=True)
class ConnectionResult:
    status: ConnectionStatus
    authentication: str = "not_applicable"


def check_connection(settings: LoggingSettings) -> ConnectionResult:
    if not settings.enabled:
        return ConnectionResult("skipped")
    url = urlsplit(settings.endpoint)
    try:
        with requests.Session() as session:
            session.trust_env = False
            response = session.get(
                f"http://{url.netloc}/health", timeout=5, allow_redirects=False
            )
        return ConnectionResult(
            "ok"
            if response.status_code == 200
            else "auth_failed"
            if response.status_code in (401, 403)
            else "failed"
        )
    except requests.RequestException:
        return ConnectionResult("unreachable")
    except Exception:
        return ConnectionResult("failed")
