from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class HeaderCheck:
    name: str
    present: bool
    value: str | None


@dataclass(slots=True)
class Finding:
    severity: str
    title: str
    detail: str


@dataclass(slots=True)
class SnapshotReport:
    domain: str
    generated_at: str
    homepage_url: str
    https_ok: bool
    http_status: int | None
    tls_expires_at: str | None
    tls_days_remaining: int | None
    security_txt_present: bool
    security_txt_url: str
    robots_txt_present: bool
    robots_txt_url: str
    spf_present: bool
    spf_records: list[str] = field(default_factory=list)
    dmarc_present: bool = False
    dmarc_records: list[str] = field(default_factory=list)
    headers: list[HeaderCheck] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    risk_score: int = 0
    rating: str = "Unknown"
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
