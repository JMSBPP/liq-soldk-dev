# Identification Strategy: USDC/DAI Dynamic vs Static Fee Mechanism

*Date: 2026-04-01*
*Source pair: USDC/DAI on Quickswap V3 (Algebra, Polygon) vs Uniswap V3*

---

## Context Summary

### Available Observables
- **Quickswap V3 (Algebra)**: sqrtPriceX96, feeGrowthGlobal, volatilityCumulative, adaptive fee level (phi_t = f(sigma_t)), tick accumulators, TVL, volume
- **Uniswap V3**: sqrtPriceX96, feeGrowthGlobal, tick accumulators, TVL, volume (static fee phi-bar)
- Both pools trade the same underlying pair (USDC/DAI, both USD-pegged)

### The Natural Experiment
The same asset pair (USDC/DAI) traded on two DEXes with fundamentally different fee mechanisms:
- **Algebra (Quickswap)**: phi_t is endogenously determined by a double-sigmoid function of recent realized volatility. Fee adapts in real-time.
- **Uniswap V3**: phi-bar is exogenously set at pool creation (typically 1bp or 5bp for stablecoin pairs). Fee is constant.

This creates a quasi-experimental design where the "treatment" is the fee mechanism and the "outcome" is the structure of LP income.

### Claims from Project Notes
- Pair1 (Algebra): (phi <- sigma) ==> FeeRevenue --> LP (LONG Vol) ==> TRADER (SHORT VOL)
- Pair2 (Uniswap): phi-bar ==> FeeRevenue --> LP (SHORT Vol) ==> TRADER (LONG VOL)

---

## Candidate Identification Strategy 1: Volatility Sensitivity of LP Fee Revenue

### Parameter of Interest
beta_2 in:

FeeRevenue_{it} = alpha + beta_1 * sigma_t + beta_2 * (sigma_t * D_i^{dynamic}) + gamma * X_{it} + epsilon_{it}

where:
- i indexes pool (Algebra vs Uniswap)
- t indexes time (block, hour, day)
- D_i^{dynamic} = 1 for Algebra pool, 0 for Uniswap pool
- sigma_t = realized volatility of USDC/DAI (common to both pools)
- X_{it} = controls (TVL, volume, gas cost)

beta_2 measures the ADDITIONAL sensitivity of fee revenue to volatility created by the dynamic fee mechanism.

### Identifying Variation
**Cross-pool x time-series interaction**: The same vol shock sigma_t hits both pools simultaneously, but the fee mechanism transmits it differently to revenue. The cross-pool difference in revenue response to the same vol shock identifies beta_2.

This is a difference-in-differences structure:
- First difference: fee revenue response to vol in Algebra pool
- Second difference: fee revenue response to vol in Uniswap pool
- beta_2 = (first difference) - (second difference)

### Exclusion Restriction
**Claim**: The fee mechanism assignment (dynamic vs static) is exogenous to USDC/DAI fundamental value dynamics.

**Formal statement**: E[D_i^{dynamic} * epsilon_{it}] = 0

**Economic justification**: Which DEX a pool is deployed on is determined by protocol governance decisions and ecosystem history, NOT by the USDC/DAI exchange rate process. Quickswap chose Algebra's engine for all pools, not specifically for USDC/DAI. Uniswap V3's static fee was a protocol-level design choice.

**Potential violations**:
1. LP self-selection: More sophisticated LPs might choose the Algebra pool precisely because they want vol exposure. This would make TVL_{it} endogenous.
2. Volume routing: Aggregators (1inch, Paraswap) route based on fee, so vol shocks may differentially affect volume across pools.
3. Chain effects: If pools are on different chains, gas cost differences could confound.

### Rank Condition
Requires: Var(sigma_t) > 0 (volatility must vary over time)
For USDC/DAI: Volatility is generally low but has documented spikes during:
- DAI depeg events (March 2023 SVB crisis: DAI briefly traded at 0.89)
- USDC depeg events (March 2023: USDC dropped to 0.87)
- MakerDAO governance changes (DSR adjustments)
- DeFi liquidation cascades

### Moment Conditions (for GMM)
E[Z_t * (FeeRevenue_{it} - alpha - beta_1 * sigma_t - beta_2 * (sigma_t * D_i) - gamma * X_{it})] = 0

Candidate instruments Z_t:
1. Lagged volatility (sigma_{t-k}): relevant for current vol, excluded from current fee revenue conditional on current vol
2. External vol measures (ETH/USD realized vol): correlated with USDC/DAI vol (common macro factor) but not directly in the fee revenue equation
3. MakerDAO DSR changes: exogenous policy shocks that affect DAI demand and thus USDC/DAI vol

---

## Candidate Identification Strategy 2: Dynamic Fee as Sufficient Statistic

### Parameter of Interest
Test whether phi_t (Algebra's adaptive fee) is a sufficient statistic for sigma_t in determining fee revenue.

H0: beta_sigma = 0 in FeeRevenue_t^{Algebra} = alpha + beta_phi * phi_t + beta_sigma * sigma_t + epsilon_t
H1: beta_sigma != 0

### Identifying Variation
Time-series variation in the Algebra pool only. The adaptive fee phi_t is a deterministic function of recent price movements (double-sigmoid of volatility accumulator). If phi_t perfectly captures the vol information relevant for revenue, then sigma_t adds no explanatory power.

### Exclusion Restriction
**Claim**: phi_t is a function of sigma_t only (through the Algebra volatility accumulator), not of other factors that independently affect revenue.

**Formal statement**: phi_t = g(sigma_{t-1}, sigma_{t-2}, ...) for known function g (the double-sigmoid)

**Economic justification**: By construction, Algebra's BasePluginV1 computes the adaptive fee from volatilityCumulative, which is derived from tick movements. The function g is deterministic and known (AdaptiveFee.sol).

**Potential violation**: The relevant "volatility" for fee revenue may differ from the specific volatility measure encoded in Algebra's accumulator. Algebra uses tick-based vol over a specific lookback; economically relevant vol might be measured differently.

### Rank Condition
Requires: phi_t and sigma_t are not perfectly collinear (if g is invertible and sigma_t is measured differently from the Algebra accumulator, this holds).

---

## Candidate Identification Strategy 3: Fee Revenue Spread as DeFi Monetary Stress Signal

### Parameter of Interest
beta in:

StressIndicator_t = alpha + beta * Spread_t + gamma * Controls_t + epsilon_t

where Spread_t = FeeRevenue_t^{Algebra} - FeeRevenue_t^{Uniswap} (normalized by TVL)

### Identifying Variation
Time-series variation in the spread. The key insight: the spread strips out common factors (pair demand, aggregate volume) and isolates the dynamic fee component. Since the dynamic fee responds to vol, the spread IS a vol signal. The question is whether this vol signal predicts DeFi monetary stress.

### Exclusion Restriction
**Claim**: The fee revenue spread affects DeFi stress indicators only through the vol channel, not directly.

**Formal statement**: E[Spread_t * epsilon_t | sigma_t] = 0

**Economic justification**: The spread is mechanically driven by the fee mechanism difference. Once you condition on vol (which the dynamic fee responds to), the spread has no independent effect on macro outcomes.

**Potential violations**:
1. Liquidity migration between pools during stress could make the spread endogenous
2. If aggregator routing changes during stress, volume composition shifts could contaminate the spread

### Macro Connections
USDC/DAI volatility signals:
- DAI mechanism stress (CDP liquidations, DSR changes, MakerDAO governance)
- USDC confidence (reserve composition concerns, regulatory risk)
- DeFi-wide monetary conditions (stablecoin demand rotation)
- Risk-free rate expectations in DeFi (DAI Savings Rate vs competitors)

---

## Testable Implications (Pre-Estimation)

| # | Implication | Type | Mathematical Statement | Source |
|---|---|---|---|---|
| T1 | LP fee revenue is more vol-sensitive under dynamic fees | Sign restriction | beta_2 > 0 | Strategy 1 |
| T2 | The vol sensitivity difference is larger during high-vol regimes | Monotonicity | d(beta_2)/d(sigma) >= 0 | Strategy 1, non-linear extension |
| T3 | Dynamic fee is sufficient statistic for vol in revenue equation | Exclusion | beta_sigma = 0 conditional on phi_t | Strategy 2 |
| T4 | Fee revenue spread predicts next-period vol | Granger causality | Spread_t -> sigma_{t+1} | Strategy 3 |
| T5 | Fee revenue spread widens during stress events | Sign restriction | Spread_t increases when DAI depeg > threshold | Strategy 3 |

---

## Data Requirements

| Variable | Source | Granularity | Period |
|---|---|---|---|
| feeGrowthGlobal{0,1} | Both pools on-chain | Per-block | Full pool history |
| sqrtPriceX96 | Both pools on-chain | Per-block | Full pool history |
| volatilityCumulative | Algebra pool only | Per-block | Full pool history |
| Adaptive fee level | Algebra pool (pluginConfig query) | Per-swap | Full pool history |
| TVL (liquidity) | Both pools on-chain | Per-block | Full pool history |
| Swap volume (directional) | Both pools event logs | Per-swap | Full pool history |
| MakerDAO DSR | MakerDAO on-chain | Per-block | Matching period |
| ETH/USD price | Chainlink or Uniswap | Per-block | Matching period |
