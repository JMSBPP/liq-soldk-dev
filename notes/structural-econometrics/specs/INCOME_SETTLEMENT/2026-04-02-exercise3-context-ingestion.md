# Exercise 3: Context Ingestion (Phase -1, Step A)

*Date: 2026-04-02*
*Status: PREPARED — waiting for Exercise 1 gate to pass before presenting to user*
*Framework: Reiss & Wolak (2007)*
*Depends on: Exercise 1 verdict (Analytics Reporter running)*

---

## Exercise 3 Question

**Does the realized variance of cCOP residual net flow respond to identifiable Colombian macro shocks?**

This is the test that directly validates the variance swap payoff. Exercise 1 tested the LEVEL response (β > 0 = macro content). Exercise 3 tests the VARIANCE response (does the spread of flow outcomes widen during stress?).

---

## Context Ingested

### 1. Macro Shock Calendar (COMPLETE)
Source: `identification/2026-04-02-exercise3-macro-shock-calendar.md`

**52 dated events** across 6 categories:

| Category | Count | Key Events |
|---|---|---|
| US_LABOR | 16 | Trump election, Sahm Rule NFP, Fed 50bp cut |
| INFLATION | 8 | Dec 2025 CPI <6% breakthrough, Feb 2026 re-acceleration |
| REGULATORY | 7 | MoneyGram USDC launch, Resolution 000240, MiniPay/El Dorado |
| COP_DEPRECIATION | 9 | Year-end 4,409/USD, BanRep rate cycle |
| OIL | 6 | OPEC+ July 2025 production spike, Feb 2026 surprise cut |
| POLITICAL | 6 | Jan 2025 tariff confrontation, Liberation Day, Dec 2025 emergency |

**Three anchor events** with documented on-chain behavioral responses:
1. Jan 25, 2025 tariff confrontation — Littio 100%+ growth in 48h
2. Sept 2025 MoneyGram USDC launch — infrastructure shock
3. Dec 24, 2025 Resolution 000240 — behavioral uncertainty

### 2. Exercise 1 Results (PENDING)

From the Analytics Reporter (running). What we need:
- The estimated residuals û_t from Exercise 1 primary specification
- The T4 heteroskedasticity test result (Breusch-Pagan on |ΔTRM|)
- If T4 passed → Exercise 3 has preliminary support
- If T4 failed → Exercise 3 is the decisive test

### 3. Methodological Precedent

**IMF WP/26/056** (Aldasoro et al.): Granular instrumental variable (GIV) strategy. Used shocks to stablecoin inflows in OTHER currencies as instruments. Key finding: 1% exogenous inflow increase → 40bps parity deviation.

**For Exercise 3**: The GIV approach suggests using shocks to cKES, PUSO, or other Mento stablecoin flows as instruments for cCOP flow variance. But these currencies were contaminated (campaigns, bots) — the instrument quality is questionable. Alternative: use the dated macro events themselves as natural experiments (event study approach).

### 4. What the Literature Says About Variance Estimation

**Realized variance** = sum of squared daily returns/flows over a window:
```
RV(t, t+h) = Σ_{s=t}^{t+h} (flow_s - mean_flow)²
```

**Event study on variance**: Compare RV in pre-event window [-30d, -1d] vs post-event window [+1d, +30d]. Test: RV_post > RV_pre (one-sided F-test on variance ratio).

**GARCH approach** (alternative): Model conditional variance as:
```
σ²_t = ω + α û²_{t-1} + β σ²_{t-1} + γ D_shock_t
```
Where D_shock is a dummy for macro event dates. γ > 0 means shock increases conditional variance. Requires more data than event study but produces a continuous variance model.

### 5. Data Available

| Variable | Source | Ready? |
|---|---|---|
| Daily cCOP residual flow | Dune #6941901 | YES |
| Exercise 1 residuals û_t | Analytics Reporter | PENDING |
| COP/USD TRM daily | trm_processed.csv | YES |
| Macro shock dates (52 events) | exercise3-macro-shock-calendar.md | YES |
| Colombian calendar controls | colombian_calendar.md | YES |
| Celo event controls | CELO_EVENT_CONTROL_VARIABLES.md | YES |

### 6. Candidate Identification Strategies (to present in Step B)

**Strategy A: Event Study**
- For each of the 52 macro shocks, compute RV in [-30d, -1d] and [+1d, +30d]
- Test: RV_post > RV_pre using variance ratio F-test
- Advantage: non-parametric, transparent, uses dated events
- Disadvantage: overlapping event windows (52 events in 18 months = average 1 event per 10 days), need to handle clustering
- Power: depends on magnitude of variance response relative to baseline variance

**Strategy B: GARCH with Shock Dummies**
- Estimate GARCH(1,1) on daily residuals from Exercise 1
- Add shock category dummies to the variance equation
- Test: γ_COP_DEPRECIATION > 0, γ_POLITICAL > 0, etc.
- Advantage: continuous model, handles overlapping events, produces a variance forecast
- Disadvantage: parametric (GARCH assumes specific error distribution), requires ~500+ obs for stable estimation

**Strategy C: Rolling Variance Comparison**
- Compute 30-day rolling RV of daily cCOP flow
- Regress rolling RV on contemporaneous macro indicators (|ΔTRM|, oil price vol, VIX)
- Test: does rolling RV respond to macro stress indicators?
- Advantage: simple, transparent, uses all data
- Disadvantage: rolling windows create serial correlation in the LHS, overlapping observations bias SE

**Strategy D: Quantile/Tail Approach**
- Instead of variance, test whether EXTREME flow days (>95th percentile) cluster around macro shocks
- Logit: P(extreme_day = 1) = f(macro_shock_dummies)
- Advantage: directly tests tail risk, which is what the variance swap exploits
- Disadvantage: few extreme days (5% of ~460 = ~23 obs), very low power

### 7. Key Decisions for User (Step B, after Exercise 1 gate)

These will be presented as AskUserQuestion when Exercise 1 passes:

1. **Which identification strategy?** Event study (A), GARCH (B), rolling variance (C), or quantile (D)?
2. **Which shock categories to test?** All 6? Or focus on the 3 anchors with documented responses?
3. **What is the variance measure?** Realized variance of raw flow, or variance of Exercise 1 residuals?
4. **Event window width?** [-30d, +30d] standard, or narrower [-5d, +5d] for clean events?
5. **How to handle overlapping events?** (52 events in 18 months)
6. **Unit of observation?** Daily rolling variance, or event-level (pre vs post)?

### 8. Connections to the Instrument

If Exercise 3 passes (variance responds to shocks):
- The variance swap payoff is justified
- The settlement variable is Var(cCOP flow) computed from Uniswap v3 pool observables
- The pricing question becomes: what is the fair "strike" variance?
- Exercise 1's β provides the mean response (for delta hedging)
- Exercise 3's γ provides the variance response (for vega pricing)
- The QA audit's T4 (heteroskedasticity) provides the bridge

If Exercise 3 fails (variance doesn't respond):
- The flow carries macro content (Exercise 1) but is predictably responsive
- A variance swap is wrong — the flow is too stable
- Alternative instrument: a simple forward/future on the flow level, not variance
- Or: the variance swap needs a different underlying (feeGrowthGlobal from the CFMM instead of raw flow)

---

## Ready to Present

When Exercise 1 Analytics Reporter returns:
- If T1 PASS → present this context + Question -1a to user
- If T1 FAIL → stop, this document is moot
