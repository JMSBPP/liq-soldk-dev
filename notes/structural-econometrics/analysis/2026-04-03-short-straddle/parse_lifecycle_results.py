"""Parse Dune query results for matched position lifecycles."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def main() -> None:
    results_path = Path(
        "/home/jmsbpp/.claude/projects/-home-jmsbpp-apps-liq-soldk-dev/"
        "b906ed3c-8e04-4d8f-9179-2bc945a290d0/tool-results/"
        "mcp-dune-getExecutionResults-1775236738723.txt"
    )
    with open(results_path) as f:
        data = json.load(f)

    print("State:", data["state"])
    print("Total rows:", data["resultMetadata"]["totalRowCount"])
    print("Cost:", data["resultMetadata"].get("executionCostCredits", "N/A"))
    print()

    cols = [c["name"] for c in data["resultMetadata"]["columns"]]
    print("Columns:", cols)
    print()

    rows = data["data"]["rows"]
    print(f"Returned {len(rows)} rows")
    print()

    # Group by pool_id
    pool_counts: Counter[str] = Counter(r["pool_id"] for r in rows)
    print("Positions per pool:")
    for pool, count in pool_counts.most_common():
        print(f"  {pool[:12]}... : {count} positions")
    print()

    # All positions with duration >= 7 and price data
    print("=== Positions with duration >= 7 days AND price data ===")
    candidates = []
    for r in rows:
        dur = r.get("duration_days", 0) or 0
        prp = r.get("price_range_pct")
        if dur >= 7 and prp is not None:
            candidates.append(r)
            print(f"  Pool: {r['pool_id'][:12]}...")
            print(f"    Depositor: {r['depositor']}")
            print(f"    Duration: {dur} days")
            print(f"    Deposit price: {r.get('deposit_price')}")
            print(f"    Withdraw price: {r.get('withdraw_price')}")
            print(f"    Price range %: {prp:.2f}%")
            print(f"    Swaps during: {r.get('swap_count_during')}")
            print(f"    Dep: {r.get('dep_amount0')} / {r.get('dep_amount1')}")
            print(f"    Wd:  {r.get('wd_amount0')} / {r.get('wd_amount1')}")
            print(f"    Amount0 ratio: {r.get('amount0_ratio')}")
            print(f"    Amount1 ratio: {r.get('amount1_ratio')}")
            print(f"    Deposit: {r.get('deposit_time')}")
            print(f"    Withdraw: {r.get('withdraw_time')}")
            print()

    if not candidates:
        print("  (none found)")
        print()
        # Show ALL positions with price data regardless of duration
        print("=== ALL positions with ANY price data ===")
        for r in rows:
            prp = r.get("price_range_pct")
            if prp is not None:
                dur = r.get("duration_days", 0) or 0
                print(f"  Pool: {r['pool_id'][:12]}... dur={dur}d prp={prp:.2f}% dep_price={r.get('deposit_price')}")

        print()
        print("=== ALL positions (no price filter), sorted by duration ===")
        sorted_rows = sorted(rows, key=lambda x: x.get("duration_days", 0) or 0, reverse=True)
        for r in sorted_rows[:30]:
            dur = r.get("duration_days", 0) or 0
            prp = r.get("price_range_pct")
            print(
                f"  Pool: {r['pool_id'][:12]}... dur={dur}d "
                f"dep_price={r.get('deposit_price')} prp={prp} "
                f"swaps={r.get('swap_count_during')} "
                f"dep0={r.get('dep_amount0')} dep1={r.get('dep_amount1')}"
            )


if __name__ == "__main__":
    main()
