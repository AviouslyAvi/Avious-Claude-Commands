"""Normalize raw kos listings into a common schema.

Schema:
{
    "source": "mamikos" | "rumah123" | "olx",
    "id": str,
    "url": str,
    "title": str,
    "raw_price_text": str,
    "price_idr_monthly": int,
    "price_idr_raw": int,
    "period": "bulan" | "tahun" | "minggu" | "hari",
    "requires_year_upfront": bool,
    "gender": "putra" | "putri" | "campur" | None,
    "neighborhood": str | None,
    "lat": float | None,
    "lng": float | None,
    "distance_km": float | None,
    "amenities": {
        "ac": bool, "km_dalam": bool, "wifi": bool, "kasur": bool,
        "lemari": bool, "parkir_motor": bool, "parkir_mobil": bool,
        "bebas_24jam": bool, "electricity_included": bool | None,
    },
    "photo_count": int | None,
    "posted_date": str | None,        # ISO date if available
    "description_raw": str,
}
"""

from __future__ import annotations

import re
from typing import Optional

JT = 1_000_000          # juta = million
M_IDR = 1_000_000_000   # miliar = billion (kos prices basically never use this, but guard)
RB = 1_000              # ribu = thousand


def parse_idr_amount(text: str) -> Optional[int]:
    """Parse a Bahasa-formatted IDR price into an int.

    Handles:  Rp 1.500.000 · 1,5jt · 1.5jt · 500rb · 15jt · Rp 15.000.000
    Returns None if no number is found.
    """
    if not text:
        return None
    t = text.lower().replace("rp", "").replace(" ", "").replace("\xa0", "")

    # Shorthand: Nrb / Njt / NM
    m = re.search(r"([0-9]+(?:[.,][0-9]+)?)\s*(jt|juta|m|miliar|rb|ribu|k)\b", t)
    if m:
        num_s, unit = m.group(1), m.group(2)
        num = float(num_s.replace(",", "."))
        if unit in ("jt", "juta"):
            return int(num * JT)
        if unit in ("m", "miliar"):
            return int(num * M_IDR)
        if unit in ("rb", "ribu", "k"):
            return int(num * RB)

    # Long form: 1.500.000 (Indonesian thousands separator) or 1500000
    digits = re.findall(r"[0-9.,]+", t)
    if digits:
        # Indonesian: . is thousands, , is decimal. Strip dots, replace , with .
        cleaned = digits[0].replace(".", "").replace(",", ".")
        try:
            return int(float(cleaned))
        except ValueError:
            return None
    return None


def parse_period(text: str) -> str:
    t = (text or "").lower()
    if "/tahun" in t or "per tahun" in t or "tahunan" in t:
        return "tahun"
    if "/bulan" in t or "per bulan" in t or "bulanan" in t:
        return "bulan"
    if "/minggu" in t or "mingguan" in t:
        return "minggu"
    if "/hari" in t or "harian" in t:
        return "hari"
    return "bulan"  # Mamikos default; Rumah123 also defaults bulanan for kos


def to_monthly(amount: int, period: str) -> int:
    if amount is None:
        return 0
    if period == "tahun":
        return amount // 12
    if period == "minggu":
        return amount * 4  # rough — 4 weeks/month
    if period == "hari":
        return amount * 30
    return amount


def detect_gender(text: str) -> Optional[str]:
    t = (text or "").lower()
    if "putra" in t:
        return "putra"
    if "putri" in t:
        return "putri"
    if "campur" in t:
        return "campur"
    return None


AMENITY_PATTERNS = {
    "ac":            r"\bac\b|\bair conditioning\b",
    "km_dalam":      r"km\s*dalam|kamar mandi dalam|private bath",
    "wifi":          r"\bwifi\b|wi-fi|internet",
    "kasur":         r"\bkasur\b|\bbed\b|tempat tidur",
    "lemari":        r"\blemari\b|wardrobe|closet",
    "parkir_motor":  r"parkir motor",
    "parkir_mobil":  r"parkir mobil",
    "bebas_24jam":   r"bebas\s*24\s*jam|24\s*hours?|24\s*jam",
}


def detect_amenities(text: str) -> dict:
    t = (text or "").lower()
    out = {key: bool(re.search(pat, t)) for key, pat in AMENITY_PATTERNS.items()}
    if "include listrik" in t or "termasuk listrik" in t:
        out["electricity_included"] = True
    elif "exclude listrik" in t or "tidak termasuk listrik" in t:
        out["electricity_included"] = False
    else:
        out["electricity_included"] = None
    return out


def detect_year_upfront(text: str, period: str) -> bool:
    if period != "tahun":
        return False
    t = (text or "").lower()
    return "bayar di muka" in t or "upfront" in t or "tahunan" in t


def normalize_listing(raw: dict, fx_usd_to_idr: float | None = None) -> dict:
    """Map a raw scraped listing dict into the common schema."""
    text_blob = " ".join(filter(None, [
        raw.get("title"), raw.get("description"), raw.get("price_text"),
        raw.get("badges_text"), raw.get("location_text"),
    ]))

    period = parse_period(raw.get("price_text", "") + " " + raw.get("badges_text", ""))
    raw_amount = parse_idr_amount(raw.get("price_text", ""))
    monthly = to_monthly(raw_amount or 0, period)

    out = {
        "source": raw.get("source", "unknown"),
        "id": raw.get("id"),
        "url": raw.get("url"),
        "title": raw.get("title", "").strip(),
        "raw_price_text": raw.get("price_text", "").strip(),
        "price_idr_raw": raw_amount,
        "price_idr_monthly": monthly,
        "period": period,
        "requires_year_upfront": detect_year_upfront(text_blob, period),
        "gender": detect_gender(text_blob),
        "neighborhood": raw.get("location_text"),
        "lat": raw.get("lat"),
        "lng": raw.get("lng"),
        "distance_km": raw.get("distance_km"),
        "amenities": detect_amenities(text_blob),
        "photo_count": raw.get("photo_count"),
        "posted_date": raw.get("posted_date"),
        "description_raw": raw.get("description", ""),
    }

    if fx_usd_to_idr and monthly:
        out["price_usd_monthly"] = round(monthly / fx_usd_to_idr)
    else:
        out["price_usd_monthly"] = None

    return out


if __name__ == "__main__":
    # Quick self-test
    sample = {
        "source": "mamikos",
        "id": "test-1",
        "url": "https://mamikos.com/x",
        "title": "Kos Putra Dago AC bebas 24 jam",
        "price_text": "Rp 1,8jt / bulan",
        "description": "KM dalam, AC, wifi, parkir motor, include listrik",
        "location_text": "Dago, Coblong, Bandung",
    }
    import json
    print(json.dumps(normalize_listing(sample, fx_usd_to_idr=16234.5), indent=2))
