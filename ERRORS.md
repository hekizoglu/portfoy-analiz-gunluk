# ERRORS

## Purpose
Teknik ve operasyonel hata kayitlari icin standart format.

## When to read this file
Yeni hata eklerken, kok neden analizi yaparken veya tekrar eden sorunlari gozden gecirirken.

## What it controls
Hata kayit sablonu, durum takibi ve prevention notlari.

## What it must not contain
Gercek secret, gereksiz stack dump coplugu.

## Related files
`QA.md`, `BUILD_TEST_FIX.md`, `PARSING_RULES.md`

## Update rules
Anlamli yeni hata turlerinde yeni kayit eklenir; mevcut kayit silinmez.

## Last updated
2026-06-30

## Error template
- Error:
- Environment:
- Symptoms:
- Root cause:
- Fix:
- Prevention:
- Related files:
- Status:

## Known initial errors
- Error: `PARSER_EMPTY_OUTPUT`
- Environment: `MVP pipeline`
- Symptoms: `Raw report mevcut ancak valid satir cikmiyor`
- Root cause: `PDF tablo ayrimi veya kolon esleme basarisiz`
- Fix: `Parser kuralini guncelle, queue item olustur`
- Prevention: `Kolon varyasyon sozlugu ve sample regression testi`
- Related files: `PARSING_RULES.md`, `QA.md`
- Status: `OPEN_TEMPLATE`

- Error: `TELEGRAM_HTTP_401_UNAUTHORIZED`
- Environment: `Local loop / Telegram send`
- Symptoms: `sendMessage cagrisi HTTP 401 donuyor ve mesaj gitmiyor`
- Root cause: `Bot token gecersiz, iptal edilmis veya yanlis`
- Fix: `BotFather uzerinden yeni token olustur, .env.local veya repo secret'i guncelle`
- Prevention: `Expose olan tokenlari rotate et; send loop'ta auth failure status'u yakala`
- Related files: `scripts/run_cycle.py`, `app/telegram_client.py`, `TELEGRAM_INTEGRATION.md`
- Status: `OPEN`
