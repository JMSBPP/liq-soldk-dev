"""
Helper: converts JSON row batches (from Dune MCP pagination) into CSVs.
Called by the main process after collecting all pages.

Usage:
    python paginate_and_save.py <json_dir> <output_csv>

Where json_dir contains files named page_000.json, page_001.json, etc.
Each file has the format: [{"col1": val1, "col2": val2, ...}, ...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


def merge_pages(json_dir: Path) -> pd.DataFrame:
    """Read all page_*.json files and concatenate into a DataFrame."""
    pages = sorted(json_dir.glob("page_*.json"))
    all_rows: list[dict] = []
    for page_file in pages:
        with open(page_file) as f:
            rows = json.load(f)
            all_rows.extend(rows)
    return pd.DataFrame(all_rows)


def main() -> None:
    json_dir = Path(sys.argv[1])
    output_csv = Path(sys.argv[2])
    df = merge_pages(json_dir)
    df.to_csv(output_csv, index=False)
    print(f"Wrote {len(df)} rows to {output_csv}")


if __name__ == "__main__":
    main()
