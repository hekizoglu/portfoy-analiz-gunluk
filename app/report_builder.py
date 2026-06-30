from __future__ import annotations

from dataclasses import dataclass
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

    @classmethod
    def from_json(cls, path: Path) -> "DailyReport":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(**payload)

    def to_markdown(self) -> str:
        lines = [
            f"Gunluk Degerleme Radari | {self.report_date} | Taslak",
            "",
            (
                f"Kapsam: {self.source_count} kurum raporu, {self.valid_row_count} gecerli satir, "
                f"{self.manual_review_count} manuel kontrol kaydi."
            ),
            "",
            "One cikan izleme adaylari",
        ]

        if self.top_candidates:
            for item in self.top_candidates:
                lines.append(
                    "- {ticker} | {broker_count} kurum | Ortalama hedef: {average_target_price} TL | "
                    "{consensus_note} | FinalScore: {final_score} | Risk: {risk_label} | Kaynak: {report_date}".format(
                        **item
                    )
                )
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

        lines.extend(["", DISCLAIMER])
        return "\n".join(lines)
