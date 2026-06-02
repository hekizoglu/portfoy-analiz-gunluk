# Günlük Otomatik Çalıştırma Promptu

> Bu dosya, zamanlanmış (scheduled) oturum tetiklendiğinde çalıştırılacak görevi tanımlar.
> Web arayüzünde "Scheduled Session" promptu olarak şu satırı kullan:
>
> **"GUNLUK_GOREV.md dosyasındaki talimatları uygula."**

---

## Görev

1. **CLAUDE.md** dosyasındaki portföyü ve 11 adımlık günlük analiz görevinin TAMAMINI uygula.
   - Güncel fiyatlar, teknik analiz, KAP bildirimleri, değerleme, makro, sektör, akış
   - 6 aracı kurum değerleme tablosu + portföy dışı fırsat taraması
   - Çıktı formatındaki 5 bölümü oluştur (Portföy Tablosu, Haberler, Strateji, Aksiyon, Takvim)

2. Analizi tamamladıktan sonra **Gmail taslağı** oluştur:
   - **Kime:** huseyinekizoglu@gmail.com
   - **Konu:** Günlük Portföy Analizi — [BUGÜNÜN TARİHİ]
   - **İçerik (htmlBody):** Tam analiz raporu, okunabilir HTML formatında (tablolar dahil)
   - `mcp__Gmail__create_draft` aracını kullan

3. Eğer o gün önemli bir gelişme varsa (sert fiyat hareketi, kritik KAP haberi,
   TCMB/Fed kararı), konuya **"⚠️ ÖNEMLİ"** etiketi ekle.

---

## Notlar
- Gmail entegrasyonu sadece TASLAK oluşturabilir, otomatik göndermez.
  Kullanıcı taslağı Gmail'den kendisi gönderir/okur.
- Türkçe yanıt ver.
- Fiyat verileri gecikmeli olabilir; raporun başına bu uyarıyı ekle.
