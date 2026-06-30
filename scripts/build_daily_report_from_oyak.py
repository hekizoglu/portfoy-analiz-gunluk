from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _score(row: dict) -> float:
    upside = max(min(float(row["upside_reported"]), 100.0), -100.0)
    rec_bonus = {"BUY": 20, "HOLD": 8, "SELL": -15, "NEUTRAL": 0}.get(
        row["recommendation_normalized"], 0
    )
    liquidity_bonus = 5 if row["ticker"] in {"THYAO", "BIMAS", "TCELL", "AKBNK", "GARAN"} else 0
    return round(max(min(50 + upside * 0.45 + rec_bonus + liquidity_bonus, 100), 0), 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="artifacts/oyak_parsed_rows.json")
    parser.add_argument("--output", default="docs/examples/sample_daily_report.json")
    args = parser.parse_args()

    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    sorted_rows = sorted(rows, key=lambda row: _score(row), reverse=True)
    top_rows = sorted_rows[:5]
    top_candidates = []
    anomalies = []
    manual_reviews = []

    for row in top_rows:
        score = _score(row)
        risk_label = "MANUAL_CONTROL" if row["upside_reported"] >= 50 else "OK"
        top_candidates.append(
            {
                "ticker": row["ticker"],
                "broker_count": 1,
                "average_target_price": row["target_price"],
                "consensus_note": "Kurum raporlarina gore one cikan",
                "final_score": score,
                "risk_label": risk_label,
                "report_date": row["report_date"],
            }
        )
        if abs(row["upside_reported"]) >= 50:
            direction = "pozitif" if row["upside_reported"] > 0 else "negatif"
            anomalies.append(
                {
                    "message": (
                        f"{row['ticker']} icin tek kurumdan gelen %{abs(int(row['upside_reported']))} "
                        f"{direction} ayrisma, manuel kontrol gerekir."
                    )
                }
            )
        if row["recommendation_normalized"] == "HOLD":
            manual_reviews.append(
                {
                    "ticker": row["ticker"],
                    "reason": "Endekse paralel tavsiye, publish dilini yumusat",
                    "risk_label": "SINGLE_BROKER",
                }
            )

    report = {
        "report_date": rows[0]["report_date"] if rows else "TODO",
        "source_count": 1,
        "valid_row_count": len(rows),
        "manual_review_count": len(manual_reviews),
        "top_candidates": top_candidates,
        "anomalies": anomalies,
        "revisions": [],
        "manual_reviews": manual_reviews,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"REPORT_OUTPUT={output_path}")
    print(f"TOP_CANDIDATES={len(top_candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
