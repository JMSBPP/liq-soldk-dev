"""Tests for Greeks estimation and implied/realized vol extraction."""
import numpy as np
from greeks_vol import (
    estimate_delta,
    estimate_gamma,
    estimate_theta,
    compute_implied_vol_lambert,
    two_scale_realized_variance,
    compute_vol_spread,
)


def test_estimate_delta_near_zero_at_strike() -> None:
    sqrt_prices = np.linspace(9.0, 11.0, 201)
    pnl = 5.0 - np.abs(sqrt_prices - 10.0)
    deltas = estimate_delta(sqrt_prices, pnl)
    assert abs(deltas[100]) < 0.2


def test_estimate_gamma_negative_at_strike() -> None:
    sqrt_prices = np.linspace(8.0, 12.0, 401)
    pnl = 5.0 - 1.5 * np.abs(sqrt_prices - 10.0)
    deltas = estimate_delta(sqrt_prices, pnl)
    gammas = estimate_gamma(sqrt_prices, deltas)
    assert gammas[200] < 0


def test_estimate_theta_positive_for_fee_accrual() -> None:
    timestamps = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    values = np.array([100.0, 101.0, 102.0, 103.0, 104.0, 105.0])
    theta = estimate_theta(timestamps, values)
    assert theta > 0.0
    assert abs(theta - 1.0) < 0.1


def test_compute_implied_vol_lambert() -> None:
    sigma = compute_implied_vol_lambert(
        daily_fee_income=10.0,
        position_value=10000.0,
        tick_range=1000,
        tick_spacing=10,
    )
    assert abs(sigma - np.sqrt(0.2)) < 0.01


def test_compute_implied_vol_lambert_zero_value() -> None:
    sigma = compute_implied_vol_lambert(
        daily_fee_income=10.0, position_value=0.0, tick_range=1000, tick_spacing=10,
    )
    assert sigma == 0.0


def test_two_scale_realized_variance_on_constant_price() -> None:
    timestamps = np.arange(0, 100, dtype=float)
    prices = np.full(100, 2000.0)
    rv = two_scale_realized_variance(timestamps, prices, slow_interval=5.0)
    assert abs(rv) < 1e-10


def test_two_scale_realized_variance_positive_for_volatile() -> None:
    np.random.seed(42)
    timestamps = np.arange(0, 365, dtype=float)
    log_returns = np.random.normal(0, 0.02, 365)
    prices = 2000.0 * np.exp(np.cumsum(log_returns))
    rv = two_scale_realized_variance(timestamps, prices, slow_interval=5.0)
    assert rv > 0.0


def test_compute_vol_spread() -> None:
    spread = compute_vol_spread(sigma_implied=0.8, sigma_realized=0.6)
    assert abs(spread - 0.2) < 1e-10
