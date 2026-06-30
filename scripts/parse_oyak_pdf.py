from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.oyak_parser import parse_oyak_pdf


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to OYAK valuation PDF.")
    parser.add_argument(
        "--source-url",
        default="https://www.oyakyatirim.com.tr/arastirma-raporlari",
        help="Official source URL for traceability.",
    )
    parser.add_argument(
        "--output",
        default="artifacts/oyak_parsed_rows.json",
        help="Output JSON file path.",
    )
    args = parser.parse_args()

    rows = parse_oyak_pdf(Path(args.input), args.source_url)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PARSED_ROWS={len(rows)}")
    print(f"OUTPUT={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
