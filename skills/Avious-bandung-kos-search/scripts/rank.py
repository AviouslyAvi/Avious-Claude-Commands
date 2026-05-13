"""Rank normalized kos listings against user criteria.

Criteria dict:
{
    "budget_idr_monthly": int | None,
    "gender": "putra" | "putri" | "campur" | None,
    "must_have": ["ac", "km_dalam", ...],
    "nice_to_have": ["wifi", "parkir_motor", ...],
    "landmark_lat": float | None,
    "landmark_lng": float | None,
    "max_radius_km": float | None,
    "exclude_year_upfront": bool,
}
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Iterable


def haversine_km(lat1, lng1, lat2, lng2) -> float:
    R = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def passes_hard_filters(listing: dict, criteria: dict) -> tuple[bool, str]:
    if criteria.get("budget_idr_monthly"):
        if not listing["price_idr_monthly"] or listing["price_idr_monthly"] > criteria["budget_idr_monthly"]:
            return False, "over budget"

    if criteria.get("gender"):
        # Mamikos `campur` accepts everyone. A `putra` listing rejects female searchers.
        listing_gender = listing.get("gender")
        target = criteria["gender"]
        if listing_gender and listing_gender != "campur" and listing_gender != target:
            return False, f"gender mismatch ({listing_gender} vs {target})"

    for must in criteria.get("must_have", []):
        if not listing["amenities"].get(must):
            return False, f"missing must-have: {must}"

    if criteria.get("exclude_year_upfront") and listing.get("requires_year_upfront"):
        return False, "requires year upfront"

    if criteria.get("max_radius_km") and listing.get("distance_km"):
        if listing["distance_km"] > criteria["max_radius_km"]:
            return False, f"outside radius ({listing['distance_km']:.1f} km)"

    return True, "ok"


def soft_score(listing: dict, criteria: dict) -> float:
    score = 0.0

    # Distance: closer = better. Up to 30 points within 5 km.
    if criteria.get("landmark_lat") and listing.get("lat"):
        dist = listing.get("distance_km") or haversine_km(
            criteria["landmark_lat"], criteria["landmark_lng"],
            listing["lat"], listing["lng"],
        )
        listing["distance_km"] = round(dist, 2)
        score += max(0, 30 - dist * 6)
    elif listing.get("distance_km") is not None:
        score += max(0, 30 - listing["distance_km"] * 6)

    # Nice-to-have amenities: 5 points each.
    for nice in criteria.get("nice_to_have", []):
        if listing["amenities"].get(nice):
            score += 5

    # Photos signal effort & freshness. 0..15 points.
    photos = listing.get("photo_count") or 0
    score += min(15, photos)

    # Listing freshness. 0..10 points if posted within 30 days.
    if listing.get("posted_date"):
        try:
            d = datetime.fromisoformat(listing["posted_date"].replace("Z", "+00:00"))
            days_old = (datetime.now(timezone.utc) - d).days
            score += max(0, 10 - days_old / 3)
        except (ValueError, TypeError):
            pass

    # 24-hour access bonus when relevant.
    if listing["amenities"].get("bebas_24jam"):
        score += 5

    # Cheaper is slightly better, all else equal.
    if criteria.get("budget_idr_monthly") and listing.get("price_idr_monthly"):
        ratio = listing["price_idr_monthly"] / criteria["budget_idr_monthly"]
        score += max(0, 10 * (1 - ratio))

    # Penalty: year-upfront still allowed but ranked below flexible listings.
    if listing.get("requires_year_upfront"):
        score -= 8

    return round(score, 2)


def rank(listings: Iterable[dict], criteria: dict, top_n: int = 10) -> list[dict]:
    kept = []
    for l in listings:
        ok, reason = passes_hard_filters(l, criteria)
        if not ok:
            l["filtered_out_reason"] = reason
            continue
        l["score"] = soft_score(l, criteria)
        kept.append(l)
    kept.sort(key=lambda x: x["score"], reverse=True)
    return kept[:top_n]


def render_markdown_table(ranked: list[dict]) -> str:
    if not ranked:
        return "_No listings matched the criteria._"
    lines = [
        "| # | Name | IDR/mo | USD/mo | Distance | Amenities | Link |",
        "|---|------|--------|--------|----------|-----------|------|",
    ]
    for i, l in enumerate(ranked, 1):
        idr = l.get("price_idr_monthly") or 0
        idr_str = f"Rp {idr:,}".replace(",", ".") if idr else "—"
        usd = l.get("price_usd_monthly")
        usd_str = f"${usd}" if usd else "—"
        dist = f"{l['distance_km']:.1f} km" if l.get("distance_km") else "—"
        am = l.get("amenities", {})
        am_chips = " ".join(k for k, v in am.items() if v is True)
        title = (l.get("title") or "—")[:48]
        url = l.get("url") or ""
        lines.append(f"| {i} | {title} | {idr_str} | {usd_str} | {dist} | {am_chips} | [link]({url}) |")
    return "\n".join(lines)


if __name__ == "__main__":
    # smoke test
    sample = [
        {
            "title": "Kos Dago AC", "price_idr_monthly": 1_800_000, "price_usd_monthly": 111,
            "gender": "putra", "amenities": {"ac": True, "km_dalam": True, "wifi": True, "bebas_24jam": True},
            "distance_km": 0.8, "photo_count": 12, "posted_date": "2026-04-15T00:00:00Z",
            "url": "https://mamikos.com/x", "requires_year_upfront": False,
        },
    ]
    crit = {"budget_idr_monthly": 2_000_000, "gender": "putra", "must_have": ["ac"],
            "nice_to_have": ["wifi", "km_dalam"], "exclude_year_upfront": False}
    print(render_markdown_table(rank(sample, crit)))
