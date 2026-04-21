# Summary Statistics: cCOP Residual Daily Flow + BanRep TRM

*Date: 2026-04-02*
*Source: Dune Query #6941901 + datos.gov.co TRM API*
*N: ~499 daily observations (Oct 31 2024 - Apr 1 2026)*

---

## On-Chain Variables (from sampled Dune results)

### Volume Measures (USD)

| Variable | Mean | Median (approx) | Min | Max | Notes |
|---|---|---|---|---|---|
| gross_volume_usd | ~$30,000-50,000 | ~$12,000 | $2.29 (2024-12-22) | $700,891 (2025-01-24) | Heavy right tail from whale days |
| income_volume_usd | ~$5,000-15,000 | ~$2,000 | $0 (many days) | $96,767 (2026-01-01) | Zero on days with no $200-2K transfers |
| small_volume_usd | ~$2,000-5,000 | ~$2,500 | $0 | ~$10,252 (2026-03-31) | Proxy for spending/micro-conversion |
| whale_volume_usd | ~$10,000-20,000 | $0 | $0 (most days) | $693,008 (2025-01-24) | Zero-inflated; only non-zero on ~30% of days |

### Count Measures

| Variable | Mean | Median (approx) | Min | Max | Notes |
|---|---|---|---|---|---|
| total_transfers | ~200 | ~150 | 1 | ~1,115 (2025-02-03) | Growing over time |
| income_count | ~15 | ~5 | 0 | ~117 (2025-12-25) | Zero-inflated |
| unique_senders | ~12 | ~12 | 1 | ~28 (2025-02-07) | Surprisingly stable given 1,310 clean addresses |

### Calendar Dummies (frequency in sample)

| Variable | Days = 1 | % of Total | Notes |
|---|---|---|---|
| is_quincena | ~33 | 6.6% | 15th + last day of each month (~2/month) |
| is_thursday | ~71 | 14.2% | 1/7 of days |
| is_weekend | ~143 | 28.7% | 2/7 of days |

---

## TRM Variables (from trm_daily.json, 357 raw records)

| Variable | Value | Notes |
|---|---|---|
| First date | 2024-10-01 | |
| Last date | 2026-04-02 | vigenciahasta extends to 2026-04-06 |
| Raw records (business days) | 357 | |
| After forward-fill (calendar days) | ~550 | |

### TRM Level (COP per 1 USD)

| Statistic | Value | Notes |
|---|---|---|
| Mean | ~3,900 COP/USD | Mid-range over sample period |
| Min | ~3,660 COP/USD (Mar 2026) | COP strengthening trend in 2026 |
| Max | ~4,450 COP/USD (late 2024) | COP was weaker in late 2024 |
| Start (Oct 1 2024) | 4,178.30 | |
| End (Apr 2 2026) | 3,675.81 | |
| Total change | -502.49 COP | COP appreciated 12% over sample |

### ΔTRM (Daily Change)

| Statistic | Value (approx) | Notes |
|---|---|---|
| Mean | ~-1.0 COP/day | Slight appreciation trend |
| Std | ~20-30 COP/day | Typical daily volatility |
| Min | ~-80 COP/day | Large appreciation day |
| Max | ~+60 COP/day | Large depreciation day |
| Zero days | ~150 (weekends/holidays) | Forward-filled days have Δ=0 |

---

## Sample Period Regimes

| Period | Dates | TRM Range | On-Chain Character |
|---|---|---|---|
| Launch/thin market | Oct-Nov 2024 | 4,100-4,250 | 1-10 transfers/day, sparse |
| Early growth | Dec 2024 - Feb 2025 | 4,050-4,250 | 10-400 transfers/day, rapid scaling |
| Steady state | Mar-Jun 2025 | 3,800-4,200 | 100-500 transfers/day |
| Hardfork window | Jul 7-12 2025 | excluded | Excluded from sample |
| Post-hardfork | Jul-Dec 2025 | 3,700-4,050 | 200-600 transfers/day |
| Mature | Jan-Apr 2026 | 3,660-3,900 | 300-530 transfers/day |

---

## Quincena Effect (Preliminary Visual Inspection)

From sampled data points:

| Date | is_quincena | gross_volume_usd | income_volume_usd | income_count | Notes |
|---|---|---|---|---|---|
| 2024-11-30 | 1 | $11,470 | $11,025 | 15 | Strong income spike |
| 2024-12-15 | 1 | $4,183 | $3,840 | 3 | Moderate |
| 2025-01-15 | 1 | $9,012 | $4,026 | 9 | Moderate |
| 2025-01-31 | 1 | $23,241 | $11,897 | 13 | Strong |
| 2025-02-15 | 1 | $5,222 | $3,642 | 6 | Moderate (weekend) |
| 2025-12-31 | 1 | $112,987 | $59,246 | 86 | Very strong (year-end) |
| 2026-03-31 | 1 | $13,216 | $426 | 2 | Weak (mostly small transfers) |

Initial observation: Quincena days show elevated income volumes in most months, consistent with the salary-cycle hypothesis (gamma_1 > 0). Year-end is particularly strong, consistent with prima de servicios bonus payments.

---

## Log-Transformed Variables (for regression)

These should be computed by the Analytics Reporter:

| Variable | Transform | Handle Zeros |
|---|---|---|
| ln_gross_volume | ln(1 + gross_volume_usd) | ln(1+V) avoids ln(0) |
| ln_income_volume | ln(1 + income_volume_usd) | ln(1+V); many zeros |
| delta_trm | No transform (already in levels) | |
| delta_trm_lag1 | No transform (already in levels) | |

Expected scale after log transform:
- ln(1 + $10,000) = 9.21
- ln(1 + $50,000) = 10.82
- ln(1 + $200,000) = 12.21
- ln(1 + $700,000) = 13.46

---

## Notes for Regression Specification

1. **N for estimation**: ~490 after dropping first 2 TRM days (null lagged change). If starting Dec 2024: ~460.
2. **Degrees of freedom**: 5 regressors + constant = 6 parameters. N/k ratio > 75 -- well-powered.
3. **Heteroskedasticity**: Volume has heavy right tail. Log transform + HAC SE addresses this.
4. **Autocorrelation**: Volume is likely AR(1). Newey-West HAC with Andrews (1991) bandwidth addresses this.
5. **Whale contamination**: Consider winsorizing at 99th percentile or adding whale dummy.
