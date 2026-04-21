"""
BanRep TRM (COP/USD) Daily Rate Processor

Reads raw JSON from datos.gov.co Socrata API, computes daily changes and lags,
forward-fills weekends/holidays, and outputs a processed CSV.

Source: https://www.datos.gov.co/resource/mcec-87by.json
Coverage: Oct 2024 - Apr 2026

Usage:
    python3 process_trm.py

Output:
    trm_processed.csv in the same directory
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Final


# --- Frozen data types ---

@dataclass(frozen=True)
class TrmRecord:
    """Single TRM observation from datos.gov.co."""
    date: date
    date_until: date
    valor: float


@dataclass(frozen=True)
class TrmProcessedRow:
    """Processed TRM row with changes and lags."""
    date: date
    trm: float
    delta_trm: float | None         # TRM_t - TRM_{t-1}
    delta_trm_lag1: float | None     # TRM_{t-1} - TRM_{t-2}
    is_weekend: int                  # 1 if Saturday or Sunday
    is_forward_filled: int           # 1 if TRM was forward-filled from prior business day


# --- Pure functions ---

RAW_FILE: Final = "trm_daily.json"
OUTPUT_FILE: Final = "trm_processed.csv"


def parse_date(s: str) -> date:
    """Parse ISO datetime string to date."""
    return datetime.fromisoformat(s.replace("T00:00:00.000", "")).date()


def load_raw_records(filepath: Path) -> list[TrmRecord]:
    """Load and parse raw JSON from datos.gov.co."""
    with open(filepath, "r") as f:
        data = json.load(f)

    records: list[TrmRecord] = []
    for row in data:
        records.append(TrmRecord(
            date=parse_date(row["vigenciadesde"]),
            date_until=parse_date(row["vigenciahasta"]),
            valor=float(row["valor"]),
        ))
    return sorted(records, key=lambda r: r.date)


def expand_to_daily(records: list[TrmRecord]) -> dict[date, float]:
    """
    Expand TRM records to daily frequency.

    BanRep publishes one rate per business day. Weekend/holiday rates have
    vigenciadesde != vigenciahasta (e.g., Friday covers Sat-Mon).
    We forward-fill: each date in [vigenciadesde, vigenciahasta] gets the same rate.
    """
    daily: dict[date, float] = {}
    for rec in records:
        d = rec.date
        while d <= rec.date_until:
            daily[d] = rec.valor
            d += timedelta(days=1)
    return daily


def build_continuous_daily_series(
    daily_map: dict[date, float],
    start: date,
    end: date,
) -> list[tuple[date, float, bool]]:
    """
    Build continuous daily series from start to end.
    Forward-fills gaps (holidays not in vigencia ranges).
    Returns list of (date, trm, is_forward_filled).
    """
    series: list[tuple[date, float, bool]] = []
    current = start
    last_known: float | None = None

    while current <= end:
        if current in daily_map:
            last_known = daily_map[current]
            series.append((current, last_known, False))
        elif last_known is not None:
            series.append((current, last_known, True))
        # else: skip days before first observation
        current += timedelta(days=1)

    return series


def compute_changes(
    series: list[tuple[date, float, bool]],
) -> list[TrmProcessedRow]:
    """Compute ΔTRM_t and ΔTRM_{t-1} for each day."""
    rows: list[TrmProcessedRow] = []

    for i, (d, trm, is_ff) in enumerate(series):
        # ΔTRM_t = TRM_t - TRM_{t-1}
        delta_trm: float | None = None
        if i >= 1:
            delta_trm = trm - series[i - 1][1]

        # ΔTRM_{t-1} = TRM_{t-1} - TRM_{t-2}
        delta_trm_lag1: float | None = None
        if i >= 2:
            delta_trm_lag1 = series[i - 1][1] - series[i - 2][1]

        is_weekend = 1 if d.weekday() >= 5 else 0

        rows.append(TrmProcessedRow(
            date=d,
            trm=trm,
            delta_trm=delta_trm,
            delta_trm_lag1=delta_trm_lag1,
            is_weekend=is_weekend,
            is_forward_filled=1 if is_ff else 0,
        ))

    return rows


def write_csv(rows: list[TrmProcessedRow], filepath: Path) -> None:
    """Write processed TRM data to CSV."""
    header = "date,trm,delta_trm,delta_trm_lag1,is_weekend,is_forward_filled"
    lines = [header]
    for r in rows:
        dt = r.delta_trm if r.delta_trm is not None else ""
        dtl = r.delta_trm_lag1 if r.delta_trm_lag1 is not None else ""
        lines.append(
            f"{r.date},{r.trm:.2f},{dt},{dtl},{r.is_weekend},{r.is_forward_filled}"
        )
    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")


def compute_summary_stats(rows: list[TrmProcessedRow]) -> dict[str, str]:
    """Compute summary statistics for validation."""
    trm_values = [r.trm for r in rows]
    delta_values = [r.delta_trm for r in rows if r.delta_trm is not None]

    def _stats(vals: list[float], name: str) -> list[str]:
        if not vals:
            return [f"  {name}: no data"]
        sorted_v = sorted(vals)
        n = len(sorted_v)
        mean = sum(sorted_v) / n
        median = sorted_v[n // 2]
        std = (sum((v - mean) ** 2 for v in sorted_v) / n) ** 0.5
        return [
            f"  {name}:",
            f"    N = {n}",
            f"    mean = {mean:.4f}",
            f"    median = {median:.4f}",
            f"    std = {std:.4f}",
            f"    min = {min(sorted_v):.4f}",
            f"    max = {max(sorted_v):.4f}",
        ]

    lines: list[str] = []
    lines.append(f"Date range: {rows[0].date} to {rows[-1].date}")
    lines.append(f"Total rows: {len(rows)}")
    lines.append(f"Forward-filled days: {sum(1 for r in rows if r.is_forward_filled)}")
    lines.append(f"Weekend days: {sum(1 for r in rows if r.is_weekend)}")
    lines.extend(_stats(trm_values, "TRM (COP/USD)"))
    lines.extend(_stats(delta_values, "ΔTRM"))
    return {"text": "\n".join(lines)}


# --- Main ---

def main() -> None:
    script_dir = Path(__file__).parent
    raw_path = script_dir / RAW_FILE
    output_path = script_dir / OUTPUT_FILE

    if not raw_path.exists():
        print(f"ERROR: {raw_path} not found. Run the curl command first.", file=sys.stderr)
        sys.exit(1)

    # Load and parse
    records = load_raw_records(raw_path)
    print(f"Loaded {len(records)} raw TRM records")
    print(f"Date range: {records[0].date} to {records[-1].date}")

    # Expand to daily with forward-fill
    daily_map = expand_to_daily(records)
    print(f"Expanded to {len(daily_map)} daily values")

    # Build continuous series
    start = date(2024, 10, 1)
    end = records[-1].date_until  # use the last vigenciahasta
    series = build_continuous_daily_series(daily_map, start, end)
    print(f"Continuous series: {len(series)} days from {series[0][0]} to {series[-1][0]}")

    # Compute changes
    processed = compute_changes(series)

    # Write CSV
    write_csv(processed, output_path)
    print(f"Wrote {len(processed)} rows to {output_path}")

    # Summary stats
    stats = compute_summary_stats(processed)
    print("\n--- Summary Statistics ---")
    print(stats["text"])


if __name__ == "__main__":
    main()
