# LOOP

## Purpose
10 dakikada bir calisacak operasyonel dongunun kurallarini tanimlar.

## When to read this file
Surekli calisan roadmap/data loop'u baslatirken veya scheduler davranisini degistirirken.

## What it controls
Dongu sirasi, cycle raporu, Telegram bildirim kosullari ve git commit/push kurallari.

## What it must not contain
Secret, onaysiz destructive git komutlari, gercek token.

## Related files
`AUTOMATION.md`, `SPRINT_15_MIN.md`, `TELEGRAM_INTEGRATION.md`, `PROJECT_MEMORY.md`

## Update rules
Dongu davranisi veya cadence degistikce guncellenir.

## Last updated
2026-06-30

## Operational cadence
- Hedef cadence: `10 dakika`
- Her cycle tek bir bounded is parcasi yapar
- Her cycle sonunda Telegram status raporu uretir
- Dosya degisikligi varsa commit/push dener

## Cycle order
1. Config yukle
2. Roadmap'teki ilk `TODO` gorevi tespit et
3. Veri pipeline'i uygunsa calistir
4. Draft veya status raporu uret
5. Telegram report gonder
6. Dosya degisti ise commit/push yap
7. Sonraki cycle zamanina kadar bekle

## Roadmap execution boundary
- Bu repo icindeki loop runner roadmap'teki sonraki gorevi tespit eder ve raporlar.
- Gercek roadmap gorevini otomatik tamamlamak ayrica AI task-runner entegrasyonu gerektirir.
- AI task-runner olmadan loop runner gorev durumunu degistirmez; yalnizca status ve data operasyonu yapar.

## Telegram cycle report minimum fields
- `cycle_timestamp`
- `next_task_id`
- `data_pipeline_status`
- `draft_status`
- `git_status`
- `push_status`

## Git policy
- Sadece mevcut repo icindeki degisiklikleri commit eder
- `git pull --rebase` denemez; remote write tek yonlu operasyon olarak kalir
- Remote yoksa push status `SKIPPED_NO_REMOTE`
