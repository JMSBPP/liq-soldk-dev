"""Tests for payoff fitting with synthetic data."""
import numpy as np
from payoff_fitting import (
    sharp_straddle_payoff,
    smoothed_straddle_payoff,
    quadratic_payoff,
    fit_straddle,
    fit_smoothed_straddle,
    fit_quadratic,
    compute_aic,
    straddle_beats_quadratic,
    FitResult,
)


def test_sharp_straddle_payoff_at_strike_equals_premium() -> None:
    result = sharp_straddle_payoff(sqrt_prices=np.array([10.0]), sqrt_strike=10.0, alpha=1.0, premium=5.0)
    assert abs(result[0] - 5.0) < 1e-10


def test_sharp_straddle_payoff_away_from_strike() -> None:
    result = sharp_straddle_payoff(sqrt_prices=np.array([12.0]), sqrt_strike=10.0, alpha=2.0, premium=5.0)
    assert abs(result[0] - 1.0) < 1e-10


def test_smoothed_straddle_approaches_sharp_for_small_sigma() -> None:
    sqrt_prices = np.linspace(8.0, 12.0, 100)
    sharp = sharp_straddle_payoff(sqrt_prices, 10.0, 1.0, 5.0)
    smoothed = smoothed_straddle_payoff(sqrt_prices, 10.0, 1.0, 5.0, sigma=0.01)
    assert np.max(np.abs(sharp - smoothed)) < 0.05


def test_compute_aic() -> None:
    aic = compute_aic(n=100, k=3, rss=100.0)
    expected = 2 * 3 + 100 * np.log(100.0 / 100)
    assert abs(aic - expected) < 1e-10


def test_straddle_beats_quadratic_on_synthetic_straddle() -> None:
    np.random.seed(42)
    n = 200
    sqrt_prices = np.linspace(8.0, 12.0, n)
    true_payoff = 5.0 - 1.5 * np.abs(sqrt_prices - 10.0)
    noise = np.random.normal(0, 0.1, n)
    observed = true_payoff + noise

    straddle_fit = fit_straddle(sqrt_prices, observed, sqrt_strike_guess=10.0)
    quad_fit = fit_quadratic(sqrt_prices, observed)

    assert straddle_beats_quadratic(straddle_fit, quad_fit, min_delta_aic=4.0)
    assert straddle_fit.r_squared > 0.6


def test_smoothed_straddle_fit_on_rounded_data() -> None:
    np.random.seed(42)
    n = 200
    sqrt_prices = np.linspace(8.0, 12.0, n)
    sigma_ldf = 0.5
    x = (sqrt_prices - 10.0) / sigma_ldf
    true_payoff = 5.0 - 1.5 * sigma_ldf * (np.abs(x) + np.log1p(np.exp(-2 * np.abs(x))))
    noise = np.random.normal(0, 0.05, n)
    observed = true_payoff + noise

    smoothed_fit = fit_smoothed_straddle(sqrt_prices, observed, sqrt_strike_guess=10.0, sigma=sigma_ldf)
    sharp_fit = fit_straddle(sqrt_prices, observed, sqrt_strike_guess=10.0)
    assert smoothed_fit.aic < sharp_fit.aic
    assert smoothed_fit.r_squared > 0.8


def test_quadratic_wins_on_parabolic_data() -> None:
    np.random.seed(42)
    n = 200
    sqrt_prices = np.linspace(8.0, 12.0, n)
    true_payoff = -0.5 * (sqrt_prices - 10.0) ** 2 + 3.0
    noise = np.random.normal(0, 0.1, n)
    observed = true_payoff + noise

    straddle_fit = fit_straddle(sqrt_prices, observed, sqrt_strike_guess=10.0)
    quad_fit = fit_quadratic(sqrt_prices, observed)
    assert not straddle_beats_quadratic(straddle_fit, quad_fit, min_delta_aic=4.0)
