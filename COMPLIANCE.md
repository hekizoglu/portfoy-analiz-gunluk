# COMPLIANCE

## Purpose
Urunun arastirma/izleme sistemi olarak kalmasi ve yatirim tavsiyesi riskinden uzak durmasi icin zorunlu uyum kurallarini tanimlar.

## When to read this file
Telegram mesaji, scoring yorumu, urun metni veya rapor dili degisirken.

## What it controls
Yasakli dil, gerekli disclaimer, source transparency ve publish blocker kurallari.

## What it must not contain
Yatirim tavsiyesi niteliginde metin, kisiyey ozel portfoy yonlendirmesi.

## Related files
`TELEGRAM_FORMAT.md`, `SCORING.md`, `REVIEW.md`, `TELEGRAM_INTEGRATION.md`

## Update rules
Uyum riski veya yayin dili kurallari degistikce guncellenir.

## Last updated
2026-06-30

## Hard rules
- Bu urun yatirim tavsiyesi vermez.
- Kisiye ozel portfoy onerisi, alim/satim talimati veya garantili getiri dili kullanilmaz.
- Düsük likiditeli hisseler manipule edici tonla one cikarilmaz.
- Dogrulanmamis kaynak veya validation'dan gecmemis veri publish edilmez.

## Required disclaimer
`Bu icerik yatirim tavsiyesi degildir. Otomatik veri analizi ve genel piyasa taramasidir. Nihai karar kullaniciya aittir.`

## Approved wording
- `izleme adayi`
- `radara giren hisse`
- `kurum raporlarina gore one cikan`
- `konsensusten pozitif ayrisan`
- `manuel kontrol gerektirir`

## Forbidden wording
- `kesin al`
- `garantili`
- `tavan adayi`
- `kacirma`
- `VIP sinyal`
- `simdi al`
- `simdi sat`

## Publish blockers
- Disclaimer yoksa
- Validation status `VALID` degilse
- Source URL veya report date eksikse
- Manuel review gerekli olup approval alinmadiysa
