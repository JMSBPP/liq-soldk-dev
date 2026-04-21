"""
Utility: Convert embedded Dune JSON rows to CSV.
Run: python3 save_dune_rows.py
Reads ccop_residual_daily.json -> writes ccop_residual_daily.csv
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
json_path = HERE / "ccop_residual_daily.json"
csv_path = HERE / "ccop_residual_daily.csv"

with open(json_path) as f:
    rows = json.load(f)

fieldnames = [
    "day", "gross_volume_usd", "income_volume_usd", "small_volume_usd",
    "whale_volume_usd", "total_transfers", "income_count", "unique_senders",
    "day_of_week", "is_quincena", "is_thursday", "is_weekend",
]

with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f"Wrote {len(rows)} rows to {csv_path}")
