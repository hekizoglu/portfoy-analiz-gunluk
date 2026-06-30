# AUTOMATION

## Purpose
Gunluk veri cekme, validation, draft olusturma ve manuel onay akisini tanimlar.

## When to read this file
Scheduler kurarken, local/CI pipeline planlarken veya runtime komut akislarini belirlerken.

## What it controls
Calisma zamani, scheduler secenekleri, step sirası ve auto-send sinirlari.

## What it must not contain
Canli secret, onaysiz auto-send varsayimi.

## Related files
`BUILD_TEST_FIX.md`, `TELEGRAM_INTEGRATION.md`, `GOOGLE_SHEETS_SCHEMA.md`, `PROJECT_MEMORY.md`

## Update rules
Pipeline step'leri veya zamanlama degistikce guncellenir.

## Last updated
2026-06-30

## Scheduler options
- Local Windows Task Scheduler
- Linux cron
- GitHub Actions
- Cloud Run / Cloud Scheduler
- Codex/Claude ajan kosulari

## Continuous roadmap loop
- Baslangic scripti: `scripts/start_roadmap_loop.ps1`
- Default cadence: `10 dakika`
- Cycle runner: `scripts/run_cycle.py`
- Telegram cycle report: config varsa her cycle sonunda gonderilir
- Commit/push: dosya degisti ise her cycle sonunda denenir

## Daily schedule
- `08:45` data pull
- `09:05` validation
- `09:15` pre-market Telegram draft
- `18:15` close-price refresh
- `18:30` closing update draft

## MVP pipeline command plan
1. `pull_sources`
   - OYAK resmi kaynagini indir veya elle saglanan belgeyi al
   - hash/fingerprint olustur
2. `parse_reports`
   - parser kurallarina gore satir adaylari uret
3. `validate_rows`
   - schema ve confidence kontrolleri uygula
4. `load_sheets`
   - `01_RAW_REPORTS`, `02_PARSED_ROWS`, `03_BROKER_VALUATIONS` tablarini guncelle
5. `compute_scores`
   - consensus/revision/anomaly placeholder veya mevcut veriyle hesapla
6. `build_telegram_draft`
   - `08_TELEGRAM_QUEUE` tabina taslak yaz
7. `approval_gate`
   - manuel kontrol ve compliance check
8. `send_if_approved`
   - yalnizca approval ve config uygunsa Telegram gonderimi

## Hard rule
Manuel approval guvenli sekilde implement edilmeden auto-send default olarak kapali kalir.
