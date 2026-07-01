from __future__ import annotations

import json
import mimetypes
import uuid
from pathlib import Path
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

    def send_document(self, document_path: str | Path, caption: str = "") -> dict:
        self.config.validate_for_send()
        path = Path(document_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        url = f"https://api.telegram.org/bot{self.config.bot_token}/sendDocument"
        boundary = f"----codextelegram{uuid.uuid4().hex}"
        body = self._build_multipart_body(
            boundary=boundary,
            fields=[
                ("chat_id", self.config.chat_id),
            ],
            file_field_name="document",
            file_path=path,
            caption=caption,
        )
        req = request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        req.add_header("Content-Length", str(len(body)))
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

    def _build_multipart_body(
        self,
        *,
        boundary: str,
        fields: list[tuple[str, str]],
        file_field_name: str,
        file_path: Path,
        caption: str = "",
    ) -> bytes:
        parts: list[bytes] = []

        def add_text_field(name: str, value: str) -> None:
            parts.append(f"--{boundary}".encode("utf-8"))
            parts.append(f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"))
            parts.append(b"")
            parts.append(value.encode("utf-8"))

        for name, value in fields:
            add_text_field(name, value)

        if caption:
            add_text_field("caption", caption)
            if self.config.parse_mode:
                add_text_field("parse_mode", self.config.parse_mode)

        mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        parts.append(f"--{boundary}".encode("utf-8"))
        parts.append(
            f'Content-Disposition: form-data; name="{file_field_name}"; filename="{file_path.name}"'.encode("utf-8")
        )
        parts.append(f"Content-Type: {mime_type}".encode("utf-8"))
        parts.append(b"")
        parts.append(file_path.read_bytes())
        parts.append(f"--{boundary}--".encode("utf-8"))
        parts.append(b"")

        return b"\r\n".join(parts)
