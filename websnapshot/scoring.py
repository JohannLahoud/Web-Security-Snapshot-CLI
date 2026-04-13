from __future__ import annotations

from websnapshot.models import Finding, SnapshotReport


def apply_scoring(report: SnapshotReport) -> SnapshotReport:
    findings: list[Finding] = []
    risk_score = 0

    if not report.https_ok:
        risk_score += 35
        findings.append(
            Finding(
                severity="High",
                title="HTTPS homepage unavailable",
                detail="The homepage could not be fetched successfully over HTTPS.",
            )
        )

    if report.tls_days_remaining is None:
        risk_score += 20
        findings.append(
            Finding(
                severity="High",
                title="TLS certificate could not be evaluated",
                detail="The remote certificate expiry date could not be determined.",
            )
        )
    elif report.tls_days_remaining <= 14:
        risk_score += 25
        findings.append(
            Finding(
                severity="High",
                title="TLS certificate is close to expiry",
                detail=f"The certificate expires in {report.tls_days_remaining} day(s).",
            )
        )
    elif report.tls_days_remaining <= 30:
        risk_score += 10
        findings.append(
            Finding(
                severity="Medium",
                title="TLS certificate expiry should be monitored",
                detail=f"The certificate expires in {report.tls_days_remaining} day(s).",
            )
        )

    header_weights = {
        "Strict-Transport-Security": ("High", 20),
        "Content-Security-Policy": ("Medium", 15),
        "X-Frame-Options": ("Medium", 10),
        "X-Content-Type-Options": ("Medium", 10),
        "Referrer-Policy": ("Low", 5),
        "Permissions-Policy": ("Low", 5),
    }

    for header in report.headers:
        if header.present:
            continue
        severity, penalty = header_weights[header.name]
        risk_score += penalty
        findings.append(
            Finding(
                severity=severity,
                title=f"{header.name} header is missing",
                detail=f"The HTTPS response did not include {header.name}.",
            )
        )

    if not report.security_txt_present:
        risk_score += 5
        findings.append(
            Finding(
                severity="Low",
                title="security.txt file was not found",
                detail="No public security.txt file was detected under /.well-known/security.txt.",
            )
        )

    if not report.robots_txt_present:
        risk_score += 2
        findings.append(
            Finding(
                severity="Info",
                title="robots.txt file was not found",
                detail="No robots.txt file was detected.",
            )
        )

    if not report.spf_present:
        risk_score += 10
        findings.append(
            Finding(
                severity="Medium",
                title="SPF record was not found",
                detail="No SPF TXT record was detected for the domain.",
            )
        )

    if not report.dmarc_present:
        risk_score += 10
        findings.append(
            Finding(
                severity="Medium",
                title="DMARC record was not found",
                detail="No DMARC TXT record was detected for the domain.",
            )
        )

    report.findings = findings
    report.risk_score = max(min(risk_score, 100), 0)
    report.rating = _rating_for_score(report.risk_score)
    return report


def _rating_for_score(score: int) -> str:
    if score <= 15:
        return "Low"
    if score <= 35:
        return "Moderate"
    if score <= 60:
        return "Elevated"
    return "High"
