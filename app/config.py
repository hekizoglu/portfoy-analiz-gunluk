from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


def _parse_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_config_map(base_dir: Path | None = None) -> dict[str, str]:
    root = base_dir or Path(__file__).resolve().parents[1]
    merged: dict[str, str] = {}

    for name in (".env", ".env.local"):
        merged.update(_parse_dotenv(root / name))

    for key, value in os.environ.items():
        merged[key] = value

    return merged


def _parse_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class TelegramConfig:
    enabled: bool
    bot_token: str
    chat_id: str
    progress_thread_id: str
    parse_mode: str

    @classmethod
    def from_env(cls, base_dir: Path | None = None) -> "TelegramConfig":
        data = load_config_map(base_dir)
        return cls(
            enabled=_parse_bool(data.get("TELEGRAM_ENABLED")),
            bot_token=data.get("TELEGRAM_BOT_TOKEN", ""),
            chat_id=data.get("TELEGRAM_CHAT_ID", ""),
            progress_thread_id=data.get("TELEGRAM_PROGRESS_THREAD_ID", ""),
            parse_mode=data.get("TELEGRAM_PARSE_MODE", "Markdown"),
        )

    def validate_for_send(self) -> None:
        if not self.enabled:
            raise ValueError("Telegram sending is disabled. Set TELEGRAM_ENABLED=true.")
        if not self.bot_token:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN.")
        if not self.chat_id:
            raise ValueError("Missing TELEGRAM_CHAT_ID.")
