from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.report_builder import DailyReport


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="docs/examples/sample_daily_report.json",
        help="Path to sample or real report JSON input.",
    )
    parser.add_argument(
        "--output",
        default="artifacts/daily_report_draft.md",
        help="Path to markdown draft output.",
    )
    args = parser.parse_args()

    report = DailyReport.from_json(Path(args.input))
    markdown = report.to_markdown()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"DRAFT_WRITTEN={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
