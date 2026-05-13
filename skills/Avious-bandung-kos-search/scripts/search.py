"""Search orchestrator: build portal URLs and merge results.

This module is intentionally a *URL builder + result-shape adapter*, not a
scraper. The actual fetching is done by Claude using the firecrawl-browser
skill (or equivalent), which handles JS rendering. This script's job:

1. Translate user criteria into portal-specific search URLs.
2. Define the expected result-shape per portal so Claude knows what to extract.
3. Provide a `merge` helper that dedupes across portals.

Usage from Claude:
    from search import build_mamikos_url, build_rumah123_url, merge_results
    url = build_mamikos_url(criteria)
    # ... fetch via firecrawl ... extract cards ... call normalize_listing on each
"""

from __future__ import annotations

from urllib.parse import urlencode


# --- Mamikos -------------------------------------------------------------

MAMIKOS_BASE = "https://mamikos.com/cari"
MAMIKOS_BANDUNG_SLUG = "bandung-kota-bandung-jawa-barat-indonesia"


def build_mamikos_url(criteria: dict) -> str:
    """Build a Mamikos search URL from criteria.

    Criteria keys used:
        landmark_lat, landmark_lng — switch to coordinate search
        max_radius_km            — radius in km (default 2 if coords given)
        budget_idr_monthly       — upper bound on monthly price
        gender                   — putra | putri | campur (mapped to URL slot)
    """
    if criteria.get("landmark_lat") and criteria.get("landmark_lng"):
        location = f"{criteria['landmark_lat']},{criteria['landmark_lng']}"
    else:
        location = MAMIKOS_BANDUNG_SLUG

    gender_slot = criteria.get("gender") or "all"
    period_slot = "bulanan"
    budget = criteria.get("budget_idr_monthly") or 15_000_000
    price_slot = f"0-{budget}"

    path = f"{MAMIKOS_BASE}/{location}/{gender_slot}/{period_slot}/{price_slot}"

    params = {"sort": "price_low"}
    if criteria.get("landmark_lat"):
        params["radius"] = criteria.get("max_radius_km") or 2

    return f"{path}?{urlencode(params)}"


# Expected card shape from Mamikos search results page.
# When extracting via firecrawl, look for these data points per card:
MAMIKOS_CARD_SHAPE = {
    "id": "data-attribute or URL slug",
    "title": "card title text",
    "url": "absolute URL to detail page",
    "price_text": "e.g. 'Rp 1.500.000 / bulan'",
    "location_text": "kelurahan + kecamatan string",
    "distance_km": "if geo search, '1.2 km' parsed to float",
    "photo_count": "badge integer or count of img tags",
    "badges_text": "promo badges joined (e.g. 'Sewa Tahunan -10%')",
    "description": "card snippet, if present",
}


# --- Rumah123 ------------------------------------------------------------

RUMAH123_BASE = "https://www.rumah123.com/sewa"


def build_rumah123_url(criteria: dict) -> str:
    """Rumah123 'kost' category search."""
    parts = ["kost", "kota-bandung"]
    params = {}
    if criteria.get("budget_idr_monthly"):
        params["price"] = f"0-{criteria['budget_idr_monthly']}"
    qs = f"?{urlencode(params)}" if params else ""
    return f"{RUMAH123_BASE}/{'/'.join(parts)}/{qs}"


# --- OLX -----------------------------------------------------------------

OLX_BASE = "https://www.olx.co.id/bandung-kota_g4000028/kost-kontrakan_c5169"


def build_olx_url(criteria: dict) -> str:
    params = {"q": "kos bandung"}
    if criteria.get("budget_idr_monthly"):
        params["pmax"] = criteria["budget_idr_monthly"]
    return f"{OLX_BASE}?{urlencode(params)}"


# --- Merge / dedupe ------------------------------------------------------

def _dedupe_key(listing: dict) -> tuple:
    """Loose dedupe — same neighborhood + similar price = likely duplicate."""
    nb = (listing.get("neighborhood") or "").lower().strip()[:30]
    price_bucket = (listing.get("price_idr_monthly") or 0) // 100_000
    title_head = (listing.get("title") or "").lower().strip()[:25]
    return (nb, price_bucket, title_head)


def merge_results(*lists: list[dict]) -> list[dict]:
    seen = {}
    for lst in lists:
        for item in lst:
            k = _dedupe_key(item)
            if k not in seen:
                seen[k] = item
            else:
                # Prefer the one with more photos / more complete data
                existing = seen[k]
                if (item.get("photo_count") or 0) > (existing.get("photo_count") or 0):
                    seen[k] = item
    return list(seen.values())


# --- Bandung sanity check ------------------------------------------------

def is_bandung_query(text: str) -> bool:
    """Reject queries that are clearly outside Bandung scope."""
    t = (text or "").lower()
    if "bandung" in t or "itb" in t or "unpad" in t or "maranatha" in t \
            or "telkom u" in t or "tel-u" in t or "unisba" in t:
        return True
    other_cities = ["jakarta", "surabaya", "yogya", "jogja", "medan", "semarang",
                    "denpasar", "bali", "makassar", "bekasi", "tangerang", "depok"]
    if any(c in t for c in other_cities):
        return False
    # Default to True if ambiguous — workflow will use city slug.
    return True


if __name__ == "__main__":
    crit = {
        "landmark_lat": -6.8915, "landmark_lng": 107.6107,
        "max_radius_km": 2, "budget_idr_monthly": 2_000_000,
        "gender": "putra",
    }
    print("Mamikos:", build_mamikos_url(crit))
    print("Rumah123:", build_rumah123_url(crit))
    print("OLX:", build_olx_url(crit))
