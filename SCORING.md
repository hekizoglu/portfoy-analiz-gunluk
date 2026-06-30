# SCORING

## Purpose
MVP final score ve risk cezalarini audit edilebilir sekilde tanimlar.

## When to read this file
Gunluk aday secimi, anomaly degerlendirmesi veya scoring degisikligi yapilirken.

## What it controls
Ana skor bilesenleri, penaltiler, normalize kurallari ve yorum sinirlari.

## What it must not contain
Kesin getiri vaadi, yatirim tavsiyesi dili, validation'siz hesap varsayimi.

## Related files
`COMPLIANCE.md`, `DATABASE_SCHEMA.md`, `TELEGRAM_FORMAT.md`, `BROKER_TRACK_RECORD.md`

## Update rules
Skor bilesenleri veya agirliklar degistikce guncellenir.

## Last updated
2026-06-30

## Final score formula
`FinalScore =`
- `25% ConsensusPotentialScore`
- `20% RevisionMomentumScore`
- `15% BrokerAgreementScore`
- `15% BrokerReliabilityScore`
- `10% FundamentalQualityScore`
- `7% TechnicalTimingScore`
- `5% LiquidityScore`
- `3% KapCatalystScore`
- `- RiskPenalties`

Tum alt skorlar 0-100 araligina normalize edilir. Final score 0-100 araliginda clamp edilir.

## Component definitions
- `ConsensusPotentialScore`: weighted/median target ile guncel fiyat arasindaki potansiyelin broker sayisi ve guven puaniyla normalize edilmis skoru
- `RevisionMomentumScore`: 7 gun, 30 gun ve ceyreklik hedef fiyat/tavsiye revizyon hizinin skoru
- `BrokerAgreementScore`: raporlar arasi dagilimin dar veya genis olmasina gore tutarlilik skoru
- `BrokerReliabilityScore`: gecmis performansi iyi brokerlara agirlik veren skor
- `FundamentalQualityScore`: rapor dilinde ve kapsamada temel destek gucu; MVP'de placeholder veya manual field olabilir
- `TechnicalTimingScore`: RSI/MA/volume gibi teknik zamanlama destegi
- `LiquidityScore`: hacim ve piyasa derinligine gore guven skoru
- `KapCatalystScore`: son KAP olaylarinin pozitif/negatif etkisi

## SurpriseScore
`SurpriseScore =`
- `40% PositiveDivergenceStrength`
- `25% RevisionAcceleration`
- `20% ReliabilityWeightedUpside`
- `15% NewCoverageBonus`
- `- DivergenceRiskPenalty`

## AnomalyScore
`AnomalyScore =`
- `50% ConsensusDeviation`
- `20% RecommendationShock`
- `15% BrokerReliabilityWeightedDistance`
- `15% RevisionShock`

## Risk penalties
- `StaleTargetPenalty`
  - 0-30 gun: `0`
  - 31-60 gun: `5`
  - 61-90 gun: `12`
  - 90+ gun: `25`
- `LowLiquidityPenalty`
  - BIST100 disi ve dusuk hacimli ise `10-30`
- `HighDivergenceRiskPenalty`
  - consensus spread cok yuksekse `5-20`
- `SingleBrokerPenalty`
  - tek broker varsa `15`
- `OldReportPenalty`
  - report date eskiyse stale penalty ile birlikte veya yerine `5-25`
- `MissingSourcePenalty`
  - traceable source eksikse `100` ve publish blocker

## Minimum publish thresholds
- `FinalScore >= 60` ise aday olabilir
- `FinalScore >= 75` ve `validation_status = VALID` ise one cikan aday olabilir
- `AnomalyScore >= 70` ise anomaly bolumune girebilir
- `SingleBrokerPenalty` varsa rapor dili yumusatilir ve manual review onerilir

## Interpretation rules
- Yuksek score otomatik yayin anlamina gelmez
- Dusuk likidite veya eksik source durumunda skor ne olursa olsun publish bloklanabilir
- Teknik skor temel analizin yerine gecmez; yalnizca zamanlama destegi verir
