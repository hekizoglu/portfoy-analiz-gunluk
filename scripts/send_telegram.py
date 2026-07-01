from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import TelegramConfig
from app.telegram_client import TelegramClient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="artifacts/daily_report_draft.md",
        help="Path to markdown text that will be sent to Telegram.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the message instead of sending it.",
    )
    parser.add_argument(
        "--document",
        default="",
        help="Optional path to the report document that will be attached to Telegram.",
    )
    parser.add_argument(
        "--approval-queue",
        default="artifacts/approval_queue/latest.json",
        help="Path to the latest approval queue JSON file.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    text = input_path.read_text(encoding="utf-8")

    if args.dry_run:
        print("DRY_RUN_MESSAGE_BEGIN")
        print(text)
        print("DRY_RUN_MESSAGE_END")
        return 0

    approval_path = Path(args.approval_queue)
    if not approval_path.exists():
        raise FileNotFoundError(f"Approval queue not found: {approval_path}")

    approval_payload = json.loads(approval_path.read_text(encoding="utf-8"))
    if approval_payload.get("approval_status") not in {"APPROVED", "PENDING"}:
        raise ValueError(
            f"Telegram send blocked because approval_status={approval_payload.get('approval_status')}"
        )

    config = TelegramConfig.from_env()
    if config.is_queue_only():
        raise ValueError("Telegram delivery mode is queue-only. Set TELEGRAM_DELIVERY_MODE=PRIVATE_TEST or APPROVED_SEND.")

    client = TelegramClient(config)
    document_path = Path(args.document) if args.document else input_path

    if document_path.exists():
        doc_result = client.send_document(document_path, caption="Gunluk rapor eki.")
        print(f"SENT_DOCUMENT_MESSAGE_ID={doc_result['result_message_id']}")
        print(f"SENT_DOCUMENT_PATH={document_path}")

    result = client.send_markdown(text)
    print(f"SENT_MESSAGE_ID={result['result_message_id']}")
    print(f"CHAT_ID={result['chat_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
