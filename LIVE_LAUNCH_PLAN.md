# LIVE_LAUNCH_PLAN

## Purpose
Uygulamayi kontrollu sekilde canliya almak icin uygulanacak yol haritasini tanimlar.

## When to read this file
Canli yayina cikmadan once, release sonrasi stabilizasyon sirasinda veya scheduler / secrets degisirken.

## What it controls
Preflight checklist, private beta, schedule activation, monitoring ve sonraki genisleme adimlari.

## What it must not contain
Hardcoded secret, auto-send varsayimi, onaysiz public kanal yayini.

## Related files
`AUTOMATION.md`, `TELEGRAM_INTEGRATION.md`, `CONFIGURATION.md`, `QA.md`, `.github/workflows/roadmap_loop.yml`

## Launch principle
Canliya alma "tam otomatik public publish" degil, once private test ve manuel approval ile baslamali.

## Phase 0 - Preflight
Hepsi tamam olmadan schedule acilmaz.

- `.env.local` veya GitHub Secrets hazir mi
- `TELEGRAM_ENABLED=true` sadece test chat icin dogrulandi mi
- `TELEGRAM_BOT_TOKEN` gecerli mi
- `TELEGRAM_CHAT_ID` test hedefi ile uyumlu mu
- `AI_TASK_RUNNER_*` alanlari girilmis mi
- `python -m compileall app scripts` geciyor mu
- `python scripts/run_cycle.py --pdf artifacts/raw/oyak_latest.pdf` geciyor mu
- Telegram dry-run cikti markdown olarak temiz mi

## Phase 1 - Private beta
Ilk gercek deneme kapali hedefte yapilir.

- Workflow `workflow_dispatch` ile manuel calistirilir
- Telegram yalnizca private test chat'e gider
- Git commit/push acik olabilir ama auto-send yine approval-gated kalir
- Hata durumlari `artifacts/cycle_reports/` altinda incelenir

## Phase 2 - Safe schedule
Private beta stabil olunca cron acilir.

- Schedule off-peak araliklara hizalanir
- DeepSeek kullaniliyorsa peak saatlerde cycle skip edilir
- `fetch -> parse -> report -> draft -> review` sirasi bozulmaz
- Yalnizca approval-ready cikti Telegram'a gider

## Phase 3 - Multi-source expansion
Tek kurum cikisindan consensus raporuna gecis.

- `P2-T03` broker normalization dictionary
- `P2-T04` consensus engine
- `P2-T05` broker count filter
- `P2-T06` new/removed coverage detection
- `P2-T07` institution comparison report
- `P2-T08` anomaly / divergence detection
- `P3-T01` KAP catalyst taxonomy

## Phase 4 - Monitoring
Canli yayinda takip edilecek sinyaller.

- Telegram send failures
- Parse / validation failures
- Empty output
- Stale source dates
- Manual review backlog
- GitHub Actions cron health

## Go-live criteria
Schedule'i acmadan once su kosullar saglanmali:

- En az bir yerel smoke test basarili
- Telegram test chat dogrulandi
- Cron peak saatlere girmiyor
- Manual approval kapisi calisiyor
- Rapor, kaynak kapsamini ve risk etiketlerini gosteriyor

## Post-launch cadence
- Her gunde bir kez cikti kalitesi gozden gecirilir
- Her yeni broker adapteri eklendiginde report spec kontrol edilir
- Hata kaliplari `ERRORS.md` ve QA dokumantasyonuna islenir
