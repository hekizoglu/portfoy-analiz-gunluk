# GOOGLE_SHEETS_SCHEMA

## Purpose
Google Sheets tabanli MVP depolama katmaninin sekme, kolon ve validation tasarimini tanimlar.

## When to read this file
Sheets dosyasi kurarken, parser ciktilarini MVP veritabanina yansitirken veya Telegram kuyruk taslagini sheets uzerinden yonetirken.

## What it controls
Sekme isimleri, kolonlar, zorunlu alanlar, ornek satirlar ve validation kurallari.

## What it must not contain
Gercek kullanici verisi, credential veya script kodu.

## Related files
`DATABASE_SCHEMA.md`, `PARSING_RULES.md`, `TELEGRAM_INTEGRATION.md`, `AUTOMATION.md`

## Update rules
MVP workflow degistikce veya yeni sekme eklendikce guncellenir.

## Last updated
2026-06-30

## 00_SETTINGS
- Columns:
  - `setting_key`
  - `setting_value`
  - `description`
  - `is_secret`
- Required fields: `setting_key`, `setting_value`
- Example row: `default_universe | BIST100 | Baslangic kapsam | false`
- Validation rules: secret alanlar placeholder olmali; gercek token sheets'te tutulmaz

## 01_RAW_REPORTS
- Columns:
  - `raw_report_id`
  - `source_name`
  - `source_url`
  - `report_date_detected`
  - `download_timestamp`
  - `content_type`
  - `source_file_hash_sha256`
  - `adapter_status`
  - `adapter_notes`
- Required fields: `raw_report_id`, `source_name`, `source_url`, `source_file_hash_sha256`, `adapter_status`
- Example row: `uuid | OYAK Yatirim valuation table | https://example.com/report.pdf | 2026-06-30 | 2026-06-30T08:46:00 | application/pdf | abc123 | READY_FOR_PARSE | Public source`
- Validation rules: hash unique olmali; source URL bos olamaz

## 02_PARSED_ROWS
- Columns:
  - `parsed_row_id`
  - `raw_report_id`
  - `row_sequence`
  - `raw_row_text`
  - `confidence_score`
  - `validation_status`
  - `validation_errors`
  - `parser_version`
- Required fields: `parsed_row_id`, `raw_report_id`, `row_sequence`, `validation_status`
- Example row: `uuid | raw-uuid | 12 | THYAO AL 130 TL | 0.95 | VALID | | v0.1`
- Validation rules: confidence 0-1; row_sequence integer

## 03_BROKER_VALUATIONS
- Columns:
  - `valuation_id`
  - `raw_report_id`
  - `parsed_row_id`
  - `ticker`
  - `company_name`
  - `sector`
  - `broker`
  - `report_date`
  - `recommendation_raw`
  - `recommendation_normalized`
  - `current_price_reported`
  - `target_price`
  - `upside_reported`
  - `currency`
  - `confidence_score`
  - `source_url`
  - `source_file_hash_sha256`
- Required fields: `valuation_id`, `ticker`, `broker`, `report_date`, `target_price`, `source_url`
- Example row: `uuid | raw-uuid | parsed-uuid | THYAO | Turk Hava Yollari | Transportation | OYAK | 2026-06-30 | AL | BUY | 100 | 130 | 30 | TRY | 0.95 | https://example.com/report.pdf | abc123`
- Validation rules: ticker uppercase; recommendation normalized controlled listeden gelmeli

## 04_CONSENSUS_DAILY
- Columns:
  - `consensus_id`
  - `ticker`
  - `consensus_date`
  - `broker_count`
  - `average_target_price`
  - `median_target_price`
  - `weighted_target_price`
  - `consensus_potential_pct`
  - `confidence_score`
- Required fields: `consensus_id`, `ticker`, `consensus_date`, `broker_count`
- Example row: `uuid | THYAO | 2026-06-30 | 4 | 128 | 130 | 129 | 29 | 0.88`
- Validation rules: broker_count >= 1

## 05_REVISIONS
- Columns:
  - `revision_id`
  - `ticker`
  - `broker`
  - `old_report_date`
  - `new_report_date`
  - `old_target_price`
  - `new_target_price`
  - `old_recommendation_normalized`
  - `new_recommendation_normalized`
  - `revision_direction`
  - `revision_pct`
- Required fields: `revision_id`, `ticker`, `broker`, `new_report_date`, `revision_direction`
- Example row: `uuid | THYAO | OYAK | 2026-06-01 | 2026-06-30 | 120 | 130 | HOLD | BUY | UP | 8.33`
- Validation rules: old/new date mantikli sirada olmali

## 06_ANOMALIES
- Columns:
  - `anomaly_id`
  - `ticker`
  - `anomaly_date`
  - `anomaly_type`
  - `severity_score`
  - `requires_manual_review`
  - `details_json`
- Required fields: `anomaly_id`, `ticker`, `anomaly_date`, `anomaly_type`
- Example row: `uuid | THYAO | 2026-06-30 | POSITIVE_DIVERGENCE | 0.91 | true | {"consensus":100,"new_target":130}`
- Validation rules: severity 0-1

## 07_SURPRISE_CANDIDATES
- Columns:
  - `candidate_id`
  - `ticker`
  - `candidate_date`
  - `final_score`
  - `surprise_score`
  - `primary_reason`
  - `risk_label`
  - `manual_review_required`
- Required fields: `candidate_id`, `ticker`, `candidate_date`, `final_score`
- Example row: `uuid | THYAO | 2026-06-30 | 78.4 | 84.0 | Positive divergence + revision | MANUAL_CONTROL | true`
- Validation rules: final_score 0-100 araliginda normalize edilmeli

## 08_TELEGRAM_QUEUE
- Columns:
  - `queue_id`
  - `queue_date`
  - `message_type`
  - `message_body_markdown`
  - `approval_status`
  - `approval_notes`
  - `compliance_check_status`
  - `source_count`
- Required fields: `queue_id`, `queue_date`, `message_type`, `message_body_markdown`, `approval_status`
- Example row: `uuid | 2026-06-30 | DAILY_PREMARKET_DRAFT | ... | PENDING | Needs analyst glance | PASS | 1`
- Validation rules: approval_status kontrollu listeden gelmeli

## 09_SENT_MESSAGES
- Columns:
  - `sent_message_id`
  - `queue_id`
  - `telegram_chat_id`
  - `telegram_message_id`
  - `sent_timestamp`
  - `delivery_status`
- Required fields: `sent_message_id`, `queue_id`, `telegram_chat_id`, `sent_timestamp`, `delivery_status`
- Example row: `uuid | queue-uuid | -5434687426 | 550 | 2026-06-30T09:16:00 | SENT`
- Validation rules: chat ID string olarak tutulur

## 10_MANUAL_REVIEW
- Columns:
  - `review_item_id`
  - `source_name`
  - `raw_report_id`
  - `parsed_row_id`
  - `review_reason`
  - `priority`
  - `status`
  - `created_at`
  - `resolved_at`
- Required fields: `review_item_id`, `review_reason`, `priority`, `status`, `created_at`
- Example row: `uuid | OYAK | raw-uuid | parsed-uuid | Currency missing | HIGH | OPEN | 2026-06-30T08:50:00 |`
- Validation rules: status kontrollu listeden gelmeli

## 11_ERRORS
- Columns:
  - `error_id`
  - `run_id`
  - `error_code`
  - `error_message`
  - `source_name`
  - `occurred_at`
  - `severity`
  - `status`
- Required fields: `error_id`, `error_code`, `error_message`, `occurred_at`, `severity`
- Example row: `uuid | run-uuid | PARSER_EMPTY_OUTPUT | No valid rows extracted | OYAK | 2026-06-30T08:51:00 | ERROR | OPEN`
- Validation rules: severity kontrollu listeden gelmeli

## 12_BROKER_SCORECARD
- Columns:
  - `track_record_id`
  - `broker`
  - `sector`
  - `window_code`
  - `hit_rate`
  - `directional_accuracy`
  - `sample_size`
  - `reliability_score`
- Required fields: `track_record_id`, `broker`, `window_code`, `sample_size`
- Example row: `uuid | OYAK | Aviation | 3M | 0.62 | 0.68 | 12 | 0.64`
- Validation rules: oranlar 0-1
