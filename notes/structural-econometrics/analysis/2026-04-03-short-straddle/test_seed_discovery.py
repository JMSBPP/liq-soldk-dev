"""Tests for seed position discovery."""
from seed_discovery import (
    PositionRecord,
    PnLResult,
    match_deposit_withdrawal,
    is_symmetric_position,
    compute_pnl,
    passes_seed_criteria,
)


def test_match_deposit_withdrawal_pairs_by_depositor_and_pool() -> None:
    deposits = [
        {"depositor": "0xaaa", "pool_id": "0x111", "shares": 100, "block_time": "2025-03-01", "amount0": 1000, "amount1": 500, "tx_hash": "0xd1"},
        {"depositor": "0xbbb", "pool_id": "0x111", "shares": 200, "block_time": "2025-03-02", "amount0": 2000, "amount1": 1000, "tx_hash": "0xd2"},
    ]
    withdrawals = [
        {"depositor": "0xaaa", "pool_id": "0x111", "shares": 100, "block_time": "2025-03-15", "amount0": 950, "amount1": 550, "tx_hash": "0xw1"},
    ]
    matched = match_deposit_withdrawal(deposits, withdrawals)
    assert len(matched) == 1
    assert matched[0].depositor == "0xaaa"
    assert matched[0].deposit_tx == "0xd1"
    assert matched[0].withdraw_tx == "0xw1"


def test_compute_pnl_profitable() -> None:
    pos = PositionRecord(
        position_id="test_001",
        architecture="bunni_v2",
        chain_id=42161,
        pool="0x111",
        pair="ETH/USDC",
        depositor="0xaaa",
        deposit_tx="0xd1",
        withdraw_tx="0xw1",
        entry_timestamp="2025-03-01",
        exit_timestamp="2025-03-15",
        entry_amount0=1.0,
        entry_amount1=2000.0,
        exit_amount0=0.9,
        exit_amount1=2100.0,
        shares=100,
        entry_price=2000.0,
        exit_price=2200.0,
    )
    pnl = compute_pnl(pos, fee_income_usd=50.0)
    assert pnl.net_pnl_usd is not None
    assert isinstance(pnl.entry_value_usd, float)


def test_is_symmetric_position_true() -> None:
    assert is_symmetric_position(tick_lower=-100, tick_upper=100, entry_tick=5, tolerance_ticks=20)


def test_is_symmetric_position_false_asymmetric() -> None:
    assert not is_symmetric_position(tick_lower=-100, tick_upper=100, entry_tick=50, tolerance_ticks=20)


def test_passes_seed_criteria_rejects_short_duration() -> None:
    assert not passes_seed_criteria(duration_days=3, is_profitable=True, is_symmetric=True, price_range_pct=10.0)


def test_passes_seed_criteria_accepts_valid() -> None:
    assert passes_seed_criteria(duration_days=14, is_profitable=True, is_symmetric=True, price_range_pct=12.0)


def test_passes_seed_criteria_rejects_unprofitable() -> None:
    assert not passes_seed_criteria(duration_days=14, is_profitable=False, is_symmetric=True, price_range_pct=12.0)
