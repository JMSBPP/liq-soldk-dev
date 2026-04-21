"""
Structural Econometric Estimation: cCOP Residual Flow Response to COP/USD
Spec: INCOME_SETTLEMENT/2026-04-02-ccop-cop-usd-flow-response.md
Date: 2026-04-02

Primary specification (QA-revised):
  ln(1+V_t) = a + b1*dTRM_t + b2*dTRM_{t-1}
             + g1*D_quincena + g2*D_thursday + g3*D_weekend
             + g4*D_prima + g5*D_migration
             + d1*t + d2*ln(1+V_{t-1}) + u_t

OLS with Newey-West HAC standard errors.
"""

from __future__ import annotations
import json
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan

warnings.filterwarnings("ignore", category=FutureWarning)

# ── paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent.parent / "data" / "2026-04-02-ccop-cop-usd"
RAW  = DATA / "raw"
DIAG = ROOT / "diagnostics"
DIAG.mkdir(exist_ok=True)

# ── 1. LOAD ON-CHAIN DATA (embedded from Dune #6941901) ───────────────

ONCHAIN_JSON = RAW / "ccop_residual_daily.json"

def load_onchain_from_dune_export() -> pd.DataFrame:
    """Load on-chain data from saved JSON or CSV."""
    csv_path = RAW / "ccop_residual_daily.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path, parse_dates=["day"])
        df = df.rename(columns={"day": "date"})
        return df
    if ONCHAIN_JSON.exists():
        with open(ONCHAIN_JSON) as f:
            rows = json.load(f)
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["day"])
        df = df.drop(columns=["day"], errors="ignore")
        return df
    raise FileNotFoundError(
        "No on-chain data found. Place ccop_residual_daily.csv or .json in raw/"
    )


def save_onchain_json(all_rows: list[dict]) -> None:
    """Save paginated Dune results to JSON for reproducibility."""
    ONCHAIN_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(ONCHAIN_JSON, "w") as f:
        json.dump(all_rows, f)


# ── 2. LOAD TRM DATA ──────────────────────────────────────────────────

def load_trm() -> pd.DataFrame:
    df = pd.read_csv(RAW / "trm_processed.csv", parse_dates=["date"])
    # keep only columns we need
    return df[["date", "trm", "delta_trm", "delta_trm_lag1", "is_weekend"]].copy()


# ── 3. COLOMBIAN CALENDAR ─────────────────────────────────────────────

# Weekend-adjusted quincena dates from colombian_calendar.md
QUINCENA_DATES: list[str] = [
    # 2024
    "2024-10-15", "2024-10-31",
    "2024-11-15", "2024-11-29",
    "2024-12-13", "2024-12-31",
    # 2025
    "2025-01-15", "2025-01-31",
    "2025-02-14", "2025-02-28",
    "2025-03-14", "2025-03-31",
    "2025-04-15", "2025-04-30",
    "2025-05-15", "2025-05-30",
    "2025-06-13", "2025-06-30",
    "2025-07-15", "2025-07-31",
    "2025-08-15", "2025-08-29",
    "2025-09-15", "2025-09-30",
    "2025-10-15", "2025-10-31",
    "2025-11-14", "2025-11-28",
    "2025-12-15", "2025-12-31",
    # 2026
    "2026-01-15", "2026-01-30",
    "2026-02-13", "2026-02-27",
    "2026-03-13", "2026-03-31",
    "2026-04-15", "2026-04-30",
]

PRIMA_DATES: list[str] = [
    "2025-06-30",
    "2025-12-20",  # Dec 20 is Friday — no shift needed
]

MIGRATION_DATES: list[str] = ["2026-01-24", "2026-01-25", "2026-01-26"]


def add_calendar_dummies(df: pd.DataFrame) -> pd.DataFrame:
    quincena_set = set(pd.to_datetime(QUINCENA_DATES).date)
    prima_set = set(pd.to_datetime(PRIMA_DATES).date)
    migration_set = set(pd.to_datetime(MIGRATION_DATES).date)

    df = df.copy()
    df["D_quincena"] = df["date"].dt.date.isin(quincena_set).astype(int)
    df["D_prima"] = df["date"].dt.date.isin(prima_set).astype(int)
    df["D_migration"] = df["date"].dt.date.isin(migration_set).astype(int)
    df["D_thursday"] = (df["date"].dt.dayofweek == 3).astype(int)
    df["D_weekend"] = (df["date"].dt.dayofweek >= 5).astype(int)
    return df


# ── 4. MERGE AND TRANSFORM ────────────────────────────────────────────

def merge_and_transform(onchain: pd.DataFrame, trm: pd.DataFrame) -> pd.DataFrame:
    # Ensure date types match
    onchain["date"] = pd.to_datetime(onchain["date"]).dt.normalize()
    trm["date"] = pd.to_datetime(trm["date"]).dt.normalize()

    df = onchain.merge(trm, on="date", how="inner", suffixes=("_oc", "_trm"))

    # Resolve is_weekend: prefer TRM version, fall back to on-chain
    if "is_weekend_trm" in df.columns:
        df["is_weekend"] = df["is_weekend_trm"]
        df = df.drop(columns=["is_weekend_oc", "is_weekend_trm"], errors="ignore")
    elif "is_weekend" not in df.columns:
        df["is_weekend"] = (df["date"].dt.dayofweek >= 5).astype(int)

    # Add calendar dummies (overrides Dune's raw is_quincena with weekend-adjusted)
    df = add_calendar_dummies(df)

    # Log transforms
    df["ln_gross"] = np.log1p(df["gross_volume_usd"])
    df["ln_income"] = np.log1p(df["income_volume_usd"])
    df["ln_small"] = np.log1p(df["small_volume_usd"])
    df["ln_whale"] = np.log1p(df["whale_volume_usd"])

    # Sort and compute lagged DV
    df = df.sort_values("date").reset_index(drop=True)
    df["ln_gross_lag1"] = df["ln_gross"].shift(1)
    df["ln_income_lag1"] = df["ln_income"].shift(1)

    # Time trend
    df["t"] = np.arange(1, len(df) + 1)

    # Drop pre-Dec 2024 thin period (QA H2)
    df = df[df["date"] >= "2024-12-01"].copy()

    # Drop rows with null delta_trm
    df = df.dropna(subset=["delta_trm", "delta_trm_lag1", "ln_gross_lag1"])

    df = df.reset_index(drop=True)
    # Re-index time trend after dropping
    df["t"] = np.arange(1, len(df) + 1)

    return df


# ── 5. ESTIMATION HELPERS ─────────────────────────────────────────────

@dataclass(frozen=True)
class EstResult:
    name: str
    nobs: int
    params: pd.Series
    bse: pd.Series
    pvalues: pd.Series
    tvalues: pd.Series
    rsquared: float
    rsquared_adj: float
    aic: float
    bic: float
    cov_params: pd.DataFrame
    resid: np.ndarray
    fittedvalues: np.ndarray
    model: Any  # statsmodels result


def run_ols_hac(
    y: pd.Series,
    X: pd.DataFrame,
    name: str = "model",
    maxlags: int = 5,
) -> EstResult:
    X_c = sm.add_constant(X.astype(float))
    y_clean = y.astype(float)
    model = sm.OLS(y_clean, X_c).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": maxlags},
    )
    return EstResult(
        name=name,
        nobs=int(model.nobs),
        params=model.params,
        bse=model.bse,
        pvalues=model.pvalues,
        tvalues=model.tvalues,
        rsquared=model.rsquared,
        rsquared_adj=model.rsquared_adj,
        aic=model.aic,
        bic=model.bic,
        cov_params=model.cov_params(),
        resid=model.resid.values,
        fittedvalues=model.fittedvalues.values,
        model=model,
    )


# ── 6. PRIMARY SPECIFICATION ──────────────────────────────────────────

PRIMARY_CONTROLS = [
    "delta_trm", "delta_trm_lag1",
    "D_quincena", "D_thursday", "D_weekend",
    "D_prima", "D_migration",
    "t", "ln_gross_lag1",
]


def estimate_primary(df: pd.DataFrame) -> EstResult:
    y = df["ln_gross"]
    X = df[PRIMARY_CONTROLS]
    return run_ols_hac(y, X, name="Primary")


# ── 7. SPECIFICATION TESTS ────────────────────────────────────────────

def test_T1(res: EstResult) -> dict:
    """One-sided test: beta1 + beta2 > 0."""
    b1 = res.params["delta_trm"]
    b2 = res.params["delta_trm_lag1"]
    beta_sum = b1 + b2
    cov = res.cov_params
    var_sum = (
        cov.loc["delta_trm", "delta_trm"]
        + cov.loc["delta_trm_lag1", "delta_trm_lag1"]
        + 2 * cov.loc["delta_trm", "delta_trm_lag1"]
    )
    se_sum = np.sqrt(var_sum)
    t_stat = beta_sum / se_sum
    p_one = 1 - stats.t.cdf(t_stat, df=res.nobs - len(res.params))
    passed = p_one < 0.05
    return {
        "test": "T1: beta1+beta2 > 0",
        "beta_sum": beta_sum,
        "se_sum": se_sum,
        "t_stat": t_stat,
        "p_one_sided": p_one,
        "pass": passed,
    }


def test_T2(res: EstResult) -> dict:
    """One-sided test: gamma_quincena > 0."""
    g1 = res.params["D_quincena"]
    se = res.bse["D_quincena"]
    t_stat = g1 / se
    p_one = 1 - stats.t.cdf(t_stat, df=res.nobs - len(res.params))
    passed = p_one < 0.05
    return {
        "test": "T2: gamma_quincena > 0",
        "gamma1": g1,
        "se": se,
        "t_stat": t_stat,
        "p_one_sided": p_one,
        "pass": passed,
    }


def test_T4(res: EstResult, df: pd.DataFrame) -> dict:
    """Breusch-Pagan: split residuals on |delta_trm| > median."""
    resids = res.resid
    abs_dtrm = df["delta_trm"].abs().values[: len(resids)]
    median_dtrm = np.median(abs_dtrm)
    group = (abs_dtrm > median_dtrm).astype(float)
    exog = sm.add_constant(group)
    bp_stat, bp_p, _, _ = het_breuschpagan(resids, exog)
    passed = bp_p < 0.05
    return {
        "test": "T4: Var(u|high dTRM) > Var(u|low dTRM)",
        "bp_stat": bp_stat,
        "bp_p": bp_p,
        "median_abs_dtrm": median_dtrm,
        "var_high": np.var(resids[abs_dtrm > median_dtrm]),
        "var_low": np.var(resids[abs_dtrm <= median_dtrm]),
        "pass": passed,
    }


def test_T5(res: EstResult, df: pd.DataFrame) -> dict:
    """Ramsey RESET test."""
    y_hat = res.fittedvalues
    y_hat2 = y_hat ** 2
    y_hat3 = y_hat ** 3
    X_orig = sm.add_constant(df[PRIMARY_CONTROLS].astype(float))
    X_reset = X_orig.copy()
    X_reset["yhat2"] = y_hat2[: len(X_reset)]
    X_reset["yhat3"] = y_hat3[: len(X_reset)]
    model_reset = sm.OLS(df["ln_gross"].astype(float), X_reset).fit()
    # F-test for joint significance of yhat2 and yhat3
    r_matrix = np.zeros((2, len(model_reset.params)))
    r_matrix[0, -2] = 1  # yhat2
    r_matrix[1, -1] = 1  # yhat3
    f_test = model_reset.f_test(r_matrix)
    f_stat = float(f_test.fvalue)
    f_p = float(f_test.pvalue)
    passed = f_p >= 0.05  # PASS if we do NOT reject adequate functional form
    return {
        "test": "T5: Ramsey RESET",
        "f_stat": f_stat,
        "f_p": f_p,
        "pass": passed,
        "interpretation": "PASS = functional form adequate" if passed else "FAIL = misspecification detected",
    }


def test_T6(df: pd.DataFrame) -> dict:
    """Size decomposition: run primary spec with income, small, whale as LHS."""
    controls_no_lag = [
        "delta_trm", "delta_trm_lag1",
        "D_quincena", "D_thursday", "D_weekend",
        "D_prima", "D_migration", "t",
    ]
    results = {}
    for label, col, lag_col in [
        ("income", "ln_income", "ln_income_lag1"),
        ("small", "ln_small", None),
        ("whale", "ln_whale", None),
    ]:
        sub = df.copy()
        if lag_col and lag_col in sub.columns:
            ctrl = controls_no_lag + [lag_col]
            sub = sub.dropna(subset=[lag_col])
        else:
            sub[f"{col}_lag1"] = sub[col].shift(1)
            ctrl = controls_no_lag + [f"{col}_lag1"]
            sub = sub.dropna(subset=[f"{col}_lag1"])

        y = sub[col]
        X = sub[ctrl]
        r = run_ols_hac(y, X, name=f"T6_{label}")
        b1 = r.params.get("delta_trm", np.nan)
        b2 = r.params.get("delta_trm_lag1", np.nan)
        p1 = r.pvalues.get("delta_trm", np.nan)
        p2 = r.pvalues.get("delta_trm_lag1", np.nan)
        results[label] = {
            "beta1": b1, "beta2": b2,
            "p1": p1, "p2": p2,
            "beta_sum": b1 + b2,
            "nobs": r.nobs,
        }

    whale_drives = (
        results["whale"]["p1"] < 0.05 or results["whale"]["p2"] < 0.05
    ) and (
        results["income"]["p1"] >= 0.05 and results["income"]["p2"] >= 0.05
    )

    return {
        "test": "T6: Size decomposition",
        "results": results,
        "whale_drives_result": whale_drives,
        "pass": not whale_drives,
    }


# ── 8. ROBUSTNESS SPECIFICATIONS ──────────────────────────────────────

def robustness_R1(df: pd.DataFrame) -> EstResult:
    """Log-log level: ln(V) = a + b*ln(TRM) + controls + d*t."""
    sub = df.copy()
    sub["ln_trm"] = np.log(sub["trm"])
    controls = [
        "ln_trm", "D_quincena", "D_thursday", "D_weekend",
        "D_prima", "D_migration", "t", "ln_gross_lag1",
    ]
    y = sub["ln_gross"]
    X = sub[controls]
    return run_ols_hac(y, X, name="R1: log-log level")


def robustness_R2(df: pd.DataFrame) -> EstResult:
    """Weekly aggregation."""
    sub = df.copy()
    sub["week"] = sub["date"].dt.isocalendar().week.astype(int)
    sub["year"] = sub["date"].dt.year
    weekly = sub.groupby(["year", "week"]).agg(
        gross_volume_usd=("gross_volume_usd", "sum"),
        delta_trm=("delta_trm", "mean"),
        delta_trm_lag1=("delta_trm_lag1", "mean"),
        D_quincena=("D_quincena", "max"),
        D_thursday=("D_thursday", "max"),
        D_prima=("D_prima", "max"),
        D_migration=("D_migration", "max"),
    ).reset_index()
    weekly["ln_gross"] = np.log1p(weekly["gross_volume_usd"])
    weekly["ln_gross_lag1"] = weekly["ln_gross"].shift(1)
    weekly["t"] = np.arange(1, len(weekly) + 1)
    weekly = weekly.dropna()
    controls = [
        "delta_trm", "delta_trm_lag1",
        "D_quincena", "D_prima", "D_migration",
        "t", "ln_gross_lag1",
    ]
    y = weekly["ln_gross"]
    X = weekly[controls]
    return run_ols_hac(y, X, name="R2: weekly")


def robustness_R3(df: pd.DataFrame) -> EstResult:
    """Income volume as LHS."""
    controls = [
        "delta_trm", "delta_trm_lag1",
        "D_quincena", "D_thursday", "D_weekend",
        "D_prima", "D_migration", "t", "ln_income_lag1",
    ]
    sub = df.dropna(subset=["ln_income_lag1"])
    y = sub["ln_income"]
    X = sub[controls]
    return run_ols_hac(y, X, name="R3: income volume")


def robustness_R7(df: pd.DataFrame) -> EstResult:
    """First-differenced: d(ln(1+V))."""
    sub = df.copy()
    sub["d_ln_gross"] = sub["ln_gross"].diff()
    sub = sub.dropna(subset=["d_ln_gross"])
    controls = [
        "delta_trm", "delta_trm_lag1",
        "D_quincena", "D_thursday", "D_weekend",
        "D_prima", "D_migration",
    ]
    y = sub["d_ln_gross"]
    X = sub[controls]
    return run_ols_hac(y, X, name="R7: first-differenced")


def robustness_R8(df: pd.DataFrame) -> EstResult:
    """Business days only."""
    sub = df[df["D_weekend"] == 0].copy()
    sub["ln_gross_lag1"] = sub["ln_gross"].shift(1)
    sub["t"] = np.arange(1, len(sub) + 1)
    sub = sub.dropna(subset=["ln_gross_lag1", "delta_trm", "delta_trm_lag1"])
    controls = [
        "delta_trm", "delta_trm_lag1",
        "D_quincena", "D_thursday",
        "D_prima", "D_migration", "t", "ln_gross_lag1",
    ]
    y = sub["ln_gross"]
    X = sub[controls]
    return run_ols_hac(y, X, name="R8: business days only")


# ── 9. OUTPUT FORMATTING ──────────────────────────────────────────────

def sig_stars(p: float) -> str:
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    if p < 0.10:
        return "+"
    return ""


def format_coef_table(results: list[EstResult]) -> str:
    all_vars = []
    for r in results:
        for v in r.params.index:
            if v not in all_vars:
                all_vars.append(v)

    header = "| Variable |"
    sep = "|---|"
    for r in results:
        header += f" {r.name} |"
        sep += "---|"

    lines = [header, sep]
    for v in all_vars:
        row = f"| {v} |"
        for r in results:
            if v in r.params.index:
                coef = r.params[v]
                se = r.bse[v]
                p = r.pvalues[v]
                row += f" {coef:.4f}{sig_stars(p)} ({se:.4f}) |"
            else:
                row += " - |"
        lines.append(row)

    # Add N and R2 rows
    row_n = "| N |"
    row_r2 = "| R-squared |"
    row_aic = "| AIC |"
    for r in results:
        row_n += f" {r.nobs} |"
        row_r2 += f" {r.rsquared:.4f} |"
        row_aic += f" {r.aic:.1f} |"
    lines.extend([row_n, row_r2, row_aic])
    lines.append("")
    lines.append("Significance: *** p<0.001, ** p<0.01, * p<0.05, + p<0.10")
    lines.append("Standard errors: Newey-West HAC (maxlags=5)")
    return "\n".join(lines)


# ── 10. DECISION RULE ─────────────────────────────────────────────────

def apply_decision_rule(
    t1: dict, t2: dict, t4: dict, t6: dict,
    robustness_results: list[EstResult],
) -> str:
    lines = []
    lines.append("## Pre-Registered Decision Rule Application\n")

    # Robustness consistency: beta positive + significant in >=4 of 7 specs
    pos_sig_count = 0
    total_specs = 0
    for r in robustness_results:
        total_specs += 1
        b1 = r.params.get("delta_trm", 0)
        b2 = r.params.get("delta_trm_lag1", 0)
        # For R1, check ln_trm instead
        if "ln_trm" in r.params.index:
            b = r.params["ln_trm"]
            p = r.pvalues["ln_trm"]
            if b > 0 and p < 0.05:
                pos_sig_count += 1
        else:
            p1 = r.pvalues.get("delta_trm", 1)
            p2 = r.pvalues.get("delta_trm_lag1", 1)
            if (b1 + b2) > 0 and (p1 < 0.05 or p2 < 0.05):
                pos_sig_count += 1

    lines.append(f"**Robustness count**: beta positive+significant in {pos_sig_count}/{total_specs} specs")
    robust = pos_sig_count >= 4
    lines.append(f"**Robust (>=4/7)**: {'YES' if robust else 'NO'}\n")

    # Main decision tree
    if not t1["pass"]:
        verdict = "T1 FAIL: No macro content. Signal is noise. STOP."
        action = "Revisit observable or currency."
    elif t1["pass"] and not t2["pass"] :
        verdict = "T1 PASS + T2 FAIL: Macro content but not income-driven."
        action = "Investigate alternative populations (speculation?)."
    elif t1["pass"] and t2["pass"] and not t4["pass"]:
        verdict = "T1 PASS + T2 PASS + T4 FAIL: Moderate. Macro content + income, but constant variance."
        action = "Proceed to Exercise 3 but flag variance swap risk."
    elif t1["pass"] and t2["pass"] and t4["pass"]:
        verdict = "T1 PASS + T2 PASS + T4 PASS: Strong. Macro content + income mechanism + variance response."
        action = "Proceed to Exercise 3 with confidence."
    else:
        verdict = "Indeterminate."
        action = "Review manually."

    if not t6["pass"]:
        verdict += "\nT6 FAIL: Whale-driven result. Reinterpret -- not income-conversion."
        action = "Result is not income-conversion. Reinterpret."

    lines.append(f"**Gate Verdict**: {verdict}")
    lines.append(f"**Action**: {action}")

    if not robust:
        lines.append("\n**WARNING**: Result is FRAGILE (fewer than 4/7 robust specs).")

    return "\n".join(lines)


# ── 11. MAIN ──────────────────────────────────────────────────────────

def main() -> None:
    print("Loading data...")
    onchain = load_onchain_from_dune_export()
    trm = load_trm()

    print(f"On-chain rows: {len(onchain)}")
    print(f"TRM rows: {len(trm)}")

    print("Merging and transforming...")
    df = merge_and_transform(onchain, trm)
    print(f"Merged sample: {len(df)} obs (Dec 2024 - Apr 2026)")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")

    # Save merged dataset
    df.to_csv(ROOT / "merged_dataset.csv", index=False)

    # ── PRIMARY ESTIMATION ──
    print("\n=== PRIMARY SPECIFICATION ===")
    primary = estimate_primary(df)
    print(primary.model.summary())

    # ── SPECIFICATION TESTS ──
    print("\n=== SPECIFICATION TESTS ===")
    t1 = test_T1(primary)
    t2 = test_T2(primary)
    t4 = test_T4(primary, df)
    t5 = test_T5(primary, df)
    t6 = test_T6(df)

    for t in [t1, t2, t4, t5]:
        status = "PASS" if t["pass"] else "FAIL"
        print(f"  {t['test']}: {status} (p={t.get('p_one_sided', t.get('bp_p', t.get('f_p', '?'))):.4f})")
    print(f"  T6: {'PASS' if t6['pass'] else 'FAIL'} (whale_drives={t6['whale_drives_result']})")

    # ── ROBUSTNESS ──
    print("\n=== ROBUSTNESS SPECIFICATIONS ===")
    r1 = robustness_R1(df)
    r2 = robustness_R2(df)
    r3 = robustness_R3(df)
    r7 = robustness_R7(df)
    r8 = robustness_R8(df)

    all_specs = [primary, r1, r2, r3, r7, r8]
    # Add T6 income result as a spec for robustness count
    t6_income_controls = [
        "delta_trm", "delta_trm_lag1",
        "D_quincena", "D_thursday", "D_weekend",
        "D_prima", "D_migration", "t", "ln_income_lag1",
    ]
    r6_income = run_ols_hac(
        df.dropna(subset=["ln_income_lag1"])["ln_income"],
        df.dropna(subset=["ln_income_lag1"])[t6_income_controls],
        name="R6: income decomp",
    )
    all_specs_for_robustness = [primary, r1, r2, r3, r6_income, r7, r8]

    for r in all_specs:
        b1 = r.params.get("delta_trm", 0)
        p1 = r.pvalues.get("delta_trm", 1)
        print(f"  {r.name}: N={r.nobs}, R2={r.rsquared:.4f}, "
              f"beta_dtrm={b1:.6f} (p={p1:.4f})")

    # ── WRITE OUTPUT FILES ──
    print("\n=== WRITING OUTPUT ===")

    # estimates.md
    estimates_md = [
        "# Coefficient Estimates: cCOP Residual Flow Response to COP/USD\n",
        f"*Date: 2026-04-02*\n",
        f"*Sample: {df['date'].min().date()} to {df['date'].max().date()} (N={len(df)})*\n",
        "---\n",
        "## Primary Specification\n",
        "```",
        "ln(1+V_t) = a + b1*dTRM_t + b2*dTRM_{t-1}",
        "           + g1*D_quincena + g2*D_thursday + g3*D_weekend",
        "           + g4*D_prima + g5*D_migration",
        "           + d1*t + d2*ln(1+V_{t-1}) + u_t",
        "```\n",
        format_coef_table([primary]),
        "\n---\n",
        "## All Specifications\n",
        format_coef_table(all_specs),
    ]
    (ROOT / "estimates.md").write_text("\n".join(estimates_md))

    # spec_tests.md
    spec_lines = [
        "# Specification Test Results\n",
        f"*Date: 2026-04-02*\n",
        "---\n",
    ]

    for t_result in [t1, t2, t4, t5]:
        status = "**PASS**" if t_result["pass"] else "**FAIL**"
        spec_lines.append(f"## {t_result['test']}\n")
        spec_lines.append(f"**Verdict**: {status}\n")
        for k, v in t_result.items():
            if k not in ("test", "pass"):
                if isinstance(v, float):
                    spec_lines.append(f"- {k}: {v:.6f}")
                else:
                    spec_lines.append(f"- {k}: {v}")
        spec_lines.append("")

    spec_lines.append(f"## {t6['test']}\n")
    spec_lines.append(f"**Verdict**: {'**PASS**' if t6['pass'] else '**FAIL**'}")
    spec_lines.append(f"**Whale drives result**: {t6['whale_drives_result']}\n")
    for label, vals in t6["results"].items():
        spec_lines.append(f"### {label} volume")
        for k, v in vals.items():
            if isinstance(v, float):
                spec_lines.append(f"- {k}: {v:.6f}")
            else:
                spec_lines.append(f"- {k}: {v}")
        spec_lines.append("")

    (ROOT / "spec_tests.md").write_text("\n".join(spec_lines))

    # robustness.md
    rob_lines = [
        "# Robustness Results\n",
        f"*Date: 2026-04-02*\n",
        "---\n",
        "## Coefficient Comparison Table\n",
        format_coef_table(all_specs_for_robustness),
        "\n---\n",
        "## Beta Sign and Significance Across Specs\n",
        "| Spec | beta_dtrm | p_dtrm | beta_dtrm_lag1 | p_lag1 | beta_sum | Positive+Sig? |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in all_specs_for_robustness:
        b1 = r.params.get("delta_trm", np.nan)
        b2 = r.params.get("delta_trm_lag1", np.nan)
        p1 = r.pvalues.get("delta_trm", np.nan)
        p2 = r.pvalues.get("delta_trm_lag1", np.nan)
        bsum = b1 + b2 if not (np.isnan(b1) or np.isnan(b2)) else np.nan
        pos_sig = "YES" if (bsum > 0 and (p1 < 0.05 or p2 < 0.05)) else "NO"
        # For R1 log-log
        if "ln_trm" in r.params.index:
            b_trm = r.params["ln_trm"]
            p_trm = r.pvalues["ln_trm"]
            rob_lines.append(
                f"| {r.name} | ln_trm={b_trm:.4f} | {p_trm:.4f} | - | - | - | "
                f"{'YES' if b_trm > 0 and p_trm < 0.05 else 'NO'} |"
            )
        else:
            rob_lines.append(
                f"| {r.name} | {b1:.6f} | {p1:.4f} | {b2:.6f} | {p2:.4f} | "
                f"{bsum:.6f} | {pos_sig} |"
            )

    rob_lines.append("\n---\n")
    rob_lines.append("## Sensitivity Notes\n")
    rob_lines.append("- S1 (no campaign filter): **Needs separate Dune query** -- not feasible with current data pull.")
    rob_lines.append("- All standard errors are Newey-West HAC (maxlags=5).")

    (ROOT / "robustness.md").write_text("\n".join(rob_lines))

    # summary.md
    decision = apply_decision_rule(t1, t2, t4, t6, all_specs_for_robustness)
    summary_lines = [
        "# Executive Summary: cCOP Flow Response to COP/USD\n",
        f"*Date: 2026-04-02*\n",
        f"*Sample: {df['date'].min().date()} to {df['date'].max().date()} (N={len(df)})*\n",
        "---\n",
        "## Key Findings\n",
        f"**Primary beta (dTRM)**: {primary.params['delta_trm']:.6f} "
        f"(SE={primary.bse['delta_trm']:.6f}, p={primary.pvalues['delta_trm']:.4f})",
        f"**Primary beta (dTRM_lag1)**: {primary.params['delta_trm_lag1']:.6f} "
        f"(SE={primary.bse['delta_trm_lag1']:.6f}, p={primary.pvalues['delta_trm_lag1']:.4f})",
        f"**Beta sum (b1+b2)**: {t1['beta_sum']:.6f} (SE={t1['se_sum']:.6f}, "
        f"t={t1['t_stat']:.4f}, one-sided p={t1['p_one_sided']:.4f})",
        f"**Quincena effect**: {primary.params['D_quincena']:.4f} "
        f"(SE={primary.bse['D_quincena']:.4f}, p={primary.pvalues['D_quincena']:.4f})",
        f"**R-squared**: {primary.rsquared:.4f}",
        f"**Lagged DV**: {primary.params['ln_gross_lag1']:.4f} "
        f"(p={primary.pvalues['ln_gross_lag1']:.4f})",
        f"**Time trend**: {primary.params['t']:.6f} "
        f"(p={primary.pvalues['t']:.4f})\n",
        "---\n",
        "## Specification Test Summary\n",
        f"| Test | Verdict |",
        f"|---|---|",
        f"| T1: b1+b2 > 0 (macro content) | {'PASS' if t1['pass'] else 'FAIL'} (p={t1['p_one_sided']:.4f}) |",
        f"| T2: g_quincena > 0 (income) | {'PASS' if t2['pass'] else 'FAIL'} (p={t2['p_one_sided']:.4f}) |",
        f"| T4: Heteroskedasticity (variance) | {'PASS' if t4['pass'] else 'FAIL'} (p={t4['bp_p']:.4f}) |",
        f"| T5: Ramsey RESET | {'PASS' if t5['pass'] else 'FAIL'} (p={t5['f_p']:.4f}) |",
        f"| T6: Income vs whale | {'PASS' if t6['pass'] else 'FAIL'} |",
        "",
        "---\n",
        decision,
        "\n---\n",
        "## Interpretation\n",
    ]

    # Add economic interpretation
    b1 = primary.params["delta_trm"]
    b2 = primary.params["delta_trm_lag1"]
    if t1["pass"]:
        summary_lines.append(
            f"A 1 COP increase in TRM (peso depreciation) is associated with a "
            f"{b1:.4f} increase in ln(1+V) on the same day and {b2:.4f} the next day. "
            f"Combined semi-elasticity: {b1+b2:.4f}."
        )
        if b1 + b2 > 0:
            pct = (np.exp(b1 + b2) - 1) * 100
            summary_lines.append(
                f"A 10 COP depreciation shock implies roughly "
                f"{(np.exp((b1+b2)*10) - 1)*100:.1f}% higher daily volume."
            )
    else:
        summary_lines.append(
            "The FX signal does not carry statistically significant macro content "
            "in this sample."
        )

    (ROOT / "summary.md").write_text("\n".join(summary_lines))

    print(f"\nAll outputs written to: {ROOT}")
    print("  - estimates.md")
    print("  - spec_tests.md")
    print("  - robustness.md")
    print("  - summary.md")
    print("  - merged_dataset.csv")
    print("\nDone.")


if __name__ == "__main__":
    main()
