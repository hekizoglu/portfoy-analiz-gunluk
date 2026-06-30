from __future__ import annotations

import argparse
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
    args = parser.parse_args()

    input_path = Path(args.input)
    text = input_path.read_text(encoding="utf-8")

    if args.dry_run:
        print("DRY_RUN_MESSAGE_BEGIN")
        print(text)
        print("DRY_RUN_MESSAGE_END")
        return 0

    config = TelegramConfig.from_env()
    client = TelegramClient(config)
    result = client.send_markdown(text)
    print(f"SENT_MESSAGE_ID={result['result_message_id']}")
    print(f"CHAT_ID={result['chat_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
