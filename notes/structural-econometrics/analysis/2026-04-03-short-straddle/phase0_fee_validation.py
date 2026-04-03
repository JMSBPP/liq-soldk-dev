"""Phase 0: Fee accrual reconstruction and validation.

Bunni V2 uses share-based accounting (ERC4626 vaults).
Fee income for a depositor = (shares / total_shares) * pool_fee_revenue * (1 - curator_rate).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final


# Curator fee precision in Bunni V2 contracts (5 decimals)
CURATOR_FEE_PRECISION: Final[int] = 100_000


@dataclass(frozen=True)
class FeeIncome:
    """Reconstructed fee income for a position."""
    token0_fees: float
    token1_fees: float


def compute_share_fee_income(
    shares_held: int,
    total_shares: int,
    pool_fee_revenue_token0: float,
    pool_fee_revenue_token1: float,
    curator_fee_rate: float,
) -> FeeIncome:
    """Compute fee income for a share-based LP position.

    Args:
        shares_held: Number of BunniToken shares held by the depositor.
        total_shares: Total supply of BunniToken shares for the pool.
        pool_fee_revenue_token0: Total token0 fees earned by the pool during period.
        pool_fee_revenue_token1: Total token1 fees earned by the pool during period.
        curator_fee_rate: Fraction taken by curator (e.g., 0.10 for 10%).

    Returns:
        FeeIncome with token0 and token1 fee amounts.
    """
    if total_shares == 0:
        return FeeIncome(token0_fees=0.0, token1_fees=0.0)

    share_fraction: float = shares_held / total_shares
    net_rate: float = 1.0 - curator_fee_rate

    return FeeIncome(
        token0_fees=share_fraction * pool_fee_revenue_token0 * net_rate,
        token1_fees=share_fraction * pool_fee_revenue_token1 * net_rate,
    )
