# BUILD_TEST_FIX

## Purpose
Build/test/fix dongusunu ve placeholder komut planini tanimlar.

## When to read this file
Ilk runtime scriptleri yazilirken, test stratejisi kurarken veya failure sonrasi duzeltme yaparken.

## What it controls
Komut sirasi, failure siniflari, retry limiti ve hata kaydi kurallari.

## What it must not contain
Kontrolsuz retry, gizli bilgi, manuel review atlama kurali.

## Related files
`QA.md`, `ERRORS.md`, `AUTOMATION.md`

## Update rules
Runtime komutlari netlestikce guncellenir.

## Last updated
2026-06-30

## Placeholder command loop
1. `python scripts/fetch_latest_oyak_pdf.py`
2. `python scripts/parse_oyak_pdf.py --input artifacts/raw/oyak_latest.pdf`
3. `python scripts/build_daily_report_from_oyak.py --input artifacts/oyak_parsed_rows.json --output artifacts/daily_report_data.json`
4. `python scripts/build_telegram_draft.py --input artifacts/daily_report_data.json --output artifacts/daily_report_draft.md`
5. `python scripts/send_telegram.py --dry-run --input artifacts/daily_report_draft.md`

## Parser test rules
- Her sample source icin en az bir golden output
- Invalid source durumunda manual review beklenmeli

## Scoring test rules
- Penalty clamp testleri
- Tek broker penalty testi
- Missing source blocker testi

## Telegram snapshot tests
- Disclaimer var mi
- Forbidden wording yok mu
- Risk label ciktisi stabil mi

## Failure classification
- `SOURCE_FAILURE`
- `PARSER_FAILURE`
- `VALIDATION_FAILURE`
- `SCORING_FAILURE`
- `QUEUE_FAILURE`
- `TELEGRAM_FAILURE`

## Max retry rules
- Source pull: `2`
- Parse/validate: `1`
- Telegram send: `1` ve sadece approved queue icin

## ERRORS.md update rules
- Yeni failure sinifi varsa `ERRORS.md`ye kayit eklenir
- Tekrarlayan hata varsa mevcut kayda yeni prevention notu eklenir
