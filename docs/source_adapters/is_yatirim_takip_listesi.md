# Is Yatirim Takip Listesi Source Adapter

## Purpose
Is Yatirim takip listesi veya arastirma tablosunu coklu kurum consensus hattina guvenli sekilde dahil etmek icin adapter tasarimi.

## When to read this file
Is Yatirim kaynak entegrasyonu, multi-broker parser genisletmesi veya recommendation normalization calismasi yapilirken.

## What it controls
Raw artifact toplama siniri, beklenen formatlar, metadata zorunluluklari, revision takibi ve manual review kurallari.

## What it must not contain
Canli scrape kodu, credential, yetkisiz erisim varsayimi veya validation'siz parser kabulu.

## Related files
`DATA_SOURCES.md`, `PARSING_RULES.md`, `docs/templates/source_adapter_template.md`, `DATABASE_SCHEMA.md`

## Update rules
Canli kaynak formati dogrulandiginda ve her buyuk yayin yapisi degisiminde guncellenir.

## Last updated
2026-06-30

## Business purpose
OYAK disinda ikinci broker kaynagini ekleyerek consensus, divergence ve broker count mantigi icin gerekli veri cesitliligini saglamak.

## Assumed access path
- Birincil varsayim: kamuya acik arastirma/takip listesi web sayfasi
- Ikincil varsayim: PDF veya XLSX ekli gunluk/haftalik takip listesi
- Alternatif: HTML tablo icinde dogrudan render edilen tavsiye listesi

## Allowed acquisition method
- Public web page fetch
- Public document download
- Kullanici tarafindan saglanan manuel belge

## Raw artifact types
- `text/html`
- `application/pdf`
- `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

## Required metadata
- `source_name = Is Yatirim takip listesi`
- `source_url`
- `download_timestamp`
- `content_type`
- `report_date_detected`
- `source_file_hash_sha256`
- `source_fingerprint_key`

## Extraction candidates
- `ticker`
- `company_name`
- `recommendation_raw`
- `target_price`
- `current_price_reported`
- `upside_reported`
- `report_date`
- `broker`
- `model_portfolio_flag` optional

## Normalization notes
- Tavsiye metinleri broker-ozel map ile normalize edilir
- `AL`, `TUT`, `SAT`, `END.USTU`, `END.PAR`, `END.ALTI` gibi varyantlar beklenir
- Hedef fiyat para birimi acik degilse `MANUAL_REVIEW`
- Takip listesi ve model portfoy ayni sey kabul edilmez; source subtype metadata'da tutulur

## Hash/fingerprint strategy
- Birincil duplicate kontrolu tam dosya hash'i
- Ikincil kontrol `source_name + report_date + normalized table signature`
- Ayni tarihte farkli hash varsa revision veya layout-change olarak isaretlenir

## Failure modes
- `SOURCE_UNAVAILABLE`
- `EMPTY_ARTIFACT`
- `UNSUPPORTED_FORMAT`
- `NEEDS_MANUAL_REVIEW`
- `INTEGRITY_FAILURE`

## Manual review triggers
- Tavsiye metni normalize edilemiyorsa
- Hedef fiyat ve cari fiyat ayni satirda ayrisamiyorsa
- HTML tabloda kolon basliklari degismisse
- XLSX sheet secimi belirsizse

## Open questions
- Resmi yayin pattern'i gunluk mu haftalik mi calisiyor
- Takip listesi ile model portfoy ayri adapter mi olmali
- Tavsiye terminolojisi OYAK'tan ne kadar farkli
