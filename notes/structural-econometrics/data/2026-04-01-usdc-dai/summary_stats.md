# Summary Statistics

*Date: 2026-04-01*
*Pool: Quickswap V3 Algebra USDC/DAI on Polygon*
*Period: Q1 2026 (90 days, daily aggregation)*
*Source: Dune queries 6937640, 6937641, 6937638*

---

## 1. Algebra Pool Variables (Daily)

### Daily Volume (USD)

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | $882,217 |
| Std Dev | $541,892 |
| Min | $320,423 (Jan 8) |
| P25 | $540,958 |
| Median | $779,178 |
| P75 | $1,106,794 |
| Max | $3,751,858 (Mar 30) |
| Total | $79,399,509 |
| CV | 0.61 |

### Daily Trade Count

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | 4,104 |
| Std Dev | 1,258 |
| Min | 2,213 (Jan 8) |
| Median | 4,095 |
| Max | 8,291 (Mar 30) |
| Total | 369,345 |

### Fee (Hundredths of Basis Point)

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | 10.0 |
| Std Dev | 0.0 |
| Min | 10 |
| Max | 10 |
| **Variation** | **NONE** |

### Average Price Deviation |USDC/DAI - 1|

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | 7.93e-05 (0.0079%) |
| Std Dev | 2.85e-05 |
| Min | 3.39e-05 (0.0034%) |
| Median | 7.70e-05 (0.0077%) |
| Max | 1.72e-04 (0.0172%) |

### Max Price Deviation (within day)

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | 5.37e-04 (0.054%) |
| Min | 1.74e-04 (0.017%) |
| Max | 6.77e-03 (0.677%, Mar 28) |

### Average Liquidity (raw uint128)

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | 5.85e19 |
| Std Dev | 1.36e19 |
| Min | 2.62e19 (Jan 8) |
| Max | 8.91e19 (Mar 22) |
| Trend | Increasing (~2.5x growth over quarter) |

---

## 2. Total Polygon DEX Volume (Daily)

| Statistic | Value |
|-----------|-------|
| N | 90 |
| Mean | $116.6M |
| Std Dev | $28.3M |
| Min | $67.1M (Jan 3) |
| Median | $113.4M |
| Max | $224.2M (Mar 30) |
| Total | $10.5B |

### Algebra Pool Share of Polygon DEX Volume

| Statistic | Value |
|-----------|-------|
| Mean | 0.76% |
| Min | 0.30% |
| Max | 1.67% |

---

## 3. MakerDAO DSR

| Statistic | Value |
|-----------|-------|
| Value during Q1 2026 | 1.25% annualized |
| Variation | NONE (constant) |
| Last change | 2025-10-27 |
| Previous value | 1.50% |
| DSR trend (2024-2026) | Monotonic decline: 15% -> 1.25% |

---

## 4. Monthly Breakdown

### January 2026

| Variable | Mean | Std Dev | Min | Max |
|----------|------|---------|-----|-----|
| Daily Volume ($) | 645,426 | 282,178 | 320,423 | 1,381,588 |
| Trade Count | 2,918 | 500 | 2,213 | 4,516 |
| VWAP Fee | 10.0 | 0.0 | 10 | 10 |
| Price Dev (%) | 0.0084 | 0.0034 | 0.0034 | 0.0170 |
| Polygon DEX Vol ($M) | 107.5 | 19.6 | 67.1 | 167.7 |

### February 2026

| Variable | Mean | Std Dev | Min | Max |
|----------|------|---------|-----|-----|
| Daily Volume ($) | 685,276 | 231,367 | 391,175 | 1,723,580 |
| Trade Count | 4,142 | 639 | 3,091 | 5,622 |
| VWAP Fee | 10.0 | 0.0 | 10 | 10 |
| Price Dev (%) | 0.0073 | 0.0023 | 0.0037 | 0.0119 |
| Polygon DEX Vol ($M) | 108.4 | 22.0 | 81.2 | 186.2 |

### March 2026

| Variable | Mean | Std Dev | Min | Max |
|----------|------|---------|-----|-----|
| Daily Volume ($) | 1,296,330 | 604,399 | 770,583 | 3,751,858 |
| Trade Count | 5,355 | 758 | 3,822 | 8,291 |
| VWAP Fee | 10.0 | 0.0 | 10 | 10 |
| Price Dev (%) | 0.0073 | 0.0017 | 0.0053 | 0.0133 |
| Polygon DEX Vol ($M) | 133.4 | 30.1 | 88.5 | 224.2 |

---

## 5. Correlations (Daily Level, N=90)

### Observable Relationships

Based on the 90 daily observations:

| Pair | Direction | Notes |
|------|-----------|-------|
| Algebra Volume vs. Polygon DEX Volume | Positive | Both increase in March |
| Algebra Volume vs. Liquidity | Positive | Both trend upward |
| Algebra Volume vs. Price Deviation | Weak positive | High-volume days slightly higher deviation |
| Polygon DEX Volume vs. Trade Count | Strong positive | Market-wide activity measure |
| Liquidity vs. Time | Strong positive | Secular growth trend |

### Correlations NOT computable

| Pair | Reason |
|------|--------|
| Volume vs. Fee | Fee is constant (zero variance) |
| Any variable vs. DSR | DSR is constant (zero variance) |
| Any variable vs. Aggregator fraction | Aggregator fraction is 0 (measurement issue) |

---

## 6. Regime Classification (As Specified)

The spec defines three regimes based on Algebra sigmoid transition points:
- **Low**: Fee near baseFee (before first sigmoid kicks in)
- **Mid**: First sigmoid active (volatility ~ beta1 = 360)
- **High**: Second sigmoid active (volatility ~ beta2 = 60000)

### Observed Regime Distribution

| Regime | Hours | Fraction |
|--------|-------|----------|
| Low (fee = 10) | 2,160 | 100% |
| Mid | 0 | 0% |
| High | 0 | 0% |

**All observations are in a single regime.** The regime interaction model collapses to a single-regime model, but even that single regime has no fee variation.

---

## 7. Data Quality Scores

| Check | Status | Details |
|-------|--------|---------|
| Temporal completeness | PASS | 90/90 days, 24/24 hours per day |
| Volume non-negative | PASS | All values > 0 |
| Price within bounds | PASS | All prices within [0.993, 1.007] |
| Fee non-negative | PASS | All fees = 10 |
| Liquidity non-negative | PASS | All values > 0 |
| No NULL values | PASS | All columns populated |
| Fee variation | **FAIL** | Zero variance -- identification impossible |
| Aggregator detection | **FAIL** | Zero aggregator trades detected (likely methodology issue) |
| DSR variation | **FAIL** | Constant during sample |
