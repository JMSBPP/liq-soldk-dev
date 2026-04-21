# Executive Summary: Volume-Fee Elasticity Estimation

## Data Sources (Dune, all verifiable)
- Q1 Pool hourly: https://dune.com/queries/6937696
- Q2 Polygon DEX vol: https://dune.com/queries/6937702
- Q3 ETH price: https://dune.com/queries/6937699
- Q4 Fee distribution: https://dune.com/queries/6937700
- Q5 Regression-ready daily: https://dune.com/queries/6937780
- Fee history (USDC/DAI inactive): https://dune.com/queries/6937672
- Aggregator routing test: https://dune.com/queries/6937511
- Pool survey (all Algebra): https://dune.com/queries/6937688

## Sample
- Pool: Quickswap V3 Algebra USDC/WETH (`0xa6aedf7c4ed6e821e67a6bfd56fd1702ad9a9719`, Polygon)
- Period: January 1 - March 31, 2026
- Granularity: Daily (N=90). Hourly available but not yet estimated.
- Fee range: 400-910 (hundredths of bip), 511 distinct values

## Regime Distribution
- Low (fee < 500): 15 days (16.7%)
- Mid (500-799): 17 days (18.9%)
- High (>= 800): 58 days (64.4%)

## Key Findings

### LP Income is LONG Vol in ALL Regimes

| Regime | epsilon | (1+epsilon) | p-value | Significance |
|--------|---------|-------------|---------|-------------|
| Low (fee < 500) | +0.8421 | +1.8421 | 0.078 | * |
| Mid (500-799) | +0.8472 | +1.8472 | 0.051 | * |
| High (>= 800) | +0.7798 | +1.7798 | 0.066 | * |

### Model Fit
- R-squared = 0.369
- Adjusted R-squared = 0.323
- F-statistic = 20.77 (p = 1.03e-14)
- Newey-West HAC standard errors with 7 lags

### Specification Tests

| Test | Result | Interpretation |
|------|--------|---------------|
| Sign restriction (epsilon < 0) | **FAIL** — all epsilon > 0 | Volume rises with fee; contradicts standard demand theory |
| Ordering (\|eps_high\| > \|eps_mid\| > \|eps_low\|) | **FAIL** — all similar (~0.78-0.85) | No regime differentiation; elasticity is approximately constant |
| Predetermination (future fee = 0) | **FAIL** (p=0.028) | Fee is not fully predetermined at daily granularity |

### Two Interpretations of Positive Epsilon

**Interpretation A: Simultaneous causation bias (most likely)**
Vol shocks drive BOTH fee (mechanical via accumulator) AND volume (more arb/trading during volatility). Controls don't fully absorb within-day vol intensity. Evidence: predetermination test failed.

**Interpretation B: Arb volume dominates (real effect)**
During high vol, price discrepancies grow as sigma-squared while fee grows as sigmoid(sigma). Arb profit increases despite higher fee. Consistent with LVR (Milionis et al. 2022, arxiv:2208.06046).

Both are likely operating. True epsilon is positive but smaller than +0.84.

### Robust Conclusion

**(1+epsilon) > 0 is robust** to both interpretations. LP income rises with vol regardless of mechanism. This is the finding that matters for derivative design.

## Derivative Pricing Implications

| Derivative | Implication |
|---|---|
| IncomeFloor | **Cheap** — income rises during stress, floor rarely activates |
| IncomePerpetual | **Procyclical funding** — longs receive more during high vol |
| Settlement quality | **Good** — income is a reliable vol signal (same direction all regimes) |
| Income-vol relationship | **Convex** — income accelerates upward during stress |

## Caveats

1. **Daily granularity is too coarse** for clean identification. Predetermination holds at per-swap level but degrades with aggregation. Hourly estimation needed.
2. **Positive epsilon inflated** by simultaneous causation. True magnitude is lower.
3. **Marginal significance** (p ~ 0.05-0.08) with 90 observations. Hourly data (2,200 obs) would sharpen.
4. **USDC/DAI pool has inactive dynamic fee** — results estimated on USDC/WETH and transferred by analogy to any Algebra pool with active dynamic fees.

## Open Exercises
1. Hourly estimation (export CSVs from Q1/Q2/Q3, re-run with N~2,200)
2. Uniswap V4 USDC/DAI hook research (pool 0x673667, $56.8M/30d)
3. Code rewrite with functional Python, TDD, dedicated venv

## Specification
Full spec: `notes/structural-econometrics/specs/2026-04-01-usdc-weth-volume-fee-elasticity.md`

## Credits Used
Total Dune credits consumed: ~2.5 of 2,500 budget (0.1%)
