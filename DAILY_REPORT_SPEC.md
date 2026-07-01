# DAILY_REPORT_SPEC

## Purpose
Gunluk piyasa raporunun hangi bilgileri icermesi gerektigini, raporun ne kadar detayli olmali oldugunu ve hangi kaynaklardan beslenmesi gerektigini tanimlar.

## When to read this file
Rapor formatini degistirirken, yeni veri kaynagi eklerken veya Telegram / Sheets cikti kalitesini artirirken.

## What it controls
Rapor bolumleri, minimum alanlar, kaynak kontrol listesi, oncelik sinyalleri ve manuel kontrol etiketi.

## What it must not contain
Yatirim tavsiyesi dili, onaysiz auto-send, canli secret, kaynaksiz kesinlik iddiasi.

## Related files
`TELEGRAM_FORMAT.md`, `QA.md`, `SCORING.md`, `PARSING_RULES.md`, `AUTOMATION.md`

## Update rules
Yeni veri sinifi, yeni kaynak veya yeni rapor bolumu eklendikce guncellenir.

## What people usually track
Profesyonel raporlarda ve research platformlarinda en cok su basliklar izlenir:

- Guncel fiyat ile hedef fiyat arasindaki fark
- Consensus expectations ve analist revizyonlari
- Yukari / asagi yonlu hedef fiyat degisimleri
- Earnings, gelir, marj ve rehberlik degisimleri
- Likidite, free float ve hacim etkisi
- Sektor rotasyonu ve endeks davranisi
- Makro faiz, doviz kuru ve enflasyon etkisi
- KAP uzerinden gelen kurumsal olaylar

Bu perspektif CFA Institute'un consensus beklentileri okuma vurgusu, Fidelity'nin research platform kaynaklari ve Morningstar'in watchlist / screener / rating changes araclariyla uyumludur.

## Where to check
Guncel kontrol noktalarinin ana kaynaklari:

- KAP: https://kap.org.tr/en
- Borsa Istanbul equity market: https://www.borsaistanbul.com/en/markets/equity-market
- Borsa Istanbul indices: https://www.borsaistanbul.com/en/indices
- TCMB statistics: https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB%2BEN/Main%2BMenu/Statistics
- TCMB exchange rates: https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB%2BEN/Main%2BMenu/Statistics
- TUIK data portal: https://veriportali.tuik.gov.tr/en
- Company investor relations and presentations
- Broker research portals and rating-change / screener pages

## Daily report shape
Rapor bir oncelik listesi gibi calismali:

1. Hızlı ozet
2. Kaynak kapsamı
3. Piyasa baglami
4. En guclu adaylar
5. Revizyonlar ve ayrismalar
6. Manuel review gerektiren kayıtlar
7. Gun icinde atilacak aksiyonlar

## Minimum sections
### 1. Hızlı ozet
- Rapor tarihi
- Toplam kaynak sayisi
- Gecerli satir sayisi
- Manuel review sayisi

### 2. Kaynak kapsamı
Her kaynak icin:
- Kaynak adi
- Nerede kontrol edilecegi
- Ne kontrol edilecegi
- Siklik

### 3. Piyasa baglami
Ozellikle su sinyaller:
- Consensus expectations
- Faiz ve FX
- Sektor rotasyonu
- KAP olaylari

### 4. Izleme adaylari
Her aday icin:
- Ticker
- Broker sayisi
- Guncel fiyat
- Ortalama hedef fiyat
- Upside
- Final skor
- Risk etiketi
- Kisa consensus notu
- Varsa katalizor notu

### 5. Revizyonlar
- Hedef fiyat yukari/asagi revizyonu
- Son 30 gun trendi
- Degisim yönu ve gücü

### 6. Anomali ve manual review
- Tek kurum verisi
- Currency belirsizligi
- Dussuk confidence
- Source verification eksigi
- OCR / parse belirsizligi

### 7. Aksiyonlar
Raporun sonundaki aksiyonlar teknik ve operasyonel olmalidir:
- Hangi kaynagin tekrar kontrol edilecegi
- Hangi task'in once tamamlanmasi gerektigi
- Hangi satirin manuel onaya gittigi

## Detail level guidance
Rapor yeterince detayli olmalidir ama gürültü yaratmamali.

- 1 ile 3 aday varsa: aday bazli daha derin aciklama ver
- 4 ile 10 aday varsa: ozet + ilk 3 aday + belirgin riskler
- 10+ aday varsa: filtre ve skor oncelikli, ayrinti manuel review'a kaydir

## Quality gates
- Yatirim tavsiyesi dili olmamali
- Kaynaksiz sayi verilmemeli
- Tek broker satirlar one cikarken risk etiketi almalı
- KAP veya makro sinyallerle celiski varsa manuel review acilmali
- Report body, Telegram markdown için temiz olmali

## Recommended next extensions
- Consensus engine
- Broker normalization dictionary
- KAP catalyst taxonomy
- Macro snapshot fetcher
- Freshness and stale-target scoring
