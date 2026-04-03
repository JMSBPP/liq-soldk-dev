"""Phase 2: Seed position discovery and documentation.

Matches Bunni V2 deposits to withdrawals, computes P&L,
and filters to seed criteria (profitable, symmetric, >= 7 days, >= 5% price move).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Final, Optional, TypeAlias

# Domain type aliases
Address: TypeAlias = str
TxHash: TypeAlias = str
PoolId: TypeAlias = str

# Seed criteria defaults
MIN_DURATION_DAYS: Final[float] = 7.0
MIN_PRICE_RANGE_PCT: Final[float] = 5.0


@dataclass(frozen=True)
class PositionRecord:
    """A single LP position lifecycle."""
    position_id: str
    architecture: str  # 'bunni_v2' or 'algebra'
    chain_id: int
    pool: PoolId
    pair: str
    depositor: Address
    deposit_tx: TxHash
    withdraw_tx: TxHash
    entry_timestamp: str
    exit_timestamp: str
    entry_amount0: float
    entry_amount1: float
    exit_amount0: float
    exit_amount1: float
    shares: int
    entry_price: float
    exit_price: float
    ldf_type: Optional[str] = None
    ldf_params: Optional[dict[str, float]] = None
    avg_fee_bps: Optional[float] = None
    tick_lower: Optional[int] = None
    tick_upper: Optional[int] = None


@dataclass(frozen=True)
class PnLResult:
    """P&L decomposition for a position."""
    entry_value_usd: float
    exit_value_usd: float
    fee_income_usd: float
    il_usd: float
    net_pnl_usd: float
    benchmark_hold_usd: float
    alpha_usd: float


def match_deposit_withdrawal(
    deposits: list[dict[str, object]],
    withdrawals: list[dict[str, object]],
) -> list[PositionRecord]:
    """Match deposits to withdrawals by depositor + pool_id.

    Simple 1:1 matching — first deposit matched to first withdrawal
    for each (depositor, pool_id) pair. Unmatched deposits (trapped by hack)
    are excluded.
    """
    deposit_queue: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for d in deposits:
        key = (str(d["depositor"]), str(d["pool_id"]))
        deposit_queue[key].append(d)

    matched: list[PositionRecord] = []
    for w in withdrawals:
        key = (str(w["depositor"]), str(w["pool_id"]))
        if deposit_queue[key]:
            d = deposit_queue[key].pop(0)
            matched.append(PositionRecord(
                position_id=f"{str(d['depositor'])[:8]}_{str(d['pool_id'])[:8]}",
                architecture="bunni_v2",
                chain_id=42161,
                pool=str(d["pool_id"]),
                pair="",
                depositor=str(d["depositor"]),
                deposit_tx=str(d["tx_hash"]),
                withdraw_tx=str(w["tx_hash"]),
                entry_timestamp=str(d["block_time"]),
                exit_timestamp=str(w["block_time"]),
                entry_amount0=float(str(d["amount0"])),
                entry_amount1=float(str(d["amount1"])),
                exit_amount0=float(str(w["amount0"])),
                exit_amount1=float(str(w["amount1"])),
                shares=int(str(d["shares"])),
                entry_price=0.0,
                exit_price=0.0,
            ))

    return matched


def compute_pnl(
    position: PositionRecord,
    fee_income_usd: float,
) -> PnLResult:
    """Compute P&L decomposition for a position.

    Assumes token1 is the numeraire (e.g., USDC).
    entry_value = amount0 * entry_price + amount1
    """
    entry_value: float = position.entry_amount0 * position.entry_price + position.entry_amount1
    exit_value: float = position.exit_amount0 * position.exit_price + position.exit_amount1
    net_pnl: float = exit_value - entry_value + fee_income_usd
    il: float = net_pnl - fee_income_usd
    benchmark: float = position.entry_amount0 * position.exit_price + position.entry_amount1
    alpha: float = net_pnl - (benchmark - entry_value)

    return PnLResult(
        entry_value_usd=entry_value,
        exit_value_usd=exit_value,
        fee_income_usd=fee_income_usd,
        il_usd=il,
        net_pnl_usd=net_pnl,
        benchmark_hold_usd=benchmark,
        alpha_usd=alpha,
    )


def is_symmetric_position(
    tick_lower: int,
    tick_upper: int,
    entry_tick: int,
    tolerance_ticks: int = 20,
) -> bool:
    """Check if an LP position is roughly symmetric around entry price."""
    midpoint: int = (tick_lower + tick_upper) // 2
    return abs(midpoint - entry_tick) <= tolerance_ticks


def passes_seed_criteria(
    duration_days: float,
    is_profitable: bool,
    is_symmetric: bool,
    price_range_pct: float,
    min_duration_days: float = MIN_DURATION_DAYS,
    min_price_range_pct: float = MIN_PRICE_RANGE_PCT,
) -> bool:
    """Check if a position passes seed selection criteria.

    Spec Section 2.4:
    1. Complete lifecycle (implied by having withdrawal)
    2. Profitable (net P&L > 0)
    3. Symmetric placement
    4. Duration >= 7 days
    5. Price range >= 5%
    """
    return (
        is_profitable
        and is_symmetric
        and duration_days >= min_duration_days
        and price_range_pct >= min_price_range_pct
    )
