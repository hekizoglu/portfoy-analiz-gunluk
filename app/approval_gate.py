from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid
from typing import Any

from app.ai_review import ReviewVerdict


DISALLOWED_PHRASES = [
    "kesin al",
    "garantili",
    "tavan adayi",
    "kacirma",
    "vip sinyal",
    "simdi al",
    "simdi sat",
]


@dataclass(slots=True)
class ApprovalDecision:
    queue_id: str
    queue_date: str
    approval_status: str
    compliance_check_status: str
    approval_notes: list[str]
    should_send_telegram: bool
    send_reason: str
    primary_review: ReviewVerdict
    secondary_review: ReviewVerdict


def build_queue_payload(
    report_data: dict[str, Any],
    draft_text: str,
    primary_review: ReviewVerdict,
    secondary_review: ReviewVerdict,
    telegram_delivery_mode: str,
) -> ApprovalDecision:
    compliance_notes: list[str] = []
    compliance_status = "PASS"

    disclaimer = (
        "Bu icerik yatirim tavsiyesi degildir. Otomatik veri analizi ve genel piyasa taramasidir. Nihai karar kullaniciya aittir."
    )
    draft_lower = draft_text.lower()
    if disclaimer.lower() not in draft_lower:
        compliance_status = "FAIL"
        compliance_notes.append("Missing disclaimer")

    for phrase in DISALLOWED_PHRASES:
        if phrase in draft_lower:
            compliance_status = "FAIL"
            compliance_notes.append(f"Forbidden wording: {phrase}")

    if not report_data.get("source_count"):
        compliance_status = "FAIL"
        compliance_notes.append("No source count")

    if not report_data.get("report_date"):
        compliance_status = "FAIL"
        compliance_notes.append("Missing report date")

    if not report_data.get("top_candidates"):
        compliance_status = "FAIL"
        compliance_notes.append("No top candidates")

    ai_signals = [primary_review.status.upper(), secondary_review.status.upper()]
    if any(status == "REJECT" for status in ai_signals):
        approval_status = "REJECTED"
    elif compliance_status != "PASS":
        approval_status = "PENDING"
    elif any(status == "PENDING" for status in ai_signals):
        approval_status = "PENDING"
    else:
        approval_status = "APPROVED"

    if approval_status == "APPROVED" and telegram_delivery_mode in {"PRIVATE_TEST", "APPROVED_SEND"}:
        should_send = True
        send_reason = f"approved_for_{telegram_delivery_mode.lower()}"
    elif approval_status == "PENDING" and compliance_status == "PASS" and telegram_delivery_mode in {"PRIVATE_TEST", "APPROVED_SEND"}:
        should_send = True
        send_reason = f"pending_review_{telegram_delivery_mode.lower()}"
    else:
        should_send = False
        send_reason = "not_approved_or_queue_only"

    queue_id = f"queue-{uuid.uuid4().hex[:12]}"
    queue_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    notes = [
        f"primary={primary_review.status}:{primary_review.summary}",
        f"secondary={secondary_review.status}:{secondary_review.summary}",
    ]
    notes.extend(compliance_notes)

    return ApprovalDecision(
        queue_id=queue_id,
        queue_date=queue_date,
        approval_status=approval_status,
        compliance_check_status=compliance_status,
        approval_notes=notes,
        should_send_telegram=should_send,
        send_reason=send_reason,
        primary_review=primary_review,
        secondary_review=secondary_review,
    )


def write_queue_record(
    decision: ApprovalDecision,
    draft_text: str,
    report_data: dict[str, Any],
    root: Path,
    telegram_delivery_mode: str,
) -> Path:
    queue_dir = root / "artifacts" / "approval_queue"
    queue_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "queue_id": decision.queue_id,
        "queue_date": decision.queue_date,
        "message_type": "DAILY_PREMARKET_DRAFT",
        "message_body_markdown": draft_text,
        "approval_status": decision.approval_status,
        "approval_notes": decision.approval_notes,
        "compliance_check_status": decision.compliance_check_status,
        "source_count": report_data.get("source_count", 0),
        "primary_review": {
            "role": decision.primary_review.role,
            "provider": decision.primary_review.provider,
            "model": decision.primary_review.model,
            "status": decision.primary_review.status,
            "summary": decision.primary_review.summary,
            "confidence": decision.primary_review.confidence,
            "reasons": decision.primary_review.reasons,
            "risks": decision.primary_review.risks,
        },
        "secondary_review": {
            "role": decision.secondary_review.role,
            "provider": decision.secondary_review.provider,
            "model": decision.secondary_review.model,
            "status": decision.secondary_review.status,
            "summary": decision.secondary_review.summary,
            "confidence": decision.secondary_review.confidence,
            "reasons": decision.secondary_review.reasons,
            "risks": decision.secondary_review.risks,
        },
        "telegram_delivery_mode": telegram_delivery_mode,
        "send_reason": decision.send_reason,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    latest_path = queue_dir / "latest.json"
    latest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    history_dir = queue_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = history_dir / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
    history_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return latest_path
