# PROJECT_MEMORY

## Purpose
Mevcut proje durumunu sonraki sprintlere kisa ve operasyonel sekilde tasir.

## When to read this file
Her sprintten once ve sprint sonunda guncelleme yaparken.

## What it controls
Aktif durum, varsayimlar, sonraki gorev, degistirilmemesi gereken sinirlar.

## What it must not contain
Uzun tarihce, kod kopyalari, gizli bilgi.

## Related files
`ROADMAP.md`, `DECISIONS.md`, `RISK_REGISTER.md`, `ERRORS.md`

## Update rules
Her sprint sonunda yalnizca gecerli durum guncellenir.

## Last updated
2026-07-01

## Current project state
Minimum dokumantasyon kontrol sistemi kuruldu. Phase 1 tasarim gorevleri tamamlandi: OYAK source adapter, parser/validation kurallari, canonical veri modeli, Google Sheets MVP semasi, scoring, Telegram manuel approval formati, error/manual review queue, gunluk pipeline komut plani ve progress notification tasarimi hazir. Git deposu baslatildi. Telegram entegrasyonu icin secret-safe konfigurasyon iskeleti eklendi; varsayilan test grup chat ID'si repoya islendi. Shell-bagimsiz universal config standardi tanimlandi. Gercek OYAK PDF'sinden 42 satir parse eden runtime script eklendi, gunluk rapor JSON'u ve Telegram draft'i uretildi, dry-run dogrulandi. Phase 2 icin Is Yatirim ve Ak Yatirim source adapter tasarimlari eklendi. DeepSeek icin TRT bazli peak/off-peak pricing pencereleri config ve scheduler katmanina eklendi. Canli OYAK PDF fetcheri ve GitHub Actions cron loop'u eklendi; repo secrets ile yerel secret gorunurlugu olmadan da canli veri akisi calisabilir. Yerel `.env.local` ile Telegram test gonderimi acildi. Broker recommendation normalization dictionary merkezi hale getirildi ve OYAK parser bu sozlugu kullanacak sekilde baglandi. Cift AI inceleme, approval queue ve private-test/approved-send teslim modu eklendi; AI secrets olmadiginda queue PENDING kalacak sekilde güvenli akış sağlandi.

## Current phase
`Phase 2 - Multi-Broker Consensus`

## Current sprint
`P2-T03` tamamlandi.

## Current assumptions
- Kaynak tasarimi bu sprintte canli site baglantisi kurmadan yapildi.
- OYAK degerleme tablolarinin PDF ve/veya HTML olarak yayinlanabilecegi varsayildi.
- BIST100-first kapsam korunuyor.
- Telegram test grubu chat ID'si `-5434687426` olarak kullanilacak.

## Active priorities
- Tum future runtime code icin `.env/.env.local/process env` precedence standardini korumak
- Sheets semasini automation/pipeline adimlarina baglamak
- Telegram gercek gonderimini `.env.local` veya aktif env ile dogrulamak
- Sheets veya lokal kalici katmana queue yazimi eklemek
- Tek kurum verisinden uretilen draft icin daha muhafazakar ranking/filtre eklemek
- Consensus engine iskeletini eklemek
- AI review secrets ve provider config olmadan auto-send beklememek

## Known risks
- OYAK formati canli dogrulama yapilmadan kesinlestirilemez.
- PDF tablo yapisi parser karmasikligini artirabilir.
- Lisans/ToS incelemesi canli entegrasyon oncesi zorunlu.
- Telegram token ve hedef chat yanlis yonetilirse secret ve itibar riski dogar.
- Bu shell oturumunda Telegram env veya `.env.local` gorunmedigi icin canli test gonderimi bloke.
- Yerel Telegram testi 401 Unauthorized verdi; mevcut token rotate gerektiriyor olabilir.

## Next task ID
`P2-T04`

## Do-not-change list
- Bu sistem yatirim tavsiyesi urunu gibi konumlandirilmayacak.
- Telegram auto-send manuel onay olmadan eklenmeyecek.
- Gizli bilgi ve canli credential repo icine yazilmayacak.
