# DATABASE_SCHEMA

## Purpose
Sistemin canonical veri modelini ve ileride Google Sheets'ten daha kalici depolamaya gecis temelini tanimlar.

## When to read this file
Veri modeli kurarken, yeni tablo eklerken veya parser/sheets alanlarini eslerken.

## What it controls
Tablo amaclari, alanlar, primary key, index ve validation kurallari.

## What it must not contain
Gercek veri dump'i, credential, migration script'i.

## Related files
`PARSING_RULES.md`, `GOOGLE_SHEETS_SCHEMA.md`, `SCORING.md`, `AUTOMATION.md`

## Update rules
Her yeni veri varligi veya alan degisikliginde guncellenir.

## Last updated
2026-06-30

## Table: raw_reports
- Purpose: ham dosya ve metadata arsivi
- Fields:
  - `raw_report_id` UUID
  - `source_name` string
  - `source_url` string
  - `content_type` string
  - `report_date_detected` date nullable
  - `download_timestamp` datetime
  - `source_file_hash_sha256` string
  - `storage_path` string
  - `adapter_status` string
  - `adapter_notes` text nullable
- Primary key: `raw_report_id`
- Important indexes: `source_file_hash_sha256`, `(source_name, report_date_detected)`
- Validation rules: hash zorunlu; storage path bos olamaz

## Table: parsed_report_rows
- Purpose: parser satir seviyesinde ara ciktilar
- Fields:
  - `parsed_row_id` UUID
  - `raw_report_id` UUID
  - `row_sequence` integer
  - `raw_row_text` text
  - `parsed_json` json
  - `parser_version` string
  - `confidence_score` numeric(5,4)
  - `validation_status` string
  - `validation_errors` text nullable
- Primary key: `parsed_row_id`
- Important indexes: `raw_report_id`, `validation_status`
- Validation rules: confidence 0-1 araliginda olmali

## Table: broker_valuations
- Purpose: normalize edilmis broker bazli degerleme satirlari
- Fields:
  - `valuation_id` UUID
  - `raw_report_id` UUID
  - `parsed_row_id` UUID
  - `ticker` string
  - `company_name` string
  - `sector` string nullable
  - `broker` string
  - `report_date` date
  - `recommendation_raw` string
  - `recommendation_normalized` string
  - `current_price_reported` numeric(18,4)
  - `target_price` numeric(18,4)
  - `upside_reported` numeric(9,4) nullable
  - `currency` string
  - `confidence_score` numeric(5,4)
  - `source_url` string
  - `source_file_hash_sha256` string
- Primary key: `valuation_id`
- Important indexes: `(ticker, report_date)`, `(broker, report_date)`
- Validation rules: `ticker`, `broker`, `report_date`, `target_price`, `source_url` zorunlu

## Table: normalized_recommendations
- Purpose: tavsiye sozluk eslemesi ve varyant yonetimi
- Fields:
  - `recommendation_map_id` UUID
  - `broker` string
  - `recommendation_raw` string
  - `recommendation_normalized` string
  - `is_active` boolean
- Primary key: `recommendation_map_id`
- Important indexes: `(broker, recommendation_raw)`
- Validation rules: normalized alan kontrollu sozlukten gelmeli

## Table: stock_master
- Purpose: temel hisse referans tablosu
- Fields:
  - `ticker` string
  - `company_name` string
  - `sector` string nullable
  - `bist_index_group` string nullable
  - `is_active` boolean
- Primary key: `ticker`
- Important indexes: `sector`, `is_active`
- Validation rules: ticker unique

## Table: daily_prices
- Purpose: fiyat ve hacim zaman serisi
- Fields:
  - `price_id` UUID
  - `ticker` string
  - `trade_date` date
  - `close_price` numeric(18,4)
  - `volume` numeric(18,2) nullable
  - `source_name` string
- Primary key: `price_id`
- Important indexes: `(ticker, trade_date)`
- Validation rules: close_price pozitif

## Table: consensus_daily
- Purpose: gunluk consensus hesaplari
- Fields:
  - `consensus_id` UUID
  - `ticker` string
  - `consensus_date` date
  - `broker_count` integer
  - `average_target_price` numeric(18,4)
  - `median_target_price` numeric(18,4)
  - `weighted_target_price` numeric(18,4) nullable
  - `recommendation_distribution_json` json
  - `consensus_potential_pct` numeric(9,4) nullable
  - `confidence_score` numeric(5,4)
- Primary key: `consensus_id`
- Important indexes: `(ticker, consensus_date)`
- Validation rules: broker_count >= 1

## Table: valuation_revisions
- Purpose: hedef fiyat ve tavsiye degisim takibi
- Fields:
  - `revision_id` UUID
  - `ticker` string
  - `broker` string
  - `old_report_date` date
  - `new_report_date` date
  - `old_target_price` numeric(18,4) nullable
  - `new_target_price` numeric(18,4) nullable
  - `old_recommendation_normalized` string nullable
  - `new_recommendation_normalized` string nullable
  - `revision_direction` string
  - `revision_pct` numeric(9,4) nullable
- Primary key: `revision_id`
- Important indexes: `(ticker, broker, new_report_date)`
- Validation rules: new_report_date >= old_report_date

## Table: anomalies
- Purpose: divergence, shock ve coverage degisimleri
- Fields:
  - `anomaly_id` UUID
  - `ticker` string
  - `anomaly_date` date
  - `anomaly_type` string
  - `severity_score` numeric(5,4)
  - `details_json` json
  - `requires_manual_review` boolean
- Primary key: `anomaly_id`
- Important indexes: `(ticker, anomaly_date)`, `anomaly_type`
- Validation rules: severity 0-1

## Table: broker_track_record
- Purpose: broker guvenilirlik olcumleri
- Fields:
  - `track_record_id` UUID
  - `broker` string
  - `sector` string nullable
  - `window_code` string
  - `hit_rate` numeric(5,4)
  - `directional_accuracy` numeric(5,4)
  - `sample_size` integer
  - `reliability_score` numeric(5,4)
- Primary key: `track_record_id`
- Important indexes: `(broker, sector, window_code)`
- Validation rules: sample_size >= 0

## Table: kap_events
- Purpose: KAP olay siniflandirmasi
- Fields:
  - `kap_event_id` UUID
  - `ticker` string
  - `event_date` date
  - `event_type` string
  - `headline` string
  - `source_url` string
  - `impact_score` numeric(5,4) nullable
- Primary key: `kap_event_id`
- Important indexes: `(ticker, event_date)`, `event_type`
- Validation rules: source_url zorunlu

## Table: technical_indicators
- Purpose: teknik filtre girdileri
- Fields:
  - `indicator_id` UUID
  - `ticker` string
  - `trade_date` date
  - `rsi_14` numeric(9,4) nullable
  - `ma_20` numeric(18,4) nullable
  - `ma_50` numeric(18,4) nullable
  - `volume_ratio_20d` numeric(9,4) nullable
  - `trend_state` string nullable
- Primary key: `indicator_id`
- Important indexes: `(ticker, trade_date)`
- Validation rules: numeric alanlar negatif olamaz

## Table: telegram_queue
- Purpose: gonderim oncesi taslak ve approval kuyrugu
- Fields:
  - `queue_id` UUID
  - `queue_date` date
  - `message_type` string
  - `message_body_markdown` text
  - `approval_status` string
  - `approval_notes` text nullable
  - `created_from_run_id` UUID nullable
  - `compliance_check_status` string
- Primary key: `queue_id`
- Important indexes: `(queue_date, approval_status)`
- Validation rules: approval_status `PENDING`, `APPROVED`, `REJECTED`

## Table: telegram_sent_messages
- Purpose: gonderilen mesajlarin audit izi
- Fields:
  - `sent_message_id` UUID
  - `queue_id` UUID
  - `telegram_chat_id` string
  - `telegram_message_id` string nullable
  - `sent_timestamp` datetime
  - `delivery_status` string
- Primary key: `sent_message_id`
- Important indexes: `queue_id`, `sent_timestamp`
- Validation rules: queue_id zorunlu

## Table: manual_review_queue
- Purpose: insan kontrolu gerektiren kayitlar
- Fields:
  - `review_item_id` UUID
  - `source_name` string
  - `raw_report_id` UUID nullable
  - `parsed_row_id` UUID nullable
  - `review_reason` string
  - `priority` string
  - `status` string
  - `created_at` datetime
  - `resolved_at` datetime nullable
- Primary key: `review_item_id`
- Important indexes: `(status, priority)`, `source_name`
- Validation rules: status `OPEN`, `IN_REVIEW`, `RESOLVED`

## Table: error_log
- Purpose: sistemsel hata kayitlari
- Fields:
  - `error_id` UUID
  - `run_id` UUID nullable
  - `error_code` string
  - `error_message` text
  - `source_name` string nullable
  - `occurred_at` datetime
  - `severity` string
  - `status` string
- Primary key: `error_id`
- Important indexes: `occurred_at`, `error_code`
- Validation rules: severity `INFO`, `WARN`, `ERROR`, `CRITICAL`

## Table: system_runs
- Purpose: pipeline kosularinin audit ve performans kaydi
- Fields:
  - `run_id` UUID
  - `run_type` string
  - `started_at` datetime
  - `finished_at` datetime nullable
  - `status` string
  - `source_count` integer nullable
  - `parsed_row_count` integer nullable
  - `queued_message_count` integer nullable
  - `notes` text nullable
- Primary key: `run_id`
- Important indexes: `started_at`, `status`
- Validation rules: started_at zorunlu
