---
name: Avious-bandung-kos-search
description: Search, normalize, rank, and archive kos-kosan (boarding-room) rentals in Bandung, Indonesia. Use this skill when the user asks to find a kos in Bandung, search Mamikos, find a room near ITB/Unpad/Maranatha/Telkom University, or any variant of "cari kos Bandung", "kost Dago", "boarding room near campus". Skips queries about whole houses, apartments, sale listings, or other Indonesian cities — those are out of scope. Output is a ranked markdown table inline plus a dated note saved to Obsidian. Prices shown in IDR and USD side-by-side.
---

# Bandung Kos Search

A purpose-built search skill for **kos-kosan** (single boarding-house rooms) for rent in Bandung, Indonesia.

## Scope

- **Rent only.** No sale listings.
- **Kos-kosan only.** No whole houses, no apartments, no Travelio short-term.
- **Bandung only.** Jatinangor (Unpad's campus ~25km east) is a separate city — confirm with the user before including.

## Workflow

1. **Parse the query** into structured criteria:
   - `landmark` (e.g., "near ITB", "near Telkom University") → look up in `references/CAMPUS_ZONES.md`
   - `budget_idr_monthly` (max IDR per month — convert "2jt" → 2,000,000)
   - `gender` (putra/putri/campur — default: don't filter unless specified)
   - `must_have_amenities` (ac, km_dalam, wifi, parkir_motor, parkir_mobil, bebas_24jam)
   - `nice_to_have_amenities` (same list, soft-scored)
   - `electricity_included` (true/false/any)

2. **Read the references** before composing portal URLs:
   - `references/MAMIKOS.md` — URL patterns and filter params
   - `references/GLOSSARY.md` — Bahasa terms (so you don't mis-parse listings)
   - `references/CAMPUS_ZONES.md` — landmark coordinates and neighborhood lists
   - `references/FX.md` — IDR→USD conversion procedure

3. **Fetch** in priority order — stop early if you have ≥10 quality results:
   - **Mamikos** first (primary inventory).
   - **Rumah123** kost category if Mamikos returns < 10.
   - **OLX** only if combined results still < 5.
   - Use the `firecrawl-browser` skill (or equivalent fetch tool) for JS-rendered pages.

4. **Normalize** every listing through `scripts/normalize.py`:
   - Period → `price_idr_monthly`
   - Flag `requires_year_upfront` if quoted only `/tahun` with bayar di muka
   - Extract amenity booleans
   - Add `price_usd_monthly` using the cached FX rate

5. **Rank** through `scripts/rank.py`:
   - Hard-filter: budget, gender, must-have amenities
   - Soft-score: distance, photo count, freshness, 24h access, year-upfront penalty
   - Take top 10

6. **Output**:
   - **Print** the ranked table inline: `Name | Price IDR/mo | Price USD/mo | Distance | Amenities | Link`
   - **Save** to Obsidian at `Fresh Obsidian Vault/Bandung Kos Search/YYYY-MM-DD-{slug}.md` via `scripts/save_to_obsidian.py`. Re-runs of the same query create new dated files; never overwrite.

7. **Footer reminder**: if results are thin (< 5), tell the user that Bandung kos inventory also lives on WhatsApp groups, Facebook groups, and physical "Terima Kos" signs — these are not scrapable but worth checking on the ground.

## Out-of-scope queries

If the user asks about a whole house, apartment, sale listing, or a city other than Bandung, decline politely and suggest the right scope ("This skill only covers kos rentals in Bandung — for apartments try Travelio directly, for houses try Rumah123 with the rumah category").

## Glossary quick-reference

`kos`/`kost` = boarding-house room · `putra`/`putri`/`campur` = male/female/mixed · `KM dalam` = private bathroom · `KM luar` = shared bathroom · `bebas 24 jam` = 24h access · `include listrik` = electricity bundled · `bayar di muka` = paid upfront · `nego` = negotiable · `1,5jt` = 1,500,000 IDR · `15jt/tahun` = 15M IDR/year (~1.25jt/month equivalent).

Read `references/GLOSSARY.md` for the full list before parsing any raw listing.
