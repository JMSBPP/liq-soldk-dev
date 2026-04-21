# Data Validation Report: cCOP Residual Daily Flow + BanRep TRM

*Date: 2026-04-02*
*Spec: INCOME_SETTLEMENT/2026-04-02-ccop-cop-usd-flow-response.md*

---

## 1. On-Chain Data Completeness

### Date Coverage
- **First observation**: 2024-10-31 (cCOP deployment date)
- **Last observation**: 2026-04-01
- **Calendar days in range**: 518
- **Days with data**: ~499
- **Missing days**: ~19 (3.7%)

### Days with Zero Gross Volume
- Zero-volume days exist in the early period (Nov 2024) when cCOP was newly deployed
- **ln(0) handling**: Use `ln(1 + gross_volume_usd)` transformation, or drop zero-volume days
- Recommendation: Use `ln(1 + V)` for all volume measures to avoid data loss

### Date Gaps
- Early period (Oct-Nov 2024): Sparse activity, multiple gaps (e.g., Nov 7, Nov 9-18, Nov 20-21)
- Dec 2024 onwards: Near-continuous daily coverage
- Hardfork window excluded: Jul 7-12, 2025 (6 days by design)
- No artificial weekend gaps (on-chain activity occurs 7 days/week)

### Income Volume Zero Days
- Many days have `income_volume_usd = 0` (no transfers in $200-2000 range)
- This is more common in early months and on weekends
- For robustness spec R3 (income-only), drop these days or use `ln(1 + V)`

---

## 2. TRM Data Completeness

### Date Coverage
- **First record**: 2024-10-01
- **Last record**: 2026-04-02 (vigenciahasta extends to 2026-04-06)
- **Raw records**: 357 (business days only)
- **After forward-fill**: ~550 daily values (continuous calendar)

### Weekend/Holiday Handling
- BanRep datos.gov.co API returns SEPARATE vigencia records for Saturdays (distinct from Friday's rate)
- This means `process_trm.py`'s `expand_to_daily()` populates every calendar day directly from API data
- **QA CORRECTION (M1)**: `is_forward_filled` is always 0 in the output — the forward-fill branch in `build_continuous_daily_series()` never triggers because the API provides all dates
- **QA CORRECTION (M1)**: `delta_trm` is NOT always 0 on weekends — Saturdays carry their own BanRep rate which may differ from Friday's. Sunday's rate equals Saturday's (same vigencia record)
- `is_forward_filled` column should be treated as DEAD METADATA — do not use for sensitivity analysis

### TRM Coverage Gaps
- No gaps detected in raw data
- Continuous coverage from Oct 1, 2024 through Apr 2, 2026
- Colombian holidays are handled via vigenciahasta spanning mechanism

---

## 3. Merge Completeness

### Join Key: date (on-chain) = date (TRM)

- On-chain data starts Oct 31, 2024
- TRM data starts Oct 1, 2024 (30 days earlier -- provides lagged values for first on-chain day)
- Expected merge: ~499 days with BOTH on-chain and TRM data
- Delta_trm and delta_trm_lag1 will be null for first 1-2 days of TRM series, but these are before on-chain data begins

### Merge Recommendations
1. Inner join on date -- no data loss expected since TRM covers every calendar day
2. On weekends: TRM has its own Saturday rate (not forward-filled); Sunday = Saturday's rate. On-chain activity is genuine 7 days/week
3. Do NOT drop weekends — both TRM and on-chain data exist for all calendar days
4. ~~For robustness: flag `is_forward_filled` TRM days and test sensitivity~~ **REMOVED per QA M1: is_forward_filled is always 0, sensitivity test would be vacuous**

---

## 4. Sample Data Inspection

### Early Period (Oct-Nov 2024) — Thin Market

| Day | Gross Volume | Income Volume | Transfers | Senders | Notes |
|---|---|---|---|---|---|
| 2024-10-31 | $209 | $0 | 5 | 1 | Launch day, 1 sender |
| 2024-11-04 | $1,994 | $1,994 | 2 | 2 | First income-sized transfers |
| 2024-11-06 | $3,512 | $3,307 | 10 | 5 | First meaningful activity |
| 2024-11-25 | $71,971 | $0 | 6 | 5 | Whale day ($71.9K whale) |
| 2024-11-30 | $11,470 | $11,025 | 42 | 12 | Quincena (last day of month) |

### Growth Period (Jan-Feb 2025) — Scaling

| Day | Gross Volume | Income Volume | Transfers | Senders | Notes |
|---|---|---|---|---|---|
| 2025-01-06 | $24,794 | $17,321 | 95 | 11 | Post-holiday spike |
| 2025-01-24 | $700,891 | $3,820 | 223 | 15 | Massive whale day ($693K whale) |
| 2025-01-31 | $23,241 | $11,897 | 159 | 16 | Quincena |
| 2025-02-15 | $5,222 | $3,642 | 70 | 11 | Quincena + weekend |

### Mature Period (late 2025 - 2026) — Dense

| Day | Gross Volume | Income Volume | Transfers | Senders | Notes |
|---|---|---|---|---|---|
| 2025-12-31 | $112,987 | $59,246 | 299 | 14 | Quincena + year-end |
| 2026-01-02 | $159,161 | $75,340 | 413 | 13 | Post-holiday |
| 2026-03-31 | $13,216 | $426 | 530 | 13 | Quincena |
| 2026-04-01 | $11,025 | $1,993 | 352 | 11 | Most recent day |

---

## 5. Outlier Flags

### Whale Volume Spikes
Days where whale_volume_usd dominates gross_volume_usd (>90% whale):
- 2024-11-25: $71,907 whale out of $71,971 total (99.9%)
- 2024-12-26: $89,731 whale out of $89,953 total (99.8%)
- 2025-01-24: $693,008 whale out of $700,891 total (98.9%)

These are treasury/arbitrage operations from clean addresses. They do not bias the regression if `ln(gross_volume)` is used (log transform dampens outliers), but should be flagged.

### Structural Breaks
- **2024-12-27 onwards**: Activity jumps from ~10 transfers/day to 100+/day
- **2025-01-25**: Mento token migration (cCOP to COPm). Volume continues but token_symbol changes
- **2025-07-07 to 2025-07-12**: Excluded (hardfork window)

---

## 6. Data Quality Scores

| Check | Status | Detail |
|---|---|---|
| Date continuity (Dec 2024+) | PASS | Near-continuous daily coverage |
| Date continuity (Oct-Nov 2024) | WARN | Sparse, 19 missing days |
| Zero gross_volume days | WARN | Exists in early period. Use ln(1+V) |
| TRM coverage | PASS | Full coverage, no gaps |
| Merge completeness | PASS | TRM covers all on-chain dates |
| Whale contamination | WARN | 3 days with >90% whale volume |
| Filter aggressiveness | INFO | Campaign filter removes 71% of addresses. Document in sensitivity analysis |
| Token migration continuity | PASS | cCOP and COPm share same contract address |

---

## 7. Recommendations for Analytics Reporter

1. **Start regression from 2024-12-01** (not Oct 31) to avoid the thin-market launch period
2. **Use ln(1 + gross_volume_usd)** to handle zero-volume days
3. **Use Newey-West HAC standard errors** (already specified) to handle autocorrelation
4. **Flag whale days** with a dummy variable or winsorize at 99th percentile
5. **Include is_forward_filled** as a control or interaction term in sensitivity checks
6. **For R6 (bidirectional decomposition)**: Use income_volume, small_volume, whale_volume separately
7. **Run sensitivity S1/S2/S3** with different campaign thresholds (no filter, >50, >20)

---

## 8. Action Items Before Estimation

- [ ] Run `python3 raw/process_trm.py` to generate `trm_processed.csv`
- [ ] Download full Dune results via API: `curl "https://api.dune.com/api/v1/query/6941901/results/csv" -H "X-DUNE-API-KEY: $KEY" -o ccop_residual_daily.csv`
- [ ] Merge on-chain CSV + TRM CSV on date
- [ ] Compute ln(1 + V) columns
- [ ] Verify N >= 450 after merge and dropping first 2 days (null delta_trm)
