from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from app.config import TelegramConfig
from app.telegram_client import TelegramClient


@dataclass(slots=True)
class ErrorAlert:
    error_code: str
    source_name: str
    severity: str
    requires_manual_review: bool
    message: str
    details: str
    timestamp: str

    def to_markdown(self) -> str:
        lines = [
            "Sistem Hata Uyarisi",
            "",
            f"Error code: {self.error_code}",
            f"Source: {self.source_name}",
            f"Severity: {self.severity}",
            f"Manual review: {'Evet' if self.requires_manual_review else 'Hayir'}",
            f"Timestamp: {self.timestamp}",
            "",
            self.message,
        ]
        if self.details:
            lines.extend(["", self.details])
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "source_name": self.source_name,
            "severity": self.severity,
            "requires_manual_review": self.requires_manual_review,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp,
        }


def build_error_alert(
    error_code: str,
    source_name: str,
    severity: str,
    requires_manual_review: bool,
    message: str,
    details: str = "",
) -> ErrorAlert:
    return ErrorAlert(
        error_code=error_code,
        source_name=source_name,
        severity=severity,
        requires_manual_review=requires_manual_review,
        message=message,
        details=details,
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def persist_error_alert(alert: ErrorAlert, root: Path) -> Path:
    out_dir = root / "artifacts" / "error_alerts"
    out_dir.mkdir(parents=True, exist_ok=True)
    latest_path = out_dir / "latest.json"
    latest_path.write_text(json.dumps(alert.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    history_dir = out_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = history_dir / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
    history_path.write_text(json.dumps(alert.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return latest_path


def send_error_alert_if_enabled(alert: ErrorAlert, root: Path) -> str:
    cfg = TelegramConfig.from_env(root)
    if not cfg.enabled or not cfg.bot_token or not cfg.chat_id:
        return "SKIPPED_MISSING_CONFIG"

    try:
        client = TelegramClient(cfg)
        client.send_markdown(alert.to_markdown())
        return "SENT"
    except Exception as exc:
        return f"FAILED_{type(exc).__name__}"
