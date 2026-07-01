# DATA_SOURCES

## Purpose
Veri kaynaklarinin erisim, risk ve parsing acisindan resmi katalogu.

## When to read this file
Yeni kaynak eklerken, adapter tasarlarken ve compliance riski degerlendirirken.

## What it controls
Kaynak onceligi, erisim varsayimlari, gerekli alanlar ve ToS sinirlari.

## What it must not contain
Yetkisiz scraping talimati, credential, calisan parser kodu.

## Related files
`PARSING_RULES.md`, `COMPLIANCE.md`, `docs/source_adapters/oyak_valuation_table.md`

## Update rules
Her yeni kaynak veya format degisikliginde guncellenir.

## Last updated
2026-06-30

## Global rule
Login-protected, ucretli veya yetki gerektiren veriler; kullanici yasal erisim ve acik konfigurasyon saglamadan scrape edilmez veya otomatik islenmez.

## Source catalog

### OYAK Yatirim valuation table
- Source name: `OYAK Yatirim valuation table`
- Type: `PDF or HTML bulletin/table`
- Access method: Kamuya acik web sayfasi veya indirilebilir gunluk rapor baglantisi varsayimi; canli entegrasyon oncesi manuel URL dogrulamasi gerekir.
- Authentication requirement: `None assumed for MVP`
- Parsing difficulty: `Medium-High`
- Reliability: `High if official source file is archived with hash`
- Update frequency: `Daily or report-driven`
- Legal/ToS risk: `Medium` - resmi yayin kullanim kosullari canli entegrasyon oncesi kontrol edilmeli.
- Required fields:
  - `ticker`
  - `company_name`
  - `broker`
  - `report_date`
  - `recommendation_raw`
  - `target_price`
  - `current_price_reported`
  - `upside_reported`
  - `currency`
  - `source_url`
  - `source_file_hash`
- MVP priority: `P0`
- Adapter notes:
  - Her dosya once raw archive alanina kaydedilmeli.
  - SHA-256 hash uretilmeli.
  - Ayni hash tekrar geldiyse duplicate olarak isaretlenmeli.
  - Tablo yapisi degisirse parser degil once adapter alarm uretmeli.

### Is Yatirim takip listesi
- Source name: `Is Yatirim takip listesi`
- Type: `HTML/PDF/XLSX bulletin`
- Access method: Kamuya acik arastirma veya takip listesi sayfasi uzerinden HTML tablo ya da indirilebilir dokuman varsayimi; canli entegrasyon oncesi resmi URL pattern dogrulanmali.
- Authentication requirement: `None assumed for public research pages`
- Parsing difficulty: `Medium`
- Reliability: `Medium-High if official page and file hash are archived`
- Update frequency: `Daily or report-driven`
- Legal/ToS risk: `Medium` - resmi yayin ve kullanim kosullari canli entegrasyon oncesi kontrol edilmeli.
- Required fields:
  - `ticker`
  - `company_name`
  - `broker`
  - `report_date`
  - `recommendation_raw`
  - `recommendation_normalized`
  - `target_price`
  - `current_price_reported`
  - `upside_reported`
  - `currency`
  - `source_url`
  - `source_file_hash`
- MVP priority: `P2`
- Adapter notes:
  - Public research page veya indirilen belge once raw archive alanina yazilmali.
  - HTML tablo varsa canonical kolon map'i ile parse edilmeli; belge linki varsa OYAK benzeri hash/fingerprint akisi izlenmeli.
  - Is Yatirim tavsiye siniflari OYAK ile birebir eslesmeyebilir; normalize sozlugu broker-bazli tutulmali.
  - Ayni gun icindeki farkli takip listesi varyantlari duplicate degil revision olarak ele alinmali.

### Ak Yatirim model portfoy
- Source name: `Ak Yatirim model portfoy`
- Type: `PDF/HTML/XLSX bulletin`
- Access method: Kamuya acik model portfoy veya arastirma sayfasindan HTML icerik ya da indirilebilir dosya varsayimi; canli entegrasyon oncesi resmi URL pattern dogrulanmali.
- Authentication requirement: `None assumed for public research pages`
- Parsing difficulty: `Medium`
- Reliability: `Medium-High if official page and file hash are archived`
- Update frequency: `Weekly or report-driven`
- Legal/ToS risk: `Medium` - resmi yayin ve kullanim kosullari canli entegrasyon oncesi kontrol edilmeli.
- Required fields:
  - `ticker`
  - `company_name`
  - `broker`
  - `report_date`
  - `recommendation_raw`
  - `recommendation_normalized`
  - `target_price`
  - `current_price_reported`
  - `upside_reported`
  - `currency`
  - `source_url`
  - `source_file_hash`
- MVP priority: `P2`
- Adapter notes:
  - Model portfoy ve hedef fiyat tablosu ayni kavram degil; `source_subtype` metadata'da tutulmali.
  - PDF/XLSX varyanti varsa hash/fingerprint akisi OYAK ile uyumlu olmali.
  - Tavsiye terimleri broker-bazli normalize edilmeli; model portfoy girisi hedef fiyat icermiyorsa consensus hattina dogrudan degil yardimci sinyal olarak alinmali.
  - Ayni tarihli farkli belge varyantlari duplicate degil revision/layout-change olarak isaretlenmeli.
