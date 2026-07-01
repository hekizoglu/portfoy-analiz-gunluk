from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
from urllib import error, request

from app.config import load_config_map


@dataclass(slots=True)
class ModelEndpointConfig:
    provider: str
    api_key: str
    base_url: str
    model: str
    temperature: float = 0.0
    enabled: bool = False

    def is_configured(self) -> bool:
        return self.enabled and bool(self.provider and self.api_key and self.base_url and self.model)


@dataclass(slots=True)
class ReviewVerdict:
    role: str
    provider: str
    model: str
    status: str
    summary: str
    confidence: float
    reasons: list[str]
    risks: list[str]
    raw_response: str = ""
    skipped_reason: str = ""

    def short_note(self) -> str:
        if self.skipped_reason:
            return f"{self.role}: SKIPPED ({self.skipped_reason})"
        return f"{self.role}: {self.status} | {self.summary}"


@dataclass(slots=True)
class DualAiReviewConfig:
    primary: ModelEndpointConfig
    secondary: ModelEndpointConfig

    @classmethod
    def from_env(cls, base_dir: Path | None = None) -> "DualAiReviewConfig":
        data = load_config_map(base_dir)
        primary = ModelEndpointConfig(
            provider=data.get("AI_TASK_RUNNER_PROVIDER", "").strip().lower(),
            api_key=data.get("AI_TASK_RUNNER_API_KEY", ""),
            base_url=data.get("AI_TASK_RUNNER_BASE_URL", ""),
            model=data.get("AI_TASK_RUNNER_MODEL", ""),
            temperature=float(data.get("AI_TASK_RUNNER_TEMPERATURE", "0.1") or 0.1),
            enabled=True,
        )

        secondary_provider = data.get("AI_SECONDARY_PROVIDER", "").strip().lower()
        secondary_api_key = data.get("AI_SECONDARY_API_KEY", "")
        secondary_base_url = data.get("AI_SECONDARY_BASE_URL", "")
        secondary_model = data.get("AI_SECONDARY_MODEL", "")
        secondary_enabled = _parse_bool(data.get("AI_SECONDARY_ENABLED"), default=True)

        if not secondary_provider and primary.is_configured():
            secondary = ModelEndpointConfig(
                provider=primary.provider,
                api_key=primary.api_key,
                base_url=primary.base_url,
                model=secondary_model or primary.model,
                temperature=float(data.get("AI_SECONDARY_TEMPERATURE", "0.0") or 0.0),
                enabled=secondary_enabled,
            )
        else:
            secondary = ModelEndpointConfig(
                provider=secondary_provider,
                api_key=secondary_api_key,
                base_url=secondary_base_url,
                model=secondary_model,
                temperature=float(data.get("AI_SECONDARY_TEMPERATURE", "0.0") or 0.0),
                enabled=secondary_enabled,
            )

        return cls(primary=primary, secondary=secondary)


def _parse_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _build_endpoint_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    return f"{base}/chat/completions"


def _extract_json_text(content: str) -> dict[str, Any]:
    parsed = json.loads(content)
    if isinstance(parsed, dict):
        return parsed
    return {"raw": parsed}


def _parse_model_response(payload: dict[str, Any], fallback_role: str, config: ModelEndpointConfig) -> ReviewVerdict:
    raw_text = ""
    try:
        raw_text = payload["choices"][0]["message"]["content"]
    except Exception:
        raw_text = json.dumps(payload, ensure_ascii=False)

    try:
        data = _extract_json_text(raw_text)
    except Exception:
        return ReviewVerdict(
            role=fallback_role,
            provider=config.provider,
            model=config.model,
            status="PENDING",
            summary="Model output JSON olarak parse edilemedi.",
            confidence=0.0,
            reasons=["JSON_PARSE_FAILED"],
            risks=["UNSTRUCTURED_MODEL_OUTPUT"],
            raw_response=raw_text,
        )

    status = str(data.get("status", "PENDING")).upper()
    summary = str(data.get("summary", "")).strip() or "No summary."
    confidence = _safe_float(data.get("confidence"), default=0.5)
    reasons = _ensure_string_list(data.get("reasons"))
    risks = _ensure_string_list(data.get("risks"))

    return ReviewVerdict(
        role=fallback_role,
        provider=config.provider,
        model=config.model,
        status=status,
        summary=summary,
        confidence=confidence,
        reasons=reasons,
        risks=risks,
        raw_response=raw_text,
    )


def _safe_float(value: Any, *, default: float = 0.5) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _ensure_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _review_prompt(role: str, report_data: dict[str, Any], draft_text: str) -> tuple[str, str]:
    system = (
        "You are a strict financial research QA reviewer. "
        "Return only a JSON object with keys: status, summary, confidence, reasons, risks. "
        "status must be APPROVE, PENDING, or REJECT. "
        "Do not give investment advice. Focus on data quality, compliance, freshness, and contradictory signals."
    )
    user = {
        "role": role,
        "report": {
            "report_date": report_data.get("report_date"),
            "source_count": report_data.get("source_count"),
            "valid_row_count": report_data.get("valid_row_count"),
            "manual_review_count": report_data.get("manual_review_count"),
            "top_candidates": report_data.get("top_candidates", [])[:5],
            "anomalies": report_data.get("anomalies", [])[:5],
            "revisions": report_data.get("revisions", [])[:5],
            "manual_reviews": report_data.get("manual_reviews", [])[:5],
            "source_snapshot": report_data.get("source_snapshot", []),
            "market_context": report_data.get("market_context", []),
            "next_actions": report_data.get("next_actions", []),
        },
        "draft_text": draft_text,
        "instructions": [
            "Approve only if the report is internally coherent, disclaimer is present, and no publish blocker is visible.",
            "PENDING if the output looks useful but not ready for public automation.",
            "REJECT if there is a compliance issue, missing disclaimer, or stale/contradictory data that would mislead users.",
            "List concrete reasons and risks as short strings.",
        ],
    }
    return system, json.dumps(user, ensure_ascii=False, indent=2)


def _call_model(config: ModelEndpointConfig, role: str, report_data: dict[str, Any], draft_text: str) -> ReviewVerdict:
    if not config.is_configured():
        return ReviewVerdict(
            role=role,
            provider=config.provider or "unset",
            model=config.model or "unset",
            status="PENDING",
            summary="AI reviewer not configured.",
            confidence=0.0,
            reasons=["AI_REVIEW_NOT_CONFIGURED"],
            risks=["NO_MODEL_ENDPOINT"],
            skipped_reason="config_missing",
        )

    system_prompt, user_prompt = _review_prompt(role, report_data, draft_text)
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": config.temperature,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        _build_endpoint_url(config.base_url),
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with request.urlopen(req, timeout=90) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
        return ReviewVerdict(
            role=role,
            provider=config.provider,
            model=config.model,
            status="PENDING",
            summary=f"AI reviewer HTTP error: {exc.code}",
            confidence=0.0,
            reasons=["HTTP_ERROR"],
            risks=[body[:120]],
            skipped_reason=f"http_{exc.code}",
        )
    except Exception as exc:
        return ReviewVerdict(
            role=role,
            provider=config.provider,
            model=config.model,
            status="PENDING",
            summary=f"AI reviewer unavailable: {type(exc).__name__}",
            confidence=0.0,
            reasons=["REQUEST_FAILED"],
            risks=[str(exc)[:120]],
            skipped_reason=type(exc).__name__,
        )

    return _parse_model_response(payload, role, config)


def evaluate_dual_review(report_data: dict[str, Any], draft_text: str, config: DualAiReviewConfig | None = None) -> tuple[ReviewVerdict, ReviewVerdict]:
    review_config = config or DualAiReviewConfig.from_env()
    primary = _call_model(review_config.primary, "primary", report_data, draft_text)
    secondary = _call_model(review_config.secondary, "secondary", report_data, draft_text)
    return primary, secondary
