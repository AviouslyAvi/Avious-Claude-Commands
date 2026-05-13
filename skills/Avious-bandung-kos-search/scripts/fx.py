"""IDR/USD exchange-rate fetcher with 24h disk cache.

See references/FX.md.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

CACHE = Path(__file__).parent.parent / ".fx_cache.json"
FALLBACK_RATE = 16_200.0
SOURCES = [
    ("exchangerate.host", "https://api.exchangerate.host/latest?base=USD&symbols=IDR",
     lambda j: float(j["rates"]["IDR"])),
    ("open.er-api.com", "https://open.er-api.com/v6/latest/USD",
     lambda j: float(j["rates"]["IDR"])),
]


def _fetch(url: str, timeout: int = 8) -> dict:
    req = Request(url, headers={"User-Agent": "bandung-kos-search/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _read_cache() -> dict | None:
    if not CACHE.exists():
        return None
    try:
        data = json.loads(CACHE.read_text())
        fetched = datetime.fromisoformat(data["fetched_at"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - fetched < timedelta(hours=24):
            return data
    except (json.JSONDecodeError, KeyError, ValueError):
        return None
    return None


def _write_cache(rate: float, source: str) -> None:
    CACHE.write_text(json.dumps({
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "usd_to_idr": rate,
        "source": source,
    }, indent=2))


def get_usd_to_idr() -> dict:
    cached = _read_cache()
    if cached:
        return cached
    for name, url, extract in SOURCES:
        try:
            data = _fetch(url)
            rate = extract(data)
            _write_cache(rate, name)
            return {"usd_to_idr": rate, "source": name,
                    "fetched_at": datetime.now(timezone.utc).isoformat()}
        except Exception:
            continue
    # Fallback
    return {"usd_to_idr": FALLBACK_RATE, "source": "fallback",
            "fetched_at": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    print(json.dumps(get_usd_to_idr(), indent=2))
