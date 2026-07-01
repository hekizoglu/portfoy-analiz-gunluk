# Ak Yatirim Model Portfoy Source Adapter

## Purpose
Ak Yatirim model portfoy veya benzer arastirma tablosunu coklu kurum veri hattina kontrollu sekilde dahil etmek icin adapter tasarimi.

## When to read this file
Ak Yatirim kaynak entegrasyonu, parser genisletmesi veya consensus yardimci-sinyal mantigi yazilirken.

## What it controls
Raw artifact toplama, beklenen formatlar, metadata zorunluluklari, subtype ayrimi ve manual review kurallari.

## What it must not contain
Canli scrape kodu, credential, validation'siz publish varsayimi.

## Related files
`DATA_SOURCES.md`, `PARSING_RULES.md`, `docs/templates/source_adapter_template.md`, `DATABASE_SCHEMA.md`

## Update rules
Canli kaynak formati dogrulandiginda ve yayin yapisi degistikce guncellenir.

## Last updated
2026-07-01

## Business purpose
OYAK ve Is Yatirim sonrasinda ucuncu broker sinyalini ekleyerek tek kurum yanlis pozitiflerini azaltmak ve ileride broker count / divergence hesaplarini guclendirmek.

## Assumed access path
- Birincil varsayim: kamuya acik model portfoy veya arastirma web sayfasi
- Ikincil varsayim: PDF veya XLSX dosyasi
- Alternatif: HTML icerisinde tablo veya kart yapisi

## Allowed acquisition method
- Public web page fetch
- Public document download
- Kullanici tarafindan saglanan manuel belge

## Raw artifact types
- `text/html`
- `application/pdf`
- `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

## Required metadata
- `source_name = Ak Yatirim model portfoy`
- `source_url`
- `download_timestamp`
- `content_type`
- `report_date_detected`
- `source_file_hash_sha256`
- `source_fingerprint_key`
- `source_subtype`

## Extraction candidates
- `ticker`
- `company_name`
- `recommendation_raw`
- `target_price` optional
- `current_price_reported` optional
- `upside_reported` optional
- `weighting_signal` optional
- `report_date`
- `broker`

## Source subtype rule
- `MODEL_PORTFOLIO`: hedef fiyat icermese bile tercih/sinyal kaydi olarak tutulur
- `VALUATION_TABLE`: hedef fiyatli ve consensus hattina uygun
- `THEMATIC_LIST`: yalnizca yardimci sinyal olarak tutulur

## Normalization notes
- `AL`, `TUT`, `SAT`, `Endeks Uzeri`, `Endekse Paralel`, `Endeks Alti` gibi varyantlar beklenir
- Hedef fiyat yoksa kayit consensus yerine auxiliary signal olarak etiketlenir
- Hedef fiyat ve tavsiye ayni tabloda degilse satir birlestirme yalnizca kaynak netse yapilir

## Hash/fingerprint strategy
- Birincil duplicate kontrolu tam dosya hash'i
- Ikincil kontrol `source_name + report_date + source_subtype + normalized table signature`
- Ayni tarihte farkli hash revision veya layout-change olarak isaretlenir

## Failure modes
- `SOURCE_UNAVAILABLE`
- `EMPTY_ARTIFACT`
- `UNSUPPORTED_FORMAT`
- `NEEDS_MANUAL_REVIEW`
- `INTEGRITY_FAILURE`

## Manual review triggers
- Kayit valuation mi model portfoy mu net degilse
- Hedef fiyat kolonlari tutarsizsa
- Tavsiye normalize edilemiyorsa
- HTML tabloda kart bazli layout parse'i bozulmussa

## Open questions
- Resmi yayin frekansi gunluk mu haftalik mi
- Model portfoy disinda ayri valuation PDF'i var mi
- Hedef fiyat icermeyen listeler scoring'e nasil agirlik verecek
