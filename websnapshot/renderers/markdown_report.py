from __future__ import annotations

from websnapshot.models import SnapshotReport

HEADER_VALUE_LIMIT = 120


def render_markdown(report: SnapshotReport) -> str:
    lines: list[str] = [
        "# Web Security Snapshot",
        "",
        f"- Domain: `{report.domain}`",
        f"- Generated: `{report.generated_at}`",
        f"- Risk score: `{report.risk_score}/100`",
        f"- Rating: `{report.rating}`",
        "",
        "## Summary",
        "",
        f"- HTTPS homepage: {'OK' if report.https_ok else 'Failed'}"
        + (f" ({report.http_status})" if report.http_status is not None else ""),
        "- TLS certificate: "
        + (
            f"expires `{report.tls_expires_at}` ({report.tls_days_remaining} days remaining)"
            if report.tls_expires_at
            else "unable to determine"
        ),
        f"- security.txt: {'Present' if report.security_txt_present else 'Missing'}",
        f"- robots.txt: {'Present' if report.robots_txt_present else 'Missing'}",
        f"- SPF: {'Present' if report.spf_present else 'Missing'}",
        f"- DMARC: {'Present' if report.dmarc_present else 'Missing'}",
        "",
        "## Security Headers",
        "",
    ]

    for header in report.headers:
        lines.append(
            f"- {header.name}: {'Present' if header.present else 'Missing'}"
            + (f" (`{_truncate_header_value(header.value)}`)" if header.value else "")
        )

    lines.extend(["", "## Findings", ""])

    if report.findings:
        for finding in report.findings:
            lines.append(f"- {finding.severity}: {finding.title}. {finding.detail}")
    else:
        lines.append("- No significant findings.")

    if report.spf_records or report.dmarc_records:
        lines.extend(["", "## DNS Records", ""])
        if report.spf_records:
            for record in report.spf_records:
                lines.append(f"- SPF: `{record}`")
        if report.dmarc_records:
            for record in report.dmarc_records:
                lines.append(f"- DMARC: `{record}`")

    if report.errors:
        lines.extend(["", "## Errors", ""])
        for error in report.errors:
            lines.append(f"- {error}")

    return "\n".join(lines) + "\n"


def _truncate_header_value(value: str) -> str:
    if len(value) <= HEADER_VALUE_LIMIT:
        return value
    return value[: HEADER_VALUE_LIMIT - 3] + "..."
