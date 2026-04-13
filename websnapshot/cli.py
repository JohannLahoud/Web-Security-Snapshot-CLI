from __future__ import annotations

import argparse
import re
from pathlib import Path

from websnapshot.renderers.json_report import render_json
from websnapshot.renderers.markdown_report import render_markdown
from websnapshot.renderers.terminal_report import render_terminal
from websnapshot.service import generate_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="websnapshot",
        description="Generate a simple public web security posture report for a domain.",
    )
    parser.add_argument("domain", help="Target domain, for example: example.com")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    report = generate_snapshot(args.domain)
    report_stem = _report_stem(report.domain)
    markdown_path = Path(f"{report_stem}-report.md")
    json_path = Path(f"{report_stem}-report.json")

    terminal_output = render_terminal(
        report,
        markdown_report_name=markdown_path.name,
        json_report_name=json_path.name,
    )
    markdown_output = render_markdown(report)
    json_output = render_json(report)

    markdown_path.write_text(markdown_output, encoding="utf-8")
    json_path.write_text(json_output + "\n", encoding="utf-8")

    print(terminal_output)
    return 0


def _report_stem(domain: str) -> str:
    return re.sub(r"[^a-z0-9.-]+", "-", domain.lower()).strip("-.") or "report"
