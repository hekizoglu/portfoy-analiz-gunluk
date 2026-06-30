# 00_CONTEXT_GRAPH

## Purpose
Bu depo icin minimum baglam okuma haritasi.

## When to read this file
Her sprintin basinda ve yeni bir gorev tipine girerken.

## What it controls
Hangi dosyanin ne zaman okunacagini ve minimum baglam sirasini.

## What it must not contain
Detayli alan kurallari veya gorev tekrarleri.

## Related files
`PROJECT_MEMORY.md`, `ROADMAP.md`, `SPRINT_15_MIN.md`, alan dosyalari.

## Update rules
Yeni belge akisi veya dependency degisikliginde guncellenir.

## Last updated
2026-06-30

## Read order
1. `PROJECT_MEMORY.md`
2. `ROADMAP.md`
3. `SPRINT_15_MIN.md`
4. Goreve bagli alan dosyasi

## Task to context
| Task type | Required files |
| --- | --- |
| Source adapter | `DATA_SOURCES.md`, `docs/templates/source_adapter_template.md` |
| Parser design | `PARSING_RULES.md`, ilgili source adapter |
| Sheets schema | `GOOGLE_SHEETS_SCHEMA.md`, `DATABASE_SCHEMA.md` |
| Scoring change | `SCORING.md`, `COMPLIANCE.md` |
| Telegram formatting | `TELEGRAM_FORMAT.md`, `COMPLIANCE.md` |
| Configuration/setup | `CONFIGURATION.md`, `.env.example`, ilgili entegrasyon dosyasi |

## Minimal context rule
Gorev icin gerekli olmayan dosyalar okunmaz; tum repo topluca yuklenmez.
