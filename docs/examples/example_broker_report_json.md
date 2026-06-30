# Example Broker Report JSON

## Purpose
Canonical broker valuation JSON ornegini ve validation beklentisini gosterir.

## When to read this file
Parser output tasarlarken, schema test ederken veya manual review formatini kontrol ederken.

## What it controls
Beklenen alan adlari, tipler ve minimum valid payload yapisi.

## What it must not contain
Uydurma publish-ready iddia, schema disi alanlar, canli token.

## Related files
`PARSING_RULES.md`, `DATABASE_SCHEMA.md`

## Update rules
Canonical JSON schema degistikce guncellenir.

## Last updated
2026-06-30

```json
{
  "ticker": "THYAO",
  "company_name": "Turk Hava Yollari",
  "broker": "Example Broker",
  "report_date": "2026-06-30",
  "recommendation_raw": "AL",
  "recommendation_normalized": "BUY",
  "current_price_reported": 100.0,
  "target_price": 130.0,
  "upside_reported": 30.0,
  "currency": "TRY",
  "source_url": "TODO",
  "source_file_hash_sha256": "TODO",
  "confidence_score": 0.95,
  "validation_status": "VALID"
}
```

## Validation notes
- `ticker` buyuk harf ve BIST sembolu olmali.
- `report_date` ISO formatinda olmali.
- `confidence_score` 0 ile 1 arasinda olmali.
- `validation_status` publish izni icin `VALID` olmali.
