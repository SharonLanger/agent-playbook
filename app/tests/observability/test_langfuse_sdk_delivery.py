"""Real pinned SDK against an independent loopback HTTP fixture."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4

import pytest
from pydantic import SecretStr

from agent_playbook.config.models import LangfuseSettings
from agent_playbook.observability.adapters.langfuse.connection import check_connection
from agent_playbook.observability.adapters.langfuse.observations import LangfuseSession


@pytest.mark.parametrize("reject", [False, True])
def test_preflight_does_not_disable_export_and_readback_is_truthful(
    reject: bool,
) -> None:
    posts: list[str] = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/api/public/projects":
                body = json.dumps(
                    {
                        "data": [
                            {
                                "id": "fixture-project",
                                "name": "fixture",
                                "organization": {"id": "org", "name": "Fixture"},
                                "metadata": {},
                            }
                        ]
                    }
                )
                self.send_response(200)
            elif self.path.startswith("/api/public/traces/") and posts and not reject:
                body = json.dumps({"id": self.path.rsplit("/", 1)[-1]})
                self.send_response(200)
            else:
                body = "{}"
                self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            self.rfile.read(length)
            posts.append(self.path)
            self.send_response(400 if reject else 200)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    settings = LangfuseSettings(
        enabled=True,
        base_url=f"http://127.0.0.1:{server.server_port}",
        public_key=SecretStr(f"pk-lf-{uuid4()}"),
        secret_key=SecretStr("sk-lf-fixture"),
    )
    try:
        assert check_connection(settings).status == "ok"
        session = LangfuseSession(settings)
        try:
            trace_id, root = session.start_trace(
                run_id=str(uuid4()), name="fixture", input={}, metadata={}
            )
            root.finish(output={"ok": True})
            result = session.verify_delivery(trace_id, timeout_seconds=0.2)
            assert any(path.endswith("/api/public/otel/v1/traces") for path in posts)
            assert result.status == ("unconfirmed" if reject else "verified")
        finally:
            session.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
