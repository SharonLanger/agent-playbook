"""LS-03: reject alternate destinations and exercise actual Requests routing."""

import sys
from io import BytesIO
from typing import Any

import pytest
import requests
from requests.adapters import HTTPAdapter

from tooling.logging import logging_smoke


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://127.0.0.1:9428/insert/opentelemetry/v1/logs",
        "http://example.org/insert/opentelemetry/v1/logs",
        "http://localhost:9428/insert/opentelemetry/v1/logs",
        "http://127.0.0.1.evil/insert/opentelemetry/v1/logs",
        "http://user:secret@127.0.0.1/insert/opentelemetry/v1/logs",
        "http://127.0.0.1:0/insert/opentelemetry/v1/logs",
        "http://127.0.0.1:65536/insert/opentelemetry/v1/logs",
        "http://127.0.0.1:bad/insert/opentelemetry/v1/logs",
        "http://127.0.0.1:9428/other",
        "http://127.0.0.1:9428/insert/opentelemetry/v1/logs?forward=remote",
        "http://127.0.0.1:9428/insert/opentelemetry/v1/logs#fragment",
    ],
)
def test_invalid_endpoint_never_constructs_exporter(
    endpoint: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_exporter(**_kwargs: Any) -> None:
        pytest.fail("invalid endpoint reached exporter construction")

    monkeypatch.setattr(logging_smoke, "OTLPLogExporter", forbidden_exporter)
    monkeypatch.setattr(sys, "argv", ["logging_smoke.py", "--endpoint", endpoint])
    with pytest.raises(SystemExit) as error:
        logging_smoke.main()
    assert error.value.code == 2


@pytest.mark.parametrize("port", ["", ":9428", ":19428"])
def test_loopback_endpoint(port: str) -> None:
    endpoint = f"http://127.0.0.1{port}/insert/opentelemetry/v1/logs"
    assert logging_smoke.local_endpoint(endpoint) == endpoint


def test_session_ignores_proxy_and_does_not_follow_redirect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destinations: list[str | None] = []

    def redirect(
        _adapter: HTTPAdapter, request: requests.PreparedRequest, **kwargs: Any
    ) -> requests.Response:
        destinations.append(request.url)
        assert not kwargs.get("proxies")
        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = "http://remote.invalid/collect"
        response.request = request
        response.url = request.url or ""
        response.raw = BytesIO(b"")
        return response

    class CheckedSession(Exception):
        pass

    def inspect_exporter(*, session: requests.Session, **_kwargs: Any) -> None:
        with pytest.raises(requests.TooManyRedirects):
            session.post(logging_smoke.DEFAULT_ENDPOINT, data=b"synthetic")
        raise CheckedSession

    monkeypatch.setenv("HTTP_PROXY", "http://proxy.invalid:8888")
    monkeypatch.setenv("ALL_PROXY", "http://proxy.invalid:8888")
    monkeypatch.setenv("NO_PROXY", "")
    monkeypatch.setattr(HTTPAdapter, "send", redirect)
    monkeypatch.setattr(logging_smoke, "OTLPLogExporter", inspect_exporter)
    monkeypatch.setattr(sys, "argv", ["logging_smoke.py"])
    with pytest.raises(CheckedSession):
        logging_smoke.main()
    assert destinations == [logging_smoke.DEFAULT_ENDPOINT]
