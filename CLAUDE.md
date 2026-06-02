# Portföy Günlük Analiz Görevi

## Portföy

| Ticker | Şirket | Sektör |
|--------|--------|--------|
| PSGYO | Pasifik GYO | Gayrimenkul (GYO) |
| EUREN | Europen Endüstri | İnşaat / Sanayi |
| PATEK | Pasifik Teknoloji | Teknoloji / Savunma |
| MOPAS | Mopaş Marketcilik | Perakende / Gıda |
| GWIND | Galata Wind Enerji | Yenilenebilir Enerji |
| KLKIM | Kalekim Kimyevi | İnşaat Malzemeleri |
| KCHOL | Koç Holding | Holding / Çeşitlendirilmiş |

---

## Günlük Analiz Görevi

Kullanıcı portföy analizi istediğinde aşağıdaki adımların TAMAMINI uygula:

### 1. Fiyat & Performans
- Her hisse için güncel fiyat, günlük değişim (%), haftalık ve aylık performans
- 52 haftalık yüksek/düşük seviyeleri ve mevcut fiyatın bu aralıktaki konumu
- ATH (tüm zamanlar en yüksek) ve mevcut fiyat arasındaki fark

### 2. Teknik Analiz
- Destek ve direnç seviyeleri
- RSI (aşırı alım >70 / aşırı satım <30 tespiti)
- MACD — momentum yönü ve sinyal kesişimi
- Hacim analizi — fiyat hareketini teyit ediyor mu, teyit etmiyor mu?
- Hareketli ortalamalar: 20, 50, 200 günlük; fiyat bu ortalamaların neresinde?
- Bollinger Bantları — volatilite sıkışması veya kırılım var mı?
- Genel teknik sinyal: Güçlü Al / Al / Nötr / Sat / Güçlü Sat

### 3. Şirkete Özel Haberler & KAP Bildirimleri
- KAP (Kamuyu Aydınlatma Platformu) son 24 saatte yeni bildirim var mı?
- Önemli sözleşme, ihale, ortaklık, yönetim değişikliği haberleri
- İçeriden alım-satım bildirimleri (yönetici/büyük ortak hareketleri)
- Temettü ilanı, bedelsiz sermaye artırımı, rüçhan hakkı bildirimleri
- Halka arz lock-up bitiş tarihleri (özellikle MOPAS için)

### 4. Değerleme Metrikleri
- F/K oranı — sektör ortalamasıyla kıyasla
- PD/DD — özellikle GYO hisseleri için kritik (PSGYO)
- FD/FAVÖK — borç dahil değerleme
- Analist hedef fiyatları ve son revizyon tarihi (yukarı/aşağı mı?)
- Temettü verimi

### 5. Finansal Sağlık (Bilanço Dönemi Yakınsa)
- Son açıklanan: ciro, FAVÖK, net kâr — piyasa beklentisine göre sapma
- Borç/Özkaynak oranı — yüksek faiz ortamında kritik
- Serbest nakit akışı pozisyonu
- Kur riski: döviz cinsinden borç ve gelir dengesi (KCHOL, GWIND için önemli)
- Bilanço açıklama tarihi varsa belirt

### 6. Sektörel & Rakip Kıyaslama
- İlgili sektör endeksi (XGMYO, XELKT, XUSIN, XUHIZ, XTCRT) günlük performansı
- Rakip hisseler ne yapıyor — portföy hissesi sektörden ayrışıyor mu?
- Sektörü etkileyen düzenleyici kararlar: EPDK (enerji), BDDK (bankacılık), SPK, Rekabet Kurumu
- Girdi/hammadde fiyatları: KLKIM için kalsiyum/katkı, GWIND için çelik/bakır/elektrik fiyatı

### 7. Akış & Pozisyonlanma
- Yabancı yatırımcı net alım-satım dengesi (haftalık BIST verisi)
- Açığa satış oranı — önceki haftaya göre artış/azalış
- Kurumsal fon hareketleri, büyük lot işlemleri
- Endeks revizyonu riski/fırsatı (BIST 30/100 giriş-çıkış takvimi)

### 8. Makro Göstergeler
- **Türkiye:** USD/TRY, EUR/TRY anlık seviye ve haftalık trend
- **Türkiye:** TCMB politika faizi, son PPK kararı ve sonraki toplantı tarihi
- **Türkiye:** Son açıklanan enflasyon (TÜFE), bir sonraki veri tarihi
- **Türkiye:** Hazine ihalesi sonuçları, CDS spreadi, Eurobond faizleri
- **Global:** Fed faiz durumu ve beklentiler, dolar endeksi seviyesi
- **Global:** Brent petrol, doğal gaz fiyatları
- **Global:** S&P 500 ve gelişmekte olan piyasalar (EEM) günlük performansı
- **Global:** Risk iştahı: VIX endeksi seviyesi

### 9. Kurumsal Aksiyon & Ekonomi Takvimi
- Önümüzdeki 7 günde: bilanço açıklama tarihleri (portföy hisselerine özel)
- Genel kurul tarihleri, temettü ödeme tarihleri
- TÜİK veri açıklama takvimi (enflasyon, büyüme, konut satışları)
- TCMB PPK toplantı tarihi
- Fed FOMC toplantı tarihi
- Türkiye Hazine ihale takvimi

### 10. Banka Değerleme Tabloları (Haftalık)
- Oyak Yatırım, İş Yatırım, Garanti BBVA Yatırım araştırma raporlarından güncel hedef fiyat ve tavsiye tablosu
- Portföy hisselerine yönelik yeni rapor/revizyon var mı?

---

## Analiz Çıktısı Formatı

Her günlük analizin sonunda şu bölümler olmalı:

1. **Portföy Durumu Tablosu** — tüm hisseler için fiyat/değişim/teknik sinyal/öneri özeti
2. **Günün En Önemli 3–5 Haberi** — portföyü doğrudan etkileyen gelişmeler
3. **Strateji Güncellemesi** — her pozisyon için AL / ARTIR / TUT / AZALT / SAT tavsiyesi ve kısa gerekçe
4. **Aksiyon Listesi** — o gün veya yakın vadede yapılacak somut işlemler
5. **Yaklaşan Kritik Tarihler** — önümüzdeki 7–14 günde dikkat edilecek takvim

---

## Notlar
- Fiyat verileri yaklaşık/gecikmeli olabilir; işlem öncesi gerçek zamanlı kaynaklardan teyit et.
- Bu analiz bilgilendirme amaçlıdır, yatırım tavsiyesi değildir.
- Türkçe yanıt ver.
