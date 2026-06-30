# OYAK Valuation Table Source Adapter

## Purpose
OYAK Yatirim degerleme tablosu kaynagini MVP icin guvenli ve izlenebilir sekilde sisteme alma tasarimi.

## When to read this file
OYAK kaynak entegrasyonu, parser tasarimi veya source validation kurallari yazilirken.

## What it controls
Adapter siniri, beklenen raw artifact yapisi, metadata zorunluluklari, diff/fingerprint akisi ve hata yonetimi.

## What it must not contain
Canli scraping kodu, credential, dogrulanmamis URL listesi, yatirim tavsiyesi dili.

## Related files
`DATA_SOURCES.md`, `PARSING_RULES.md`, `DATABASE_SCHEMA.md`, `COMPLIANCE.md`

## Update rules
Canli kaynak formati dogrulandiginda ve her buyuk format degisiminde guncellenir.

## Last updated
2026-06-30

## Adapter objective
OYAK tarafindan yayinlanan degerleme icerigini once ham belge olarak arsivlemek, sonra normalize edilebilir satirlara donusturmek ve dogrulanamayan her durumda yayin hattini durdurmak.

## Business boundary
- Bu adapter sadece kaynak alma ve ham metadata uretme sorumlulugunu tasir.
- Tavsiye normallestirme, scoring ve Telegram formatlama bu adapterin disindadir.
- Adapter, yetkisiz veya login gerektiren erisim akisi varsaymaz.

## Assumed source forms
- Birincil varsayim: gunluk veya periyodik degerleme tablosu PDF yayini
- Ikincil varsayim: resmi web sayfasinda HTML tablo veya PDF linki
- Alternatif: XLS/XLSX eki olan rapor linki

## Required adapter inputs
- `source_name`: `OYAK Yatirim valuation table`
- `run_date`
- `discovery_url` veya manuel saglanan belge URL'si
- `allowed_access_mode`: `public_web_only`

## Required adapter outputs
- `raw_artifact_path`
- `source_url`
- `download_timestamp`
- `content_type`
- `source_file_hash_sha256`
- `source_fingerprint_key`
- `report_date_detected`
- `adapter_status`
- `adapter_notes`

## Field extraction candidates for parser handoff
Parser asamasina asagidaki aday alanlar iletilir:
- `ticker`
- `company_name`
- `sector`
- `recommendation_raw`
- `target_price`
- `current_price_reported`
- `upside_reported`
- `currency`
- `report_date`
- `broker`

## Acquisition flow
1. Kaynak URL veya belge linki public-web kuralina gore dogrulanir.
2. Icerik indirilmeden once URL ve erisim zamani kaydedilir.
3. Belge binary olarak arsivlenir; ham dosya degistirilmez.
4. SHA-256 hash uretilir.
5. `source_name + report_date_detected + source_file_hash_sha256` ile fingerprint anahtari uretilir.
6. Onceki fingerprint ile karsilastirilir.
7. Yeni fingerprint ise parser kuyruguna verilir; ayni fingerprint ise duplicate/no-change olarak isaretlenir.

## Diff and fingerprint strategy
- Birincil duplicate kontroli: tam dosya hash eslesmesi
- Ikincil degisim kontroli: normalize metin tablo imzasi
- Ayni tarihte farkli hash gelirse `format_or_content_changed` olayi olusturulur
- Format degisikligi parsera gecmeden once review gerektirir

## Failure handling
- URL erisilemiyorsa: `adapter_status = SOURCE_UNAVAILABLE`
- Icerik bos veya cok kisa ise: `adapter_status = EMPTY_ARTIFACT`
- Content type beklenmeyense: `adapter_status = UNSUPPORTED_FORMAT`
- Report date tespit edilemiyorsa: `adapter_status = NEEDS_MANUAL_REVIEW`
- Hash uretilemezse: `adapter_status = INTEGRITY_FAILURE`

Bu durumlarin hicbirinde Telegram kuyruguna veri gitmez.

## Manual review triggers
- Bir dosyada birden fazla tablo varyanti varsa
- Ticker kolonlari acik degilse
- Hedef fiyat para birimi belirsizse
- Tavsiye metni tablo disi notlarla karismissa
- Ayni gun icinde birbirini tutmayan iki resmi dosya tespit edilirse

## Compliance guardrails
- Yalnizca resmi veya kullanicinin yasal erisim sagladigi kaynaklar kullanilir.
- Kaynak dogrulanmadan veya hashlenmeden parser ve scoring baslamaz.
- Adapter hicbir sekilde al/sat dili uretmez.

## Open questions
- OYAK resmi yayin formatinin MVP'de PDF mi HTML mi oldugu canli dogrulama ile netlestirilecek.
- Raporda sektor ve para birimi alanlari her zaman acik mi, degil mi kontrol edilecek.
