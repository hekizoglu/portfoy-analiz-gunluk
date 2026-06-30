from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from zoneinfo import ZoneInfo


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


@dataclass(slots=True)
class AiTaskRunnerConfig:
    provider: str
    api_key: str
    base_url: str
    model: str
    deepseek_offpeak_only: bool
    deepseek_timezone: str

    @classmethod
    def from_env(cls, base_dir: Path | None = None) -> "AiTaskRunnerConfig":
        data = load_config_map(base_dir)
        return cls(
            provider=data.get("AI_TASK_RUNNER_PROVIDER", "").strip().lower(),
            api_key=data.get("AI_TASK_RUNNER_API_KEY", ""),
            base_url=data.get("AI_TASK_RUNNER_BASE_URL", ""),
            model=data.get("AI_TASK_RUNNER_MODEL", ""),
            deepseek_offpeak_only=_parse_bool(data.get("DEEPSEEK_OFFPEAK_ONLY"), default=True),
            deepseek_timezone=data.get("DEEPSEEK_TIMEZONE", "Europe/Istanbul"),
        )

    def is_configured(self) -> bool:
        return bool(self.provider and self.api_key and self.base_url and self.model)

    def current_local_hour(self) -> int:
        tz = ZoneInfo(self.deepseek_timezone)
        return datetime.now(tz).hour

    def is_deepseek_peak_window(self) -> bool:
        if self.provider != "deepseek":
            return False
        hour = self.current_local_hour()
        return (4 <= hour < 7) or (9 <= hour < 13)

    def should_run_now(self) -> bool:
        if self.provider != "deepseek":
            return True
        if not self.deepseek_offpeak_only:
            return True
        return not self.is_deepseek_peak_window()
