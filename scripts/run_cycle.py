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

from app.ai_review import DualAiReviewConfig, evaluate_dual_review
from app.approval_gate import build_queue_payload, write_queue_record
from app.error_alert import build_error_alert, persist_error_alert, send_error_alert_if_enabled
from app.config import AiTaskRunnerConfig, TelegramConfig
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

    try:
        next_task = find_next_todo_task(ROOT / "ROADMAP.md")
        next_task_id = next_task.task_id if next_task else "NO_TODO"
        ai_cfg = AiTaskRunnerConfig.from_env(ROOT)

        pipeline_status = "SKIPPED_NO_PDF"
        draft_status = "SKIPPED"

        pdf_input = args.pdf

        if ai_cfg.provider == "deepseek" and not ai_cfg.should_run_now():
            pipeline_status = "SKIPPED_DEEPSEEK_PEAK_WINDOW"
            draft_status = "SKIPPED_PRICING_WINDOW"
        else:
            if not pdf_input:
                code, stdout, stderr = _run(
                    "scripts/fetch_latest_oyak_pdf.py",
                    "--output",
                    "artifacts/raw/oyak_latest.pdf",
                )
                if code != 0:
                    pipeline_status = f"FETCH_FAILED: {stderr or stdout}"
                else:
                    pdf_input = "artifacts/raw/oyak_latest.pdf"

        if pipeline_status.startswith("FETCH_FAILED"):
            draft_status = "FAILED"
        elif pdf_input and pipeline_status != "SKIPPED_DEEPSEEK_PEAK_WINDOW":
            code, stdout, stderr = _run(
                "scripts/parse_oyak_pdf.py",
                "--input",
                pdf_input,
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

        cycle_dir = ROOT / "artifacts" / "cycle_reports"
        cycle_dir.mkdir(parents=True, exist_ok=True)
        cycle_path = cycle_dir / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

        telegram_cfg = TelegramConfig.from_env(ROOT)
        telegram_delivery_mode = telegram_cfg.delivery_mode
        report_data_path = ROOT / "artifacts" / "daily_report_data.json"
        draft_path = ROOT / "artifacts" / "daily_report_draft.md"
        report_data: dict = {}
        draft_text = ""
        if report_data_path.exists():
            report_data = json.loads(report_data_path.read_text(encoding="utf-8"))
        if draft_path.exists():
            draft_text = draft_path.read_text(encoding="utf-8")

        ai_review_config = DualAiReviewConfig.from_env(ROOT)
        primary_review, secondary_review = evaluate_dual_review(report_data, draft_text, ai_review_config)
        decision = build_queue_payload(
            report_data=report_data,
            draft_text=draft_text,
            primary_review=primary_review,
            secondary_review=secondary_review,
            telegram_delivery_mode=telegram_delivery_mode,
        )
        queue_path = write_queue_record(decision, draft_text, report_data, ROOT, telegram_delivery_mode)

        telegram_status = "SKIPPED"
        error_alert_status = "SKIPPED"
        error_alert_path = ""
        alert_reason = ""
        if pipeline_status != "OK" or primary_review.status == "PENDING" or secondary_review.status == "PENDING":
            if pipeline_status != "OK":
                alert_reason = pipeline_status
            elif primary_review.status == "PENDING" or secondary_review.status == "PENDING":
                alert_reason = "AI_REVIEW_PENDING_OR_MISSING"
            alert = build_error_alert(
                error_code="CYCLE_WARNING",
                source_name="run_cycle",
                severity="ERROR" if pipeline_status != "OK" else "WARN",
                requires_manual_review=True,
                message="Cycle finished with a blocker or unresolved review state.",
                details=alert_reason,
            )
            error_alert_path = str(persist_error_alert(alert, ROOT))
            error_alert_status = send_error_alert_if_enabled(alert, ROOT)
        if decision.should_send_telegram or args.send_telegram:
            if telegram_cfg.enabled and telegram_cfg.bot_token and telegram_cfg.chat_id:
                if decision.should_send_telegram:
                    client = TelegramClient(telegram_cfg)
                    sent_doc = False
                    sent_text = False
                    doc_error = ""
                    text_error = ""
                    if draft_path.exists():
                        try:
                            client.send_document(draft_path, caption="Gunluk rapor eki.")
                            sent_doc = True
                        except Exception as exc:
                            doc_error = type(exc).__name__
                    if draft_text:
                        try:
                            client.send_markdown(draft_text)
                            sent_text = True
                        except Exception as exc:
                            text_error = type(exc).__name__
                    if sent_doc and sent_text:
                        telegram_status = "SENT_APPROVED_TEXT_AND_DOC"
                    elif sent_doc:
                        telegram_status = "SENT_APPROVED_DOC_ONLY" if not sent_text else "SENT_APPROVED_TEXT_AND_DOC"
                    elif sent_text:
                        telegram_status = "SENT_APPROVED_TEXT_ONLY"
                    else:
                        failure_bits = [bit for bit in (doc_error, text_error) if bit]
                        telegram_status = f"FAILED_{','.join(failure_bits)}" if failure_bits else "FAILED_UNKNOWN"
                else:
                    telegram_status = f"SKIPPED_{decision.approval_status}"
            else:
                telegram_status = "SKIPPED_MISSING_CONFIG"

        final_report = build_cycle_report(
            next_task_id=next_task_id,
            pipeline_status=f"{pipeline_status}; telegram={telegram_status}; approval={decision.approval_status}; compliance={decision.compliance_check_status}; queue={queue_path.name}",
            draft_status=draft_status,
            git_status="PENDING_COMMIT_PUSH",
        )
        cycle_path.write_text(final_report, encoding="utf-8")

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

        print(json.dumps({
            "cycle_report": str(cycle_path),
            "next_task_id": next_task_id,
            "telegram_status": telegram_status,
            "git_status": git_status,
            "ai_provider": ai_cfg.provider or "unset",
            "primary_ai_status": primary_review.status,
            "secondary_ai_status": secondary_review.status,
            "approval_status": decision.approval_status,
            "compliance_check_status": decision.compliance_check_status,
            "telegram_delivery_mode": telegram_delivery_mode,
            "approval_queue": str(queue_path),
            "error_alert_status": error_alert_status,
            "error_alert_path": error_alert_path,
        }, ensure_ascii=False))
        return 0
    except Exception as exc:
        error_alert_status = "SKIPPED_MISSING_CONFIG"
        error_alert_path = ""
        try:
            alert = build_error_alert(
                error_code="CYCLE_FATAL",
                source_name="run_cycle",
                severity="ERROR",
                requires_manual_review=True,
                message="Run cycle crashed before completion.",
                details=f"{type(exc).__name__}: {exc}",
            )
            error_alert_path = str(persist_error_alert(alert, ROOT))
            error_alert_status = send_error_alert_if_enabled(alert, ROOT)
        except Exception as alert_exc:
            error_alert_status = f"FAILED_{type(alert_exc).__name__}"

        print(json.dumps({
            "cycle_report": "",
            "next_task_id": "UNKNOWN",
            "telegram_status": "FAILED_FATAL",
            "git_status": "SKIPPED",
            "ai_provider": "unknown",
            "primary_ai_status": "UNKNOWN",
            "secondary_ai_status": "UNKNOWN",
            "approval_status": "UNKNOWN",
            "compliance_check_status": "UNKNOWN",
            "telegram_delivery_mode": "UNKNOWN",
            "approval_queue": "",
            "error_alert_status": error_alert_status,
            "error_alert_path": error_alert_path,
            "fatal_error": f"{type(exc).__name__}: {exc}",
        }, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
