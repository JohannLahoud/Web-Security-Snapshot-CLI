from __future__ import annotations

import argparse
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

    terminal_output = render_terminal(report)
    markdown_output = render_markdown(report)
    json_output = render_json(report)

    Path("report.md").write_text(markdown_output, encoding="utf-8")
    Path("report.json").write_text(json_output + "\n", encoding="utf-8")

    print(terminal_output)
    return 0
