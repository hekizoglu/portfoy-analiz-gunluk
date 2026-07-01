from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import json
from pathlib import Path


DISCLAIMER = (
    "Bu icerik yatirim tavsiyesi degildir. Otomatik veri analizi ve genel piyasa "
    "taramasidir. Nihai karar kullaniciya aittir."
)


@dataclass(slots=True)
class DailyReport:
    report_date: str
    source_count: int
    valid_row_count: int
    manual_review_count: int
    top_candidates: list[dict]
    anomalies: list[dict]
    revisions: list[dict]
    manual_reviews: list[dict]
    source_snapshot: list[dict] = field(default_factory=list)
    market_context: list[dict] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, path: Path) -> "DailyReport":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            report_date=str(payload.get("report_date", "TODO")),
            source_count=int(payload.get("source_count", 0)),
            valid_row_count=int(payload.get("valid_row_count", 0)),
            manual_review_count=int(payload.get("manual_review_count", 0)),
            top_candidates=_ensure_list(payload.get("top_candidates")),
            anomalies=_ensure_list(payload.get("anomalies")),
            revisions=_ensure_list(payload.get("revisions")),
            manual_reviews=_ensure_list(payload.get("manual_reviews")),
            source_snapshot=_ensure_list(payload.get("source_snapshot")),
            market_context=_ensure_list(payload.get("market_context")),
            next_actions=_ensure_str_list(payload.get("next_actions")),
        )

    def _format_candidate(self, item: dict[str, Any]) -> str:
        parts = [str(item.get("ticker", "?"))]

        if item.get("broker_count") is not None:
            parts.append(f"{item['broker_count']} kurum")
        if item.get("current_price") is not None:
            parts.append(f"Guncel fiyat: {item['current_price']} TL")
        if item.get("average_target_price") is not None:
            parts.append(f"Ort. hedef: {item['average_target_price']} TL")
        if item.get("upside_pct") is not None:
            parts.append(f"Upside: %{item['upside_pct']}")
        if item.get("consensus_note"):
            parts.append(str(item["consensus_note"]))
        if item.get("catalyst"):
            parts.append(f"Katalizor: {item['catalyst']}")
        if item.get("final_score") is not None:
            parts.append(f"Skor: {item['final_score']}")
        if item.get("risk_label"):
            parts.append(f"Risk: {item['risk_label']}")
        if item.get("report_date"):
            parts.append(f"Kaynak tarihi: {item['report_date']}")

        return " | ".join(parts)

    def to_markdown(self) -> str:
        lines = [
            f"Gunluk Degerleme Radari | {self.report_date} | Taslak",
            "",
            (
                f"Kapsam: {self.source_count} kurum raporu, {self.valid_row_count} gecerli satir, "
                f"{self.manual_review_count} manuel kontrol kaydi."
            ),
            "",
            "Bugun kontrol edilen kaynaklar",
        ]

        if self.source_snapshot:
            for item in self.source_snapshot:
                lines.append(
                    "- {name} | Nerede: {where} | Ne kontrol edilir: {check} | Siklik: {cadence}".format(
                        name=item.get("name", "?"),
                        where=item.get("where", "?"),
                        check=item.get("check", "?"),
                        cadence=item.get("cadence", "?"),
                    )
                )
        else:
            lines.append("- Kaynak snapshot tanimli degil.")

        lines.extend(["", "Piyasa baglami"])
        if self.market_context:
            for item in self.market_context:
                lines.append(
                    "- {theme} | Neden onemli: {why} | Kontrol yeri: {where}".format(
                        theme=item.get("theme", "?"),
                        why=item.get("why", "?"),
                        where=item.get("where", "?"),
                    )
                )
        else:
            lines.append("- Piyasa baglami icin ek veri yok.")

        lines.extend(["", "One cikan izleme adaylari"])

        if self.top_candidates:
            for item in self.top_candidates:
                lines.append(f"- {self._format_candidate(item)}")
        else:
            lines.append("- Bugun publish esigini gecen aday bulunmadi.")

        lines.extend(["", "Anomali / ayrisma uyarilari"])
        if self.anomalies:
            for item in self.anomalies:
                lines.append(f"- {item['message']}")
        else:
            lines.append("- Bugun kritik anomaly tespit edilmedi.")

        lines.extend(["", "Revizyon momentumu"])
        if self.revisions:
            for item in self.revisions:
                lines.append(f"- {item['message']}")
        else:
            lines.append("- Dikkat gerektiren yeni revizyon serisi yok.")

        lines.extend(["", "Manuel kontrol gerektirenler"])
        if self.manual_reviews:
            for item in self.manual_reviews:
                lines.append(f"- {item['ticker']} | {item['reason']} | {item['risk_label']}")
        else:
            lines.append("- Manuel kontrol kuyrugunda acik kritik kayit yok.")

        lines.extend(["", "Bugun atilacak aksiyonlar"])
        if self.next_actions:
            for item in self.next_actions:
                lines.append(f"- {item}")
        else:
            lines.append("- Ek aksiyon tanimli degil.")

        lines.extend(["", DISCLAIMER])
        return "\n".join(lines)


def _ensure_list(value: Any) -> list[dict]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _ensure_str_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []
