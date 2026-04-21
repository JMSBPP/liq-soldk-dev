"""
Volume-Fee Elasticity Estimation: Algebra USDC/WETH Pool

Extracts data from Dune API via pagination, joins datasets,
and estimates the structural econometric model.

Dune Query Sources (all non-temp, verifiable):
- Q1 Pool hourly: https://dune.com/queries/6937696
- Q2 Polygon DEX vol: https://dune.com/queries/6937702
- Q3 ETH price: https://dune.com/queries/6937699
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white

# === Constants ===

RAW_DIR: Final[Path] = Path("notes/structural-econometrics/data/2026-04-01-usdc-weth/raw")
ANALYSIS_DIR: Final[Path] = Path("notes/structural-econometrics/analysis/2026-04-01-usdc-weth")

REGIME_LOW_THRESHOLD: Final[int] = 500
REGIME_HIGH_THRESHOLD: Final[int] = 800
HAC_MAXLAGS: Final[int] = 24  # hourly data, 24-hour lag structure


# === Data Loading ===

def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(path, parse_dates=["hour"])


def join_datasets(
    pool_df: pd.DataFrame,
    dex_vol_df: pd.DataFrame,
    eth_price_df: pd.DataFrame,
) -> pd.DataFrame:
    """Join pool, DEX volume, and ETH price data on hour."""
    merged = pool_df.merge(dex_vol_df, on="hour", how="inner", suffixes=("", "_dex"))
    merged = merged.merge(eth_price_df, on="hour", how="inner", suffixes=("", "_eth"))
    return merged


# === Variable Construction ===

def add_regime_dummies(
    df: pd.DataFrame,
    low_threshold: int = REGIME_LOW_THRESHOLD,
    high_threshold: int = REGIME_HIGH_THRESHOLD,
) -> pd.DataFrame:
    """Add D_low, D_mid, D_high regime dummies based on avg_fee."""
    df = df.copy()
    df["D_low"] = (df["avg_fee"] < low_threshold).astype(int)
    df["D_mid"] = ((df["avg_fee"] >= low_threshold) & (df["avg_fee"] < high_threshold)).astype(int)
    df["D_high"] = (df["avg_fee"] >= high_threshold).astype(int)
    return df


def add_log_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Add log-transformed variables for regression."""
    df = df.copy()
    df["ln_volume"] = np.log(df["volume_usd"].clip(lower=1e-10))
    df["ln_fee"] = np.log(df["avg_fee"].clip(lower=1))
    df["ln_total_dex_vol"] = np.log(df["total_volume_usd"].clip(lower=1e-10))
    df["ln_eth_price"] = np.log(df["eth_price_usd"].clip(lower=1e-10))
    df["ln_liquidity"] = np.log(df["avg_liquidity"].astype(float).clip(lower=1))
    # Interaction terms
    df["ln_fee_x_D_low"] = df["ln_fee"] * df["D_low"]
    df["ln_fee_x_D_mid"] = df["ln_fee"] * df["D_mid"]
    df["ln_fee_x_D_high"] = df["ln_fee"] * df["D_high"]
    return df


def add_lead_fee(df: pd.DataFrame) -> pd.DataFrame:
    """Add ln(phi_{t+1}) for predetermination test."""
    df = df.copy()
    df = df.sort_values("hour")
    df["ln_fee_lead"] = df["ln_fee"].shift(-1)
    return df


def prepare_regression_data(df: pd.DataFrame) -> pd.DataFrame:
    """Full pipeline: regimes, logs, leads, drop nulls."""
    df = add_regime_dummies(df)
    df = add_log_variables(df)
    df = add_lead_fee(df)
    df = df.dropna(subset=["ln_volume", "ln_fee", "ln_total_dex_vol", "ln_eth_price", "ln_liquidity"])
    df = df[df["volume_usd"] > 0]
    return df


# === Estimation ===

@dataclass(frozen=True)
class RegressionResult:
    """Immutable container for regression output."""
    name: str
    nobs: int
    r_squared: float
    r_squared_adj: float
    coefficients: dict[str, float]
    std_errors: dict[str, float]
    t_values: dict[str, float]
    p_values: dict[str, float]
    f_statistic: float
    f_pvalue: float
    summary_text: str


def estimate_ols_hac(
    df: pd.DataFrame,
    y_col: str,
    x_cols: list[str],
    name: str = "model",
    maxlags: int = HAC_MAXLAGS,
) -> RegressionResult:
    """Estimate OLS with Newey-West HAC standard errors."""
    y = df[y_col]
    X = sm.add_constant(df[x_cols])
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})

    return RegressionResult(
        name=name,
        nobs=int(model.nobs),
        r_squared=float(model.rsquared),
        r_squared_adj=float(model.rsquared_adj),
        coefficients={k: float(v) for k, v in model.params.items()},
        std_errors={k: float(v) for k, v in model.bse.items()},
        t_values={k: float(v) for k, v in model.tvalues.items()},
        p_values={k: float(v) for k, v in model.pvalues.items()},
        f_statistic=float(model.fvalue) if model.fvalue is not None else 0.0,
        f_pvalue=float(model.f_pvalue) if model.f_pvalue is not None else 1.0,
        summary_text=str(model.summary()),
    )


def estimate_main_model(df: pd.DataFrame) -> RegressionResult:
    """Main specification: regime-specific elasticities."""
    x_cols = [
        "ln_fee_x_D_low", "ln_fee_x_D_mid", "ln_fee_x_D_high",
        "ln_total_dex_vol", "ln_eth_price", "ln_liquidity",
    ]
    return estimate_ols_hac(df, "ln_volume", x_cols, name="main_regime_model")


def estimate_constant_elasticity(df: pd.DataFrame) -> RegressionResult:
    """Alternative: single epsilon (no regimes)."""
    x_cols = ["ln_fee", "ln_total_dex_vol", "ln_eth_price", "ln_liquidity"]
    return estimate_ols_hac(df, "ln_volume", x_cols, name="constant_elasticity")


def estimate_revenue_model(df: pd.DataFrame) -> RegressionResult:
    """Alternative: ln(revenue) as outcome. Coeff on ln(phi) = 1 + epsilon."""
    df = df.copy()
    df["ln_revenue"] = np.log((df["volume_usd"] * df["avg_fee"]).clip(lower=1e-10))
    x_cols = [
        "ln_fee_x_D_low", "ln_fee_x_D_mid", "ln_fee_x_D_high",
        "ln_total_dex_vol", "ln_eth_price", "ln_liquidity",
    ]
    return estimate_ols_hac(df, "ln_revenue", x_cols, name="revenue_model")


def estimate_predetermination_test(df: pd.DataFrame) -> RegressionResult:
    """Specification test: add phi_{t+1}. Should have zero coefficient."""
    df_clean = df.dropna(subset=["ln_fee_lead"])
    x_cols = [
        "ln_fee_x_D_low", "ln_fee_x_D_mid", "ln_fee_x_D_high",
        "ln_total_dex_vol", "ln_eth_price", "ln_liquidity",
        "ln_fee_lead",
    ]
    return estimate_ols_hac(df_clean, "ln_volume", x_cols, name="predetermination_test")


def estimate_quantile_regimes(df: pd.DataFrame) -> RegressionResult:
    """Sensitivity: quantile-based thresholds (p33=851, p67=896)."""
    df = df.copy()
    df["D_low"] = (df["avg_fee"] < 851).astype(int)
    df["D_mid"] = ((df["avg_fee"] >= 851) & (df["avg_fee"] < 896)).astype(int)
    df["D_high"] = (df["avg_fee"] >= 896).astype(int)
    df["ln_fee_x_D_low"] = df["ln_fee"] * df["D_low"]
    df["ln_fee_x_D_mid"] = df["ln_fee"] * df["D_mid"]
    df["ln_fee_x_D_high"] = df["ln_fee"] * df["D_high"]
    x_cols = [
        "ln_fee_x_D_low", "ln_fee_x_D_mid", "ln_fee_x_D_high",
        "ln_total_dex_vol", "ln_eth_price", "ln_liquidity",
    ]
    return estimate_ols_hac(df, "ln_volume", x_cols, name="quantile_regimes")


# === Reporting ===

def format_coeff_table(result: RegressionResult) -> str:
    """Format coefficient table as markdown."""
    lines = [
        f"### {result.name}",
        f"N = {result.nobs}, R² = {result.r_squared:.4f}, Adj R² = {result.r_squared_adj:.4f}",
        f"F = {result.f_statistic:.2f} (p = {result.f_pvalue:.4f})",
        "",
        "| Variable | Coefficient | Std Error (HAC) | t-stat | p-value | Sig |",
        "|---|---|---|---|---|---|",
    ]
    for var in result.coefficients:
        coeff = result.coefficients[var]
        se = result.std_errors[var]
        t = result.t_values[var]
        p = result.p_values[var]
        sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
        lines.append(f"| {var} | {coeff:.4f} | {se:.4f} | {t:.3f} | {p:.4f} | {sig} |")
    return "\n".join(lines)


def interpret_elasticity(result: RegressionResult) -> str:
    """Interpret epsilon for derivative pricing."""
    lines = ["### Derivative Pricing Implications\n"]
    for regime in ["D_low", "D_mid", "D_high"]:
        key = f"ln_fee_x_{regime}"
        if key in result.coefficients:
            eps = result.coefficients[key]
            p = result.p_values[key]
            income_effect = 1 + eps
            if eps > -1:
                vol_exposure = "LONG vol"
                floor_price = "cheap (rarely pays in stress)"
            elif eps < -1:
                vol_exposure = "SHORT vol"
                floor_price = "expensive (pays in stress)"
            else:
                vol_exposure = "vol-neutral"
                floor_price = "standard pricing"
            lines.append(
                f"- **{regime}**: epsilon = {eps:.4f} (p={p:.4f}), "
                f"(1+epsilon) = {income_effect:.4f} -> LP income is **{vol_exposure}** -> "
                f"IncomeFloor is {floor_price}"
            )
    return "\n".join(lines)


# === Main ===

def main() -> None:
    """Run full estimation pipeline."""
    print("Loading data...")
    pool_df = load_csv(RAW_DIR / "q1_pool_hourly.csv")
    dex_vol_df = load_csv(RAW_DIR / "q2_polygon_dex_vol.csv")
    eth_price_df = load_csv(RAW_DIR / "q3_eth_price.csv")

    print(f"Pool rows: {len(pool_df)}, DEX vol rows: {len(dex_vol_df)}, ETH price rows: {len(eth_price_df)}")

    print("Joining datasets...")
    merged = join_datasets(pool_df, dex_vol_df, eth_price_df)
    print(f"Merged rows: {len(merged)}")

    print("Preparing regression data...")
    df = prepare_regression_data(merged)
    print(f"Regression-ready rows: {len(df)}")
    print(f"Regime counts: low={df['D_low'].sum()}, mid={df['D_mid'].sum()}, high={df['D_high'].sum()}")

    # === Main Model ===
    print("\nEstimating main model (regime-specific elasticities)...")
    main_result = estimate_main_model(df)
    print(main_result.summary_text)

    # === Alternative: Constant Elasticity ===
    print("\nEstimating constant elasticity model...")
    const_result = estimate_constant_elasticity(df)

    # === Alternative: Revenue Model ===
    print("\nEstimating revenue model (coeff = 1 + epsilon)...")
    rev_result = estimate_revenue_model(df)

    # === Specification Test: Predetermination ===
    print("\nRunning predetermination test (future fee)...")
    predet_result = estimate_predetermination_test(df)

    # === Sensitivity: Quantile Regimes ===
    print("\nEstimating with quantile-based regime thresholds...")
    quant_result = estimate_quantile_regimes(df)

    # === Write Results ===
    print("\nWriting results...")

    # estimates.md
    estimates_md = "\n\n".join([
        "# Estimation Results: Volume-Fee Elasticity\n",
        "## Data Sources (Dune, all verifiable)",
        "- Q1 Pool hourly: https://dune.com/queries/6937696",
        "- Q2 Polygon DEX vol: https://dune.com/queries/6937702",
        "- Q3 ETH price: https://dune.com/queries/6937699\n",
        "## Main Model: Regime-Specific Elasticities\n",
        format_coeff_table(main_result),
        interpret_elasticity(main_result),
        "\n---\n",
        "## Full statsmodels output\n",
        f"```\n{main_result.summary_text}\n```",
    ])
    (ANALYSIS_DIR / "estimates.md").write_text(estimates_md)

    # spec_tests.md
    spec_tests_lines = [
        "# Specification Tests\n",
        "## Data Sources (Dune, all verifiable)",
        "- Q1: https://dune.com/queries/6937696",
        "- Q2: https://dune.com/queries/6937702",
        "- Q3: https://dune.com/queries/6937699\n",
        "## Test 1: Sign Restriction (epsilon < 0)\n",
    ]
    for regime in ["D_low", "D_mid", "D_high"]:
        key = f"ln_fee_x_{regime}"
        if key in main_result.coefficients:
            eps = main_result.coefficients[key]
            p = main_result.p_values[key]
            passed = "PASS" if eps < 0 else "FAIL"
            spec_tests_lines.append(f"- {regime}: epsilon = {eps:.4f}, p = {p:.4f} -> **{passed}**")

    spec_tests_lines.extend([
        "\n## Test 2: Ordering |epsilon_high| > |epsilon_mid| > |epsilon_low|\n",
    ])
    eps_vals = {}
    for regime in ["D_low", "D_mid", "D_high"]:
        key = f"ln_fee_x_{regime}"
        if key in main_result.coefficients:
            eps_vals[regime] = abs(main_result.coefficients[key])
    if len(eps_vals) == 3:
        ordering_holds = eps_vals["D_high"] > eps_vals["D_mid"] > eps_vals["D_low"]
        spec_tests_lines.append(
            f"|epsilon_low| = {eps_vals['D_low']:.4f}, "
            f"|epsilon_mid| = {eps_vals['D_mid']:.4f}, "
            f"|epsilon_high| = {eps_vals['D_high']:.4f}"
        )
        spec_tests_lines.append(f"Ordering holds: **{'PASS' if ordering_holds else 'FAIL'}**")

    spec_tests_lines.extend([
        "\n## Test 3: Predetermination (future fee coefficient = 0)\n",
        format_coeff_table(predet_result),
    ])
    if "ln_fee_lead" in predet_result.p_values:
        p_lead = predet_result.p_values["ln_fee_lead"]
        coeff_lead = predet_result.coefficients["ln_fee_lead"]
        passed = "PASS" if p_lead > 0.05 else "FAIL"
        spec_tests_lines.append(
            f"\nFuture fee coefficient = {coeff_lead:.4f}, p = {p_lead:.4f} -> **{passed}**"
        )
        spec_tests_lines.append(
            f"{'Predetermination holds: future fee does not predict current volume.' if passed == 'PASS' else 'WARNING: Predetermination may be violated.'}"
        )

    (ANALYSIS_DIR / "spec_tests.md").write_text("\n".join(spec_tests_lines))

    # sensitivity.md
    sensitivity_md = "\n\n".join([
        "# Sensitivity Analysis\n",
        "## Data Sources (Dune, all verifiable)",
        "- Q1: https://dune.com/queries/6937696",
        "- Q2: https://dune.com/queries/6937702",
        "- Q3: https://dune.com/queries/6937699\n",
        "## Alternative 1: Constant Elasticity (no regimes)\n",
        format_coeff_table(const_result),
        "\n## Alternative 2: Revenue as Outcome (coeff = 1 + epsilon)\n",
        format_coeff_table(rev_result),
        interpret_elasticity(rev_result),
        "\n## Sensitivity: Quantile-Based Regime Thresholds (851/896)\n",
        format_coeff_table(quant_result),
        interpret_elasticity(quant_result),
    ])
    (ANALYSIS_DIR / "sensitivity.md").write_text(sensitivity_md)

    # summary.md
    summary_lines = [
        "# Executive Summary: Volume-Fee Elasticity Estimation\n",
        "## Data Sources (Dune, all verifiable)",
        "- Q1 Pool hourly: https://dune.com/queries/6937696",
        "- Q2 Polygon DEX vol: https://dune.com/queries/6937702",
        "- Q3 ETH price: https://dune.com/queries/6937699",
        "- Q4 Fee distribution: https://dune.com/queries/6937700\n",
        f"## Sample: {len(df)} hourly observations, Jan-Mar 2026\n",
        f"## Regime Distribution",
        f"- Low (fee < 500): {df['D_low'].sum()} hours ({100*df['D_low'].mean():.1f}%)",
        f"- Mid (500-799): {df['D_mid'].sum()} hours ({100*df['D_mid'].mean():.1f}%)",
        f"- High (>= 800): {df['D_high'].sum()} hours ({100*df['D_high'].mean():.1f}%)\n",
        "## Key Findings\n",
    ]

    for regime in ["D_low", "D_mid", "D_high"]:
        key = f"ln_fee_x_{regime}"
        if key in main_result.coefficients:
            eps = main_result.coefficients[key]
            p = main_result.p_values[key]
            income_effect = 1 + eps
            if eps > -1:
                conclusion = "LP income is LONG vol -> IncomeFloor is cheap"
            elif eps < -1:
                conclusion = "LP income is SHORT vol -> IncomeFloor is expensive"
            else:
                conclusion = "LP income is vol-neutral"
            sig = "significant" if p < 0.05 else "not significant"
            summary_lines.append(
                f"- **{regime}**: epsilon = {eps:.4f} (p={p:.4f}, {sig}), "
                f"(1+epsilon) = {income_effect:.4f} -> {conclusion}"
            )

    summary_lines.extend([
        f"\n## Model Fit",
        f"- R² = {main_result.r_squared:.4f}",
        f"- Adjusted R² = {main_result.r_squared_adj:.4f}",
        f"- F-statistic = {main_result.f_statistic:.2f} (p = {main_result.f_pvalue:.6f})",
    ])

    (ANALYSIS_DIR / "summary.md").write_text("\n".join(summary_lines))

    print("\nDone. Results written to:")
    print(f"  {ANALYSIS_DIR / 'estimates.md'}")
    print(f"  {ANALYSIS_DIR / 'spec_tests.md'}")
    print(f"  {ANALYSIS_DIR / 'sensitivity.md'}")
    print(f"  {ANALYSIS_DIR / 'summary.md'}")


if __name__ == "__main__":
    main()
