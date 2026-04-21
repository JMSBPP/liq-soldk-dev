# Summary Statistics: USDC/WETH Volume-Fee Elasticity Data

*Generated: 2026-04-01*
*Based on API sample pulls across Q1 2026 (full data on Dune)*

---

## 1. Descriptive Statistics

### Fee (from Q4 full distribution, 142,422 events)

| Statistic | Value | Notes |
|-----------|-------|-------|
| Mean | 784.6 | hundredths of bip |
| Std Dev | 182.7 | |
| Min | 400 | ~4 bips (0.04%) |
| p10 | 417 | |
| p25 | 729 | |
| Median (p50) | 888 | |
| p75 | 899 | |
| p90 | 901 | |
| Max | 910 | ~9.1 bips (0.091%) |
| Distinct values | 511 | Confirms active dynamic fee |
| CV | 23.3% | Sufficient variation for regression |

### Volume USD (from Q1 hourly samples)

| Statistic | Approximate Value | Source |
|-----------|-------------------|--------|
| Typical range | $1,500 -- $50,000 per hour | Sampled rows |
| Low-activity hours | ~$1,400-2,200 | Jan 1 early hours |
| Moderate hours | ~$5,000-15,000 | Mid-quarter typical |
| High-activity hours | ~$30,000-50,000 | Late quarter spikes |
| Observations with zero volume | ~4 (missing hours) | Coverage analysis |

*Note: Full distribution statistics require downloading all ~2,156 rows from Dune. The API 100-row limit prevents computing exact percentiles here.*

### Trade Count (hourly)

| Statistic | Approximate Value |
|-----------|-------------------|
| Typical range | 20-330 per hour |
| Low activity | ~20-40 |
| Moderate | ~80-160 |
| High activity | ~200-330 |

### Liquidity (avg_liquidity, from swap events)

| Statistic | Approximate Value |
|-----------|-------------------|
| Early Jan | ~2.05e16 |
| Mid Feb | ~0.8-0.9e16 |
| Mid Mar | ~1.3-1.7e16 |
| Late Mar | ~1.7-2.0e16 |

Liquidity shows meaningful time variation (~2x range), which is important for the liquidity control variable in the regression.

### ETH Price (from Q3)

| Statistic | Value |
|-----------|-------|
| Jan 1 price | ~$2,975 |
| Mid-March price | ~$2,200-2,300 |
| Late March price | ~$2,100-2,200 |
| Approximate range | ~$2,100-$3,000 |
| Direction | Declining over Q1 2026 |

ETH declined roughly 25-30% over Q1 2026, providing substantial exogenous price variation.

### ETH Hourly Log Returns

| Statistic | Value |
|-----------|-------|
| Typical magnitude | 0.0003-0.009 |
| Range observed | approximately -0.009 to +0.005 |
| First observation | null (no prior price for LAG) |

---

## 2. Correlations (Qualitative, from sampled observations)

### Fee vs Volume

| Observation | Pattern |
|-------------|---------|
| Low fee (400-401) periods | Low volume ($1,500-4,600/hr) |
| High fee (898-900) periods | Variable volume ($5,000-50,000/hr) |
| Interpretation | Positive raw correlation -- but this is **confounded**: high vol causes high fee (via volatility accumulator), and high fee may deter some volume. The regression with controls will disentangle. |

### Fee vs ETH Price

| Observation | Pattern |
|-------------|---------|
| Jan 1 (ETH ~$2,975) | Fee = 400-401 (low) |
| Feb 11 (ETH declining) | Fee = 898-900 (high) |
| Mar 31 (ETH ~$2,100-2,200) | Fee = 610-888 (mixed) |
| Interpretation | Negative raw correlation: lower ETH price period has higher fees. Consistent with: declining ETH price -> more volatility -> higher fee. |

### Fee vs Liquidity

| Observation | Pattern |
|-------------|---------|
| Low fee (Jan 1) | Liquidity ~2.05e16 |
| High fee (Feb 11) | Liquidity ~0.8-0.9e16 |
| High fee (Mar 4) | Liquidity ~1.1-1.7e16 |
| Interpretation | Weak negative correlation: higher fees tend to coincide with lower liquidity. Consistent with: high vol -> LPs withdraw -> lower liquidity AND higher fee. |

### Volume vs ETH Price

| Observation | Pattern |
|-------------|---------|
| Jan 1 (ETH ~$2,975) | Volume $1,500-4,600 |
| Mar 4 (ETH declining) | Volume $8,400-50,000 |
| Mar 31 (ETH ~$2,100) | Volume $12,000-49,000 |
| Interpretation | Negative raw correlation with level, but higher volume during active decline. ETH sell-off drives trading activity. |

### Total Polygon DEX Volume vs Pool Volume

| Observation | Pattern |
|-------------|---------|
| Jan 1 00:00 | Polygon: $4.1M, Pool: $3,100 (0.08%) |
| Jan 1 08:00 | Polygon: $5.4M, Pool: $2,200 (0.04%) |
| Mar 31 16:00 | Polygon: $5.6M, Pool: $49,100 (0.88%) |
| Interpretation | Pool share of Polygon volume is small (0.04-0.9%) and variable. This pool is a minor venue -- most USDC/WETH volume goes through Uniswap V3. But the variation is what matters for identification. |

---

## 3. Key Findings for Specification

### 3.1 Fee Regime Recalibration Required

The original spec's regime thresholds (based on AdaptiveFee.sol default parameters: gamma1=59/beta1=360 and gamma2=8500/beta2=60000) produce:
- Low (<200): 0% of observations
- Mid (200-600): ~15% of observations
- High (>=600): ~85% of observations

This is not a useful partition. The USDC/WETH pool's fee range (400-910) sits entirely above the default "low" threshold.

**Recommended thresholds**: 500 / 800 (natural breaks in bimodal distribution)

### 3.2 Bimodal Fee Structure

The fee distribution has two clear clusters:
1. **Low-volatility regime** (fee 400-500, ~17% of events): The volatility accumulator is low, fee sits near baseFee
2. **High-volatility regime** (fee 850-910, ~69% of events): The volatility accumulator is saturated, fee near second sigmoid max

The transition zone (500-800, ~14% of events) is where the double-sigmoid is actively transitioning. This is economically the most interesting region for elasticity estimation -- the fee is genuinely varying in response to changing conditions.

### 3.3 Sufficient Identifying Variation

| Requirement | Status |
|-------------|--------|
| Fee variation (CV > 10%) | PASS: CV = 23.3% |
| Distinct fee values > 100 | PASS: 511 distinct values |
| Volume variation | PASS: $1.5K-$50K range |
| ETH price variation | PASS: ~30% decline over Q1 |
| Observations > 2,000 | PASS: ~2,156 hourly obs |
| Multiple regime hours | PARTIAL: bimodal, need recalibrated thresholds |

### 3.4 Predetermination Argument Holds

Sampled rows confirm fee events (fee_event_count) are consistently fewer than swap events (swap_count) -- the fee is set BEFORE the swap executes, via the `beforeSwap` hook. The `Fee` event fires when fee changes, and the swap then executes at that fee. This supports the predetermination identification strategy from the original spec.

### 3.5 VWAP Fee vs Simple Average Fee

In all sampled rows, `vwap_fee` and `avg_fee` are within 0-3 hundredths of bip of each other. This suggests that within any given hour, large trades and small trades face nearly the same fee (because the fee changes slowly relative to swap frequency). Either measure is suitable as the endogenous variable. Recommend using `vwap_fee` as baseline (theoretically preferred) with `avg_fee` as sensitivity check.

---

## 4. Recommended Next Steps

1. **Download full datasets** from Dune (queries 6937696, 6937702, 6937699) via web UI or Python SDK
2. **Recalibrate regime thresholds** to 500/800 (natural breaks) and test with quantile-based (p33/p67) as sensitivity
3. **Compute derived variables** in Python/R:
   - `ln(volume_usd)`, `ln(vwap_fee)`, `ln(total_polygon_dex_volume_usd)`, `ln(avg_liquidity)`
   - Realized volatility from 24h rolling window of `log_return`
   - ETH price from `avg_sqrtPriceX96` (cross-validate with `prices.hour`)
4. **Join Q1 + Q2 + Q3 on `hour`** (inner join)
5. **Run specification tests** from the original spec (Section 5):
   - Test 1: epsilon < 0 (sign restriction)
   - Test 2: |epsilon_high| > |epsilon_mid| > |epsilon_low| (ordering)
   - Test 3: coefficient on phi_{t+1} = 0 (predetermination)
