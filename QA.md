# QA

## Purpose
Parser, veri kalitesi, scoring ve Telegram yayin kalitesi icin zorunlu kalite guvencesi cercevesini tanimlar.

## When to read this file
Yeni veri hatti eklerken, publish oncesi kalite kontrol yaparken veya regression riski incelerken.

## What it controls
QA kontrol basliklari, queue gecis kurallari ve definition of done.

## What it must not contain
Belgesiz publish istisnalari, manuel kontrolu atlayan kisayollar.

## Related files
`PARSING_RULES.md`, `DATABASE_SCHEMA.md`, `TELEGRAM_FORMAT.md`, `BUILD_TEST_FIX.md`

## Update rules
Yeni QA kontrol sinifi veya hata paterni eklendikce guncellenir.

## Last updated
2026-06-30

## Parser QA
- Her raw report icin en az bir satir parse edilmis mi
- Confidence score dagilimi beklenen aralikta mi
- Validation status dagilimi anomalik mi
- Text layer olmayan PDF'ler otomatik manual review'a gitti mi

## Data validation QA
- `ticker`, `broker`, `report_date`, `target_price`, `source_url` zorunlu
- Duplicate hash tekrar veri olarak yayina cikmiyor mu
- Currency eksik kayitlar publish disi tutuluyor mu

## Scoring QA
- FinalScore 0-100 araliginda mi
- Negative penalty uygulamasi clamp mantigini bozmuyor mu
- Tek broker kayitlari `SINGLE_BROKER` etiketi aliyor mu

## Telegram format QA
- Disclaimer var mi
- Forbidden wording kontrolu gecti mi
- Kaynak tarihi gosteriliyor mu
- Manual review gerektirenler acik etiketlendi mi

## Compliance QA
- Yatirim tavsiyesi dili yok
- Validation disi veri publish olmuyor
- Dusuk likidite kayitlari uyarisiz one cikmiyor

## Regression QA
- Yeni parser kural degisikligi onceki valid formatlari bozmamali
- Queue alanlari Google Sheets ve canonical DB ile uyumlu kalmali

## Backtest QA
- Lookahead bias tetikleyen alanlar production publish ile karismamali

## Google Sheets QA
- Tab adlari beklenen sirada mi
- Zorunlu kolonlar eksiksiz mi
- Approval status kontrollu sozlukte mi

## Automation QA
- Data pull, parse, validate, draft, approval adimlari sira ile kosuyor mu
- `TELEGRAM_ENABLED=false` iken gonderim denenmiyor mu

## Manual review queue design
- Queue statuses:
  - `OPEN`
  - `IN_REVIEW`
  - `RESOLVED`
  - `REJECTED`
- Priority levels:
  - `HIGH`
  - `MEDIUM`
  - `LOW`
- Queue creation triggers:
  - confidence `< 0.85`
  - source verification eksik
  - para birimi eksik
  - OCR gerekli
  - tek broker + yuksek divergence

## Error queue design
- Error severities:
  - `INFO`
  - `WARN`
  - `ERROR`
  - `CRITICAL`
- Error statuses:
  - `OPEN`
  - `ACKNOWLEDGED`
  - `FIXED`
  - `WONT_FIX`
- Error to review bridge:
  - parser schema hatasi varsa review item ac
  - source unavailable ise run failure kaydi ac
  - empty output ise publish blokla

## Definition of done
- Source artifact hashlenmis
- Parser valid row veya acik manual review sonucu uretmis
- Scoring hesaplanabilir durumda
- Telegram draft disclaimer ve risk etiketleriyle hazir
- Approval status `PENDING` veya `APPROVED`
