from __future__ import annotations

import json
from urllib import parse, request

from app.config import TelegramConfig


class TelegramClient:
    def __init__(self, config: TelegramConfig) -> None:
        self.config = config

    def send_markdown(self, text: str) -> dict:
        self.config.validate_for_send()
        url = f"https://api.telegram.org/bot{self.config.bot_token}/sendMessage"
        payload = {
            "chat_id": self.config.chat_id,
            "text": text,
            "parse_mode": self.config.parse_mode,
            "disable_web_page_preview": True,
        }
        if self.config.progress_thread_id:
            payload["message_thread_id"] = self.config.progress_thread_id

        body = parse.urlencode(payload).encode("utf-8")
        req = request.Request(url, data=body, method="POST")
        with request.urlopen(req, timeout=20) as response:
            raw = response.read().decode("utf-8")
        data = json.loads(raw)
        if not data.get("ok"):
            raise RuntimeError("Telegram API returned non-ok response.")
        return {
            "ok": True,
            "result_message_id": data.get("result", {}).get("message_id"),
            "chat_id": self.config.chat_id,
        }
