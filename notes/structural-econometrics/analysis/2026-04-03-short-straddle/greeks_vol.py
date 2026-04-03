"""Phase 4: Model-free Greeks estimation and implied/realized vol extraction.

Greeks: finite differences on empirical payoff curves.
Implied vol: Lambert (2021) perpetual LP formula.
Realized vol: two-scale estimator (Zhang-Mykland-Ait-Sahalia 2005).
"""
from __future__ import annotations

from typing import Final, TypeAlias

import numpy as np
from numpy.typing import NDArray

# Type aliases
FloatArray: TypeAlias = NDArray[np.float64]

# Constants
DAYS_PER_YEAR: Final[float] = 365.0


def estimate_delta(
    sqrt_prices: FloatArray,
    pnl: FloatArray,
) -> FloatArray:
    """Estimate delta via central finite differences: d(pnl) / d(sqrt_price)."""
    return np.gradient(pnl, sqrt_prices)


def estimate_gamma(
    sqrt_prices: FloatArray,
    deltas: FloatArray,
) -> FloatArray:
    """Estimate gamma via finite differences on delta: d(delta) / d(sqrt_price)."""
    return np.gradient(deltas, sqrt_prices)


def estimate_theta(
    timestamps_days: FloatArray,
    position_values: FloatArray,
) -> float:
    """Estimate theta as average daily value change via OLS regression."""
    n = len(timestamps_days)
    if n < 2:
        return 0.0
    X = np.column_stack([np.ones(n), timestamps_days])
    beta, _, _, _ = np.linalg.lstsq(X, position_values, rcond=None)
    return float(beta[1])


def compute_implied_vol_lambert(
    daily_fee_income: float,
    position_value: float,
    tick_range: int,
    tick_spacing: int,
) -> float:
    """Compute implied vol using Lambert (2021) perpetual LP formula.

    sigma_implied = sqrt(2 * (daily_fee_income / position_value) * (tick_range / tick_spacing))

    This is the breakeven vol: realized vol at which the LP exactly breaks even.
    Profitable positions have sigma_realized < sigma_implied.
    """
    if position_value <= 0 or tick_spacing <= 0:
        return 0.0
    fee_rate: float = daily_fee_income / position_value
    range_factor: float = tick_range / tick_spacing
    return float(np.sqrt(2.0 * fee_rate * range_factor))


def two_scale_realized_variance(
    timestamps: FloatArray,
    prices: FloatArray,
    slow_interval: float = 5.0,
) -> float:
    """Two-scale realized variance estimator (Zhang-Mykland-Ait-Sahalia 2005).

    Handles microstructure noise from AMM bid-ask bounce.

    Args:
        timestamps: Event timestamps (in days).
        prices: Spot prices at each timestamp.
        slow_interval: Subsampling interval for the slow scale (in days).

    Returns:
        Annualized realized variance (sigma^2 * 365).
    """
    n = len(prices)
    if n < 3:
        return 0.0

    log_prices: FloatArray = np.log(prices)
    total_time: float = float(timestamps[-1] - timestamps[0])
    if total_time <= 0:
        return 0.0

    # Fast scale: all observations
    fast_returns: FloatArray = np.diff(log_prices)
    rv_fast: float = float(np.sum(fast_returns**2))

    # Slow scale: subsample at slow_interval
    n_slow_bins: int = max(1, int(total_time / slow_interval))
    slow_edges: FloatArray = np.linspace(float(timestamps[0]), float(timestamps[-1]), n_slow_bins + 1)
    slow_prices: FloatArray = np.interp(slow_edges, timestamps, log_prices)
    slow_returns: FloatArray = np.diff(slow_prices)
    rv_slow: float = float(np.sum(slow_returns**2))

    # Two-scale: RV_2scale = RV_slow - (n_bar / n) * RV_fast
    n_bar: float = n / max(n_slow_bins, 1)
    rv_two_scale: float = max(rv_slow - (n_bar / n) * rv_fast, 0.0)

    # Annualize
    duration_days: float = total_time
    return rv_two_scale * (DAYS_PER_YEAR / duration_days) if duration_days > 0 else 0.0


def compute_vol_spread(
    sigma_implied: float,
    sigma_realized: float,
) -> float:
    """Compute vol spread = implied - realized."""
    return sigma_implied - sigma_realized
