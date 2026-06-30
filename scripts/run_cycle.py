from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import TelegramConfig
from app.roadmap import find_next_todo_task
from app.telegram_client import TelegramClient


def _run(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def build_cycle_report(next_task_id: str, pipeline_status: str, draft_status: str, git_status: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines = [
        f"Cycle Report | {ts}",
        "",
        f"Next task: {next_task_id}",
        f"Data pipeline: {pipeline_status}",
        f"Draft status: {draft_status}",
        f"Git status: {git_status}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default="")
    parser.add_argument("--source-url", default="https://www.oyakyatirim.com.tr/arastirma-raporlari")
    parser.add_argument("--send-telegram", action="store_true")
    parser.add_argument("--commit-push", action="store_true")
    args = parser.parse_args()

    next_task = find_next_todo_task(ROOT / "ROADMAP.md")
    next_task_id = next_task.task_id if next_task else "NO_TODO"

    pipeline_status = "SKIPPED_NO_PDF"
    draft_status = "SKIPPED"

    if args.pdf:
        code, stdout, stderr = _run(
            "scripts/parse_oyak_pdf.py",
            "--input",
            args.pdf,
            "--source-url",
            args.source_url,
        )
        if code != 0:
            pipeline_status = f"PARSE_FAILED: {stderr or stdout}"
        else:
            code, stdout, stderr = _run(
                "scripts/build_daily_report_from_oyak.py",
                "--input",
                "artifacts/oyak_parsed_rows.json",
                "--output",
                "artifacts/daily_report_data.json",
            )
            if code != 0:
                pipeline_status = f"REPORT_FAILED: {stderr or stdout}"
            else:
                code, stdout, stderr = _run(
                    "scripts/build_telegram_draft.py",
                    "--input",
                    "artifacts/daily_report_data.json",
                    "--output",
                    "artifacts/daily_report_draft.md",
                )
                pipeline_status = "OK" if code == 0 else f"DRAFT_FAILED: {stderr or stdout}"
                draft_status = "READY" if code == 0 else "FAILED"

    report = build_cycle_report(
        next_task_id=next_task_id,
        pipeline_status=pipeline_status,
        draft_status=draft_status,
        git_status="PENDING",
    )
    cycle_dir = ROOT / "artifacts" / "cycle_reports"
    cycle_dir.mkdir(parents=True, exist_ok=True)
    cycle_path = cycle_dir / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    cycle_path.write_text(report, encoding="utf-8")

    telegram_status = "SKIPPED"
    if args.send_telegram:
        cfg = TelegramConfig.from_env(ROOT)
        if cfg.enabled and cfg.bot_token and cfg.chat_id:
            TelegramClient(cfg).send_markdown(report)
            telegram_status = "SENT"
        else:
            telegram_status = "SKIPPED_MISSING_CONFIG"

    git_status = "SKIPPED"
    if args.commit_push:
        proc = subprocess.run(
            [sys.executable, "scripts/commit_and_push.py", "--message", f"chore: cycle report {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        git_status = (proc.stdout.strip() or proc.stderr.strip() or f"RC={proc.returncode}")

    final_report = build_cycle_report(
        next_task_id=next_task_id,
        pipeline_status=f"{pipeline_status}; telegram={telegram_status}",
        draft_status=draft_status,
        git_status=git_status,
    )
    cycle_path.write_text(final_report, encoding="utf-8")
    print(json.dumps({"cycle_report": str(cycle_path), "next_task_id": next_task_id, "telegram_status": telegram_status, "git_status": git_status}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
