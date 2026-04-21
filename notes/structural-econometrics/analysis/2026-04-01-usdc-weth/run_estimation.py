"""
Quick estimation using the first 200 rows of Q1 data to validate the model.

Once full data is exported from Dune web UI, replace with full dataset.
This script validates that the model runs and produces sensible results.

Dune Query Sources (all non-temp, verifiable):
- Q1 Pool hourly: https://dune.com/queries/6937696
- Q2 Polygon DEX vol: https://dune.com/queries/6937702
- Q3 ETH price: https://dune.com/queries/6937699
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
import statsmodels.api as sm


REGIME_LOW: Final[int] = 500
REGIME_HIGH: Final[int] = 800
HAC_LAGS: Final[int] = 24


@dataclass(frozen=True)
class EstimationInput:
    pool_df: pd.DataFrame
    dex_vol_df: pd.DataFrame
    eth_price_df: pd.DataFrame


@dataclass(frozen=True)
class ModelResult:
    name: str
    nobs: int
    r2: float
    r2_adj: float
    coeffs: dict[str, float]
    ses: dict[str, float]
    tvals: dict[str, float]
    pvals: dict[str, float]
    summary: str


def load_json_rows(path: Path) -> pd.DataFrame:
    with open(path) as f:
        rows = json.load(f)
    df = pd.DataFrame(rows)
    if "hour" in df.columns:
        df["hour"] = pd.to_datetime(df["hour"])
    return df


def build_regression_df(inp: EstimationInput) -> pd.DataFrame:
    df = inp.pool_df.merge(inp.dex_vol_df, on="hour", how="inner")
    df = df.merge(inp.eth_price_df, on="hour", how="inner")

    df["D_low"] = (df["avg_fee"] < REGIME_LOW).astype(int)
    df["D_mid"] = ((df["avg_fee"] >= REGIME_LOW) & (df["avg_fee"] < REGIME_HIGH)).astype(int)
    df["D_high"] = (df["avg_fee"] >= REGIME_HIGH).astype(int)

    df["ln_vol"] = np.log(df["volume_usd"].clip(lower=0.01))
    df["ln_fee"] = np.log(df["avg_fee"].clip(lower=1))
    df["ln_dex"] = np.log(df["total_polygon_dex_volume_usd"].clip(lower=1))
    df["ln_eth"] = np.log(df["eth_price_usd"].clip(lower=1))
    df["ln_liq"] = np.log(pd.to_numeric(df["avg_liquidity"], errors="coerce").clip(lower=1))

    df["ln_fee_low"] = df["ln_fee"] * df["D_low"]
    df["ln_fee_mid"] = df["ln_fee"] * df["D_mid"]
    df["ln_fee_high"] = df["ln_fee"] * df["D_high"]

    df = df.sort_values("hour").dropna(subset=["ln_vol", "ln_fee", "ln_dex", "ln_eth", "ln_liq"])
    df = df[df["volume_usd"] > 0].reset_index(drop=True)
    return df


def run_ols_hac(df: pd.DataFrame, y: str, xs: list[str], name: str) -> ModelResult:
    Y = df[y]
    X = sm.add_constant(df[xs])
    res = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    return ModelResult(
        name=name, nobs=int(res.nobs),
        r2=float(res.rsquared), r2_adj=float(res.rsquared_adj),
        coeffs={k: float(v) for k, v in res.params.items()},
        ses={k: float(v) for k, v in res.bse.items()},
        tvals={k: float(v) for k, v in res.tvalues.items()},
        pvals={k: float(v) for k, v in res.pvalues.items()},
        summary=str(res.summary()),
    )


def print_result(r: ModelResult) -> None:
    print(f"\n{'='*60}")
    print(f"Model: {r.name}  |  N={r.nobs}  |  R²={r.r2:.4f}  |  Adj R²={r.r2_adj:.4f}")
    print(f"{'='*60}")
    print(f"{'Variable':<20} {'Coeff':>10} {'SE(HAC)':>10} {'t':>8} {'p':>8}")
    print("-" * 60)
    for var in r.coeffs:
        c = r.coeffs[var]
        s = r.ses[var]
        t = r.tvals[var]
        p = r.pvals[var]
        sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
        print(f"{var:<20} {c:>10.4f} {s:>10.4f} {t:>8.3f} {p:>8.4f} {sig}")

    # Derivative pricing interpretation
    for regime, key in [("LOW", "ln_fee_low"), ("MID", "ln_fee_mid"), ("HIGH", "ln_fee_high")]:
        if key in r.coeffs:
            eps = r.coeffs[key]
            income_effect = 1 + eps
            exposure = "LONG vol" if eps > -1 else "SHORT vol" if eps < -1 else "vol-neutral"
            print(f"\n  {regime}: epsilon={eps:.4f}, (1+eps)={income_effect:.4f} -> LP income is {exposure}")


def main() -> None:
    data_dir = Path("notes/structural-econometrics/data/2026-04-01-usdc-weth/raw")

    q1 = load_json_rows(data_dir / "q1_sample.json")
    q2 = load_json_rows(data_dir / "q2_sample.json")
    q3 = load_json_rows(data_dir / "q3_sample.json")

    print(f"Q1 rows: {len(q1)}, Q2 rows: {len(q2)}, Q3 rows: {len(q3)}")

    inp = EstimationInput(pool_df=q1, dex_vol_df=q2, eth_price_df=q3)
    df = build_regression_df(inp)

    print(f"\nRegression-ready: {len(df)} rows")
    print(f"Regimes: low={df['D_low'].sum()}, mid={df['D_mid'].sum()}, high={df['D_high'].sum()}")
    print(f"Fee range: {df['avg_fee'].min():.0f} - {df['avg_fee'].max():.0f}")

    # Main model
    main_xs = ["ln_fee_low", "ln_fee_mid", "ln_fee_high", "ln_dex", "ln_eth", "ln_liq"]
    main_r = run_ols_hac(df, "ln_vol", main_xs, "Regime-Specific Elasticity")
    print_result(main_r)

    # Constant elasticity
    const_r = run_ols_hac(df, "ln_vol", ["ln_fee", "ln_dex", "ln_eth", "ln_liq"], "Constant Elasticity")
    print_result(const_r)

    # Revenue model
    df["ln_rev"] = np.log((df["volume_usd"] * df["avg_fee"]).clip(lower=0.01))
    rev_r = run_ols_hac(df, "ln_rev", main_xs, "Revenue Model (coeff = 1+eps)")
    print_result(rev_r)

    # Predetermination test
    df["ln_fee_lead"] = df["ln_fee"].shift(-1)
    df_predet = df.dropna(subset=["ln_fee_lead"])
    predet_xs = main_xs + ["ln_fee_lead"]
    predet_r = run_ols_hac(df_predet, "ln_vol", predet_xs, "Predetermination Test")
    print_result(predet_r)
    if "ln_fee_lead" in predet_r.pvals:
        p = predet_r.pvals["ln_fee_lead"]
        print(f"\n  Predetermination test: p={p:.4f} -> {'PASS (p>0.05)' if p > 0.05 else 'FAIL (p<0.05)'}")


if __name__ == "__main__":
    main()
