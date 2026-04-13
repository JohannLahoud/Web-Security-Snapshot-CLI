from __future__ import annotations

import json

from websnapshot.models import SnapshotReport


def render_json(report: SnapshotReport) -> str:
    return json.dumps(report.to_dict(), indent=2)
