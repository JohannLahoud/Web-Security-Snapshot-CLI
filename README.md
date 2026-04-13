# web-security-snapshot

`web-security-snapshot` is a small Python CLI for taking a fast, read-only snapshot of a domain's public web security posture.

It focuses on practical defensive hygiene checks:

- HTTPS homepage fetch
- Common security header inspection
- TLS certificate expiry lookup
- `/.well-known/security.txt`
- `/robots.txt`
- DNS TXT lookup for SPF and DMARC
- Simple risk score and findings summary

The CLI writes:

- terminal summary
- `<domain>-report.md`
- `<domain>-report.json`

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e . --no-build-isolation
```

If your environment has restricted network access, `--no-build-isolation` avoids pip creating a temporary build environment that may try to download packaging dependencies again.

## Usage

```bash
python -m websnapshot github.com
```

Or after installing as a script entry point:

```bash
websnapshot github.com
```

## Sample Output

```text
Web Security Snapshot
Target: github.com
Generated: 2026-04-13T10:15:10+00:00

Risk score: 5/100
Rating: Low

Checks
- HTTPS homepage: OK (200)
- TLS certificate: OK (expires 2026-07-01T23:59:59+00:00, 79 days left)
- security.txt: Present
- robots.txt: Present
- SPF: Present
- DMARC: Present

Security headers
- Strict-Transport-Security: Present
- Content-Security-Policy: Present
- X-Frame-Options: Present
- X-Content-Type-Options: Present
- Referrer-Policy: Present
- Permissions-Policy: Missing

Findings
1. Low: Permissions-Policy header is missing. The HTTPS response did not include Permissions-Policy.

Reports written:
- github.com-report.md
- github.com-report.json
```

## Output Files

- `<domain>-report.json` contains structured results for automation and archival.
- `<domain>-report.md` contains a human-readable summary.

## PyInstaller

Use the bundled spec file:

```bash
pyinstaller --clean websnapshot.spec
```

Built executable output will be placed under `dist/`.

## Notes

- The risk score is `0-100`, where higher values indicate higher observed public-facing risk.
- The tool only checks public-facing defensive hygiene indicators and does not perform exploitation or network scanning.
- Some domains may fail local TLS verification depending on the machine trust store, proxying, or interception in the current environment; certificate verification remains enabled intentionally.
- Some sites may intentionally omit certain headers depending on architecture or CDN behavior; results should be interpreted as a practical posture snapshot, not a formal audit.
