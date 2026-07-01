# CONFIGURATION

## Purpose
Proje genelinde shell ve ortamdan bagimsiz konfigurasyon standardini tanimlar.

## When to read this file
Yeni entegrasyon eklerken, local ortam kurarken veya CI/CD konfigurasyonu yaparken.

## What it controls
Config kaynaklari, oncelik sirasi, secret yonetimi ve environment variable isimleri.

## What it must not contain
Gercek token, sifre, private key veya ortam spesifik hassas veri.

## Related files
`.env.example`, `.gitignore`, `TELEGRAM_INTEGRATION.md`, `SECURITY.md`, `PROJECT_MEMORY.md`

## Update rules
Yeni config gruplari veya secret politikasi degistikce guncellenir.

## Last updated
2026-06-30

## Universal configuration standard
Bu projede konfigurasyon shell komutlarina bagli olmayacak. Ana standart repo kokundeki `.env` dosyasidir.

## Source precedence
Konfigurasyon okuma sirasi asagidaki gibi olmalidir:
1. Process environment variables
2. Repo-local `.env.local`
3. Repo-local `.env`
4. `.env.example` sadece referans dokumani olarak kullanilir

Bu sayede:
- Local developer kendi `.env.local` degerleriyle calisabilir
- CI sistemi dogrudan environment variable verebilir
- Repo ortak defaultlari `.env` veya `.env.example` uzerinden dokumante eder

## Required Telegram keys
- `TELEGRAM_ENABLED`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TELEGRAM_PROGRESS_THREAD_ID`
- `TELEGRAM_PARSE_MODE`
- `TELEGRAM_DELIVERY_MODE`

## Required AI task runner keys
- `AI_TASK_RUNNER_PROVIDER`
- `AI_TASK_RUNNER_API_KEY`
- `AI_TASK_RUNNER_BASE_URL`
- `AI_TASK_RUNNER_MODEL`
- `AI_TASK_RUNNER_TEMPERATURE`
- `AI_SECONDARY_ENABLED`
- `AI_SECONDARY_PROVIDER`
- `AI_SECONDARY_API_KEY`
- `AI_SECONDARY_BASE_URL`
- `AI_SECONDARY_MODEL`
- `AI_SECONDARY_TEMPERATURE`
- `DEEPSEEK_OFFPEAK_ONLY`
- `DEEPSEEK_TIMEZONE`

## Repository rule
- `.env` ve `.env.local` git'e eklenmez
- Gercek token sadece local environment veya secret manager'da tutulur
- Repo icinde yalnizca `.env.example` paylasilir

## Cross-platform setup examples
### Recommended
Repo kokunde `.env` veya `.env.local` olustur:

```dotenv
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=REPLACE_WITH_REAL_TOKEN
TELEGRAM_CHAT_ID=-5434687426
TELEGRAM_PROGRESS_THREAD_ID=
TELEGRAM_PARSE_MODE=Markdown
TELEGRAM_DELIVERY_MODE=APPROVAL_QUEUE_ONLY
AI_TASK_RUNNER_PROVIDER=deepseek
AI_TASK_RUNNER_API_KEY=REPLACE_WITH_REAL_TOKEN
AI_TASK_RUNNER_BASE_URL=https://api.deepseek.com
AI_TASK_RUNNER_MODEL=deepseek-chat
AI_TASK_RUNNER_TEMPERATURE=0.1
AI_SECONDARY_ENABLED=true
AI_SECONDARY_PROVIDER=
AI_SECONDARY_API_KEY=
AI_SECONDARY_BASE_URL=
AI_SECONDARY_MODEL=
AI_SECONDARY_TEMPERATURE=0.0
DEEPSEEK_OFFPEAK_ONLY=true
DEEPSEEK_TIMEZONE=Europe/Istanbul
```

### Temporary PowerShell override
```powershell
$env:TELEGRAM_ENABLED="true"
$env:TELEGRAM_BOT_TOKEN="REPLACE_WITH_REAL_TOKEN"
$env:TELEGRAM_CHAT_ID="-5434687426"
```

### Temporary bash override
```bash
export TELEGRAM_ENABLED=true
export TELEGRAM_BOT_TOKEN="REPLACE_WITH_REAL_TOKEN"
export TELEGRAM_CHAT_ID="-5434687426"
```

### Temporary cmd override
```cmd
set TELEGRAM_ENABLED=true
set TELEGRAM_BOT_TOKEN=REPLACE_WITH_REAL_TOKEN
set TELEGRAM_CHAT_ID=-5434687426
```

## Loader contract for future application code
Gelecekte eklenecek tum runtime kodlari su kurala uymalidir:
- Once process env oku
- Sonra varsa `.env.local` oku
- Sonra varsa `.env` oku
- Eksik zorunlu alan varsa fail-fast yap
- Secret degerleri loglama

## DeepSeek pricing window rule
Kullanici tarafindan verilen fiyat bilgisine gore DeepSeek peak saatleri Türkiye saatiyle `04:00-07:00` ve `09:00-13:00` araligidir.

Bu repo icinde:
- `DEEPSEEK_OFFPEAK_ONLY=true` ise AI task-runner bu saatlerde calismaz
- Off-peak saatler: `00:00-03:59`, `07:00-08:59`, `13:00-23:59`
- Zaman dilimi `DEEPSEEK_TIMEZONE=Europe/Istanbul` olarak kabul edilir

## Fail-fast rules
- `TELEGRAM_ENABLED=true` ise `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` zorunludur
- Token veya chat ID eksikse gonderim denenmez
- Invalid config durumlari `ERRORS.md` veya run log'una yazilmalidir
