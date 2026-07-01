from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import re

import pdfplumber

from app.recommendation_normalizer import normalize_recommendation


TICKER_RE = re.compile(r"^[A-Z0-9]{4,5}$")

MISENCODED_MAP = {
    "BankacÃ„Â±lÃ„Â±k": "Bankacilik",
    "SigortacÃ„Â±lÃ„Â±k": "Sigortacilik",
    "AracÃ„Â± Kurum": "Araci Kurum",
    "HavacÃ„Â±lÃ„Â±k": "Havacilik",
    "Yiyecek & Ã„Â°ÃƒÂ§ecek": "Yiyecek & Icecek",
    "SaÃ„Å¸lÃ„Â±k": "Saglik",
    "Gayrimenkul & Ã„Â°nÃ…Å¸aat": "Gayrimenkul & Insaat",
    "TelekomÃƒÂ¼nikasyon": "Telekomunikasyon",
}


@dataclass(slots=True)
class OyakValuationRow:
    ticker: str
    sector: str
    broker: str
    report_date: str
    recommendation_raw: str
    recommendation_normalized: str
    current_price_reported: float
    target_price: float
    upside_reported: float
    source_url: str
    source_file_hash_sha256: str
    confidence_score: float
    validation_status: str
    company_name: str = ""
    currency: str = "TRY"

    def to_dict(self) -> dict:
        payload = asdict(self)
        if not payload["company_name"]:
            payload["company_name"] = self.ticker
        return payload


def _extract_report_date(text: str) -> str:
    match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    if not match:
        raise ValueError("Could not detect report date in OYAK PDF.")
    return datetime.strptime(match.group(1), "%d/%m/%Y").strftime("%Y-%m-%d")


def _clean_sector(raw: str) -> str:
    sector = raw.split(" KapanÄ±ÅŸ Hedef Fiyat", 1)[0].replace("*", "").strip()
    return MISENCODED_MAP.get(sector, sector)


def _parse_price_pair(raw: str) -> tuple[float, float]:
    parts = raw.split()
    if len(parts) < 2:
        raise ValueError(f"Could not parse current/target price pair from: {raw}")
    return float(parts[0].replace(",", "")), float(parts[1].replace(",", ""))


def _parse_pct(raw: str) -> float:
    return float(raw.replace("%", "").replace(",", "."))


def parse_oyak_pdf(pdf_path: Path, source_url: str) -> list[dict]:
    file_hash = sha256(pdf_path.read_bytes()).hexdigest()
    rows: list[dict] = []
    current_sector = ""

    with pdfplumber.open(pdf_path) as pdf:
        table = pdf.pages[0].extract_table() or []
        report_date = _extract_report_date(pdf.pages[0].extract_text() or "")

    for row in table:
        first = (row[0] or "").strip()
        second = (row[1] or "").strip() if len(row) > 1 and row[1] else ""
        third = (row[2] or "").strip() if len(row) > 2 and row[2] else ""
        fifth = (row[4] or "").strip() if len(row) > 4 and row[4] else ""

        if not first:
            continue
        if "KapanÄ±ÅŸ Hedef Fiyat" in first and not TICKER_RE.match(first.split()[0]):
            current_sector = _clean_sector(first)
            continue
        if not TICKER_RE.match(first):
            continue

        recommendation_normalized = normalize_recommendation("OYAK Yatirim", second)
        if recommendation_normalized is None or not third or not fifth:
            continue

        current_price, target_price = _parse_price_pair(third)
        upside = _parse_pct(fifth)
        entry = OyakValuationRow(
            ticker=first,
            sector=current_sector,
            broker="OYAK Yatirim",
            report_date=report_date,
            recommendation_raw=second,
            recommendation_normalized=recommendation_normalized,
            current_price_reported=current_price,
            target_price=target_price,
            upside_reported=upside,
            source_url=source_url,
            source_file_hash_sha256=file_hash,
            confidence_score=0.95,
            validation_status="VALID",
        )
        rows.append(entry.to_dict())

    if not rows:
        raise ValueError("No OYAK valuation rows parsed from PDF.")
    return rows
