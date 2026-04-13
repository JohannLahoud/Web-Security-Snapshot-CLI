from __future__ import annotations

from dataclasses import dataclass

import requests


SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


@dataclass(slots=True)
class HttpInspection:
    url: str
    ok: bool
    status_code: int | None
    headers: dict[str, str]
    errors: list[str]


def fetch_homepage(domain: str, timeout: int = 10) -> HttpInspection:
    url = f"https://{domain}"
    errors: list[str] = []

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "web-security-snapshot/0.1"},
        )
        return HttpInspection(
            url=response.url,
            ok=True,
            status_code=response.status_code,
            headers=dict(response.headers),
            errors=errors,
        )
    except requests.RequestException as exc:
        errors.append(f"HTTPS homepage fetch failed: {exc}")
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
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "web-security-snapshot/0.1"},
        )
        return response.status_code == 200, response.url
    except requests.RequestException:
        return False, url
