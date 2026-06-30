# TELEGRAM_INTEGRATION

## Purpose
Proje gelismeleri, pipeline ozetleri ve manuel onay kuyrugu mesajlari icin Telegram entegrasyon sinirlarini tanimlar.

## When to read this file
Telegram bildirimi, approval queue veya ilerleme raporu akisi tasarlanirken.

## What it controls
Mesaj turleri, gonderim kurallari, secret gereksinimleri ve compliance sinirlari.

## What it must not contain
Bot token, chat ID, canli webhook URL, otomatik al/sat dili.

## Related files
`CONFIGURATION.md`, `COMPLIANCE.md`, `SECURITY.md`, `TELEGRAM_FORMAT.md`, `PROJECT_MEMORY.md`

## Update rules
Telegram kapsami veya approval modeli degistikce guncellenir.

## Last updated
2026-06-30

## Integration scope
- `Progress updates`: sprint tamamlandi, blocker olustu, manuel review bekliyor
- `Daily bulletin draft`: sadece manuel onay kuyruguna yazilir
- `Error alerts`: parser failure, source unavailable, empty artifact

## Hard rules
- Canli gonderim `TELEGRAM_ENABLED=true` olmadan acilmaz.
- Bot token ve chat ID `process env`, `.env.local` veya `.env` uzerinden saglanir; repo icine hardcode edilmez.
- Development sirasinda otomatik public kanal yayini acilmaz.
- Uyum metni olmayan hicbir piyasa ozeti gonderilmez.
- Hatali veya validation'dan gecmemis parser ciktilari Telegram'a gitmez.

## Required environment variables
- `TELEGRAM_ENABLED`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TELEGRAM_PROGRESS_THREAD_ID`
- `TELEGRAM_PARSE_MODE`

## Current configured target
- Default test group chat ID: `-5434687426`
- Bot token repo icine yazilmaz; universal config standardi `CONFIGURATION.md` icinde tanimlidir.

## Universal config note
Telegram entegrasyonu shell-spesifik komutlara bagli degildir. Gelecekteki tum notifier ve worker kodlari `CONFIGURATION.md` icindeki precedence kurali ile config okumak zorundadir.

## Message classes
### Progress message
- Kullanim: sprint sonu veya sistem ilerleme bildirimi
- Icerik:
  - sprint ID
  - degisen dosyalar
  - sonraki gorev ID
  - blocker varsa nedeni

### Manual approval draft
- Kullanim: yayin oncesi taslak kontrol
- Icerik:
  - kaynak sayisi
  - tarih
  - ozet bulgular
  - zorunlu disclaimer

### Error alert
- Kullanim: parser/source failure
- Icerik:
  - hata tipi
  - source
  - run timestamp
  - manual review gerekip gerekmedigi

## Delivery modes
- `DRY_RUN`: mesaj gonderilmez, sadece stdout/log/queue preview uretilir
- `PRIVATE_TEST`: mesaj sadece test grup veya topic'e gider
- `APPROVAL_QUEUE_ONLY`: Telegram'a gonderim yok, sadece `08_TELEGRAM_QUEUE` tabina taslak yazar
- `APPROVED_SEND`: yalnizca `approval_status=APPROVED` olan queue item gonderilir

## Progress notification contract
Progress mesajlari su minimum alanlari icermelidir:
- `run_id` veya `sprint_id`
- `status`
- `changed_files_count`
- `next_task_id`
- `timestamp`

## Error notification contract
Error mesajlari su minimum alanlari icermelidir:
- `error_code`
- `source_name`
- `severity`
- `requires_manual_review`
- `timestamp`

## Manual approval draft contract
Taslak queue item su minimum alanlari icermelidir:
- `queue_id`
- `queue_date`
- `message_body_markdown`
- `approval_status=PENDING`
- `compliance_check_status`
- `source_count`

## Security and rate limits
- Token loglanmaz
- Telegram API response body secret icerebilecegi varsayimiyla sanitize edilir
- Ayni queue item iki kez gonderilmeden once sent-log kontrol edilir
- Retry limiti `1`'dir; tekrarli hata manual incelemeye gider

## Recommended implementation order
1. Secret-safe config loading
2. Dry-run notifier
3. Progress message sender
4. Manual approval queue sender
5. Error alert sender
6. Rate limit ve retry guard

## Initial recommendation
Ilk adimda yalnizca private test chat veya topic kullanilsin. Tum gelismeleri anlik gondermek yerine sprint sonu ve hata odakli ozet gondermek daha izlenebilir ve daha ucuzdur.
