# Mamikos — URL patterns and filter params

Mamikos (https://mamikos.com) is the dominant kos-kosan portal in Indonesia. Use it as the primary source for all Bandung kos searches.

## Base search URL pattern

```
https://mamikos.com/cari/bandung-kota-bandung-jawa-barat-indonesia/all/bulanan/0-15000000?...
                       └─────────── city slug ──────────────┘  └ gender ┘ └ rental period ┘ └ price range ┘
```

- **City slug** for Bandung: `bandung-kota-bandung-jawa-barat-indonesia`
- **Gender**: `all` (any) · `putra` (male only) · `putri` (female only) · `campur` (mixed)
- **Period**: `bulanan` (monthly — default) · `tahunan` (yearly) · `mingguan` (weekly) · `harian` (daily)
- **Price range**: `min-max` in IDR (e.g., `0-2000000` for under 2jt/month). Use `bulanan` price brackets when comparing.

Default for our use case: `bandung-kota-bandung-jawa-barat-indonesia/all/bulanan/0-{budget_idr}`.

## Geo / proximity search

When the user says "near ITB" or "near Telkom University", switch from the city-wide URL to a coordinate search:

```
https://mamikos.com/cari/-6.8915,107.6107/all/bulanan/0-2000000?radius=2
```

- `lat,lng` go in the path slot where the city slug normally sits.
- `radius` is in km (1–5 sensible).
- See `CAMPUS_ZONES.md` for ITB/Unpad/Maranatha/Telkom anchor coordinates.

## Filter query params

Append as `&filter[]=value` (Mamikos uses array-style query params):

| Param | Values | Meaning |
| --- | --- | --- |
| `gender` | `putra` `putri` `campur` | Tenant gender |
| `price_range` | `min-max` IDR | Monthly budget |
| `facilities[]` | `ac` `kasur` `lemari` `meja_belajar` `kursi` `tv` `kulkas` | In-room facilities |
| `facilities_bath[]` | `kamar_mandi_dalam` (private bath) `wc_duduk` `air_panas` | Bathroom |
| `facilities_share[]` | `wifi` `parkir_motor` `parkir_mobil` `dapur` `ruang_tamu` `laundry` | Shared facilities |
| `rules[]` | `bebas_24jam` `boleh_pasutri` (couples ok) `boleh_anak` (kids ok) | House rules |
| `sort` | `price_low` `price_high` `recommendation` | Result ordering |

## Listing card fields (what to extract per result)

Each Mamikos card on a search results page exposes:
- Listing title (often `Kos {Putra|Putri|Campur} {District} {Code}`)
- Price + period (e.g., `Rp 1.500.000 / bulan`)
- Location text (kelurahan / kecamatan / city)
- Distance from search center (km, when geo search)
- Photo count badge
- "Promo" badges (often `Sewa Tahunan -10%` etc.)
- Facility icons (need to map icon class → facility name)
- URL to detail page (for full description, house rules, photos, contact)

For the ranking pass we only need: `title, price_text, location_text, distance_km, photo_count, badges, url`. The detail page is only needed when ranking is tight or when amenity data is missing from the card.

## Pagination

Mamikos paginates search results — typically 20 cards per page. Append `&page=N` to walk pages. Stop after 3 pages or 50 candidates, whichever comes first; ranking quality drops fast past page 2.

## Rate-limit / scraping caveats

- Mamikos is JS-rendered — plain `curl` returns a near-empty shell. Use `firecrawl-browser` or Playwright.
- Aggressive scraping triggers a Cloudflare challenge. Throttle to ≤ 1 req / 2s and back off on 403.
- The site occasionally A/B tests new card markup. If the selector you used last week returns zero hits, re-inspect before assuming "no results".

## Quick smoke-test URL

For Avi's most common query — kos near ITB under 2jt/month — paste this into a browser to sanity-check Mamikos availability before building filters:

```
https://mamikos.com/cari/-6.8915,107.6107/all/bulanan/0-2000000?radius=2&sort=price_low
```
