from __future__ import annotations

from dataclasses import dataclass

import certifi
import requests
from requests import Response
from requests.exceptions import RequestException, SSLError


SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]

USER_AGENT = "web-security-snapshot/0.1"
CA_BUNDLE_PATH = certifi.where()


@dataclass(slots=True)
class HttpInspection:
    url: str
    ok: bool
    status_code: int | None
    headers: dict[str, str]
    errors: list[str]


def _https_get(url: str, timeout: int) -> Response:
    return requests.get(
        url,
        timeout=timeout,
        allow_redirects=True,
        headers={"User-Agent": USER_AGENT},
        verify=CA_BUNDLE_PATH,
    )


def _format_request_error(url: str, exc: RequestException) -> str:
    if isinstance(exc, SSLError):
        return (
            "HTTPS request failed: TLS certificate verification failed for "
            f"{url} using certifi CA bundle at {CA_BUNDLE_PATH}. "
            f"Underlying error: {exc}"
        )
    return f"HTTPS request failed for {url}: {exc}"


def fetch_homepage(domain: str, timeout: int = 10) -> HttpInspection:
    url = f"https://{domain}"
    errors: list[str] = []

    try:
        response = _https_get(url, timeout)
        return HttpInspection(
            url=response.url,
            ok=True,
            status_code=response.status_code,
            headers=dict(response.headers),
            errors=errors,
        )
    except RequestException as exc:
        errors.append(_format_request_error(url, exc))
        return HttpInspection(
            url=url,
            ok=False,
            status_code=None,
            headers={},
            errors=errors,
        )


def fetch_optional_text(domain: str, path: str, timeout: int = 10) -> tuple[bool, str]:
    url = f"https://{domain}{path}"
    try:
        response = _https_get(url, timeout)
        return response.status_code == 200, response.url
    except RequestException:
        return False, url
