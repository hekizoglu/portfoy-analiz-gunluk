# PARSING_RULES

## Purpose
Ham broker raporlarindan yapisal veri cikarimi, dogrulama ve manual review akisini tanimlar.

## When to read this file
Yeni parser tasarlarken, extraction hatasi incelerken veya schema validation degisimi yaparken.

## What it controls
PDF/HTML/XLS/email parsing stratejileri, LLM destekli extraction sinirlari, confidence score ve publish guard kurallari.

## What it must not contain
Uydurma veri, validation'siz parser kabulleri, secret veya canli credential.

## Related files
`docs/source_adapters/oyak_valuation_table.md`, `DATABASE_SCHEMA.md`, `QA.md`, `TELEGRAM_INTEGRATION.md`

## Update rules
Her yeni kaynak sinifi, parser failure paterni veya validation kurali degisiminde guncellenir.

## Last updated
2026-06-30

## Parsing principles
- Parser ham artifact'i degistirmez; yalnizca kopya uzerinde calisir.
- Extraction ile normalization ayridir.
- Validation gecmeyen hicbir veri scoring veya Telegram kuyruguna gitmez.
- OYAK adapterinden gelen metadata parser icin zorunlu context'tir.

## OYAK PDF parsing flow
1. Adapter `raw_artifact_path`, `source_file_hash_sha256`, `report_date_detected`, `content_type` uretir.
2. PDF ise once text-layer kontrolu yapilir.
3. Text-layer varsa tablo satirlari ve dipnotlar ayristirilir.
4. Text-layer yoksa OCR gereksinimi `manual_review_required` olarak isaretlenir; MVP'de otomatik OCR zorunlu degildir.
5. Tablo bloklari kolon basliklarina gore aday satirlara bolunur.
6. Her aday satir broker valuation JSON adayina donusturulur.
7. JSON schema validation uygulanir.
8. Validation gecen satirlar normalize kuyruguna gider.
9. Validation gecmeyen satirlar `manual_review_queue`'ya gider.

## PDF extraction strategy
- Birincil hedef: secilebilir text iceren PDF
- Kolon tespiti icin baslik varyasyonlari desteklenir:
  - `Hisse`
  - `Sirket`
  - `Tavsiye`
  - `Hedef Fiyat`
  - `Getiri Potansiyeli`
  - `Son Fiyat`
- Satir birlestirme kurali: bir ticker baslayip sonraki ticker gelene kadar ayni kayda ait metin birlestirilebilir.
- Dipnotlar tablo satiri sanilmamali; ticker/desen eslesmesi olmayan satirlar ayiklanir.

## HTML parsing strategy
- Resmi sayfada yayimlanan tablolar DOM tabanli okunur.
- Script ile sonradan yuklenen veri varsa ham JSON response bulunmadan extraction yapilmaz.
- HTML tabloda kolon basliklari canonical alan isimlerine map edilir.

## XLS/XLSX parsing strategy
- Ilk sheet veya naming pattern ile degerleme tablosu secilir.
- Formul sonuc degerleri okunur, formul metni yayina tasinmaz.
- Bos satirlar, toplam satirlari ve aciklama bloklari veri olarak alinmaz.

## Email attachment parsing strategy
- Sadece kullanicinin yasal yetkilendirdigi mailbox kullanilir.
- Attachment once raw artifact olarak hashlenir.
- Dosya tipi attachment metadata ve mime-type ile dogrulanir.

## LLM-assisted JSON extraction
- LLM yalnizca zor satir birlestirme, kolon hizalama veya bozuk PDF text temizleme asamasinda yardimci olabilir.
- LLM ciktilari her zaman strict JSON schema validation'dan gecmek zorundadir.
- LLM'e ham belge yerine mumkun olan en dar tablo parcasi verilir.
- LLM confidence ve rule-based confidence ayri tutulur.

## Strict JSON schema validation
Asagidaki alanlar zorunludur:
- `ticker`
- `company_name`
- `broker`
- `report_date`
- `recommendation_raw`
- `recommendation_normalized`
- `target_price`
- `current_price_reported`
- `source_url`
- `confidence_score`
- `validation_status`

Validation kurallari:
- `ticker` buyuk harf, 3-5 karakter ve BIST sembol kurallariyla uyumlu olmali
- `report_date` ISO `YYYY-MM-DD` olmali
- `target_price` ve `current_price_reported` pozitif sayi olmali
- `confidence_score` 0 ile 1 arasinda olmali
- `validation_status` yalnizca `VALID`, `INVALID`, `MANUAL_REVIEW`

## Field normalization rules
- `recommendation_raw` kaynak metindir; degistirilmez
- `recommendation_normalized` kontrollu sozlukten gelir: `BUY`, `HOLD`, `SELL`, `OUTPERFORM`, `UNDERPERFORM`, `NEUTRAL`
- Para birimi yoksa `TRY` varsayma; `MANUAL_REVIEW` isaretle
- Yuzde alanlari `numeric_percent` olarak saklanir, `%` sembolu tutulmaz

## Confidence score model
Toplam score 0-1 araligindadir ve su sinyallerle hesaplanir:
- +0.30 zorunlu kolonlar net bulundu
- +0.20 ticker regex eslesti
- +0.20 fiyat alanlari parse edildi
- +0.10 tavsiye sozluk eslesmesi bulundu
- +0.10 report date dogrulandi
- +0.10 kaynak hash ve metadata tam

Su durumlarda puan dusurulur:
- -0.25 tablo satiri birlestirme belirsiz
- -0.20 para birimi eksik
- -0.20 OCR gerekli
- -0.15 birden fazla hedef fiyat adayi var

## Manual review rules
Asagidaki durumlar otomatik olarak manual review'a gider:
- Confidence score `< 0.85`
- Para birimi belirsiz
- Ticker veya company name eksik
- Tavsiye normalize edilemiyor
- Ayni ticker icin ayni belgede celisen iki hedef fiyat var
- OCR gerektiren PDF

## Hash/fingerprint tracking
- Her parser calismasi `source_file_hash_sha256` ile iliskilendirilir
- Ayni hash uzerinde ayni parser version tekrar kosarsa duplicate run olarak isaretlenir
- Farkli hash ama ayni report_date gelirse content revision olarak tutulur

## Parser failure handling
- Extraction crash: `PARSER_RUNTIME_FAILURE`
- Bos satir uretimi: `PARSER_EMPTY_OUTPUT`
- Schema mismatch: `PARSER_SCHEMA_FAILURE`
- Encoding sorunu: `PARSER_ENCODING_FAILURE`
- Format belirsizligi: `PARSER_UNSUPPORTED_LAYOUT`

Bu durumlar `ERRORS.md` ve `manual_review_queue` icin aday olay uretir.

## Publish guard
- `validation_status != VALID` ise Telegram kuyruguna cikamaz
- `source_url` veya `source_file_hash_sha256` eksikse publish bloklanir
- Compliance disclaimer eklenmemis mesaja publish izni verilmez
