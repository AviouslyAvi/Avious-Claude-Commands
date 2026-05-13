"""Save a kos search result as a dated note in Fresh Obsidian Vault.

Vault path matches the `documentation` skill's preset:
  /Users/aviouslyavi/Library/CloudStorage/GoogleDrive-avimusicproductions@gmail.com/My Drive/Documents/Fresh Obsidian
Subfolder: `Bandung Kos Search/YYYY-MM-DD-{slug}.md`

Re-runs of the same query never overwrite — the slug is suffixed with a counter
if the file already exists.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

VAULT = Path(
    "/Users/aviouslyavi/Library/CloudStorage/"
    "GoogleDrive-avimusicproductions@gmail.com/My Drive/Documents/Fresh Obsidian"
)
SUBFOLDER = "Bandung Kos Search"


def slugify(text: str, max_len: int = 50) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:max_len].rstrip("-") or "search"


def _next_available_path(base: Path) -> Path:
    if not base.exists():
        return base
    stem, suffix = base.stem, base.suffix
    parent = base.parent
    n = 2
    while True:
        candidate = parent / f"{stem} ({n}){suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def render_note(query: str, criteria: dict, fx: dict, ranked: list[dict],
                all_candidates: list[dict], table_md: str) -> str:
    today = date.today().isoformat()
    fx_block = (
        f"fx_rate: {fx.get('usd_to_idr')}\n"
        f"fx_source: {fx.get('source')}\n"
        f"fx_fetched_at: {fx.get('fetched_at')}\n"
    )
    crit_lines = "\n".join(f"- **{k}**: {v}" for k, v in criteria.items() if v not in (None, [], ""))
    raw_json = json.dumps(all_candidates, indent=2, ensure_ascii=False)
    return f"""---
type: kos-search
date: {today}
query: {json.dumps(query)}
{fx_block}---

# Bandung Kos Search — {today}

**Query:** {query}

## Criteria

{crit_lines or "_(none specified)_"}

## Top {len(ranked)} ranked

{table_md}

## Notes

_(annotate after viewing — strike through dead leads, star top picks)_

## Raw candidates ({len(all_candidates)})

<details>
<summary>Click to expand</summary>

```json
{raw_json}
```

</details>
"""


def save(query: str, criteria: dict, fx: dict, ranked: list[dict],
         all_candidates: list[dict], table_md: str) -> Path:
    folder = VAULT / SUBFOLDER
    folder.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    filename = f"{today}-{slugify(query)}.md"
    target = _next_available_path(folder / filename)
    target.write_text(render_note(query, criteria, fx, ranked, all_candidates, table_md))
    return target


if __name__ == "__main__":
    p = save(
        query="kos near ITB under 2jt with AC",
        criteria={"budget_idr_monthly": 2_000_000, "must_have": ["ac"]},
        fx={"usd_to_idr": 16234.5, "source": "exchangerate.host",
            "fetched_at": "2026-04-27T08:00:00Z"},
        ranked=[],
        all_candidates=[],
        table_md="_test_",
    )
    print(f"Saved to: {p}")
