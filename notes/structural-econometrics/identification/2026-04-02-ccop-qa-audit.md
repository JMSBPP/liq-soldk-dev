# QA Audit: cCOP Structural Econometric Specification

*Auditor: Model QA Specialist (independent, not involved in specification development)*
*Date: 2026-04-02*
*Specification Under Review: INCOME_SETTLEMENT/2026-04-02-ccop-cop-usd-flow-response.md*
*Framework: Reiss & Wolak (2007), 19 questions*
*Documents Reviewed: 18 files across specification, identification trail, data pipeline, research context, exercise structure, and instrument definition*

---

## Overall Verdict: PASS WITH CONDITIONS

The specification is intellectually honest, well-documented, and follows the Reiss & Wolak framework with appropriate rigor for a reduced-form sanity check. The identification strategy is defensible, the data pipeline is transparent, and the research context is thorough. However, there are several material issues that must be addressed before estimation, and two conceptual disconnects between what this exercise tests and what the variance swap actually needs. None of the issues are fatal, but some require either explicit acknowledgment or additional robustness work.

---

## A. Identification Strategy

### A1: TRM Exogeneity -- PASS

**Reasoning**: The claim that BanRep TRM is exogenous to Celo is well-supported. The cCOP market is approximately 0.001% of Colombian interbank FX volume. No rational agent would attempt to move a $11.85B/year market via a $10-20M on-chain market. The spec correctly identifies the strongest attack (stress-event reverse causality where on-chain demand leads TRM by hours) and correctly argues this creates attenuation bias, making the estimate conservative.

**Strongest attacks on exogeneity**:

1. **Common driver confounding**: Both TRM changes and cCOP volume could respond simultaneously to the same unobserved news shock (e.g., a Petro policy announcement). The control set currently lacks a proxy for Colombian political/news sentiment. The Thursday dummy and weekend dummy do not capture event-driven confounding. DELTA-TRM captures part of this, but the concern is that on days with large Colombian news events, both TRM moves and cCOP volume spikes are driven by the news, not by TRM causing volume.

2. **Aggregation-level reverse causality**: While cCOP cannot move TRM, the broader stablecoin-to-COP market (including Littio's $200M/month, El Dorado P2P, Bitso, Binance Colombia) collectively could. If the specification captures a correlation that actually runs through these larger channels, beta does not identify the cCOP-specific response but rather the shared macro response of the entire Colombian crypto-to-COP ecosystem.

3. **Measurement timing mismatch as identification threat**: The spec states TRM is backward-looking by one day. On-chain activity is real-time. If agents react to the CURRENT peso situation (which TRM has not yet priced), then DELTA-TRM_t is a stale measure of today's FX shock. The lag term DELTA-TRM_{t-1} partially addresses this, but the concern is that DELTA-TRM_{t+1} (which the researcher cannot include without look-ahead bias) is the true causal driver. This means the test is structurally conservative, which the spec acknowledges. But it also means a non-significant beta does not necessarily mean no macro content -- it could mean the timing is wrong.

**Recommendation**: Add a Colombian VIX proxy or a binary "large TRM move" dummy to capture event-driven days. Consider including DELTA-TRM_{t+1} in a non-causal specification purely as a diagnostic for leading behavior (clearly labeled as descriptive, not identified).

### A2: Filtering Definition -- PASS WITH CONDITIONS

**Reasoning**: The five-filter definition (UBI + bots + campaigns + dust + hardfork) is conceptually sound and well-documented. Each filter has a clear rationale and its impact is quantified.

**Concerns**:

1. **The UBI filter is based on sender behavior, not address labels**: The rule ">80% of transactions on Thursdays AND >= 3 transactions" is a heuristic. It will catch most ImpactMarket UBI recipients but could also catch a real Colombian user who happens to convert mostly on Thursdays (e.g., someone paid weekly on Thursdays). The 80% threshold is aggressive -- a user with 4 transactions, 3 on Thursday and 1 on Monday, gets flagged. The spec does not discuss false-positive rates.

2. **The bot filter threshold of >1000 transactions AND <10 counterparties** is reasonable but could miss bots that operate across more counterparties or with fewer transactions. More critically, it does not filter by transaction pattern (e.g., regular interval, fixed-size transactions). A bot making 900 transactions to 5 counterparties would pass. This is likely a minor issue given the 26 addresses flagged.

3. **The hardfork window is correctly specified** (July 7-12, 2025). However, the Mento token migration (January 25, 2026) is mentioned as a structural break in CELO_EVENT_CONTROL_VARIABLES.md but is NOT excluded from the sample and has no dummy variable in the specification. The SQL query uses `token_symbol IN ('cCOP', 'COPm')` which aggregates both tokens, but the migration day itself may have anomalous volume from technical operations.

**Recommendation**: Add a migration window dummy (January 24-26, 2026) to the specification. Report the false-positive rate of the Thursday filter by checking how many flagged addresses have any income-sized ($200-2000) transactions.

### A3: Campaign Filter Removing 71% of Addresses -- NEEDS_REVISION

**Severity: Medium**

**Reasoning**: This is the most consequential filter in the pipeline. The campaign filter removes 3,563 of 4,990 addresses (71.4%) based on a single criterion: the address first appeared on a day when more than 50 new senders were active. This is a blunt instrument.

**Problems**:

1. **The threshold of 50 is arbitrary**. The campaign days range from 60 new senders (February 19, May 23) to 1,931 new senders (July 31). The February 19 event with 77 new senders could plausibly be organic growth rather than a campaign. The spec's own queries.md acknowledges the "Feb 19 and May 23 thresholds (77 and 60) are borderline."

2. **Survivorship bias**: The filter assumes ALL addresses onboarded on campaign days are campaign participants. But some fraction of those addresses may have continued organic activity well beyond the campaign. An address that first appeared on July 31, 2025 during the mass onboarding but subsequently transacted income-sized amounts weekly for 8 months is being excluded despite behavioral evidence of being a real user. The filter penalizes acquisition channel, not behavior.

3. **Selection bias in the residual**: By removing 71% of addresses, the residual population of 1,310 addresses may be systematically different from the true income-conversion population. Specifically, the residual is biased toward early adopters (pre-campaign) who are more likely to be crypto-native, developer-community members, or Celo insiders. The "representative household" of the residual may look nothing like the typical Colombian income converter.

4. **The sensitivity analysis S1/S2/S3 is specified but not yet executed**. The spec proposes testing different filter levels, which is the right approach. However, the severity of this finding warrants making S1 (no campaign filter) and a behavioral version (campaign addresses that survived > 30 days and had >= 3 income-sized transactions) mandatory, not optional.

**Recommendation**: (a) Replace the campaign filter with a behavior-based filter: flag addresses first appearing on campaign days BUT exempt those with 3+ income-sized transactions and activity spanning 30+ days post-onboarding. (b) Run the regression with and without the campaign filter. If beta is consistent, the issue is resolved. If beta changes sign or significance, the result is filter-dependent and cannot be trusted.

### A4: Population Calibration Exercise (56 Overlapping Addresses) -- NEEDS_REVISION

**Severity: Medium**

**Reasoning**: The calibration exercise found 56 addresses that use both cCOP/COPm and COPM tokens. The spec concludes "calibration passed" based on timezone match (UTC 12-13), size match on old cCOP ($1,008 vs $730 median), and the finding that distributions diverge for functional reasons (spending vs. conversion).

**Problems**:

1. **56 addresses out of 4,642 cCOP senders and 945 COPM senders is a 1.2%/5.9% overlap rate**. This is extremely thin for a calibration claim. The spec acknowledges the overlap is "non-zero" but then leaps to "ground-truth calibration points exist." The existence of 56 intermediary addresses does not validate that the broader populations are similar. These 56 addresses have an average of 1,300-1,600 transactions each -- they are power users, likely apps or payment processors, NOT representative of the typical income converter.

2. **The conclusion changed mid-exercise**: The original hypothesis was "cCOP residual approximates COPM" (alpha approximately equals 1). The data showed they are different (KS test would reject equality). The spec then pivoted to "cCOP residual IS the income signal directly -- no interpolation needed." This is a legitimate intellectual pivot, but it undermines the stated purpose of the calibration exercise. If no interpolation is needed, then the 56-address overlap test is irrelevant, and the spec should not claim it as "calibration passed."

3. **The real claim needs its own test**: If the claim is "after filtering, the cCOP residual captures income conversion directly," the test should be: do the 1,310 clean addresses show income-conversion behavioral signatures (income-sized transactions, quincena timing, Colombian timezone) at the POPULATION level? The spec has this data (size distribution, temporal patterns) but has not formally tested it for the residual population specifically.

**Recommendation**: (a) Drop the "calibration passed" language. Replace with "population overlap is minimal; cCOP and COPM serve different economic functions." (b) Add a formal behavioral test of the residual population: compute the fraction of residual volume that is income-sized ($200-2000), the quincena effect within the residual, and the temporal pattern (should peak UTC 13-15 for Colombia). (c) If the residual fails these behavioral tests, the "income conversion signal" claim is unsupported.

### A5: Equilibrium Concept Coherence -- PASS

**Reasoning**: "Price-taking relative to TRM + agnostic on-chain" is a defensible equilibrium concept for a reduced-form exercise. The spec correctly identifies that strategic on-chain interaction (aggregators, arbitrageurs) does not affect the reduced-form because it is absorbed into the error term. The caveat about stress-event leading indicator behavior is well-documented and the conservative bias direction is correctly argued.

**Minor concern**: The spec claims agents are "agnostic" about on-chain interaction, but the data shows aggregators (0x6619, 0x2ac5) and arbitrage bots (0x2021) account for a large fraction of volume. If these intermediaries react to DELTA-TRM differently than retail users (e.g., faster, larger, in opposite direction), the reduced-form beta is a volume-weighted average that may be dominated by intermediary behavior rather than income-conversion behavior. The robustness spec R6 (decompose by size bucket) addresses this -- it should be mandatory.

---

## B. Specification Quality

### B6: Functional Form -- PASS WITH CONDITIONS

**Reasoning**: Log-level with DELTA-TRM is a reasonable first choice. The log transformation handles the heavy right tail, and first-differencing TRM addresses the common trend (COP appreciated 12% over the sample, from 4,178 to 3,676).

**Concerns**:

1. **ln(1+V) is a poor approximation when V is large**. For V = $50,000, ln(1+V) = 10.82, while ln(V) = 10.82. The difference is negligible for large V. But for V near zero, ln(1+V) approximately equals V, which means zero-volume days contribute approximately zero to the regression rather than being excluded. This is fine but the interpretation of beta changes: it is no longer a pure elasticity.

2. **The robustness R1 (log-log with time trend) is important** because the primary spec does not include a time trend. Both ln(V) and TRM are trending (V upward due to growth, TRM downward due to appreciation). Differencing TRM removes the trend on the RHS, but the LHS still has an upward trend from growing adoption. Without a time trend or first-differencing the LHS, the regression may attribute the growth trend to any RHS variable that happens to trend similarly.

3. **An alternative functional form not considered**: First-difference both sides: DELTA-ln(V_t) = alpha + beta1 * DELTA-TRM_t + controls + u_t. This would remove any common trend and focus purely on day-to-day comovement. Consider adding this as R7.

**Recommendation**: Add a first-differenced specification (DELTA-ln(V) on DELTA-TRM) as robustness R7. Report the Durbin-Watson statistic for the primary specification to assess residual autocorrelation magnitude.

### B7: Control Sufficiency -- NEEDS_REVISION

**Severity: Medium**

**Reasoning**: The current control set is {quincena, Thursday, weekend}. These are calendar effects. The specification is missing several potentially important confounders.

**Missing controls**:

1. **Time trend or month fixed effects**: The on-chain market grew from 5 transfers/day (Oct 2024) to 500+/day (Mar 2026). This secular growth is not captured by any control. If TRM happened to decline (COP appreciation) while volume grew (adoption), the regression would find a negative beta -- not because depreciation reduces volume but because both series trend in opposite directions. A linear time trend (as in R1) or monthly dummies should be in the primary spec, not just robustness.

2. **Celo-wide activity control**: Total Celo DEX volume, total Mento broker volume, or cUSD transfer count would control for ecosystem-level shocks (e.g., a protocol upgrade that increases all Celo activity, not just cCOP). Without this, a Celo-wide event that happens to coincide with a TRM move would be attributed to beta.

3. **Lagged dependent variable**: The spec acknowledges volume is autocorrelated (AR(1) structure) and addresses this with HAC standard errors. But HAC only fixes the standard errors, not the omitted-variable bias. If ln(V_{t-1}) belongs in the model and is correlated with DELTA-TRM_t, the coefficient is biased. Adding ln(V_{t-1}) as a control directly addresses this and changes the interpretation to "the MARGINAL change in volume from an FX shock, controlling for the previous day's activity level."

4. **Migration dummy**: As noted in A2, the January 2026 token migration is a structural event not controlled for.

5. **MiniPay + El Dorado integration (November 19, 2025)**: Listed in CELO_EVENT_CONTROL_VARIABLES.md as a Colombian-specific event. This created a new fiat on/off-ramp and could have structurally shifted the volume process. At minimum, a dummy or a regime-break test is warranted.

**Recommendation**: Add to the primary specification: (a) linear time trend, (b) ln(V_{t-1}), and (c) a migration dummy. Add to robustness: month fixed effects and Celo-wide activity proxy. Discuss in the methodology why each was included or excluded.

### B8: Quincena Dummy Specification -- NEEDS_REVISION

**Severity: Low**

**Reasoning**: The quincena dummy is coded as 1 if DAY(date) = 15 OR date = LAST_DAY_OF_MONTH. This is correct for the legal definition (Colombian Labor Code Art. 134). However:

1. **Weekend/holiday shifting**: When the 15th falls on a Saturday or Sunday, employers typically pay on the preceding Friday. The dummy as coded fires on the calendar 15th regardless. This means the volume spike may appear on Friday the 13th or 14th, while the dummy fires on Saturday the 15th when the spike has already passed. This creates measurement error in the dummy that attenuates gamma_1 toward zero.

2. **Similarly for last day of month**: If the 31st is a Sunday, payroll typically hits on Friday the 29th. The dummy fires on the 31st.

3. **Prima de servicios bonus (June 30 and December 20)**: These are mentioned in the data dictionary as structural events but have NO separate dummy in the specification. December 20 and June 30 are mandated extra bonus payments (one month's salary split in two). These are much larger than regular quincena and should be separately identified. Including them in the quincena dummy dilutes the quincena effect (the few bonus days are dominated by regular quincena days in the estimate).

**Recommendation**: (a) Adjust the quincena dummy to fire on the Friday before if the 15th or last day falls on a weekend. (b) Add a separate prima_de_servicios dummy for June 30 and December 20 (and the business day before if these fall on weekends). (c) Consider a 3-day window version of the quincena dummy (day before, day of, day after) to capture timing uncertainty.

### B9: Specification Tests -- PASS WITH CONDITIONS

**Reasoning**: T1 (beta_1 + beta_2 > 0) and T2 (gamma_1 > 0) are reasonable sign restrictions that directly map to the economic hypotheses.

**Concerns**:

1. **T1 is a joint test but is implemented as a one-sided t-test on the sum**. The correct implementation requires computing the variance of (beta_1 + beta_2), which involves the covariance of the two estimates: Var(beta_1 + beta_2) = Var(beta_1) + Var(beta_2) + 2*Cov(beta_1, beta_2). Ensure the test uses the HAC-consistent variance-covariance matrix, not just the individual standard errors.

2. **There is no test for whether the model specification itself is adequate**. A Ramsey RESET test would detect functional form misspecification. An F-test comparing the primary spec against the spec with all robustness controls would test whether the omitted variables matter. Neither is proposed.

3. **Stronger tests exist**: (a) A Granger causality test (does lagged DELTA-TRM predict ln(V) controlling for lagged ln(V)?) would directly test the causal timing. (b) A placebo test using SHUFFLED dates of DELTA-TRM would test whether the result is spurious. (c) The R6 decomposition (beta for income-sized vs. small vs. whale) provides a much more powerful test: if beta is positive for income-sized and zero for whale-sized, the income-conversion mechanism is supported.

**Recommendation**: Add Ramsey RESET test for functional form. Add placebo test (permutation of DELTA-TRM across dates, compute distribution of placebo betas, check if real beta exceeds 95th percentile). Make R6 mandatory.

### B10: Sample Size (N approximately 499) -- PASS

**Reasoning**: With 6 parameters (constant + 5 regressors), the N/k ratio exceeds 80. This is adequate for OLS with HAC standard errors. The concern is not the total sample size but the effective sample size after accounting for autocorrelation and the thin early period.

**Minor concern**: If the recommendation to start from December 2024 is followed (as validation report suggests), N drops to approximately 460. If monthly fixed effects are added (17 dummies), N/k drops to approximately 19, which is still adequate but loses substantial degrees of freedom. Use quarterly fixed effects instead if monthly is too costly.

---

## C. Data Quality

### C11: Validation Report WARN Items -- NEEDS_REVISION

**Severity: Medium**

**Reasoning**: The validation report flags three WARN items. My assessment of each:

1. **Zero-volume days (early period)**: Using ln(1+V) is acceptable but the analyst should verify that zero-volume days are not systematically correlated with TRM movements. If TRM tends to be flat on weekends (forward-filled, DELTA-TRM = 0) and volume is also low on weekends, there is a mechanical correlation between low volume and zero DELTA-TRM that is not economic. The weekend dummy partially captures this, but zero-volume days should be investigated separately.

2. **Whale contamination (3 days with >90% whale volume)**: The log transformation dampens but does not eliminate the influence. A single day with $700K in whale volume (January 24, 2025) has ln(1+V) = 13.46 versus a typical day at 10-11. This is a 2-3 standard deviation outlier in the LHS variable. If this day coincides with a large TRM move, it will exert outsized leverage on beta. The spec proposes winsorization but does not mandate it.

3. **Thin early period (Oct-Nov 2024)**: The validation report recommends starting from December 2024. The summary statistics show launch day had 1 sender and $209 volume. The regression assumes a stationary data-generating process, which clearly does not hold during the launch phase. Including it adds noise and potentially biases results.

**Recommendation**: (a) Drop October-November 2024 from the estimation sample (start December 1, 2024). (b) Winsorize gross_volume_usd at the 99th percentile as a robustness check. (c) Add a whale dummy (1 if whale_volume > 90% of gross_volume) as a control in the primary spec. (d) Report Cook's distance for the top 5 highest-leverage observations.

### C12: TRM Timing Lag -- PASS

**Reasoning**: Including both DELTA-TRM_t and DELTA-TRM_{t-1} correctly captures the one-day backward-looking nature of TRM. The spec identifies that the attenuation bias from timing mismatch makes the test conservative. This is well-reasoned.

**Minor concern**: The spec claims DELTA-TRM is the relevant RHS variable, but TRM is published as COP per USD. A positive DELTA-TRM means COP depreciation. The sign prediction is beta > 0 (depreciation increases conversion volume). Verify that the sign convention is consistently applied in the data dictionary, the query, and the interpretation. The data dictionary correctly states "Positive DELTA-TRM = COP depreciation." This is consistent.

### C13: Forward-Filling TRM on Weekends -- NEEDS_REVISION

**Severity: Low**

**Reasoning**: Forward-filling creates approximately 150 days (29% of sample) where DELTA-TRM = 0 mechanically. On these days, the regression is estimating the intercept plus calendar effects, not the FX response. This is not wrong, but it means 29% of the sample provides no identifying variation for beta.

**Problem**: The is_forward_filled flag is in the processed TRM data but is NOT in the regression specification as a control or interaction. If weekend volume is systematically different AND the weekend dummy does not fully capture this, the zero-DELTA-TRM weekends create a mass point in the distribution of the RHS variable that may distort the fit.

**Alternative approach**: Exclude forward-filled days from the estimation of beta (restrict to business days only) as a robustness check. This reduces N to approximately 350 but ensures every observation has genuine DELTA-TRM variation.

**Recommendation**: (a) Run the primary regression on all days as specified. (b) As robustness, run on business days only (is_forward_filled = 0). (c) Report the difference in beta. If beta is stable, the forward-filling is innocuous.

### C14: Early Thin-Market Period (Oct-Nov 2024) -- NEEDS_REVISION

**Severity: Medium**

**Reasoning**: The validation report shows October 31, 2024 had 1 sender and $209 volume. November 4 had 2 senders and $1,994. November 25 had a $71,971 whale day with 5 senders. This is not a functioning market -- it is a deployment testing phase. Including it in the regression assumes these data points are drawn from the same DGP as March 2026 with 530 transfers and $13,216 volume. They are not.

The summary statistics show 19 missing days concentrated in this period (Nov 7, Nov 9-18, Nov 20-21). These are not randomly missing -- they are missing because there was no activity. Including them (with ln(1+0) = 0 volume) systematically pulls the intercept down and adds noise to every coefficient.

**Recommendation**: Start the sample from December 1, 2024. Document the excluded period as "launch phase" in the methodology. Report the N and R-squared for both the full and truncated samples.

---

## D. Economic Logic

### D15: Bidirectional Flow Argument -- PASS WITH CONDITIONS

**Reasoning**: The argument that BOTH income converters (USD to COP) and savings hedgers (COP to USD) increase activity during COP depreciation, therefore gross volume increases (beta > 0), is clever but has a subtle flaw.

**The flaw**: The LHS variable is ln(gross_volume_usd), which sums ALL transfer volume. But the spec uses transfers from the `stablecoins_multichain.transfers` table filtered by `"from" = ca.address`. This captures OUTGOING transfers from clean addresses. It does NOT separately measure directionality. A $500 transfer from Address A to Address B is counted as volume, but we do not know if this represents:
- A receiving USD remittance and converting to COP (income conversion)
- A moving COP savings into USD (savings hedging)
- An internal transfer between wallets (noise)

The bidirectional argument predicts gross volume increases for BOTH populations, which is consistent with beta > 0 on gross volume. The argument holds IF both populations actually transact more when COP depreciates. But what if income converters have INELASTIC conversion (they convert the same USD amount regardless of rate, because they need COP for rent) while savings hedgers are ELASTIC (they rush to convert during stress)? In that case, beta > 0 is driven entirely by the savings-hedger population, and the "income conversion" interpretation is unsupported.

The R6 robustness spec (decompose into small/income/whale) is the right test for this, but it tests by SIZE, not by DIRECTION. The spec cannot distinguish conversion direction from transfer size alone.

**Recommendation**: (a) Acknowledge that beta > 0 on gross volume is consistent with EITHER income-conversion response OR savings-hedging response OR both. (b) The R6 decomposition partially addresses this: if beta is positive for income-sized ($200-2000) AND positive for small ($1-50), the income-conversion channel is supported. (c) If feasible, use Mento broker swap direction data (cCOP to cUSD vs. cUSD to cCOP) to decompose by direction rather than size. Dune's mento_celo.broker_evt_swap table may have this.

### D16: Variance Swap Relevance -- NEEDS_REVISION

**Severity: High**

**Reasoning**: This is the most important conceptual issue in the entire specification. The exercise tests whether the LEVEL of daily volume responds to FX CHANGES. The variance swap pays the REALIZED VARIANCE of net flow. These are different economic objects.

**The disconnect**: beta > 0 means "volume goes up when COP depreciates." The variance swap needs "variance of volume goes up when macro shocks hit." These are related but not equivalent:

1. If volume increases SMOOTHLY with COP depreciation (steady beta), the variance of volume could actually DECREASE (less noise, more predictable). The variance swap would not pay out.

2. If volume increases ERRATICALLY during stress (some depreciation days see huge spikes, others do not), the variance increases. But this is not what beta captures -- beta is the AVERAGE response.

3. What the variance swap actually needs is: Var(epsilon_t | stress) > Var(epsilon_t | normal), where epsilon is the residual after removing the predictable component. This is a HETEROSKEDASTICITY test, not a mean-response test.

**What Exercise 1 actually tests**: "Does the on-chain flow carry macro content?" This is a necessary but not sufficient condition for the variance swap. If beta = 0, the flow is pure noise and the instrument is dead (correctly gated). If beta > 0, the flow responds to macro -- but you still need Exercise 3 (variance response to shocks) to justify the variance swap specifically.

**The spec acknowledges this**: The exercise structure document correctly frames Exercise 1 as a "sanity check" and reserves Exercise 3 for the variance response. However, the spec document itself (the formal Reiss & Wolak 19-question spec) is written ONLY for Exercise 1, and the gate condition is "if beta_1 + beta_2 > 0, the instrument has economic justification." This overstates what Exercise 1 proves.

**Recommendation**: (a) Revise the gate condition language. Exercise 1 should gate "the on-chain flow carries macro content." The instrument justification requires BOTH Exercise 1 (mean response) AND Exercise 3 (variance response). (b) Add a heteroskedasticity test to Exercise 1 as a preview: test whether the variance of residuals is larger on days with |DELTA-TRM| > median versus days with |DELTA-TRM| < median. This is a quick Breusch-Pagan or White test that can be computed alongside the regression. (c) If the residual variance shows no heteroskedasticity pattern with TRM, flag this as a risk for the variance swap even if beta > 0.

### D17: Market Size Sufficiency -- PASS WITH CONDITIONS

**Reasoning**: The cCOP market is small ($10-20M total, growing). The COPM market is larger ($200M/month) but mostly off-chain via Minteo's API, not on Celo DEXs. The question is whether the results are ECONOMICALLY significant, not just statistically significant.

**Assessment**: For the purpose of Exercise 1 (sanity check), economic significance is secondary. The exercise asks "does the signal carry macro content?" If it does, the signal can be AMPLIFIED as the market grows. The Celo cCOP/cUSD Uniswap v3 pool has 96,660 trades -- sufficient for a settlement oracle if properly designed.

**Concern**: The R5 robustness spec proposes using COPM transfers as a validation. However, COPM's on-chain volume on Celo is also small (104,775 transfers total, $22K DEX liquidity). The vast majority of COPM activity is off-chain through Minteo's API. R5 may not add much validation power because COPM on-chain data is equally thin.

**Recommendation**: Acknowledge that Exercise 1 is a proof-of-concept on a small market. The economic significance question should be deferred to Exercise 3 (variance response) and the instrument sizing specification.

### D18: Panoptic Deployment on Celo -- NEEDS_REVISION

**Severity: Medium (for the instrument, not for Exercise 1)**

**Reasoning**: The exercise structure document and INCOME_SETTLEMENT.md reference Panoptic V2/SFPM for the settlement layer. Panoptic is deployed on Ethereum mainnet and select L2s. Celo is an OP Stack L2 as of March 2025, but Panoptic deployment on Celo is not confirmed.

**For Exercise 1**: This is irrelevant. The regression does not depend on Panoptic.

**For the instrument**: This is a blocking issue. If Panoptic is not deployed on Celo, the settlement mechanism needs an alternative design. The spec references "borrow from existing pools" (Panoptic pattern) but this requires Panoptic's SFPM (Semi-Fungible Position Manager) contracts.

**Recommendation**: (a) Verify Panoptic deployment status on Celo L2. (b) If not deployed, either plan for deployment or design an alternative settlement mechanism. (c) Separate the econometric exercise (Exercise 1) from the instrument engineering -- Exercise 1 does not require Panoptic.

---

## E. Gaps and Omissions

### E19: Missing Specification Elements -- NEEDS_REVISION

**Severity: Medium (cumulative)**

1. **No time trend in primary spec**: As discussed in B7. The market grew 100x over the sample period. This is the single most important omission.

2. **No lagged dependent variable**: The spec acknowledges autocorrelation but only addresses it through HAC standard errors, not through the model itself.

3. **No stationarity test**: The spec does not propose an ADF or KPSS test on ln(V_t). If the volume series is I(1) (unit root), the regression in levels is spurious. The first-differenced spec (recommended as R7) addresses this.

4. **No out-of-sample test**: The entire sample is used for estimation. Given N approximately equals 460, a simple 80/20 train/holdout split would test whether beta estimated on 2024-2025 data predicts 2026 volume patterns.

5. **No pre-registration**: The robustness specs R1-R6 and sensitivity analyses S1-S3 are defined, but the decision rule for "what constitutes failure" is not stated. If 3 of 6 robustness specs give significant beta and 3 do not, is the test passed or failed? Define the decision rule before running the regressions.

6. **The prima de servicios bonus (June 30, December 20) is mentioned in the data dictionary and event control variables but has no dummy variable in the specification**. This is a known, legally-mandated income shock worth one month's salary. If it falls on or near a TRM movement day, it will be absorbed into beta rather than gamma.

### E20: Additional Robustness Checks

1. **Rolling-window beta stability**: Compute beta in rolling 90-day windows. If beta flips sign or loses significance in some windows, the relationship is unstable and the instrument is unreliable.

2. **Asymmetry test**: Does volume respond differently to COP depreciation (DELTA-TRM > 0) versus appreciation (DELTA-TRM < 0)? If the savings-hedging channel dominates, the response should be asymmetric (strong for depreciation, weak for appreciation). Test by splitting DELTA-TRM into positive and negative components.

3. **Whale exclusion robustness**: Re-run with income_volume_usd as LHS instead of gross_volume_usd. If beta survives, the whale contamination concern is moot.

4. **Cross-validation with COPM Polygon data**: If COPM on Polygon has richer data than COPM on Celo, it provides an independent behavioral reference. This would require expanding the data pipeline to include Polygon.

5. **Placebo currency test**: Run the same specification on cKES or PUSO (using their respective FX rates). If beta > 0 for those currencies too, the result may be a Celo ecosystem artifact rather than a Colombia-specific income signal. If beta approximately equals 0 for cKES/PUSO but positive for cCOP, the Colombia-specific interpretation is supported.

### E21: Alternative Explanations for beta > 0

1. **Common trend**: Both volume and TRM may be driven by Colombian macro conditions (e.g., oil prices affect COP and also affect economic activity that drives on-chain volume). Without a proper instrument, beta captures the total correlation, not the causal effect. The spec's reduced-form approach is explicitly agnostic about causality, but the INTERPRETATION jumps to "the flow responds to FX movements." It could be "both respond to the same underlying macro shock."

2. **Survivorship bias in the filter**: If the campaign filter removes addresses that are disproportionately noise-generating, the residual will mechanically show stronger correlations with ANY RHS variable, including TRM. Test by comparing R-squared of the regression with and without the campaign filter. If R-squared increases substantially after filtering, the filter may be creating the signal.

3. **Measurement artifacts from TRM forward-filling**: On Mondays, DELTA-TRM can be large (accumulating Friday-to-Monday FX movement). If volume is also systematically higher on Mondays (post-weekend catch-up), a mechanical correlation appears. Test by including a Monday dummy or excluding Mondays.

4. **Arbitrage-driven volume**: If arbitrageurs respond to TRM movements by rebalancing cCOP/cUSD pools, the volume response is mechanical (arbitrage) not economic (income conversion). The bot filter removes some of these, but aggregators (276 Uniswap takers) likely include active arbitrageurs. The R6 decomposition by size bucket is critical for this -- arbitrage tends to be in the whale bucket.

### E22: Literature Support -- PASS WITH CONDITIONS

**Reasoning**: The literature review is thorough and correctly identifies the most relevant papers.

1. **IMF WP/26/056 (Aldasoro et al.)** is correctly cited as the closest methodological precedent. Their GIV strategy identifies stablecoin-to-FX causality. The spec does NOT attempt to replicate this strategy (which would require multi-currency data) but acknowledges it as a template. This is honest and appropriate.

2. **BIS WP/1265 (Auer et al.)** gravity model supports the remittance-cost association with stablecoin flows. This is relevant but tangential -- the spec does not use a gravity model.

3. **Missing citation**: Angrist & Pischke (2009) is cited for the reduced-form justification, which is appropriate. However, the spec does not cite any paper on LOG-LEVEL regressions with trending data, which is the relevant econometric issue. Consider citing Hamilton (1994) or Wooldridge (2019) on spurious regression concerns with non-stationary data.

4. **The Shiller (1993) reference is foundational** for the broader project but is NOT directly relevant to Exercise 1. Exercise 1 tests whether volume responds to FX, not whether income markets should exist. The connection is made through the exercise structure document, which correctly sequences the exercises. However, the formal spec cites Shiller without explicitly connecting the citation to a specific claim in the specification.

---

## F. Ranked Action Items

### Priority 1: Must Fix Before Estimation

| # | Action | Finding Ref | Severity |
|---|--------|-------------|----------|
| F1 | Add linear time trend to primary specification | B7, E19 | High |
| F2 | Truncate sample to start December 1, 2024 | C14, C11 | High |
| F3 | Revise gate condition: Exercise 1 gates "macro content," NOT instrument justification | D16 | High |
| F4 | Add heteroskedasticity test (Breusch-Pagan on |DELTA-TRM| groups) to preview variance swap relevance | D16 | High |
| F5 | Define pre-registered decision rule for what constitutes pass/fail across robustness specs | E19 | High |

### Priority 2: Strongly Recommended Before Estimation

| # | Action | Finding Ref | Severity |
|---|--------|-------------|----------|
| F6 | Replace campaign filter with behavior-based filter (or mandate S1/S2/S3 as primary, not robustness) | A3 | Medium |
| F7 | Add lagged dependent variable ln(V_{t-1}) to primary spec | B7 | Medium |
| F8 | Add prima de servicios dummy (June 30, Dec 20) | B8, E19 | Medium |
| F9 | Adjust quincena dummy for weekend shifting | B8 | Low |
| F10 | Add migration dummy (Jan 24-26, 2026) | A2, B7 | Medium |
| F11 | Mandate R6 (size-bucket decomposition) as required, not optional | A5, D15 | Medium |
| F12 | Add whale dummy for days with >90% whale volume | C11 | Medium |

### Priority 3: Recommended for Robustness

| # | Action | Finding Ref | Severity |
|---|--------|-------------|----------|
| F13 | Run first-differenced spec DELTA-ln(V) on DELTA-TRM as R7 | B6 | Low |
| F14 | Run business-days-only regression (drop forward-filled TRM) | C13 | Low |
| F15 | Run rolling 90-day window beta stability test | E20 | Low |
| F16 | Run asymmetry test (positive vs. negative DELTA-TRM) | E20 | Low |
| F17 | Run placebo test (permuted DELTA-TRM) | B9, E20 | Low |
| F18 | Run placebo currency test on cKES or PUSO | E21 | Low |
| F19 | Add ADF/KPSS stationarity test on ln(V) | E19 | Low |
| F20 | Report Cook's distance for top 5 leverage observations | C11 | Low |
| F21 | Revise population calibration language (drop "calibration passed" claim) | A4 | Low |

### Priority 4: Deferred to Exercise 3

| # | Action | Finding Ref | Severity |
|---|--------|-------------|----------|
| F22 | Verify Panoptic deployment on Celo L2 | D18 | Medium (instrument) |
| F23 | Add Mento broker direction data for inflow/outflow decomposition | D15 | Medium (instrument) |
| F24 | Design Exercise 3 variance response test formally | D16 | High (instrument) |

---

## G. Summary of Strengths

Despite the conditions and revision items, this specification demonstrates several notable strengths:

1. **Intellectual honesty**: The spec explicitly states the bidirectional flow argument, acknowledges the leading-indicator timing issue, correctly identifies attenuation bias direction, and frames Exercise 1 as a sanity check rather than a definitive test. This is uncommon and commendable.

2. **Transparent data pipeline**: Every Dune query has a permanent ID and URL. The TRM source is documented with exact API endpoint. Filter definitions are explicit and reproducible. This meets the reproducibility standard.

3. **Research depth**: 15 background research documents covering the Colombian economy, Celo ecosystem, off-chain behavior, literature precedents, and competitive landscape. The specification is informed by actual data, not assumptions.

4. **Appropriate humility about market size**: The spec acknowledges cCOP is tiny relative to the interbank market and does not overstate the economic significance of the exercise.

5. **Well-structured robustness plan**: Six robustness specs (R1-R6) and three sensitivity analyses (S1-S3) cover functional form, frequency, outcome measure, periodicity, cross-token, and directional decomposition. The issue is not the plan but the absence of a pre-registered decision rule.

---

*QA Analyst: Model QA Specialist (Claude Opus 4.6)*
*QA Date: 2026-04-02*
*Next Scheduled Review: After estimation results (Exercise 1 completion)*
*Documents reviewed: 18 files, approximately 350KB total*
