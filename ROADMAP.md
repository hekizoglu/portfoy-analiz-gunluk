# ROADMAP

## Purpose
15 dakikalik sprintlerle ilerleyen resmi gorev listesi.

## When to read this file
Yeni bir sprint baslatirken ve sonraki gorevi secerken.

## What it controls
Gorev sirasi, sprint kapsamı, kabul kriterleri ve gecis bagimliliklari.

## What it must not contain
Uygulama kodu, gizli bilgi, tamamlanmamis iddialar.

## Related files
`00_CONTEXT_GRAPH.md`, `SPRINT_15_MIN.md`, `PROJECT_MEMORY.md`, alan bazli tasarim dosyalari.

## Update rules
Her sprint sonunda yalnizca etkilenen gorevin durumu guncellenir.

## Last updated
2026-06-30

## Phase 1 - MVP: OYAK + Google Sheets + Telegram Manual Queue

### Task P1-T01
- ID: `P1-T01`
- Title: Create OYAK valuation table source adapter design
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `00_CONTEXT_GRAPH.md`, `SPRINT_15_MIN.md`, `DATA_SOURCES.md`, `docs/templates/source_adapter_template.md`
- Output files: `DATA_SOURCES.md`, `docs/source_adapters/oyak_valuation_table.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - OYAK kaynagi icin erisim yontemi, beklenen formatlar, zorunlu alanlar, hash/diff stratejisi ve failure handling tanimlanmis olmali.
  - Tasarim login-protected veya yetkisiz scraping varsaymamalidir.
  - Sonraki parser tasarimina girdi olacak alan haritasi ve adapter arayuzu tanimli olmalidir.
- Risk notes: OYAK kaynak formati degisebilir; PDF/HTML ayrimi ilk canli inceleme yapilana kadar varsayimsaldir.
- Next task: `P1-T02`

### Task P1-T02
- ID: `P1-T02`
- Title: Create PDF parsing strategy
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `PARSING_RULES.md`, `docs/source_adapters/oyak_valuation_table.md`
- Output files: `PARSING_RULES.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - PDF extraction flow, validation gates, confidence score ve manual review kurallari yazili olmali.
  - OYAK adapter tasarimi ile uyumlu field extraction adimlari belirtilmeli.
- Risk notes: PDF tablolari tutarsiz olabilir.
- Next task: `P1-T03`

### Task P1-T03
- ID: `P1-T03`
- Title: Create broker valuation JSON schema
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `PARSING_RULES.md`, `DATABASE_SCHEMA.md`
- Output files: `PARSING_RULES.md`, `DATABASE_SCHEMA.md`, `docs/examples/example_broker_report_json.md`
- Acceptance criteria:
  - JSON alanlari, tipleri, zorunlu alanlar ve validation kurallari acik olmali.
- Risk notes: Kaynaklar arasi alan isimleri farkli olabilir.
- Next task: `P1-T04`

### Task P1-T04
- ID: `P1-T04`
- Title: Create Google Sheets tab schema
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `GOOGLE_SHEETS_SCHEMA.md`, `DATABASE_SCHEMA.md`
- Output files: `GOOGLE_SHEETS_SCHEMA.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - Tum MVP tablari, kolonlari ve validation mantigi tanimli olmali.
- Risk notes: Google Sheets olcegi sinirli.
- Next task: `P1-T05`

### Task P1-T05
- ID: `P1-T05`
- Title: Create first scoring formula
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `SCORING.md`, `COMPLIANCE.md`
- Output files: `SCORING.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - MVP icin acik ve audit edilebilir bir puanlama formulu yazilmali.
- Risk notes: Erken scoring asiri kesinlik izlenimi verebilir.
- Next task: `P1-T06`

### Task P1-T06
- ID: `P1-T06`
- Title: Create Telegram manual approval format
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `TELEGRAM_FORMAT.md`, `COMPLIANCE.md`
- Output files: `TELEGRAM_FORMAT.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - Manuel onay kuyrugu formatı ve zorunlu uyari metni tanimli olmali.
- Risk notes: Uyumsuz dil itibar/compliance riski yaratir.
- Next task: `P1-T07`

### Task P1-T07
- ID: `P1-T07`
- Title: Create error/manual review queue design
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `QA.md`, `DATABASE_SCHEMA.md`
- Output files: `QA.md`, `DATABASE_SCHEMA.md`, `ERRORS.md`
- Acceptance criteria:
  - Hata ve manuel inceleme kuyrugu durumlari ile gecisleri tanimli olmali.
- Risk notes: Validation eksigi yanlis yayin riskine yol acar.
- Next task: `P1-T08`

### Task P1-T08
- ID: `P1-T08`
- Title: Create daily pipeline command plan
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `AUTOMATION.md`, `BUILD_TEST_FIX.md`
- Output files: `AUTOMATION.md`, `BUILD_TEST_FIX.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - Gunluk komut akisi, manuel onay duragi ve retry politikasi yazili olmali.
- Risk notes: Otomatik gonderim erken baglanmamali.
- Next task: `P1-T09`

### Task P1-T09
- ID: `P1-T09`
- Title: Create Telegram progress notification design
- Phase: `Phase 1`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `TELEGRAM_INTEGRATION.md`, `SECURITY.md`, `COMPLIANCE.md`
- Output files: `TELEGRAM_INTEGRATION.md`, `PROJECT_MEMORY.md`
- Acceptance criteria:
  - Progress, error ve manual approval mesaj siniflari tanimli olmali.
  - Secret kullanimi sadece environment variable uzerinden tarif edilmeli.
  - Public auto-send yerine private/manual-safe akis belirtilmeli.
- Risk notes: Yanlis hedef chat veya secrets sizmasi kritik risktir.
- Next task: `P2-T01`

## Phase 2 - Multi-Broker Consensus
### Task P2-T01
- ID: `P2-T01`
- Title: Add Is Yatirim source design
- Phase: `Phase 2`
- Status: `DONE`
- Estimated sprint count: `1`
- Input files: `DATA_SOURCES.md`, `docs/templates/source_adapter_template.md`
- Output files: `DATA_SOURCES.md`
- Acceptance criteria: Is Yatirim kaynagi tasarimi eklenmis olmali.
- Risk notes: Format ve erisim belirsiz olabilir.
- Next task: `P2-T02`

## Phase 3 - KAP + Technical + Risk Filters
### Task P3-T01
- ID: `P3-T01`
- Title: Add KAP catalyst taxonomy
- Phase: `Phase 3`
- Status: `TODO`
- Estimated sprint count: `1`
- Input files: `KAP_CATALYSTS.md`
- Output files: `KAP_CATALYSTS.md`
- Acceptance criteria: KAP olay taksonomisi yazili olmali.
- Risk notes: Yanlis siniflama gurultu yaratir.
- Next task: `P3-T02`

## Phase 4 - Backtesting + Broker Track Record
### Task P4-T01
- ID: `P4-T01`
- Title: Create backtest data model
- Phase: `Phase 4`
- Status: `TODO`
- Estimated sprint count: `1`
- Input files: `BACKTESTING.md`, `DATABASE_SCHEMA.md`
- Output files: `BACKTESTING.md`, `DATABASE_SCHEMA.md`
- Acceptance criteria: Backtest veri modeli ve bias uyarilari tanimli olmali.
- Risk notes: Lookahead bias kritik risk.
- Next task: `P4-T02`

## Phase 5 - Productization
### Task P5-T01
- ID: `P5-T01`
- Title: PostgreSQL/Supabase migration plan
- Phase: `Phase 5`
- Status: `TODO`
- Estimated sprint count: `1`
- Input files: `ARCHITECTURE.md`, `DATABASE_SCHEMA.md`
- Output files: `ARCHITECTURE.md`
- Acceptance criteria: Gecis stratejisi ve veri tasima adimlari yazili olmali.
- Risk notes: MVP karmasikligi erken artmamali.
- Next task: `P5-T02`
