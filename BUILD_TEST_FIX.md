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
1. `python -m scripts.pull_sources`
2. `python -m scripts.parse_reports`
3. `python -m scripts.validate_rows`
4. `python -m scripts.compute_scores`
5. `python -m scripts.build_telegram_draft`
6. `python -m scripts.send_telegram --dry-run`

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
