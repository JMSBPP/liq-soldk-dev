
# DESCRIPTION
'''
A derivative settling on LP fee revenue from an Algebra (dynamic-fee) CFMM pool, where the adaptive fee's sigmoid response to volatility creates a natural vol exposure for LPs. The instrument provides exposure to (or hedge against) the volatility sensitivity of LP income.
'''

Payoff \propto f(epsilon, FeeRevenue_t) where epsilon = volume-fee elasticity

======

Pool: Quickswap V3 Algebra USDC/WETH (0xa6aedf, Polygon)
Comparison: Uniswap V3 USDC/DAI on Polygon is 100% aggregator spillover — not independent
V4 research: PoolManager singleton, $56.8M likely misattributed V3 volume (see research/)

======

## CORE FINDING

epsilon > 0 in ALL vol regimes (low/mid/high) => (1+epsilon) > 1 => LP income is LONG vol

| Regime | epsilon | (1+epsilon) | Interpretation |
|--------|---------|-------------|----------------|
| Low (fee < 500)  | +0.84 | +1.84 | LONG vol |
| Mid (500-799)    | +0.85 | +1.85 | LONG vol |
| High (>= 800)    | +0.78 | +1.78 | LONG vol |

Caveat: positive epsilon partly from simultaneous causation bias (vol shocks drive both fee AND volume). True epsilon is positive but smaller. Direction (1+epsilon > 0) is robust.

## EXERCISES

1. HOURLY ESTIMATION: Re-estimate with N~2,200 hourly obs (predetermination test should pass at hourly granularity)
   - Data ready: https://dune.com/queries/6937696 (pool), https://dune.com/queries/6937702 (DEX vol), https://dune.com/queries/6937699 (ETH price)

2. SEPARATE BIAS FROM REAL EFFECT: Decompose positive epsilon into simultaneous causation (bias) vs arb-volume-dominates (real, per LVR framework Milionis 2022)

3. USDC/DAI FEE REACTIVATION: If governance re-enables dynamic fee on the USDC/DAI Algebra pool, re-estimate on stablecoin pair

4. UNISWAP V4 HOOKS: Research what hooks the V4 pool uses (see research/2026-04-01-uniswap-v4-hooks-usdc-dai.md)

## EXPECTED LONGS

- LPs ON ALGEBRA POOLS {
        technology: provide concentrated liquidity on dynamic-fee pools
        benefit: income rises with vol (epsilon > -1 confirmed)
        cost: IL still applies (price component)
        use_case: NATURAL POSITION (already long vol by being LP)
}

- VOL SELLERS {
        technology: sell income floor to LPs
        benefit: collect premium on cheap floors (income rises in stress, floor rarely pays)
        use_case: PREMIUM COLLECTION
}

## EXPECTED SHORTS

- LPs HEDGING TAIL RISK {
        technology: buy income floor on their own fee revenue
        benefit: protection if epsilon flips to < -1 in extreme stress (volume flight dominates fee increase)
        use_case: TAIL HEDGING
}

- PROTOCOLS / TREASURIES {
        technology: cap LP income to budget rewards
        benefit: income cap limits payout during high-vol periods
        use_case: BUDGET MANAGEMENT
}

## KEY IMPLICATION (from initial draft reasoning)

The arb-volume-dominates interpretation (2) implies:
- During high vol, price discrepancies between pool and CEX grow as sigma^2
- The fee grows as sigmoid(sigma) — sublinear at high vol
- Arb profit per trade increases despite higher fee -> more arb volume
- Consistent with LVR framework (Milionis et al. 2022, arxiv:2208.06046)

==> VARIANCE SWAP DEFINED AS THE SPREAD ON LP INCOME BETWEEN ALGEBRA AND UNISWAP CAN BE A HEDGE FOR ARBITRAGE

The Algebra-vs-UniV3 fee revenue spread is a natural variance swap payoff. Arbers who are short vol (their PnL falls when vol-driven competition squeezes arb margins) can hedge by going long this spread.

## SPECS
- [USDC/WETH spec](./2026-04-01-usdc-weth-volume-fee-elasticity.md)
- [USDC/DAI spec (inactive fee)](./2026-04-01-usdc-dai-volume-fee-elasticity.md)

## RESEARCH
- [V4 hooks](./research/2026-04-01-uniswap-v4-hooks-usdc-dai.md)
- [Estimation summary](./research/summary.md)
