# IDR ↔ USD conversion

Avi wants prices shown in both IDR and USD side-by-side. Use a freely available rate source, cache it for 24h, and record which rate was used in every saved Obsidian note.

## Source (priority order)

1. **exchangerate.host** — `https://api.exchangerate.host/latest?base=USD&symbols=IDR` — free, no API key, returns JSON `{rates: {IDR: 16234.5}}`.
2. **open.er-api.com** — `https://open.er-api.com/v6/latest/USD` — backup, also free.
3. **Hardcoded fallback** — if both APIs fail, use `USD_IDR = 16200` and flag the listing note with `fx_source: fallback` so Avi knows the conversion is approximate.

## Cache

Cache file: `~/.claude/skills/bandung-kos-search/.fx_cache.json`

```json
{
  "fetched_at": "2026-04-27T08:00:00Z",
  "usd_to_idr": 16234.5,
  "source": "exchangerate.host"
}
```

Refresh logic: if `fetched_at` is more than 24 hours old, re-fetch. Otherwise use the cached value.

## Conversion

```
price_usd_monthly = round(price_idr_monthly / usd_to_idr)
```

Round to whole USD — sub-dollar precision is meaningless here.

## Display format

In the markdown table:
```
| Rp 1.500.000 | $92 |
```

In the Obsidian note frontmatter, record:
```yaml
fx_rate: 16234.5
fx_source: exchangerate.host
fx_fetched_at: 2026-04-27T08:00:00Z
```

This lets Avi compare results from different days and understand any apparent USD price drift is FX, not landlord pricing.
