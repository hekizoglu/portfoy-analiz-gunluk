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
        "source_snapshot": [
            {
                "name": "OYAK Yatirim",
                "where": "https://www.oyakyatirim.com.tr/arastirma-raporlari",
                "check": "Latest valuation table PDF",
                "cadence": "per release",
            },
            {
                "name": "KAP",
                "where": "https://kap.org.tr/en",
                "check": "Material events, financial statements, corporate actions",
                "cadence": "intraday",
            },
            {
                "name": "Borsa Istanbul",
                "where": "https://www.borsaistanbul.com/en/markets/equity-market",
                "check": "Equity market, sector flow and daily bulletin",
                "cadence": "intraday",
            },
            {
                "name": "TCMB",
                "where": "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB%2BEN/Main%2BMenu/Statistics",
                "check": "Data release calendar, rates, exchange rates and markets data",
                "cadence": "daily",
            },
            {
                "name": "TUIK",
                "where": "https://veriportali.tuik.gov.tr/en",
                "check": "Inflation, industrial production and confidence releases",
                "cadence": "calendar-driven",
            },
        ],
        "market_context": [
            {
                "theme": "Consensus expectations",
                "why": "Prices embed expectations, so the report should show whether the narrative is optimistic or pessimistic.",
                "where": "Research tabs, broker revisions and market prices",
            },
            {
                "theme": "Macro rates and FX",
                "why": "Valuation multiples and risk appetite are sensitive to policy rate and TRY moves.",
                "where": "TCMB statistics and exchange-rate pages",
            },
            {
                "theme": "Sector rotation and liquidity",
                "why": "Top names move differently from thin names; liquidity and float should affect ranking.",
                "where": "Borsa Istanbul equity market and indices pages",
            },
            {
                "theme": "Corporate events",
                "why": "KAP disclosures can invalidate a target-price assumption very quickly.",
                "where": "KAP material event disclosures",
            },
        ],
        "next_actions": [
            "Implement consensus engine output so the report can compare current price, average target and median target.",
            "Add broker count filter so single-broker names are visually separated from consensus names.",
            "Keep manual approval on until KAP, macro and consensus checks are wired into the pipeline.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"REPORT_OUTPUT={output_path}")
    print(f"TOP_CANDIDATES={len(top_candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
