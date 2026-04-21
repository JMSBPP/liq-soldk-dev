# Structural Econometric Specification: Volume-Fee Elasticity in Algebra USDC/DAI Pool

*Date: 2026-04-01*
*Framework: Reiss & Wolak (2007), Handbook of Econometrics Vol 6A, Ch. 64*
*Pool: Quickswap V3 Algebra USDC/DAI (`0xbc8f3da0bd42e1f2509cd8671ce7c7e5f7fd39c8`, Polygon)*

---

## 1. Research Question

**Economic question**: How sensitive is trading volume in the Algebra USDC/DAI pool to changes in the dynamic fee?

**Parameter of interest**: Volume-fee elasticity epsilon = d(ln V_A) / d(ln phi), estimated separately for three vol regimes (low, mid, high) defined by the Algebra sigmoid transition points.

**Why this matters**: The elasticity determines whether LP income is genuinely long volatility (epsilon > -1, fee increase dominates volume loss) or short volatility (epsilon < -1, volume loss dominates fee increase). This is the foundation for pricing income-settled derivatives:
- IncomeFloor (put on fee revenue): cheap if epsilon > -1, expensive if epsilon < -1
- IncomePerpetual (funding rate on income): procyclical if epsilon > -1, countercyclical if epsilon < -1
- Settlement quality: |1 + epsilon| determines signal strength of income as vol proxy

**Unit of observation**: One observation per hour for the Algebra pool, covering 3 months (~2,200 observations).

**Outcome variable**: ln(V_A(t)) -- log hourly swap volume in the Algebra pool.

---

## 2. Economic Model

### 2.1 Economic Environment
Multi-pool USDC/DAI market on Polygon. All USDC/DAI pools (Algebra, Uniswap V3, V4, Balancer, Sushiswap) are part of the system. Volume allocation across pools is jointly determined by aggregator routing.

**Empirical finding (Dune query, 2026-04-01)**: The Uniswap V3 USDC/DAI pool on Polygon is ~100% aggregator spillover from the Algebra pool. 1,048 shared transactions account for essentially all Uniswap V3 volume ($4.5M of $4.5M/30d). The two pools are not independent markets -- they are two sides of the same routing decision. This rules out cross-pool comparison; the specification focuses on the Algebra pool.

### 2.2 Economic Actors
- **Aggregator router**: Observes all pool states (fee, liquidity, price) across all USDC/DAI pools on Polygon simultaneously. Splits swap orders to minimize execution cost.
- **Passive LP**: Observes pool state + external oracle (CEX prices, other yields, macro indicators). Provides liquidity for extended periods at chosen tick ranges.
- **Arbitrageur**: Observes all pool states + CEX USDC/DAI price. Trades to align pool price with market (LVR model per Milionis et al. 2022, arxiv:2208.06046).

### 2.3 Information Structure
- **Aggregator**: All USDC/DAI pool states on Polygon (fee, liquidity depth, current price)
- **Passive LP**: Pool state + external oracle (CEX prices, competing yield opportunities, macro indicators)
- **Arbitrageur**: All pool states + CEX USDC/DAI price

### 2.4 Primitives
- **CFMM trading function**: Concentrated liquidity x*y=k per tick (Algebra/Uniswap V3 math). Technological primitive.
- **Dynamic fee function**: Algebra's AdaptiveFee.sol double-sigmoid of volatilityCumulative. Institutional primitive (fixed by governance during sample).
- **Aggregator cost function**: How aggregators evaluate total execution cost (fee + price impact + gas) across pools. Technological primitive.

### 2.5 Exogenous Variables
- USDC/DAI realized volatility (driven by DAI mechanism stress, USDC confidence -- external to the pool)
- Total Polygon DEX volume (aggregate demand for DEX trading)
- MakerDAO DAI Savings Rate (monetary policy)
- USDC/DAI price deviation from 1.0 (pair-specific depeg events)

### 2.6 Model Type
Reduced-form. The elasticity epsilon captures the total volume response to fee changes from all actors combined, without decomposing by actor. Justified by Angrist & Pischke (2009, Ch. 1): reduced-form estimates with credible identification are preferable to structural models with debatable assumptions.

---

## 3. Stochastic Model

### 3.1 Unobserved Heterogeneity
Two sources of variables observed by agents but not the researcher:

1. **Off-chain order flow**: Aggregators see pending user orders before routing. We only see executed swaps. Large orders arriving during high-vol periods inflate volume despite high fee.
   - Bias direction: **Upward** on epsilon (toward zero) -- underestimates fee deterrence
   - Mitigation: USDC/DAI deviation control captures depeg-triggered rebalancing

2. **LP private strategies**: LPs reposition based on private signals (proprietary vol forecasts, CEX data). Liquidity withdrawal during high vol reduces depth, reducing volume independently of fee.
   - Bias direction: **Downward** on epsilon (more negative) -- overestimates fee deterrence
   - Mitigation: Hourly active liquidity as control variable

**Net effect**: Opposing biases partially cancel. Residual bias direction unknown without data.

### 3.2 Agent Uncertainty
Demand arrival shocks: unpredictable hourly swap demand. Even knowing fee, liquidity, and macro environment, the exact number and size of swaps in the next hour is stochastic. This is the structural error term u_t. Uncorrelated with phi_t by the predetermination argument.

### 3.3 Measurement
- **Volume**: Measured exactly from on-chain swap events. No measurement error.
- **Fee**: Aggregated as volume-weighted average per hour (phi_t = sum(fee_i * volume_i) / sum(volume_i) for all swaps in hour t). Minimizes aggregation error relative to time-weighted or end-of-hour alternatives.

### 3.4 Implied Error Structure
u_t = demand arrival shock + residual off-chain flow effect + residual LP strategy effect

Properties:
- E[u_t | phi_t, X_t] approximately 0 (by predetermination + controls)
- Var(u_t) likely heteroskedastic (higher during high-vol hours)
- Cov(u_t, u_{t-1}) likely nonzero (hourly volume is autocorrelated)
- Addressed by Newey-West HAC standard errors

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
           + gamma_2 * DSR_t
           + gamma_3 * |USDC/DAI - 1|_t
           + gamma_4 * ln(Liquidity_t)
           + u_t
```

Regime dummies D_low, D_mid, D_high defined by Algebra sigmoid transition points (gamma1, gamma2 parameters from AdaptiveFee.sol). These are mechanically determined by the deployed contract parameters, not researcher choices.

### 4.2 Distributional Assumptions
Non-parametric. No distributional assumption on u_t. Estimated by OLS with Newey-West heteroskedasticity and autocorrelation consistent (HAC) standard errors.

### 4.3 Implied Econometric Equation

See Section 4.1. The equation has:
- **LHS**: ln(hourly volume in Algebra USDC/DAI pool)
- **Parameters of interest**: epsilon_low, epsilon_mid, epsilon_high (3 regime-specific volume-fee elasticities)
- **Controls**: Total DEX volume (common demand), DSR (DAI demand channel), USDC/DAI deviation (pair-specific stress), active liquidity (LP channel)
- **Error**: u_t (demand arrival + residual unobserved heterogeneity)

### 4.4 Identification

**Identifying variation**: Predetermination of phi_t.

The Algebra adaptive fee is set by the `beforeSwap` hook in `AlgebraBasePluginV1.sol` (line 256-259). The hook:
1. Writes a new timepoint to the volatility accumulator (using current block tick data from PRIOR swaps)
2. Computes the fee from the newly written timepoint via `_getFeeAtLastTimepoint()`
3. Returns the fee to the pool
4. The swap then executes at this fee

The fee for swap N is computed BEFORE swap N's volume is realized. At per-swap level, predetermination is exact. At hourly aggregation, phi_t (volume-weighted average) is dominated by the accumulator's moving average over past periods.

**Exclusion restriction**: After controlling for {total Polygon DEX volume, MakerDAO DSR, USDC/DAI price deviation, active liquidity}, the only remaining channel through which phi_t affects V_A(t) is the direct fee-sensitivity of traders.

**Known violation risk**: USDC/DAI-specific events (depeg) not fully captured by the deviation control (nonlinear response during extreme events). Mitigated by deviation control + sensitivity analysis excluding stress windows.

---

## 5. Specification Tests

| # | Implication | Type | Mathematical Statement | Test | What Failure Means |
|---|---|---|---|---|---|
| 1 | Higher fee reduces volume | Sign restriction | epsilon_low < 0, epsilon_mid < 0, epsilon_high < 0 | t-test on each epsilon | If any epsilon > 0: omitted variable inflating volume during high-fee periods |
| 2 | Fee sensitivity increases with vol regime | Ordering | \|epsilon_high\| > \|epsilon_mid\| > \|epsilon_low\| | Wald test on ordered differences | If violated: the sigmoid regime decomposition doesn't capture volume response structure |
| 3 | Fee is predetermined | Exclusion | Coefficient on phi_{t+1} = 0 in augmented equation | t-test on future fee coefficient | If significant: predetermination fails, identification is invalid, need IV |

---

## 6. Sensitivity Analysis

### 6.1 Sensitive Assumptions

1. **Regime thresholds**: Test three definitions:
   - (a) Sigmoid transition points from AdaptiveFee.sol parameters (baseline)
   - (b) Quantile-based: 33rd/67th percentile of observed fee distribution
   - (c) Fixed basis points (to be determined from data range)
   - **Why**: Fee transitions are mechanical but volume response might break at different points

2. **Stress window exclusion**: Remove hours with |USDC/DAI - 1| > threshold. Test whether epsilon estimates change.
   - **Why**: Depeg events could dominate the regression; derivative pricing needs epsilon reliable across conditions

3. **ETH price as additional control**: Add ETH hourly price/returns.
   - **Why**: Indirect channel through DAI collateral liquidations; dropped from baseline as indirect but could matter

### 6.2 Alternative Specifications

1. **Constant elasticity (no regimes)**: Single epsilon instead of three. F-test vs regime model.
   - **Why**: Tests whether regime decomposition adds explanatory power

2. **Aggregator-only volume**: Dependent variable = volume from aggregator-routed transactions only (identified by known router contracts or shared tx_hash pattern).
   - **Why**: Tests whether fee sensitivity differs for sophisticated vs all volume

3. **Revenue as outcome**: Replace ln(V_A) with ln(R_A) = ln(phi * V_A). Coefficient on ln(phi) becomes (1 + epsilon).
   - **Why**: Directly answers "does income rise or fall with fee?" -- the derivative-relevant specification. If coefficient > 0: income rises with fee (long vol confirmed). If < 0: income falls (short vol).

---

## 7. Data Requirements

| Variable | Source | Granularity | Aggregation Method |
|---|---|---|---|
| V_A(t) | Algebra pool swap events (dex.trades or decoded events) | Per-swap -> hourly | Sum of swap amounts per hour |
| phi_t | Algebra pool fee (from swap events or plugin state) | Per-swap -> hourly | Volume-weighted average |
| D_low, D_mid, D_high | Derived from phi_t and AdaptiveFee.sol sigmoid parameters | Hourly | Based on volume-weighted average fee |
| TotalDEXVol_t | dex.trades, all pairs, Polygon | Per-swap -> hourly | Sum of all DEX volume on Polygon per hour |
| DSR_t | MakerDAO on-chain (Ethereum mainnet) | Per-block -> hourly | Last value per hour |
| \|USDC/DAI - 1\|_t | Algebra pool price (sqrtPriceX96) or oracle | Per-swap -> hourly | Time-weighted average deviation |
| Liquidity_t | Algebra pool active liquidity at current tick | Per-block -> hourly | Average or end-of-hour snapshot |
| Routing fraction | Shared tx_hash analysis (Algebra + other pools) | Per-swap -> hourly | Count of shared txs / total txs |

**Dune credit budget**: ~2,500 credits/month (community plan). Estimated 15-40 credits for main data pull. Multiple months of hourly data fits within budget.

---

## 8. Connection to Derivative Design

The estimated epsilon values map directly to income derivative specifications:

| epsilon regime | Income-vol relationship | IncomeFloor pricing | IncomePerpetual funding | Settlement quality |
|---|---|---|---|---|
| epsilon > -1 (inelastic) | Income RISES with vol | Cheap (rarely pays out in stress) | Procyclical (longs receive more in high vol) | \|1 + epsilon\| > 0: income is a vol signal |
| epsilon = -1 (unit elastic) | Income vol-neutral | Standard put pricing | Vol-neutral funding | \|1 + epsilon\| = 0: income carries no vol info |
| epsilon < -1 (elastic) | Income FALLS with vol | Expensive (pays out in stress) | Countercyclical (longs receive less in high vol) | \|1 + epsilon\| > 0: income is an inverse vol signal |

The regime-specific estimates allow differential pricing across market conditions:
- epsilon_low for baseline derivative behavior
- epsilon_mid for moderate stress pricing
- epsilon_high for tail risk / IncomeFloor payoff in crisis

---

## 9. References

- Reiss, P. & Wolak, F. (2007). "Structural Econometric Modeling: Rationales and Examples from Industrial Organization." Handbook of Econometrics Vol 6A, Ch. 64.
- Angrist, J. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press. Ch. 1 (reduced-form vs structural), Ch. 3.2.3 (bad controls), Ch. 4 (IV/exclusion restrictions).
- Wooldridge, J. (2010). *Econometric Analysis of Cross Section and Panel Data*. MIT Press. Ch. 5 (identification), Ch. 9.2 (predetermined variables).
- Milionis, J., Moallemi, C., Roughgarden, T., & Zhang, A. (2022). "Loss-Versus-Rebalancing." arxiv:2208.06046. (LVR framework for LP adverse selection)
- Lambert, G. (2021). "On-Chain Volatility and Uniswap V3." (Fee-vol relationship for static-fee pools)
- Aquilina, M., Foley, S., Gambacorta, L., & Krekel, V. (2024). "Decentralised Dealers." BIS Working Paper 1227. (80% TVL/fees to 7% of sophisticated LPs)
- Shiller, R. (1993). "Aggregate Income Risks and Hedging Mechanisms." NBER WP 4396. (Perpetual claims on income indices)
- Algebra Protocol. AdaptiveFee.sol, VolatilityOracle.sol, AlgebraBasePluginV1.sol. (Dynamic fee mechanism implementation)

---

## 10. Scope Boundaries

**In scope**: Volume-fee elasticity estimation for the Algebra USDC/DAI pool on Polygon. Characterization of income dynamics across vol regimes. Connection to income derivative pricing.

**Out of scope (separate exercises)**:
- Uniswap V4 USDC/DAI pool comparison (requires research on V4 hooks)
- Predictive content of income dynamics for macro/DeFi stress (stage 2, after epsilon is estimated)
- Other pairs or chains
- Full structural model with actor-specific objectives and equilibrium

---

*Specification derived through interactive Reiss & Wolak (2007) pipeline. Every component was confirmed by user decision via AskUserQuestion. No specification component was written autonomously.*
