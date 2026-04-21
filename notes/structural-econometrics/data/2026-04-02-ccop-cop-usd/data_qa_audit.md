# Data Pipeline QA Audit

*Auditor: Model QA Specialist (Independent)*
*Date: 2026-04-02*
*Pipeline under review: cCOP Residual Daily Flow + BanRep TRM*
*Spec: INCOME_SETTLEMENT/2026-04-02-ccop-cop-usd-flow-response.md*

---

## Overall Verdict: PASS WITH CONDITIONS

The data pipeline correctly implements the user-approved filtering definition and produces a dataset suitable for the specified regression. However, there are **2 Medium** and **4 Low** severity findings that should be addressed before the Analytics Reporter runs estimation. No High-severity (model-invalidating) issues were found.

---

## A. Query-to-Spec Alignment

### A1: Filter Implementation -- PASS

All five filter conditions from the user-approved definition are implemented correctly in Query #6941901:

| Filter | Spec Definition | SQL Implementation | Match? |
|---|---|---|---|
| Thursday UBI | >80% of txns on Thursdays AND >=3 txns | `total_txns >= 3 AND CAST(thursday_txns AS DOUBLE) / total_txns > 0.8` | YES |
| Bot | >1000 txns AND <10 unique counterparties | `total_txns > 1000 AND unique_counterparties < 10` | YES |
| Campaign spike | First appeared on days with >50 new senders | `HAVING COUNT(*) > 50` on `first_date` grouped by address_stats | YES |
| Dust | amount_usd < $1 | `t.amount_usd >= 1.0` | YES |
| Hardfork window | block_date BETWEEN 2025-07-07 AND 2025-07-12 | `CAST(t.block_time AS DATE) NOT BETWEEN DATE '2025-07-07' AND DATE '2025-07-12'` | YES |

**Detail on filter logic**: The query uses a single-pass design with CTEs (`address_stats` -> `campaign_days` -> `flagged_addresses` -> `clean_addresses`) joined via INNER JOIN. This means only transfers FROM clean sender addresses are included. The filter is applied to the `"from"` (sender) side only. This is consistent with the spec, which defines the filter on sender behavior.

### A2: Filter Thresholds -- PASS

All numeric thresholds match exactly:
- Thursday: >0.8 (80%) with >=3 txns -- correct
- Bot: >1000 txns AND <10 counterparties -- correct
- Campaign: >50 new senders/day -- correct
- Dust: <$1 excluded (>= $1 included) -- correct
- Hardfork: Jul 7-12 inclusive via BETWEEN -- correct

### A3: Output Columns -- PASS

| Spec Requirement | Query Column | Computed Correctly? |
|---|---|---|
| gross_volume | `SUM(t.amount_usd)` | YES |
| income_volume ($200-$2000) | `SUM(CASE WHEN t.amount_usd BETWEEN 200 AND 2000 ...)` | YES |
| small_volume ($1-$50) | `SUM(CASE WHEN t.amount_usd BETWEEN 1 AND 50 ...)` | YES |
| whale_volume (>$2000) | `SUM(CASE WHEN t.amount_usd > 2000 ...)` | YES |
| total_transfers | `COUNT(*)` | YES |
| income_count | `SUM(CASE WHEN ... BETWEEN 200 AND 2000 THEN 1 ...)` | YES |
| unique_senders | `COUNT(DISTINCT t."from")` | YES |
| day_of_week | `day_of_week(CAST(...))` | YES (ISO: 1=Mon, 7=Sun) |
| is_quincena | DAY=15 OR LAST_DAY_OF_MONTH | YES -- see A4 |
| is_thursday | day_of_week = 4 | YES |
| is_weekend | day_of_week IN (6,7) | YES |

### A4: Quincena Dummy -- PASS

```sql
CASE WHEN DAY(CAST(t.block_time AS DATE)) = 15 
     OR CAST(t.block_time AS DATE) = LAST_DAY_OF_MONTH(CAST(t.block_time AS DATE)) 
     THEN 1 ELSE 0 END
```

This correctly handles variable month lengths (28/29/30/31) via DuneSQL's `LAST_DAY_OF_MONTH()` built-in function. The implementation is robust to leap years and variable month lengths.

### A5: Token Scope -- PASS

```sql
AND token_symbol IN ('cCOP', 'COPm')
```

Correctly includes both Mento tokens (cCOP = pre-migration, COPm = post-migration) and excludes COPM (Minteo). The diagnostic query #6941902 confirms three distinct symbols exist: cCOP (227,536 txns), COPm (55,222 txns), COPM (104,830 txns). Case sensitivity in DuneSQL correctly distinguishes COPm from COPM.

### A6: Missing Volume Bucket -- LOW (Info)

**Observation**: The spec mentions a "mid-range ($50-200)" bucket implicitly (data_dictionary.md line 29: "gross = income + small + mid-range ($50-200) + whale"). However, there is no explicit `mid_volume_usd` column for the $50-$200 range in the query output. The mid-range is included in `gross_volume_usd` but cannot be isolated.

**Impact**: Does not affect the primary or robustness regressions (which use gross, income, small, and whale). However, if R6 (bidirectional decomposition) needs a clean decomposition, the mid-range gap means gross != small + income + whale.

**Recommendation**: Accept as-is for Exercise 1. If R6 is run, add a `mid_volume_usd` column or document that gross - small - income - whale = mid-range.

**Finding severity: Info**

---

## B. TRM Processing

### B7: JSON Parsing -- PASS

`process_trm.py` correctly parses the datos.gov.co Socrata JSON format:
- `vigenciadesde`: parsed via `datetime.fromisoformat()` after stripping the `.000` suffix
- `vigenciahasta`: parsed to determine coverage span
- `valor`: cast to float (raw is string in JSON)
- Records sorted by date after loading

The `parse_date` function uses string replacement `s.replace("T00:00:00.000", "")` which is specific to the datos.gov.co format (always midnight timestamps). This is fragile if the API ever returns different time components, but acceptable for a one-shot data pull.

### B8: Delta TRM Direction -- PASS

```python
delta_trm = trm - series[i - 1][1]  # TRM_t - TRM_{t-1}
```

This is correct: positive delta_trm = COP depreciation (more COP needed per USD), which is the economically meaningful direction documented in the data dictionary. Confirmed by CSV: 2024-10-02 has TRM=4224.21, previous day TRM=4178.30, delta_trm=45.91 = 4224.21 - 4178.30. Correct.

### B9: Lagged Delta TRM -- PASS

```python
delta_trm_lag1 = series[i - 1][1] - series[i - 2][1]  # TRM_{t-1} - TRM_{t-2}
```

Correct: this is the one-period lag of delta_trm. Confirmed by CSV: row for 2024-10-03 has delta_trm_lag1=45.91 which equals the delta_trm from 2024-10-02. Correct chain.

### B10: Weekend Forward-Fill -- NEEDS REVISION (Medium)

**Observation**: The `is_forward_filled` column is **always 0** in the entire 553-row output. It is never set to 1 for any record.

**Root cause**: The datos.gov.co API returns records where weekends have their OWN `vigenciadesde` entry (e.g., Oct 5 Saturday has `vigenciadesde=2024-10-05, vigenciahasta=2024-10-07, valor=4173.66`). The `expand_to_daily()` function expands this range into the `daily_map`, so when `build_continuous_daily_series()` checks `if current in daily_map`, it finds Saturday/Sunday/Monday all present, and the `elif` branch (which sets `is_forward_filled=True`) never executes.

**Consequence**: The `is_forward_filled` flag is dead metadata. The validation report claims "delta_trm = 0 on weekends" (validation.md, section 2), but this is INCORRECT. Examining the CSV:

- 2024-10-05 (Saturday): delta_trm = -24.07 (NON-ZERO)
- 2024-10-06 (Sunday): delta_trm = 0.0 (zero, as expected)
- 2026-03-28 (Saturday): delta_trm = -6.40 (NON-ZERO)
- 2026-03-29 (Sunday): delta_trm = 0.0 (zero, as expected)

Saturdays carry a non-zero delta_trm because the datos.gov.co API publishes a distinct rate for Saturday that may differ from Friday's rate (both derived from Friday's trading, but the Saturday vigencia value can differ). Only Sundays have delta_trm=0 because Sunday's rate equals Saturday's rate within the same vigencia range.

**Impact on regression**: For the primary specification, DELTA_TRM on weekends is a regressor. Saturday having genuine non-zero delta_trm is economically correct (it reflects the latest available FX information). Sunday having delta_trm=0 is also correct (no new information). However, the validation report's documentation is misleading, and the `is_forward_filled` flag is useless for the sensitivity check recommended in validation.md section 3 ("flag is_forward_filled TRM days and test sensitivity").

**Remediation**:
1. Fix `is_forward_filled` logic: mark a date as forward-filled if `is_weekend=1 AND delta_trm=0` (Sunday pattern), OR replace with a simpler `is_business_day` flag (Python `weekday() < 5`).
2. Correct validation.md section 2: "delta_trm = 0 on Sundays and holidays (same rate as prior day). Saturdays may have non-zero delta_trm because BanRep publishes a distinct vigencia rate."
3. Or, if the intent is to mark economically-stale TRM days, use: `is_stale_trm = 1 if delta_trm == 0 and is_weekend == 1`.

**Finding severity: Medium** -- The dead flag will silently pass through to the Analytics Reporter, who may rely on it for sensitivity analysis per the validation report's recommendation. The sensitivity check would be vacuous (no rows flagged).

### B11: Date Parsing Edge Cases -- LOW

**Observation**: The `parse_date` function replaces `"T00:00:00.000"` with empty string before calling `fromisoformat()`. This is brittle:
- If any record has a different time component (e.g., `T12:00:00.000`), the replacement fails silently and `fromisoformat` receives `"2024-10-05T12:00:00"`, which parses as a datetime, not a date. The `.date()` call would then strip the time, so the result would still be correct.
- If a record has no time component (just `"2024-10-05"`), the replacement is a no-op and parsing succeeds.

**Impact**: Low risk. The datos.gov.co API consistently uses midnight timestamps. The function would still produce correct dates even with non-midnight timestamps due to the `.date()` call.

**Finding severity: Low**

### B12: TRM Processed CSV Verification -- PASS WITH OBSERVATION

**CSV structure**: 553 data rows + 1 header = 554 lines total. Columns: date, trm, delta_trm, delta_trm_lag1, is_weekend, is_forward_filled. Correct.

**Date range**: 2024-10-01 to 2026-04-06. The end date extends 4 days beyond Apr 2 because the last vigenciahasta in the raw JSON extends to Apr 6. This is benign -- the on-chain data only goes to Apr 1, so the extra TRM rows are ignored in the merge.

**Null handling**: First row (2024-10-01) has empty delta_trm and delta_trm_lag1. Second row (2024-10-02) has empty delta_trm_lag1. All subsequent rows have values. Correct behavior.

**Floating point**: Values show full double precision (e.g., `45.909999999999854` instead of `45.91`). This is cosmetic and does not affect regression estimation, but the CSV should ideally round to 2 decimal places for readability and to avoid false precision implications.

**Finding severity: Low** (floating point display only)

---

## C. Data Dictionary

### C13: Variable Coverage -- PASS

All variables in the spec equation are defined in data_dictionary.md:

| Spec Variable | Dictionary Entry | Defined? |
|---|---|---|
| ln(V_t) | ln_gross_volume (merged dataset section) | YES |
| DELTA_TRM_t | delta_trm | YES |
| DELTA_TRM_{t-1} | delta_trm_lag1 | YES |
| D_quincena | is_quincena | YES |
| D_thursday | is_thursday | YES |
| D_weekend | is_weekend | YES |
| ln(income_volume) | ln_income_volume (merged dataset section) | YES |

### C14: Units -- PASS

| Variable | Units Stated? | Correct? |
|---|---|---|
| gross_volume_usd | "USD" | YES |
| income_volume_usd | "USD" | YES |
| trm | "COP/USD" | YES |
| delta_trm | "COP" | YES |
| is_quincena | "0/1" | YES |
| is_thursday | "0/1" | YES |
| is_weekend | "0/1" | YES |

### C15: Filtering Steps -- PASS

All five filter steps are documented in the "Filter Definitions" section of data_dictionary.md with rule, rationale, and impact for each.

### C16: Merge Procedure -- PASS

The merge procedure is documented in the "Merged Dataset Variables" section: join on `date = day`, with specific column mappings. The validation report (section 3) provides additional merge recommendations.

---

## D. Validation Report

### D17: Zero-Volume Day Counts -- NEEDS REVISION (Low)

**Observation**: The validation report (section 1) states "Zero-volume days exist in the early period (Nov 2024)" but does not provide an EXACT count of zero-volume days. For a QA document, the precise count matters because:
- It determines how many observations are effectively lost if the analyst drops zeros
- It affects the interpretation of ln(1+V) for those days (ln(1) = 0)

**Recommendation**: Add exact counts: "X days with gross_volume_usd = 0, Y days with income_volume_usd = 0, concentrated in [specific date range]."

**Finding severity: Low** -- The information is available in the Dune results but not surfaced in the validation document.

### D18: Whale Contamination Flags -- PASS

Three whale-dominated days are flagged (>90% whale volume): 2024-11-25, 2024-12-26, 2025-01-24. The recommendation to use log transform (dampens outliers) or add whale dummy is appropriate.

### D19: Start Date Recommendation -- PASS

The recommendation to start from Dec 2024 (instead of Oct 31) is justified by:
- Oct-Nov 2024 has only sparse data (1-10 transfers/day)
- 19 missing days concentrated in this period
- Single-sender launch day (Oct 31)
- Regression starting from Dec 2024 would have ~460 observations, still well-powered (N/k > 75)

### D20: Unflagged Data Quality Issues -- MEDIUM

**Finding 1: Sender-side-only filtering is underdocumented**

The query filters on `t."from"` (sender) via INNER JOIN with `clean_addresses`. This means:
- A transfer FROM a clean address TO a bot address IS included
- A transfer FROM a bot address TO a clean address is EXCLUDED
- The filter is asymmetric by design (sender behavior defines address type)

This is economically reasonable (the sender initiates the conversion), but neither the data dictionary nor the validation report explicitly states that filtering is sender-side only. An analyst might assume transfers involving filtered addresses on EITHER side are excluded.

**Recommendation**: Add to data_dictionary.md: "Filters are applied to the SENDER (from) address only. A clean sender may send to a filtered address, and that transfer is included."

**Finding 2: Campaign filter overlap with hardfork window**

The campaign days (2025-07-30, 2025-07-31) are close to but not overlapping with the hardfork window (2025-07-07 to 2025-07-12). However, the July 2025 period has BOTH the hardfork exclusion AND the campaign mass-onboarding starting July 30. The validation report does not flag whether the campaign addresses were active during the hardfork window -- if so, their hardfork-window transactions are already excluded, and the campaign filter is redundant for those dates. Not a bug, but worth noting.

**Finding 3: No documentation of query `is_temp` status**

Dune queries can be temporary (auto-deleted after 30 days) or permanent. Neither queries.md nor execution_ids.json documents whether the queries are permanent (`is_temp: false`). If any query is temporary, the pipeline is not reproducible after 30 days.

**Finding severity: Medium** (Finding 1 + Finding 3 combined -- the asymmetric filter is a documentation gap that could mislead the analyst, and the `is_temp` status is a reproducibility risk)

---

## E. Merge Logic

### E21: Date Join Ambiguity -- PASS

The on-chain data uses `CAST(block_time AS DATE) AS day` and the TRM data uses `date` (calendar date). Both are plain dates without timezone complications. The join is unambiguous: one row per day on each side.

### E22: Weekend TRM Behavior -- PASS WITH OBSERVATION

On weekends:
- TRM is populated (Saturday has its own vigencia rate, Sunday carries the same value)
- On-chain data has genuine weekend activity (blockchain runs 24/7)
- delta_trm on Saturday may be non-zero (see finding B10); on Sunday it is zero

The merge produces valid rows for weekends. The `is_weekend` dummy in the regression absorbs the baseline activity level difference. No data loss.

### E23: Zero On-Chain Volume + Valid TRM -- PASS

On days where TRM exists but on-chain has zero volume (early period), the on-chain query simply does not emit a row for that day (no transfers pass the filters). After merge:
- Inner join: these days are dropped (TRM row exists but no on-chain row)
- This is correct behavior -- no need to impute zero-volume days that never had activity

The validation report correctly recommends inner join with no data loss expected since "TRM covers every calendar day."

### E24: ln(1+V) Appropriateness -- PASS WITH CAVEAT

The recommendation to use `ln(1 + gross_volume_usd)` is standard practice for handling zeros. However:

**Observation**: For the primary LHS variable (gross_volume_usd), the minimum non-zero value in the sampled data is $2.29 (2024-12-22). If the regression starts from Dec 2024 per the recommendation, actual zeros may be rare or nonexistent.

**Caveat**: The ln(1+V) transformation creates a nonlinear distortion for small values:
- ln(1 + $2.29) = 1.19 vs ln($2.29) = 0.83 -- 43% difference
- ln(1 + $10,000) = 9.21 vs ln($10,000) = 9.21 -- 0.01% difference

For days with gross volume < $100, the +1 shift materially affects the log value. Since the regression is estimated on a range from ~$2 to ~$700K, the log transform with +1 is acceptable because very-small-volume days are rare and in the tail. However, the analyst should verify: if starting from Dec 2024, are there any days with exactly zero gross volume? If not, plain `ln(V)` avoids the distortion entirely.

**Recommendation**: Check for zeros after the Dec 2024 start date. If none exist, use `ln(V)` instead of `ln(1+V)` to avoid the small-value distortion.

---

## F. Reproducibility

### F25: End-to-End Reproducibility -- PASS WITH CONDITIONS

The pipeline can be reproduced as follows:
1. Download Dune results via API: `curl "https://api.dune.com/api/v1/query/6941901/results/csv" -H "X-DUNE-API-KEY: $KEY"` -- documented in queries.md
2. Fetch TRM JSON: datos.gov.co Socrata API -- URL documented in process_trm.py header (`https://www.datos.gov.co/resource/mcec-87by.json`), but exact query parameters (date range, limit) are NOT documented
3. Run `python3 process_trm.py` -- documented, deterministic, no external dependencies beyond standard library
4. Merge CSVs on date -- documented in data_dictionary.md

**Gap**: The exact `curl` command or API parameters used to fetch `trm_daily.json` are not documented anywhere. The datos.gov.co Socrata API requires `$where` clauses and `$limit` parameters to fetch the correct date range. Without these, the fetch is not reproducible.

### F26: Dune Query Permanence -- NEEDS REVISION (Medium, combined with D20-F3)

The execution_ids.json records query IDs and execution IDs, but does NOT record whether queries are `is_temp: false` (permanent). The queries.md lists URLs but does not confirm permanence.

For reproducibility, the queries MUST be permanent. If they are temporary, they auto-delete after 30 days, making the pipeline irreproducible.

**Recommendation**: Verify via Dune API that all queries have `is_temp: false`. Document this in execution_ids.json. If any are temporary, convert them to permanent.

### F27: datos.gov.co API Documentation -- NEEDS REVISION (Low)

**Observation**: The process_trm.py docstring says `Source: https://www.datos.gov.co/resource/mcec-87by.json` but does not document:
- The exact query parameters used (e.g., `$where=vigenciadesde >= '2024-10-01'`, `$limit=1000`)
- Whether authentication was needed (the data_dictionary says "None" -- good)
- The exact curl command that produced trm_daily.json

**Recommendation**: Add the exact curl command to either process_trm.py or a README in the raw/ directory:
```bash
curl "https://www.datos.gov.co/resource/mcec-87by.json?\$where=vigenciadesde>='2024-10-01T00:00:00.000'&\$limit=5000&\$order=vigenciadesde" -o trm_daily.json
```

**Finding severity: Low** -- The data is already fetched and saved as trm_daily.json. The missing documentation is a reproducibility gap for future re-fetches.

---

## G. Ranked Issues (Priority Order)

Issues that must be addressed before the Analytics Reporter runs estimation:

### Priority 1 (Must Fix)

| # | Finding | Severity | Section | Action Required |
|---|---|---|---|---|
| 1 | `is_forward_filled` column is always 0 (dead metadata) | Medium | B10 | Fix the flag logic OR remove the column and update all documentation that references it. The validation report's recommendation to "flag is_forward_filled TRM days and test sensitivity" is currently vacuous. |
| 2 | Dune query `is_temp` status undocumented | Medium | D20/F26 | Verify all 6 queries are permanent via Dune API. Add `"is_temp": false` to execution_ids.json. If any are temporary, convert them immediately. |

### Priority 2 (Should Fix)

| # | Finding | Severity | Section | Action Required |
|---|---|---|---|---|
| 3 | Sender-side-only filtering underdocumented | Medium | D20 | Add explicit statement to data_dictionary.md that filters apply to sender (`"from"`) only. |
| 4 | Validation report incorrectly claims "delta_trm = 0 on weekends" | Low | B10 | Correct to: "delta_trm = 0 on Sundays (same rate as Saturday). Saturdays may have non-zero delta_trm." |
| 5 | datos.gov.co fetch command undocumented | Low | F27 | Add exact curl command to process_trm.py or raw/ directory. |
| 6 | Zero-volume day counts not explicit in validation report | Low | D17 | Add exact counts of zero-volume days by variable and date range. |

### Priority 3 (Nice to Have)

| # | Finding | Severity | Section | Action Required |
|---|---|---|---|---|
| 7 | Floating point display in CSV | Low | B12 | Round delta_trm and delta_trm_lag1 to 2 decimal places in write_csv(). |
| 8 | Missing mid-range volume bucket ($50-200) | Info | A6 | Document that gross != small + income + whale. Add mid_volume_usd if R6 decomposition is needed. |
| 9 | ln(1+V) vs ln(V) choice should depend on zero count | Info | E24 | Check for zeros after Dec 2024 start date. If none, use ln(V). |

---

## H. Positive Findings (What the Pipeline Does Well)

1. **Single-pass query design**: The CTE-based approach computes address flags and aggregates in one query, avoiding the risk of version mismatch between separate filter and aggregation queries.

2. **Correct quincena implementation**: Using `LAST_DAY_OF_MONTH()` instead of hardcoded day numbers handles variable month lengths correctly.

3. **Token scope precision**: Case-sensitive filtering correctly distinguishes COPm (Mento, included) from COPM (Minteo, excluded).

4. **Functional Python style**: `process_trm.py` uses frozen dataclasses, pure functions, no mutable state, and no external dependencies. Fully reproducible with standard library only.

5. **Comprehensive documentation**: The data_dictionary.md covers all variables, filters, and merge logic. The validation report flags genuine quality concerns (whale contamination, thin market, zero-volume days).

6. **Diagnostic queries**: Four diagnostic queries (#6941892, #6941902, #6941903, #6941906) provide independent verification of filter behavior and token scope.

---

**QA Analyst**: Model QA Specialist (Independent)
**QA Date**: 2026-04-02
**Pipeline Owner**: Data Engineer Agent
**Next Action**: Address Priority 1 findings before Analytics Reporter execution
