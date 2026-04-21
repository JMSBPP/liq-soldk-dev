# Data Validation Report

*Date: 2026-04-01*
*Pool: Quickswap V3 Algebra USDC/DAI on Polygon*

---

## 1. Coverage

### Temporal Coverage
- **Period requested**: 2026-01-01 to 2026-03-31 (90 days, ~2,160 hours)
- **Days with data**: 90 / 90 (100%)
- **Active hours per day**: 24 / 24 for all 90 days (100%)
- **Assessment**: COMPLETE -- no missing hours or days

### Algebra Pool Data
- **Total daily rows**: 90
- **Total swaps**: 369,345 (sum of daily trade_count)
- **Mean daily trades**: 4,104
- **Range**: 2,213 (Jan 8) to 8,291 (Mar 30)
- **Volume range**: $320K (Jan 8) to $3.75M (Mar 30)

### Total Polygon DEX Volume
- **Total daily rows**: 90
- **Range**: $67.1M (Jan 3) to $224.2M (Mar 30)
- **Active projects**: 14-16 per day

### MakerDAO DSR
- **Total DSR changes (2024-present)**: 24
- **DSR changes during Q1 2026**: 0
- **DSR value during Q1 2026**: Constant at 1.25% annualized (set 2025-10-27)

---

## 2. CRITICAL FINDING: Zero Fee Variation

### Observation
The Algebra adaptive fee is CONSTANT at 10 (hundredths of bip = 0.1 basis point = 0.001%) for the ENTIRE Q1 2026 sample:

| Statistic | Value |
|-----------|-------|
| min_fee (all days) | 10 |
| max_fee (all days) | 10 |
| median_fee (all days) | 10 |
| vwap_fee (all days) | 10.0 (floating point noise only) |
| Standard deviation | 0 |

### Implication for Identification
**The volume-fee elasticity epsilon is UNIDENTIFIED in this sample.** With Var(ln(phi_t)) = 0, the regression coefficient on ln(phi_t) has undefined standard errors. OLS cannot estimate a slope when the regressor is constant.

### Possible Explanations

1. **Low volatility regime**: The Algebra double-sigmoid is designed so that at very low realized volatility, the fee stays near baseFee. However, the observed fee of 10 is *below* the documented baseFee of 100. This suggests either:
   - The pool parameters were updated from the defaults (baseFee may have been reduced to 10)
   - The USDC/DAI pair has a custom fee configuration (stablecoin pairs often use lower baseFee)
   - The plugin configuration changed from what the spec documents

2. **Stablecoin stability**: USDC/DAI price deviation during Q1 2026 is tiny (mean: 0.007%, max: 0.67%), indicating very low realized volatility -- well below any sigmoid transition point.

3. **Contract-level override**: The fee may be hardcoded or governance-set to a fixed value, bypassing the dynamic mechanism.

### Action Required
Before proceeding with the econometric specification:
- **Verify current Algebra plugin parameters** for this specific pool on-chain
- **Extend the sample window** to search for periods with fee variation (e.g., include volatile periods from 2024-2025)
- **Consider alternative pools** where the dynamic fee actually varies (e.g., ETH/USDC Algebra pool which would have more volatility)

---

## 3. CRITICAL FINDING: Zero Aggregator Traffic

### Observation
`aggregator_volume_fraction = 0` and `aggregator_trade_count = 0` for ALL 90 days.

### Possible Explanations

1. **Router address mismatch**: The `evt_tx_from` field may not match aggregator router contracts because:
   - Aggregators may use newer contract versions not in our list
   - On Polygon, aggregators may use different proxy addresses than Ethereum mainnet
   - Trades may be routed through intermediate contracts where evt_tx_from is the user's EOA, not the router

2. **Methodology limitation**: The spec mentions using "shared tx_hash method" as an alternative to router address matching. Swaps that appear in both the Algebra pool and other pools within the same transaction are aggregator-routed. This method was NOT implemented in the current query.

3. **Prior analysis contradicts this**: The spec cites "1,048 shared transactions" between Algebra and Uniswap V3 pools. This suggests aggregator traffic exists but is not being captured by our `evt_tx_from` matching approach.

### Action Required
- Implement shared `evt_tx_hash` method: count swaps where the same tx_hash appears in both Algebra and another DEX pool
- Verify aggregator router addresses are correct for Polygon (may differ from Ethereum mainnet)

---

## 4. Price Deviation Quality

| Statistic | Value |
|-----------|-------|
| Mean daily avg deviation | 0.0079% |
| Max daily avg deviation | 0.017% (Jan 13) |
| Max single-swap deviation | 0.68% (Mar 28) |
| Median daily avg deviation | ~0.007% |

**Assessment**: The USDC/DAI peg is extremely tight during Q1 2026. No stress events or significant depegs. The max single-swap deviation of 0.68% on March 28 coincides with the highest volume day ($3.07M).

---

## 5. Liquidity Quality

| Statistic | Value |
|-----------|-------|
| Min daily avg liquidity | 2.62e19 (Jan 8-9) |
| Max daily avg liquidity | 8.91e19 (Mar 22-23) |
| Trend | Increasing over Q1 2026 (~2.5x growth) |

**Assessment**: Liquidity grew substantially during Q1 2026, from ~$26B to ~$89B in raw units. This is a real signal -- LP activity increased over the quarter. The growth is non-trivial and would be an important control variable if fee variation existed.

---

## 6. Volume Trend

| Month | Mean Daily Volume | Total Volume |
|-------|------------------|--------------|
| January | $645K | $20.0M |
| February | $685K | $19.2M |
| March | $1.30M | $40.2M |

**Assessment**: Strong upward trend. March volume is ~2x January. Volume tracks with total Polygon DEX volume (which also increased in March). The Algebra pool's share of total Polygon DEX volume is approximately 0.5-1.5%.

---

## 7. DSR Monotonic Decline

The DSR has been in secular decline since its peak at 15% in March 2024:
- 2024-03-10: 15.0%
- 2024-12-08: 11.5%
- 2025-03-24: 3.5%
- 2025-10-27: 1.25% (current, covers all of Q1 2026)

**Assessment**: DSR is constant during the sample, providing no cross-sectional variation. It drops out of the regression (absorbed by intercept).

---

## 8. Summary of Identification Viability

| Variable | Has Variation? | Usable? |
|----------|---------------|---------|
| V_A(t) (volume) | YES -- substantial daily and hourly variation | YES (LHS) |
| phi_t (fee) | NO -- constant at 10 | **FATAL: Cannot be RHS variable** |
| TotalDEXVol_t | YES -- $67M to $224M daily | YES (control) |
| DSR_t | NO -- constant at 1.25% | NO -- drops out |
| Price deviation | YES -- small but nonzero variation | YES (control) |
| Liquidity | YES -- 2.5x growth over quarter | YES (control) |
| Aggregator fraction | NO (measurement issue, likely 0 due to methodology) | NEEDS FIX |

### Bottom Line
**The volume-fee elasticity regression as specified CANNOT be estimated with Q1 2026 data.** The identifying variation (fee changes from the dynamic mechanism) does not exist in this sample. Every observation has fee = 10.

### Recommended Next Steps
1. Query historical periods with known fee variation (e.g., high-volatility periods in 2024)
2. Query a different Algebra pool where the dynamic fee is more active (ETH/USDC, ETH/MATIC)
3. Verify the actual fee parameters on-chain for this specific USDC/DAI pool
4. Consider the shared-tx_hash aggregator identification method
