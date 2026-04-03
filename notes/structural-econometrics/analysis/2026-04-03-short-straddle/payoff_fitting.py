"""Phase 3: Payoff shape fitting for short straddle identification.

Model A (sharp): P(S) = premium - alpha * |sqrt(S) - sqrt(K)|
Model B (smoothed): P(S) = premium - alpha * sigma * log(2 * cosh((sqrt(S) - sqrt(K)) / sigma))
Null hypothesis (quadratic): P(S) = a + b*sqrt(S) + c*S

Match criterion: straddle AIC beats quadratic AIC by delta > 4.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize_scalar

# Type aliases
FloatArray: TypeAlias = NDArray[np.float64]

# Constants
MIN_DELTA_AIC: Final[float] = 4.0
DEFAULT_SEARCH_RANGE: Final[float] = 2.0


@dataclass(frozen=True)
class FitResult:
    """Result of a payoff model fit."""
    model_name: str
    r_squared: float
    aic: float
    rss: float
    n_params: int
    n_obs: int
    params: dict[str, float]


def sharp_straddle_payoff(
    sqrt_prices: FloatArray,
    sqrt_strike: float,
    alpha: float,
    premium: float,
) -> FloatArray:
    """Compute sharp straddle payoff: premium - alpha * |sqrt(S) - sqrt(K)|."""
    return premium - alpha * np.abs(sqrt_prices - sqrt_strike)


def smoothed_straddle_payoff(
    sqrt_prices: FloatArray,
    sqrt_strike: float,
    alpha: float,
    premium: float,
    sigma: float,
) -> FloatArray:
    """Compute smoothed straddle payoff using log-cosh approximation.

    smoothed_abs(x, sigma) = sigma * log(2 * cosh(x / sigma))
    Approximates |x| with a rounded tip controlled by sigma.
    """
    x = (sqrt_prices - sqrt_strike) / sigma
    abs_x = np.abs(x)
    smooth_abs = sigma * (abs_x + np.log1p(np.exp(-2.0 * abs_x)))
    return premium - alpha * smooth_abs


def quadratic_payoff(
    sqrt_prices: FloatArray,
    a: float,
    b: float,
    c: float,
) -> FloatArray:
    """Compute quadratic null model: a + b*sqrt(S) + c*S."""
    return a + b * sqrt_prices + c * sqrt_prices**2


def compute_aic(n: int, k: int, rss: float) -> float:
    """Compute Akaike Information Criterion: AIC = 2k + n * ln(RSS / n)."""
    return 2.0 * k + n * np.log(rss / n)


def _fit_ols_with_strike_search(
    sqrt_prices: FloatArray,
    observed_pnl: FloatArray,
    sqrt_strike_guess: float,
    search_range: float,
    feature_fn: object,  # Callable[[FloatArray, float], FloatArray] but keeping simple
) -> tuple[float, NDArray[np.float64], float, float]:
    """Internal: search for best strike K via OLS, return (best_k, beta, rss, r2)."""
    n = len(sqrt_prices)
    mean_y = np.mean(observed_pnl)
    ss_tot = float(np.sum((observed_pnl - mean_y) ** 2))

    def neg_r_squared(sqrt_k: float) -> float:
        features = feature_fn(sqrt_prices, sqrt_k)  # type: ignore[operator]
        X = np.column_stack([np.ones(n), features])
        beta, _, _, _ = np.linalg.lstsq(X, observed_pnl, rcond=None)
        residuals = observed_pnl - X @ beta
        rss = float(np.sum(residuals**2))
        return -(1.0 - rss / ss_tot) if ss_tot > 0 else 0.0

    result = minimize_scalar(
        neg_r_squared,
        bounds=(sqrt_strike_guess - search_range, sqrt_strike_guess + search_range),
        method="bounded",
    )
    best_k = float(result.x)

    features = feature_fn(sqrt_prices, best_k)  # type: ignore[operator]
    X = np.column_stack([np.ones(n), features])
    beta, _, _, _ = np.linalg.lstsq(X, observed_pnl, rcond=None)
    residuals = observed_pnl - X @ beta
    rss = float(np.sum(residuals**2))
    r2 = 1.0 - rss / ss_tot if ss_tot > 0 else 0.0

    return best_k, beta, rss, r2


def fit_straddle(
    sqrt_prices: FloatArray,
    observed_pnl: FloatArray,
    sqrt_strike_guess: float,
    search_range: float = DEFAULT_SEARCH_RANGE,
) -> FitResult:
    """Fit sharp straddle model with constrained K search."""
    def sharp_features(prices: FloatArray, sqrt_k: float) -> FloatArray:
        return np.abs(prices - sqrt_k)

    best_k, beta, rss, r2 = _fit_ols_with_strike_search(
        sqrt_prices, observed_pnl, sqrt_strike_guess, search_range, sharp_features,
    )
    return FitResult(
        model_name="sharp_straddle",
        r_squared=r2,
        aic=compute_aic(len(sqrt_prices), k=3, rss=rss),
        rss=rss,
        n_params=3,
        n_obs=len(sqrt_prices),
        params={"sqrt_strike": best_k, "alpha": float(-beta[1]), "premium": float(beta[0])},
    )


def fit_smoothed_straddle(
    sqrt_prices: FloatArray,
    observed_pnl: FloatArray,
    sqrt_strike_guess: float,
    sigma: float,
    search_range: float = DEFAULT_SEARCH_RANGE,
) -> FitResult:
    """Fit smoothed straddle model for GeometricDistribution positions."""
    def smoothed_features(prices: FloatArray, sqrt_k: float) -> FloatArray:
        x = (prices - sqrt_k) / sigma
        abs_x = np.abs(x)
        return sigma * (abs_x + np.log1p(np.exp(-2.0 * abs_x)))

    best_k, beta, rss, r2 = _fit_ols_with_strike_search(
        sqrt_prices, observed_pnl, sqrt_strike_guess, search_range, smoothed_features,
    )
    return FitResult(
        model_name="smoothed_straddle",
        r_squared=r2,
        aic=compute_aic(len(sqrt_prices), k=3, rss=rss),
        rss=rss,
        n_params=3,
        n_obs=len(sqrt_prices),
        params={"sqrt_strike": best_k, "alpha": float(-beta[1]), "premium": float(beta[0]), "sigma": sigma},
    )


def fit_quadratic(
    sqrt_prices: FloatArray,
    observed_pnl: FloatArray,
) -> FitResult:
    """Fit quadratic null model: a + b*sqrt(S) + c*S."""
    n = len(sqrt_prices)
    mean_y = np.mean(observed_pnl)
    ss_tot = float(np.sum((observed_pnl - mean_y) ** 2))

    X = np.column_stack([np.ones(n), sqrt_prices, sqrt_prices**2])
    beta, _, _, _ = np.linalg.lstsq(X, observed_pnl, rcond=None)
    residuals = observed_pnl - X @ beta
    rss = float(np.sum(residuals**2))
    r2 = 1.0 - rss / ss_tot if ss_tot > 0 else 0.0

    return FitResult(
        model_name="quadratic",
        r_squared=r2,
        aic=compute_aic(n, k=3, rss=rss),
        rss=rss,
        n_params=3,
        n_obs=n,
        params={"a": float(beta[0]), "b": float(beta[1]), "c": float(beta[2])},
    )


def straddle_beats_quadratic(
    straddle_fit: FitResult,
    quadratic_fit: FitResult,
    min_delta_aic: float = MIN_DELTA_AIC,
) -> bool:
    """Check if straddle model beats quadratic by delta-AIC > threshold."""
    delta = quadratic_fit.aic - straddle_fit.aic
    return delta > min_delta_aic
