# web-security-snapshot

`web-security-snapshot` is a lightweight Python CLI that generates a simple public web security posture report for a domain.

It performs non-intrusive defensive hygiene checks only:

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

## Features

- Lightweight dependency set
- Simple clean architecture
- No brute force, port scanning, or offensive checks
- Easy to package later with PyInstaller

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

Risk score: 42/100
Rating: Elevated

Checks
- HTTPS homepage: OK (200)
- TLS certificate: OK (expires 2026-07-01T23:59:59+00:00, 79 days left)
- security.txt: Missing
- robots.txt: Present
- SPF: Present
- DMARC: Missing

Security headers
- Strict-Transport-Security: Missing
- Content-Security-Policy: Missing
- X-Frame-Options: Present
- X-Content-Type-Options: Present
- Referrer-Policy: Missing
- Permissions-Policy: Missing

Findings
1. High: Strict-Transport-Security header is missing. The HTTPS response did not include Strict-Transport-Security.
2. Medium: Content-Security-Policy header is missing. The HTTPS response did not include Content-Security-Policy.
3. Medium: DMARC record was not found. No DMARC TXT record was detected for the domain.
4. Low: security.txt file was not found. No public security.txt file was detected under /.well-known/security.txt.

Reports written:
- github.com-report.md
- github.com-report.json
```

## Output Files

`<domain>-report.json` contains structured results for automation and archival.

`<domain>-report.md` contains a human-readable professional summary.

## Project Structure

```text
websnapshot/
  __init__.py
  __main__.py
  cli.py
  models.py
  scoring.py
  service.py
  checks/
    __init__.py
    dns_checks.py
    http_checks.py
    tls_checks.py
  renderers/
    __init__.py
    json_report.py
    markdown_report.py
    terminal_report.py
```

## PyInstaller

This project is structured to work cleanly with one-file packaging:

```bash
pyinstaller --clean --onefile --name websnapshot websnapshot.spec
```

Built executable output will be placed under `dist/`.

## Notes

- The risk score is `0-100`, where higher values indicate higher observed public-facing risk.
- The tool only checks public-facing defensive hygiene indicators.
- It does not attempt exploitation, enumeration beyond the requested records, or any network scanning behavior.
- Some domains may fail local TLS verification depending on the machine trust store, proxying, or interception in the current environment; certificate verification remains enabled intentionally.
- Some sites may intentionally omit certain headers depending on architecture or CDN behavior; results should be interpreted as a practical posture snapshot, not a formal audit.
