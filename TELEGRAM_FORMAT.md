# TELEGRAM_FORMAT

## Purpose
Gunluk Telegram bulteninin yapisini, zorunlu compliance metinlerini ve manuel onay akisini tanimlar.

## When to read this file
Gunluk rapor taslagi uretirken, message template degistirirken veya approval queue olustururken.

## What it controls
Mesaj bolumleri, risk etiketleri, forbidden wording, source/date gosterimi ve approval formatini.

## What it must not contain
Al/sat talimati, garantili getiri tonu, validation'siz publish metni.

## Related files
`COMPLIANCE.md`, `SCORING.md`, `TELEGRAM_INTEGRATION.md`, `GOOGLE_SHEETS_SCHEMA.md`

## Update rules
Yayin dili veya approval modeli degistikce guncellenir.

## Last updated
2026-06-30

## Daily message structure
1. Baslik
2. Veri kapsami ozeti
3. One cikan izleme adaylari
4. Anomali / ayrisma uyarilari
5. Revizyon momentumu dikkat notlari
6. Manuel kontrol gerektirenler
7. Zorunlu disclaimer

## Header format
`Gunluk Degerleme Radari | YYYY-MM-DD | Taslak`

## Top candidates section
Her satir su blokta olmalidir:
- `Ticker`
- `Kurum sayisi`
- `Ortalama hedef fiyat`
- `Konsensuse gore durum`
- `FinalScore`
- `Risk etiketi`
- `Kaynak tarihi`

Ornek satir:
`THYAO | 4 kurum | Ortalama hedef: 128 TL | Konsensusten pozitif ayrisan | FinalScore: 78 | Risk: Manuel kontrol gerekir | Kaynak: 2026-06-30`

## Anomaly alerts section
Kullan:
- `Konsensusten %X pozitif ayrisan yeni rapor`
- `Konsensusten %X negatif ayrisan yeni rapor`
- `Yeni coverage tespit edildi`
- `Coverage kaldirildi, manuel kontrol gerekir`

## Revision momentum section
Kullan:
- `Son 30 gunde tekrar eden yukari yonlu hedef fiyat revizyonu`
- `Ardisik asagi yonlu revizyonlar dikkat gerektirir`

## Manual review section
Asagidaki siniflari goster:
- `Kaynak dogrulamasi eksik`
- `Para birimi belirsiz`
- `Tek kurum verisine dayaniyor`
- `Dusuk likidite nedeniyle manuel kontrol gerekir`

## Risk labels
- `MANUAL_CONTROL`
- `LOW_LIQUIDITY`
- `STALE_TARGET`
- `HIGH_DIVERGENCE`
- `SINGLE_BROKER`
- `SOURCE_CHECK_REQUIRED`

## Source/date display rules
- Her ana bulgu satirinda `Kaynak: YYYY-MM-DD` bulunur
- Mumkunse kurum adi da eklenir
- Source URL mesaj icinde zorunlu degil; queue metadata'da tutulur

## Forbidden words
- `kesin al`
- `garantili`
- `tavan adayi`
- `kacirma`
- `VIP sinyal`
- `simdi al`
- `simdi sat`

## Required disclaimer
`Bu icerik yatirim tavsiyesi degildir. Otomatik veri analizi ve genel piyasa taramasidir. Nihai karar kullaniciya aittir.`

## Manual approval queue format
Approval icin queue'ya su alanlar yazilir:
- `queue_id`
- `queue_date`
- `message_type`
- `message_body_markdown`
- `approval_status = PENDING`
- `compliance_check_status`
- `source_count`
- `approval_notes`

## Approval gates
- En az bir `VALID` source olmalı
- Disclaimer eklenmis olmali
- Forbidden wording kontrolu gecmeli
- `manual_review_required = true` olan satirlar ilgili bolumde acikca etiketlenmeli

## Example message
```markdown
Gunluk Degerleme Radari | 2026-06-30 | Taslak

Kapsam: 1 kurum raporu, 8 gecerli satir, 2 manuel kontrol kaydi.

One cikan izleme adaylari
- THYAO | 4 kurum | Ortalama hedef: 128 TL | Konsensusten pozitif ayrisan | FinalScore: 78 | Risk: MANUAL_CONTROL | Kaynak: 2026-06-30

Anomali / ayrisma uyarilari
- THYAO icin konsensusten %12 pozitif ayrisan yeni rapor, manuel kontrol gerekir.

Revizyon momentumu
- Son 30 gunde yukari yonlu hedef fiyat revizyon serisi izleniyor.

Manuel kontrol gerektirenler
- XYZAO | Tek kurum verisine dayaniyor | SOURCE_CHECK_REQUIRED

Bu icerik yatirim tavsiyesi degildir. Otomatik veri analizi ve genel piyasa taramasidir. Nihai karar kullaniciya aittir.
```
