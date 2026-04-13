from __future__ import annotations

from dataclasses import dataclass

import dns.exception
import dns.resolver


@dataclass(slots=True)
class DnsTxtInspection:
    spf_records: list[str]
    dmarc_records: list[str]
    errors: list[str]


def lookup_txt_hygiene(domain: str) -> DnsTxtInspection:
    errors: list[str] = []
    spf_records = _lookup_txt_records(domain, "v=spf1", errors, label="SPF")
    dmarc_records = _lookup_txt_records(f"_dmarc.{domain}", "v=DMARC1", errors, label="DMARC")
    return DnsTxtInspection(
        spf_records=spf_records,
        dmarc_records=dmarc_records,
        errors=errors,
    )


def _lookup_txt_records(name: str, prefix: str, errors: list[str], label: str) -> list[str]:
    try:
        answers = dns.resolver.resolve(name, "TXT")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return []
    except dns.exception.DNSException as exc:
        errors.append(f"{label} TXT lookup failed: {exc}")
        return []

    records: list[str] = []
    for answer in answers:
        joined = "".join(part.decode("utf-8", errors="ignore") for part in answer.strings)
        if joined.lower().startswith(prefix.lower()):
            records.append(joined)

    return records
