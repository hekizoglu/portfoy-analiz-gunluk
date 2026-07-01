from __future__ import annotations

import re
import unicodedata


CANONICAL_RECOMMENDATIONS = {
    "BUY",
    "HOLD",
    "SELL",
    "NEUTRAL",
    "OUTPERFORM",
    "UNDERPERFORM",
}

SOURCE_FAMILY_ALIASES = {
    "OYAK YATIRIM": "oyak",
    "OYAK YATIRIM VALUATION TABLE": "oyak",
    "IS YATIRIM": "is",
    "IS YATIRIM TAKIP LISTESI": "is",
    "AK YATIRIM": "ak",
    "AK YATIRIM MODEL PORTFOY": "ak",
}

COMMON_VARIANTS = {
    "BUY": "BUY",
    "AL": "BUY",
    "EU": "BUY",
    "HOLD": "HOLD",
    "TUT": "HOLD",
    "EP": "HOLD",
    "SELL": "SELL",
    "SAT": "SELL",
    "EA": "SELL",
    "NEUTRAL": "NEUTRAL",
    "NÖTR": "NEUTRAL",
    "NOTR": "NEUTRAL",
    "GG": "NEUTRAL",
    "OUTPERFORM": "OUTPERFORM",
    "UNDERPERFORM": "UNDERPERFORM",
}

SOURCE_SPECIFIC_VARIANTS = {
    "oyak": {
        "EU": "BUY",
        "E U": "BUY",
        "E Ãœ": "BUY",
        "EÃœ": "BUY",
        "EÃƒÅ“": "BUY",
        "EP": "HOLD",
        "EA": "SELL",
        "GG": "NEUTRAL",
    },
    "is": {
        "END.USTU": "OUTPERFORM",
        "END USTU": "OUTPERFORM",
        "ENDUSTU": "OUTPERFORM",
        "END.PAR": "NEUTRAL",
        "END PAR": "NEUTRAL",
        "ENDPAR": "NEUTRAL",
        "END.ALTI": "UNDERPERFORM",
        "END ALTI": "UNDERPERFORM",
        "ENDALTI": "UNDERPERFORM",
    },
    "ak": {
        "ENDEKS UZERI": "OUTPERFORM",
        "ENDEKS USTU": "OUTPERFORM",
        "ENDEKSE PARALEL": "NEUTRAL",
        "ENDEKS ALTI": "UNDERPERFORM",
    },
}


def _family_key(source_name: str) -> str:
    source = source_name.strip().upper()
    return SOURCE_FAMILY_ALIASES.get(source, "generic")


def _ascii_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    normalized = normalized.upper().strip()
    normalized = normalized.replace("&", " AND ")
    normalized = re.sub(r"[\s_/-]+", " ", normalized)
    normalized = re.sub(r"[^A-Z0-9. ]+", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def normalize_recommendation(source_name: str, recommendation_raw: str) -> str | None:
    raw = recommendation_raw.strip()
    if not raw:
        return None

    source_variants = SOURCE_SPECIFIC_VARIANTS.get(_family_key(source_name), {})
    if raw in source_variants:
        return source_variants[raw]

    ascii_raw = _ascii_key(raw)
    if ascii_raw in source_variants:
        return source_variants[ascii_raw]
    if ascii_raw in COMMON_VARIANTS:
        return COMMON_VARIANTS[ascii_raw]

    compact_ascii = ascii_raw.replace(" ", "")
    if compact_ascii in source_variants:
        return source_variants[compact_ascii]
    if compact_ascii in COMMON_VARIANTS:
        return COMMON_VARIANTS[compact_ascii]

    if raw.upper() in CANONICAL_RECOMMENDATIONS:
        return raw.upper()

    return None
