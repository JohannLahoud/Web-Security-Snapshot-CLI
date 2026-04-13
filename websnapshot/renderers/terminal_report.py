from __future__ import annotations

from websnapshot.models import SnapshotReport


def render_terminal(report: SnapshotReport) -> str:
    lines = [
        "Web Security Snapshot",
        f"Target: {report.domain}",
        f"Generated: {report.generated_at}",
        "",
        f"Risk score: {report.risk_score}/100",
        f"Rating: {report.rating}",
        "",
        "Checks",
        f"- HTTPS homepage: {_render_https(report)}",
        f"- TLS certificate: {_render_tls(report)}",
        f"- security.txt: {'Present' if report.security_txt_present else 'Missing'}",
        f"- robots.txt: {'Present' if report.robots_txt_present else 'Missing'}",
        f"- SPF: {'Present' if report.spf_present else 'Missing'}",
        f"- DMARC: {'Present' if report.dmarc_present else 'Missing'}",
        "",
        "Security headers",
    ]

    for header in report.headers:
        lines.append(f"- {header.name}: {'Present' if header.present else 'Missing'}")

    lines.extend(["", "Findings"])

    if report.findings:
        for index, finding in enumerate(report.findings, start=1):
            lines.append(f"{index}. {finding.severity}: {finding.title}.")
    else:
        lines.append("1. No significant findings.")

    if report.errors:
        lines.extend(["", "Errors"])
        for error in report.errors:
            lines.append(f"- {error}")

    lines.extend(["", "Reports written:", "- report.md", "- report.json"])
    return "\n".join(lines)


def _render_https(report: SnapshotReport) -> str:
    if report.https_ok:
        return f"OK ({report.http_status})"
    return "Failed"


def _render_tls(report: SnapshotReport) -> str:
    if report.tls_expires_at and report.tls_days_remaining is not None:
        return f"OK (expires {report.tls_expires_at}, {report.tls_days_remaining} days left)"
    return "Unable to determine"
