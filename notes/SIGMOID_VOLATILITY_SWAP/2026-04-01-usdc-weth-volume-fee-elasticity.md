# Structural Econometric Specification: Volume-Fee Elasticity in Algebra USDC/WETH Pool

*Date: 2026-04-01*
*Framework: Reiss & Wolak (2007), Handbook of Econometrics Vol 6A, Ch. 64*
*Pool: Quickswap V3 Algebra USDC/WETH (`0xa6aedf7c4ed6e821e67a6bfd56fd1702ad9a9719`, Polygon)*
*Supersedes: 2026-04-01-usdc-dai-volume-fee-elasticity.md (USDC/DAI pool had constant fee — no identifying variation)*

---

## 0. Pool Switch Rationale

The original specification targeted USDC/DAI on Algebra. Data pull revealed:
- The adaptive fee has been constant at 10 (0.1bp) since September 2024 (governance override)
- Dynamic fee was only active Oct 2023 - Jan 2024 (4 months, sparse variation)
- With zero fee variation, the volume-fee elasticity cannot be estimated

USDC/WETH on Algebra was selected because:
- Active dynamic fees: 511 distinct fee values in last 90 days
- Meaningful volume: $8.3M/30d, ~57K trades
- ETH price volatility continuously activates the sigmoid fee mechanism
- Connects to the project's macro framework (ETH price is a macro variable)

The econometric specification transfers directly — same equation, same identification. Only the controls change (ETH price replaces DAI-specific variables).

---

## 1. Research Question

**Economic question**: How sensitive is trading volume in the Algebra USDC/WETH pool to changes in the dynamic fee?

**Parameter of interest**: Volume-fee elasticity epsilon = d(ln V_A) / d(ln phi), estimated separately for three vol regimes (low, mid, high) defined by the Algebra sigmoid transition points.

**Why this matters**: The elasticity determines whether LP income is genuinely long volatility (epsilon > -1, fee increase dominates volume loss) or short volatility (epsilon < -1, volume loss dominates fee increase). This is the foundation for pricing income-settled derivatives:
- IncomeFloor (put on fee revenue): cheap if epsilon > -1, expensive if epsilon < -1
- IncomePerpetual (funding rate on income): procyclical if epsilon > -1, countercyclical if epsilon < -1
- Settlement quality: |1 + epsilon| determines signal strength of income as vol proxy

**Unit of observation**: One observation per hour for the Algebra pool, covering 3 months (Jan-Mar 2026, ~2,200 observations).

**Outcome variable**: ln(V_A(t)) — log hourly swap volume in the Algebra pool.

---

## 2. Economic Model

### 2.1 Economic Environment
Multi-pool USDC/WETH market on Polygon. All USDC/WETH pools (Algebra/Quickswap, Uniswap V3/V4, Sushiswap, Balancer) are part of the system. Volume allocation across pools is jointly determined by aggregator routing.

### 2.2 Economic Actors
- **Aggregator router**: Observes all pool states (fee, liquidity, price) across all USDC/WETH pools on Polygon simultaneously. Splits swap orders to minimize execution cost.
- **Passive LP**: Observes pool state + external oracle (CEX prices, other yields, macro indicators). Provides liquidity for extended periods at chosen tick ranges.
- **Arbitrageur**: Observes all pool states + CEX ETH/USD price. Trades to align pool price with market (LVR model per Milionis et al. 2022, arxiv:2208.06046).

### 2.3 Information Structure
- **Aggregator**: All USDC/WETH pool states on Polygon (fee, liquidity depth, current price)
- **Passive LP**: Pool state + external oracle (CEX prices, competing yield opportunities, macro indicators)
- **Arbitrageur**: All pool states + CEX ETH/USD price

### 2.4 Primitives
- **CFMM trading function**: Concentrated liquidity x*y=k per tick (Algebra/Uniswap V3 math). Technological primitive.
- **Dynamic fee function**: Algebra's AdaptiveFee.sol double-sigmoid of volatilityCumulative. Institutional primitive (fixed by governance during sample).
- **Aggregator cost function**: How aggregators evaluate total execution cost (fee + price impact + gas) across pools. Technological primitive.

### 2.5 Exogenous Variables
- ETH/USD price (driven by global crypto markets — exogenous to this specific Polygon pool)
- Total Polygon DEX volume (aggregate demand for DEX trading)
- ETH realized volatility (computed from hourly ETH price changes — drives the Algebra fee through the volatility accumulator)

### 2.6 Model Type
Reduced-form. The elasticity epsilon captures the total volume response to fee changes from all actors combined, without decomposing by actor. Justified by Angrist & Pischke (2009, Ch. 1).

---

## 3. Stochastic Model

### 3.1 Unobserved Heterogeneity
1. **Off-chain order flow**: Aggregators see pending user orders before routing. Large orders during high-vol periods inflate volume despite high fee.
   - Bias direction: **Upward** on epsilon (toward zero)
   - Mitigation: ETH realized vol control captures macro vol events

2. **LP private strategies**: LPs reposition based on private signals. Liquidity withdrawal during high vol reduces depth and volume independently of fee.
   - Bias direction: **Downward** on epsilon (more negative)
   - Mitigation: Hourly active liquidity as control variable

### 3.2 Agent Uncertainty
Demand arrival shocks: unpredictable hourly swap demand. Uncorrelated with phi_t by predetermination.

### 3.3 Measurement
- **Volume**: Measured exactly from on-chain swap events. No measurement error.
- **Fee**: Aggregated as volume-weighted average per hour from algebrapool_evt_fee events.

---

## 4. Estimation Strategy

### 4.1 Functional Form
Log-log with regime interaction:

```
ln(V_A(t)) = alpha
           + epsilon_low * ln(phi_t) * D_low(t)
           + epsilon_mid * ln(phi_t) * D_mid(t)
           + epsilon_high * ln(phi_t) * D_high(t)
           + gamma_1 * ln(TotalDEXVol_t)
           + gamma_2 * ln(ETH_price_t)
           + gamma_3 * ln(Liquidity_t)
           + u_t
```

Regime dummies D_low, D_mid, D_high defined by observed fee distribution (bimodal structure):
- **Baseline thresholds (500/800)**: Derived from natural breaks in the fee distribution
  - D_low: avg_fee < 500 (~17% of hours — fee near baseFee floor, low vol accumulator)
  - D_mid: 500 <= avg_fee < 800 (~14% of hours — sigmoid transition zone)
  - D_high: avg_fee >= 800 (~69% of hours — near saturation, high vol accumulator)
- Fee range observed: 400 to 910 (hundredths of bip)
- Default AdaptiveFee.sol sigmoid thresholds (200/600) are NOT usable — 0% of observations fall in "low"
- Sensitivity: test with quantile-based thresholds (p33=851 / p67=896)

### 4.2 Distributional Assumptions
Non-parametric. OLS with Newey-West HAC standard errors.

### 4.3 Identification

**Identifying variation**: Predetermination of phi_t. The Algebra adaptive fee is set by the beforeSwap hook from the volatility accumulator state, computed BEFORE the swap executes. Confirmed in contract code (AlgebraBasePluginV1.sol lines 256-259, 297-319).

**Exclusion restriction**: After controlling for {total Polygon DEX volume, ETH price, active liquidity}, the only remaining channel through which phi_t affects V_A(t) is direct fee sensitivity.

**Controls (3 variables)**:
1. Total Polygon DEX volume (common demand shock)
2. ETH/USD price (pair-specific external price — drives both vol→fee and trading demand)
3. Active liquidity (LP channel control — absorbs LP withdrawal bias)

---

## 5. Specification Tests

| # | Implication | Type | Mathematical Statement | Test |
|---|---|---|---|---|
| 1 | Higher fee reduces volume | Sign | epsilon_low < 0, epsilon_mid < 0, epsilon_high < 0 | t-test |
| 2 | Fee sensitivity increases with vol | Ordering | \|epsilon_high\| > \|epsilon_mid\| > \|epsilon_low\| | Wald test |
| 3 | Fee is predetermined | Exclusion | Coefficient on phi_{t+1} = 0 | t-test |

---

## 6. Sensitivity Analysis

### 6.1 Sensitive Assumptions
1. **Regime thresholds**: (a) sigmoid transition points, (b) quantile-based, (c) fixed bp cutoffs
2. **Stress window exclusion**: Exclude hours with extreme ETH price moves (>5% hourly)
3. **ETH realized vol as additional control**: Computed from hourly price changes, separate from ETH price level

### 6.2 Alternative Specifications
1. **Constant elasticity (no regimes)**: Single epsilon. F-test vs regime model.
2. **Aggregator-only volume**: Volume from aggregator-routed transactions only.
3. **Revenue as outcome**: ln(R_A) = ln(phi * V_A). Coefficient on ln(phi) = (1 + epsilon). Directly answers derivative pricing question.

---

## 7. Data Requirements

| Variable | Source | Aggregation |
|---|---|---|
| V_A(t) | dex.trades for pool 0xa6aedf | Sum per hour |
| phi_t | algebrapool_evt_fee for pool 0xa6aedf | Volume-weighted average per hour |
| D_low/mid/high | Derived from phi_t + sigmoid params | Per hour |
| TotalDEXVol_t | dex.trades, all pairs, Polygon | Sum per hour |
| ETH_price_t | prices.usd (WETH) | Average per hour |
| Liquidity_t | algebrapool_evt_swap liquidity field | Average per hour |

---

## 8. Connection to Derivative Design

Same as original spec — see Section 8 of 2026-04-01-usdc-dai-volume-fee-elasticity.md. The mapping from epsilon to derivative pricing is pair-agnostic.

---

## 9. References

Same as original spec, plus:
- Algebra Protocol fee history data: Dune query 6937672 (confirms USDC/DAI fee was constant; USDC/WETH has active dynamic fees)
- Dune query 6937688 (survey of Algebra pools with fee variation)

---

*Specification derived through interactive Reiss & Wolak (2007) pipeline. Pool switched from USDC/DAI to USDC/WETH after data validation revealed zero fee variation in the original pool.*
