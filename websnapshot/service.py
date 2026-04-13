from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlparse

from websnapshot.checks.dns_checks import lookup_txt_hygiene
from websnapshot.checks.http_checks import SECURITY_HEADERS, fetch_homepage, fetch_optional_text
from websnapshot.checks.tls_checks import inspect_certificate_expiry
from websnapshot.models import HeaderCheck, SnapshotReport
from websnapshot.scoring import apply_scoring


def generate_snapshot(domain: str) -> SnapshotReport:
    normalized_domain = normalize_domain(domain)

    homepage = fetch_homepage(normalized_domain)
    tls = inspect_certificate_expiry(normalized_domain)
    security_txt_present, security_txt_url = fetch_optional_text(
        normalized_domain, "/.well-known/security.txt"
    )
    robots_txt_present, robots_txt_url = fetch_optional_text(normalized_domain, "/robots.txt")
    dns = lookup_txt_hygiene(normalized_domain)

    header_checks = [
        HeaderCheck(
            name=header_name,
            present=header_name in homepage.headers,
            value=homepage.headers.get(header_name),
        )
        for header_name in SECURITY_HEADERS
    ]

    report = SnapshotReport(
        domain=normalized_domain,
        generated_at=datetime.now(timezone.utc).isoformat(),
        homepage_url=homepage.url,
        https_ok=homepage.ok,
        http_status=homepage.status_code,
        tls_expires_at=tls.expires_at,
        tls_days_remaining=tls.days_remaining,
        security_txt_present=security_txt_present,
        security_txt_url=security_txt_url,
        robots_txt_present=robots_txt_present,
        robots_txt_url=robots_txt_url,
        spf_present=bool(dns.spf_records),
        spf_records=dns.spf_records,
        dmarc_present=bool(dns.dmarc_records),
        dmarc_records=dns.dmarc_records,
        headers=header_checks,
        errors=[*homepage.errors, *dns.errors, *([tls.error] if tls.error else [])],
    )

    return apply_scoring(report)


def normalize_domain(raw_domain: str) -> str:
    value = raw_domain.strip().lower()
    if "://" in value:
        parsed = urlparse(value)
        value = parsed.netloc or parsed.path
    return value.split("/", 1)[0]
