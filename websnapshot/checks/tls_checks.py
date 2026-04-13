from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import socket
import ssl


@dataclass(slots=True)
class TlsInspection:
    expires_at: str | None
    days_remaining: int | None
    error: str | None


def inspect_certificate_expiry(domain: str, port: int = 443, timeout: int = 10) -> TlsInspection:
    context = ssl.create_default_context()

    try:
        with socket.create_connection((domain, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                certificate = secure_sock.getpeercert()
    except OSError as exc:
        return TlsInspection(
            expires_at=None,
            days_remaining=None,
            error=f"TLS certificate lookup failed: {exc}",
        )

    not_after = certificate.get("notAfter")
    if not not_after:
        return TlsInspection(
            expires_at=None,
            days_remaining=None,
            error="TLS certificate did not include an expiry date.",
        )

    expires_dt = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days_remaining = max((expires_dt - now).days, 0)

    return TlsInspection(
        expires_at=expires_dt.isoformat(),
        days_remaining=days_remaining,
        error=None,
    )
