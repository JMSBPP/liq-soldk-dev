# Structural Econometric Specification: cCOP Residual Flow Response to COP/USD Movements

*Date: 2026-04-02*
*Framework: Reiss & Wolak (2007), Handbook of Econometrics Vol 6A, Ch. 64*
*Token: cCOP/COPm (Mento, Celo) — filtered residual after UBI/bot/campaign/dust removal*
*Exercise: 1 (sanity check — does the signal carry macro content?)*

---

## 1. Research Question

**Economic question**: Does the daily cCOP residual conversion volume respond to COP/USD exchange rate movements?

**Parameter of interest**: β₁ = d(ln V_t) / d(ΔTRM_t) — the semi-elasticity of daily conversion volume to same-day COP/USD changes. Secondary: β₂ = lagged response (1-day).

**Why this matters**: This is the prerequisite gate for establishing that the on-chain flow carries **macro content**. If β₁ + β₂ ≈ 0, the flow does not respond to FX movements — it is disconnected from macro conditions and no derivative on it can serve as a macro hedge. If β₁ + β₂ > 0, the flow responds to FX — a necessary but NOT sufficient condition for the variance swap. The variance swap additionally requires that the VARIANCE of flow (not just the level) responds to macro stress — this is tested in Exercise 3. (QA H3: Exercise 1 gates "macro content," not "instrument justification.")

**Additionally**: γ₁ > 0 (quincena effect) validates that the flow is income-driven — people convert more on salary payment days (15th and last day of month), tethering the on-chain signal to real income timing.

**Unit of observation**: One observation per day for the cCOP/COPm residual, covering Oct 2024 - Apr 2026 (~540 days).

**Outcome variable**: 
- Primary: ln(gross_volume_usd) — log daily gross volume after filtering
- Robustness: ln(income_volume_usd) — log daily volume in $200-$2000 range only

---

## 2. Economic Model

### 2.1 Economic Environment
COP conversion market spanning on-chain (Celo: Mento broker, Uniswap v3, Carbon DeFi) and off-chain (Littio, Nequi/Wenia, MoneyGram USDC, El Dorado P2P, bank FX desks). On-chain is the observed system; off-chain is exogenous context. The on-chain market is infinitesimally small relative to the total Colombian FX market ($11.85B/year bank-intermediated remittances vs ~$10-20M on-chain).

**Off-chain finding** (OFFCHAIN_COP_BEHAVIOR.md): On-chain USDC demand is a LEADING indicator of TRM direction during stress events. TRM is backward-looking by one trading day. This justifies including ΔTRM_{t-1} in the specification.

### 2.2 Economic Actors
1. **Income converter** (remittance/freelancer): Receives USD, converts to COP for spending
2. **Savings hedger** (Littio-type): Converts COP→USD to escape depreciation
3. **Aggregator/router**: Routes flow across Mento/Uniswap/Carbon to minimize execution cost
4. **Arbitrageur/bot**: Keeps prices aligned across venues and vs TRM

### 2.3 Information Structure
| Actor | Observes | Private (unobservable to researcher) |
|---|---|---|
| Income converter | TRM, payday schedule | Own income amount, timing, personal needs |
| Savings hedger | TRM, inflation, political news, Littio yield | Savings balance, risk aversion, expectations |
| Aggregator | All on-chain venue states | Pending order flow |
| Arbitrageur | All on-chain + TRM | Execution latency, gas strategy |

### 2.4 Primitives
- **Technological**: CFMM trading function (Uniswap v3 concentrated liquidity), Mento broker reserve mechanism, Carbon DeFi limit orders
- **Institutional**: Colombian quincena salary cycle (Labor Code Art. 134: pay on 15th and last day of month). Prima de servicios bonus (Art. 306: June 30 and December 20)
- **Macroeconomic**: COP/USD exchange rate process (BanRep TRM), exogenous to Celo

### 2.5 Exogenous Variables
- BanRep TRM (COP/USD official rate) — determined by Colombian interbank market, exogenous to Celo. Justified by: cCOP market is ~0.001% of interbank volume. Agents are price-takers relative to TRM.

CPI, US unemployment, oil price reserved for Exercise 3 (variance response to macro shocks). Parsimony principle for Exercise 1.

### 2.6 Model Type
Reduced-form. β captures the total volume response to FX changes from all actors combined, without decomposing by actor type. Justified by Angrist & Pischke (2009, Ch. 1): reduced-form estimates with credible identification are preferable to structural models with debatable assumptions.

### 2.7 Equilibrium Concept
Price-taking relative to TRM (agents cannot move the interbank rate). Agnostic on within-chain interaction (aggregators, arbs may interact strategically on-chain, but this doesn't affect the reduced-form). 

**Caveat**: During stress events, on-chain demand may LEAD TRM by hours/days (off-chain research finding). Stress windows flagged but not excluded — the leading indicator effect creates a conservative bias (TRM hasn't moved yet → ΔTRM underestimates the shock → beta is attenuated).

---

## 3. Stochastic Model

### 3.1 Unobserved Heterogeneity
Private income timing and off-chain alternative rates. Income converters know when their salary arrives; savings hedgers know their COP balance and risk tolerance. Both observe El Dorado P2P rates and Littio yields (off-chain alternatives not in our dataset).

**Bias direction**: Selection — agents who choose on-chain may differ systematically from those who choose off-chain (e.g., more tech-savvy, different income bracket). The on-chain sample is not representative of ALL Colombian income converters, only those who selected into crypto rails.

### 3.2 Agent Uncertainty
Future COP/USD trajectory. Nobody knows if COP will depreciate further tomorrow. This uncertainty drives the timing of conversions — creating genuine stochastic variation in daily flow that is not explained by today's TRM level. This is the structural error term u_t.

### 3.3 Measurement Error
**LHS (filtering imprecision)**: The residual filter imperfectly separates income conversion from UBI/bot/campaign activity. Some real users may be excluded; some noise may remain. Effect: inflates standard errors, does NOT bias β.

**RHS (TRM timing lag)**: BanRep TRM reflects the previous trading day's weighted average. On-chain flow is real-time. 1-day mismatch creates measurement error in ΔTRM. Effect: ATTENUATION BIAS — β is biased toward zero. If β is significant despite this, the true effect is stronger.

Both sources are conservative — they make it HARDER to find significance.

### 3.4 Implied Error Structure
u_t = private income timing shock + future COP trajectory uncertainty + off-chain rate shock + filtering residual

Properties:
- E[u_t | ΔTRM_t, controls] ≈ 0 (by TRM exogeneity + controls)
- Var(u_t) likely heteroskedastic (higher during stress events, lower in thin market period)
- Cov(u_t, u_{t-1}) likely nonzero (volume is autocorrelated — high-activity day followed by high-activity day)
- Addressed by Newey-West HAC standard errors with automatic bandwidth

---

## 4. Estimation Strategy

### 4.1 Functional Forms
**Primary**: Log-level (change specification) — QA REVISED: added time trend (H1), lagged DV (M-B7), migration dummy (M-B7), prima dummy (M-B8)
```
ln(V_t) = α + β₁ ΔTRM_t + β₂ ΔTRM_{t-1} 
         + γ₁ D_quincena_t + γ₂ D_thursday_t + γ₃ D_weekend_t 
         + γ₄ D_prima_t + γ₅ D_migration_t
         + δ₁ t + δ₂ ln(V_{t-1})
         + u_t
```

Where (new controls per QA):
- δ₁·t = linear time trend (QA H1: market grew 100x over sample; without this, β captures trend correlation)
- δ₂·ln(V_{t-1}) = lagged dependent variable (QA M-B7: controls autocorrelation directly, not just via HAC SE)
- D_prima = 1 on June 30 and December 20 (prima de servicios bonus, ~1 month extra salary; QA M-B8)
- D_migration = 1 on January 24-26, 2026 (Mento token migration cCOP→COPm; QA M-B7)
- D_quincena = 1 if 15th or last day of month, **shifted to preceding Friday if falls on weekend** (QA M-B8)

**Robustness R1**: Log-log (level specification)
```
ln(V_t) = α + β ln(TRM_t) + γ₁ D_quincena_t + γ₂ D_thursday_t + γ₃ D_weekend_t + δ·t + u_t
```

**Robustness R7** (QA B6 recommendation): First-differenced both sides
```
Δln(V_t) = α + β₁ ΔTRM_t + β₂ ΔTRM_{t-1} + γ₁ D_quincena_t + γ₂ D_thursday_t + γ₃ D_weekend_t + u_t
```
(removes any common trend; focuses on day-to-day comovement)

### 4.2 Distributional Assumptions
Non-parametric. No distributional assumption on u_t. Estimated by OLS with Newey-West HAC standard errors (automatic bandwidth selection per Andrews 1991). Robust to heteroskedasticity and autocorrelation.

### 4.3 Implied Econometric Equation

PRIMARY (QA-revised):
```
ln(V_t) = α + β₁ ΔTRM_t + β₂ ΔTRM_{t-1} 
         + γ₁ D_quincena + γ₂ D_thursday + γ₃ D_weekend 
         + γ₄ D_prima + γ₅ D_migration
         + δ₁ t + δ₂ ln(V_{t-1})
         + u_t
```

- **LHS**: ln(1 + daily cCOP residual gross volume in USD)
- **Sample**: December 1, 2024 — April 1, 2026 (~460 daily obs; QA H2: excludes thin Oct-Nov launch period)
- **Parameters of interest**: β₁ (same-day FX response), β₂ (lagged FX response)
- **Controls**: quincena (salary cycle, weekend-adjusted), Thursday (governance/UBI residual), weekend (activity level), prima (bonus payments), migration (token transition), time trend (secular growth), lagged volume (autocorrelation)
- **Error**: u_t (private income timing + future COP uncertainty + filtering residual)
- **SE**: Newey-West HAC
- **N**: ~540 daily observations

### 4.4 Identification
β is identified by DAILY VARIATION in ΔTRM, after controlling for calendar effects.

**Source of variation**: Day-to-day changes in COP/USD driven by the Colombian interbank market (central bank interventions, trade balance, capital flows, political events). These are exogenous to the Celo cCOP market.

**Threat to identification**: During stress events, on-chain flow may lead TRM → reverse causality. Mitigated by: (1) stress events are rare (<5% of sample), (2) the leading indicator effect attenuates β (conservative), (3) robustness check R2 (weekly) aggregates past the intraday timing issue.

---

## 5. Specification Tests

| # | Implication | Type | Mathematical Statement | Test | Interpretation if FAILS |
|---|---|---|---|---|---|
| T1 | Flow responds to FX | Sign restriction | β₁ + β₂ > 0 | One-sided t-test on sum (using HAC var-cov matrix for Var(β₁+β₂)) | Signal has no macro content → instrument is dead |
| T2 | Flow is income-driven | Sign restriction | γ₁ > 0 | One-sided t-test on γ₁ | Flow is not tethered to salary timing → may be speculation |
| T3 | Cross-spec consistency | Informal overid | sign(β_primary) = sign(β_R1) = sign(β_R2) = sign(β_R7) | Visual comparison | Result depends on modeling choices → not robust |
| **T4** | **Variance responds to FX stress** | **Heteroskedasticity** | **Var(û_t \| \|ΔTRM\| > median) > Var(û_t \| \|ΔTRM\| < median)** | **Breusch-Pagan splitting on \|ΔTRM\|** | **Residual variance is constant → variance swap has no macro trigger → Exercise 3 may fail (QA H4)** |
| T5 | Functional form adequate | Misspecification | RESET test rejects | Ramsey RESET (squared/cubed fitted values) | Functional form is wrong → re-specify |
| **T6** | **Income decomposition** | **Sign pattern** | **β_income > 0 AND β_whale ≈ 0** | **R6 size decomposition (MANDATORY per QA)** | **β driven by whales not income → income-conversion interpretation unsupported** |

### QA H4: Why T4 Matters (Variance Swap Bridge)

The QA audit identified a critical conceptual gap: β > 0 tests whether the LEVEL of flow responds to FX. The variance swap pays REALIZED VARIANCE. These are different:
- β > 0 with stable residual variance → flow is predictably responsive → LOW variance → swap doesn't pay
- β > 0 with heteroskedastic residuals (higher variance during FX stress) → flow is erratically responsive → HIGH variance during stress → swap pays when needed

T4 bridges Exercise 1 (mean response) to Exercise 3 (variance response). If T4 passes, we have preliminary evidence that the variance swap mechanism works. If T4 fails, Exercise 3 must provide stronger evidence.

### QA H5: Pre-Registered Decision Rule

**Before running the regression, the following decision rule is locked:**

| Outcome | Interpretation | Action |
|---|---|---|
| T1 PASS + T2 PASS + T4 PASS | Strong: macro content + income mechanism + variance response | Proceed to Exercise 3 with confidence |
| T1 PASS + T2 PASS + T4 FAIL | Moderate: macro content + income, but constant variance | Proceed to Exercise 3 but flag variance swap risk |
| T1 PASS + T2 FAIL + T4 any | Weak: macro content but not income-driven | Investigate alternative populations (speculation?) |
| T1 FAIL | Dead: no macro content | Stop. Signal is noise. Revisit observable or currency. |
| T6 FAIL (β_whale drives result) | Misleading: whales not income | Result is not income-conversion → reinterpret |

**Robustness consistency rule**: β must be positive and significant in at least 4 of 7 specifications (primary + R1-R4 + R6 + R7) to be considered robust. If fewer than 4, the result is fragile.

---

## 6. Sensitivity Analysis

### 6.1 Sensitive Assumptions
**Filtering definition**: The cCOP residual depends on how strictly we filter. Tested via:
- S1: NO filter — raw cCOP/COPm transfers, dust only removed
- S2: CURRENT filter — UBI + bots + campaigns + dust + hardfork
- S3: TIGHT filter — current + remove top 22 power users

If β is consistent across S1-S3, the result is robust to filter choice.

### 6.2 Alternative Specifications

| Spec | Description | Purpose |
|---|---|---|
| R1 | Log-log level with time trend | Functional form robustness |
| R2 | Weekly aggregation (74 obs) with quincena dummy | Frequency robustness |
| R3 | Income-sized volume only ($200-$2000) | Outcome measure robustness |
| R4 | Quincena-aligned biweekly periods (~36 obs) | Natural periodicity alignment |
| R5 | COPM (Minteo) transfers instead of cCOP | Cross-token validation |
| **R6** | **Decompose into small ($1-50) vs income ($200-2000) vs whale ($2000+)** | **MANDATORY (QA): if β_income > 0 and β_whale ≈ 0, income mechanism supported** |
| R7 | First-differenced: Δln(V_t) on ΔTRM (QA B6) | Removes any common trend, pure day-to-day comovement |
| R8 | Business days only (exclude weekends where ΔTRM may be stale) (QA C13) | Tests if forward-filled TRM weekends distort β |

### QA M-A3: Campaign Filter Sensitivity (MANDATORY)

The campaign filter removes 71% of addresses. The following sensitivity variants are REQUIRED, not optional:

| Variant | Filter | Purpose |
|---|---|---|
| S1 | No campaign filter (only UBI + bots + dust + hardfork) | Tests if β survives with all onboarded users included |
| S2 | Current filter (>50 new senders/day) | Primary specification |
| S3 | Current + remove top 22 power users | Most aggressive |
| **S4** | **Behavioral rescue: campaign addresses that survived >30d AND had ≥3 income-sized ($200-2000) txns** | **QA M-A3: tests if real users were incorrectly excluded by the blunt campaign filter** |

---

## 7. Data Requirements

### On-chain (Dune — existing queries)
| Variable | Query ID | Status |
|---|---|---|
| cCOP residual daily volume | #6940887 (weekly; need daily version) | Needs daily re-query |
| cCOP size distribution | #6940855 | Complete |
| cCOP top senders/receivers | #6940020, #6940021 | Complete |
| COPM transfers | stablecoins_multichain.transfers | Needs query for R5 |

### Off-chain
| Variable | Source | Status |
|---|---|---|
| BanRep TRM daily | datos.gov.co Socrata API (no auth) | Access confirmed (BANREP_TRM_ACCESS.md) |
| Colombian calendar (quincena, holidays) | Manual construction | Needed |

### Control variable documentation
| Variable | Source |
|---|---|
| CELO_EVENT_CONTROL_VARIABLES.md | Hardfork, UBI, governance, migration dates |
| Colombian quincena | 15th + last day of month |
| Prima de servicios | June 30, December 20 |

---

## 8. References

- Reiss, P.C. & Wolak, F.A. (2007). "Structural Econometric Modeling: Rationales and Examples from Industrial Organization." Handbook of Econometrics Vol 6A, Ch. 64.
- Angrist, J.D. & Pischke, J.S. (2009). *Mostly Harmless Econometrics*. Princeton University Press. Ch. 1, 3, 4, 5.
- Aldasoro, I., Beltran, P. & Grinberg, F. (2026). "Stablecoin Inflows and Spillovers to FX Markets." IMF Working Paper WP/26/056. [Granular IV strategy for stablecoin→FX identification]
- Auer, R., Lewrick, U. & Paulick, J. (2025). "DeFiying Gravity." BIS Working Paper 1265. [Gravity model: stablecoin flows ~ remittance corridor costs]
- Reuter, K. (2025). "How to Estimate International Stablecoin Flows." IMF Working Paper WP/25/141. [AI geographic attribution methodology]
- Andrews, D.W.K. (1991). "Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation." Econometrica 59(3): 817-858. [Newey-West bandwidth selection]
- Shiller, R.J. (1993). *Macro Markets: Creating Institutions for Managing Society's Largest Economic Risks*. Oxford University Press. Ch. 3-6.
- Colombian Labor Code Art. 134 (quincena), Art. 306 (prima de servicios).

---

## 9. Permanent Dune Query Registry

See: `identification/2026-04-02-ccop-identification-progress.md` for complete list of 32 queries.
