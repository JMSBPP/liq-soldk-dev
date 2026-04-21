# REMITTANCE_VOLATILITY_SWAP -- Context Map & Research Plan

*Date: 2026-04-02*
*Status: Research mapping (no implementation decisions made)*

---

## 1. Context Map: How the Files Connect

### Dependency Graph of Ideas

```
FOUNDATIONAL THEORY (Shiller)
    |
    |-- MACRO_RISKS.md
    |       "What macro risks exist for underserved countries?"
    |       Identifies: LocalInflation, InterestRateShock, TermsOfTrade,
    |                   CapitalFlight, RemittanceCorridorRisk
    |       Psychology of framing risk as insurance
    |       FinancialContract = Claim + Settlement + BasisRisk
    |
    |-- MACRO_RISKS_CHECKPOINT.md
    |       References to Shiller (1993), macroDerivatives001/002 PDFs
    |       Anchors the literature backbone
    |
    |-- MACRO_DERIVATIVES.md
    |       CDS analogy: systematic vs. idiosyncratic credit risk
    |       MacroDefaultSwap: payoff on Agg(M) = aggregate macro observables
    |       Decomposition: d risk(lender) = beta1*Agg(M) + beta2*S
    |
    v
SETTLEMENT THEORY
    |
    |-- INCOME_SETTLEMENT.md
    |       Core thesis: income settlement > price settlement
    |       GDP ~ 3% hedgeable (corporate dividends) + 97% non-hedgeable
    |       Defines instrument span: IncomeFloor, IncomeSwap, IncomeCap,
    |           RelativeIncome, IncomeSwaption, IncomePerpetual,
    |           CrossCountrySpread
    |       Maps Shiller constructs to CFMM: LP = long income, trader = short
    |       LP_Position = Income_Component (fees) + Price_Component (IL)
    |
    |-- PRICE_SETTLEMENT.md
    |       When to use price settlement: illiquid cash markets
    |       Perpetuals as settlement mechanism
    |
    |-- SIGNAL_TO_INDEX.md
    |       Three-phase pipeline:
    |       Phase 1: Signal Processing (Shannon/Wiener/Kalman)
    |       Phase 2: Index Construction (Laspeyres/Paasche/Fisher)
    |       Phase 3: Settlement (derivatives pricing / Shiller)
    |
    v
ARCHITECTURE (refs/macro-risk/ARCHITECTURE.md)
    |
    |-- Three-layer system:
    |       Layer 1: Algebra pairwise pools (read observables)
    |       Layer 2: Balancer V3 virtual simplex (joint distribution)
    |       Layer 3: Modular Index Engine (user-defined indexes + settlement)
    |
    |-- Defines the Remittance Health Index (RHI) as a Layer 3 example
    |-- Universal Measurement Basis: DAI/USDC/AMPL/ETH/wstETH + EM slots
    |-- Zero-bootstrapped liquidity principle (Panoptic/SFPM pattern)
    |
    v
EMPIRICAL WORK (two completed/in-progress specs)
    |
    |-- SIGMOID_VOLATILITY_SWAP/2026-04-01-usdc-dai-volume-fee-elasticity.md
    |       Full Reiss-Wolak spec for Algebra USDC/DAI pool
    |       Estimates volume-fee elasticity across sigmoid regimes
    |       Foundation: determines whether LP income is long or short vol
    |       Status: Spec complete, estimation pending
    |       METHODOLOGICAL TEMPLATE for all subsequent econometric work
    |
    |-- INCOME_SETTLEMENT/2026-04-02-net-trading-volume-remittance-income.md
    |       Phase -1 brainstorm for the REMITTANCE question
    |       Maps the three-arrow identification chain:
    |           net_flow(USDC->cNGN) --> remittance_inflow --> household_income
    |       Candidate country table with liquidity assessment
    |       Contamination problem: remittance vs. speculation vs. arb vs. yield
    |       Status: Phase -1, no identification decisions made yet
    |       THIS IS THE DIRECT PRE-REQUISITE FOR THE REMITTANCE VOL SWAP
    |
    v
STABLECOIN FLOWS (REMITTANCE_VOLATILITY_SWAP/STABLECOIN_FLOWS.md)
    |
    |-- IMF research on international stablecoin flows
    |-- Key empirical findings for LATAM:
    |       Parity deviation +40 bps per +1% inflow
    |       FX depreciation co-moves with inflows
    |       CIP basis widens with inflows
    |-- Instrumental variable: idiosyncratic shocks to stablecoin net inflows
    |       in OTHER currencies as IV for a given country's flows
    |-- Banking crisis (March 2023) as natural experiment
    |
    v
THE INSTRUMENT: REMITTANCE_VOLATILITY_SWAP.md
    |
    |-- Payoff proportional to Var(Net USDT -> FX)
    |-- Expected longs: local fintechs, payment apps, LPs
    |-- Expected shorts: (contingent on PRE_REQ being established)
    |-- Exercises: migration shock, local recession, capital controls, inflation
    |
    v
DATA FEASIBILITY
    |
    |-- mento_research.md: 15 Mento stablecoins, $18.5B volume 2025
    |       African pools extremely thin ($200-$12K TVL)
    |       BRLA/BRZ on Polygon = best EM liquidity
    |       Primary liquidity through Mento exchange, not Uniswap
    |
    |-- stabull_deep_dive.md: Oracle-anchored AMM, 16 stablecoins
    |       $300K TVL, not compatible with Panoptic-style options (FATAL)
    |       But relevant for FX rate data and swap volume observation
    |
    v
SUPPORTING CONTEXT
    |
    |-- PENSION_FUNDS.md: Institutional demand for short-vol strategies
    |       PutWrite/BuyWrite overlay on Panoptic
    |       Bridges to: who are the natural SHORTS of this variance swap?
    |
    |-- ECONOMETRICS_NOTES.md: Heckman selection bias, diff-in-diff references
    |       Methodological toolbox for identification
```

### Key Feedback Loops

1. The SIGMOID_VOLATILITY_SWAP econometric spec is the **methodological blueprint**. Every subsequent spec (including the remittance pre-req) follows Reiss-Wolak (2007) pipeline with interactive human decisions.

2. The INCOME_SETTLEMENT framework defines the instrument taxonomy. The REMITTANCE_VOLATILITY_SWAP is a specific instantiation -- it is a **variance swap on a flow signal**, settled against income implications.

3. The ARCHITECTURE three-layer stack determines WHERE each piece fits:
   - The observable (Net USDT -> FX) is a Layer 1 read from pairwise pools
   - The index construction (Var of that flow) is a Layer 3 product
   - Settlement goes through Panoptic/Voltaire

4. The STABLECOIN_FLOWS IMF research provides the **external validation** that stablecoin flows affect FX markets. The IMF IV strategy (cross-currency flow shocks) is directly applicable to identification.

---

## 2. The Instrument: Precisely Described

### What It Is

A **variance swap on net remittance flows**, where the underlying observable is the net directional volume of USD-equivalent stablecoins being swapped into a local-currency stablecoin on-chain.

**Payoff**: proportional to Var(Net USDT -> FX) over a settlement period

Where "Net USDT -> FX" means: total volume of (USDC/USDT -> cNGN/cKES/etc.) minus total volume of (cNGN/cKES/etc. -> USDC/USDT), capturing net purchasing power transfer into the local economy.

### Why Variance (Not Level)

The instrument is deliberately on the **variance** of the flow, not the level. This is because:
- The LEVEL of remittance flows is approximately stable (regular monthly patterns)
- The VARIANCE spikes during crises (migration shocks, local recessions, capital controls)
- Hedgers care about unpredictability, not volume per se
- A payment app can handle high but predictable volume; it cannot handle volatile, unpredictable surges and collapses

### Expected Longs (from the spec)

1. **Local Fintechs / Lenders**: Lend to users whose income depends on remittances. When Var(Net USDT -> FX) rises, default risk rises because borrowers' income becomes unpredictable. They are long the swap to hedge credit exposure. The relation is explicit: UP(Var) => UP(default risk).

2. **Payment Apps**: Operate off-ramps into local currency and handle USD inflows. Their cost is operational stress when flows spike unpredictably -- staffing, liquidity management, compliance capacity. They hedge against flow volatility, not flow direction.

3. **LPs in the corridor pools**: Their LVR exposure (d LVR / d volatility of volume > 0) means they lose more to adverse selection when volume is volatile. The variance swap hedges the non-fee component of LP risk.

### Expected Shorts

The spec notes that the identity of shorts is **contingent on PRE_REQ** being established. The reasoning is:

- If Var(Net USDT -> FX) is proven to predict household income instability, then the payoff has real economic value during crises
- Natural shorts would be entities that BENEFIT from remittance volatility or are INDIFFERENT to it:
  - Speculators / vol sellers (analogous to pension funds selling puts -- collect variance risk premium)
  - Corridor arbitrageurs who profit MORE during high-volatility periods (arb profits scale with sigma-squared per LVR)
  - Potentially: diaspora remittance platforms that earn per-transaction fees and benefit from volume spikes regardless of direction
  - Re-insurers or macro hedge funds taking the other side as portfolio diversification

This is left deliberately open -- it is an economic decision requiring human judgment.

### The Settlement Question

The variance is computed from on-chain observables (swap event data from pools). This follows the income settlement > price settlement thesis from INCOME_SETTLEMENT.md:
- The flow data accrues over time (not flash-loanable)
- It reads protocol state directly (no external oracle needed for the flow itself)
- It IS the fundamental (net purchasing power transfer), not a proxy

However, there is a critical gap: the on-chain observable measures swap volume, which is a PROXY for actual remittance flow. The basis risk (distance between the claim and the settlement observable) depends entirely on how contaminated the flow data is with non-remittance activity.

---

## 3. The Pre-Requisite Chain

### What Must Be Established

The spec identifies one critical pre-requisite before the instrument can be economically justified:

```
PRE_REQ: (Net USDT -> FX) ---(predicts/explains?)--> (d household income from cross-border transfers)
```

This decomposes into a chain of three identification problems (from the econometric spec in `INCOME_SETTLEMENT/2026-04-02-net-trading-volume-remittance-income.md`):

### Arrow 1: net_flow(USDC -> cNGN) --> remittance_inflow(Nigeria)

**What must be shown**: That the net directional flow of stablecoins into a local-currency pool is a meaningful signal of actual remittance activity, not dominated by speculation, arbitrage, or yield-seeking.

**Order of operations**:
1. Query on-chain swap data for the relevant corridor pools
2. Analyze transaction size distribution (remittances are typically $200-$2000)
3. Analyze frequency patterns (remittances are monthly/payday-aligned)
4. Analyze directional asymmetry (remittances should show persistent net inflow to local currency)
5. Decide on contamination strategy: filter, decompose, or accept noise and bound attenuation bias

**Key human decision needed**: Which contamination strategy to use. This is an identification decision that cannot be made autonomously.

### Arrow 2: remittance_inflow --> household_income_from_transfers

**What must be shown**: That the on-chain observable (send-side swap) maps temporally and quantitatively to actual household receipt of income.

**Issues**:
- We observe the SEND side (on-chain swap), not the RECEIVE side (cash-out)
- Timing lag: does the swap precede, coincide with, or follow the actual household receipt?
- Channel coverage: what fraction of actual remittances flow through on-chain stablecoin rails vs. Western Union, M-Pesa, bank transfers?

**Validation data needed**: World Bank quarterly remittance data, CBN BOP data, mobile money volumes (for cross-validation, not as the primary signal)

### Arrow 3: household_income_from_transfers --> total_household_income_variation

**What must be shown**: That for the relevant population (remittance-receiving households), variation in remittance income is a dominant driver of total income variation.

**This is the easiest arrow**: Development economics literature establishes that remittances can be 30-60% of household income for receiving households. For this subpopulation, remittance volatility plausibly dominates total income volatility. The relevant literature exists (World Bank, Ratha et al.).

### Sequencing

The arrows must be established in order 3 -> 2 -> 1 (from easiest to hardest):

1. **First** (literature review): Establish Arrow 3 from existing development economics research. This is a desk exercise with no data requirements.

2. **Second** (data feasibility): Test whether Arrow 1 is even queryable. How many swaps per day? What is the size distribution? Is there directional asymmetry? This requires Dune queries on the relevant pools.

3. **Third** (identification): If Arrow 1 data exists, design the identification strategy for linking on-chain flow to actual remittance income. This is the hard econometric problem and requires the full Reiss-Wolak treatment with human decisions at every step.

4. **Fourth** (estimation): Only after identification is specified, estimate the relationship and run specification tests.

### What "Predicts/Explains" Means

The spec itself notes uncertainty about whether the relationship is "predicts" or "explains." This matters:

- **Predicts**: net_flow(t) -> remittance_income(t+1). Granger causality. Useful for forecasting. Weaker claim.
- **Explains**: net_flow(t) IS (a component of) remittance_income(t). Contemporaneous. Useful for settlement. Stronger claim.

For the VARIANCE SWAP, the relevant claim is probably contemporaneous: Var(net_flow) co-moves with Var(household_income). The hedger does not need to forecast; they need the payoff to correlate with their realized risk.

---

## 4. Data Feasibility

### Corridor-by-Corridor Assessment

Based on the Mento research and Stabull deep dive, here is an honest assessment of where on-chain data exists:

#### Tier 1: Feasible Now (enough data to attempt analysis)

**Brazil (BRLA/BRZ on Polygon Uniswap)**
- Best on-chain EM stablecoin liquidity globally
- ~$906M volume Jan-Jul 2025, 660% YoY growth
- Active Uniswap pools on Polygon
- BUT: remittance dependency is only ~0.3% of GDP (low signal)
- Use case: methodological proof-of-concept, not the strongest economic case

**Mexico (MXNe on Base Aerodrome/Uniswap)**
- 637.7M pesos transfer value in July 2025 alone
- Growing DEX activity on Base
- Remittance dependency ~4.2% of GDP (meaningful)
- Better remittance-to-liquidity ratio than Brazil

#### Tier 2: Possibly Feasible (data exists but thin)

**South Africa (ZARP on Base Uniswap/Stabull)**
- Institutional backing (Old Mutual)
- Dual-venue liquidity (Uniswap + Stabull)
- BUT: remittance dependency only ~0.3% of GDP
- More relevant for capital flight / FX depreciation instruments than remittance

**Kenya (cKES on Celo Uniswap V3)**
- ~$4.8K TVL in Uniswap pool, but cKES/USDT pool shows ~$35K TVL / ~$124K daily volume (from ARCHITECTURE.md)
- Remittance dependency ~3.4% of GDP
- M-Pesa dominates remittance receipt -- question is what fraction goes through stablecoin rails
- Primary liquidity through Mento exchange (not Uniswap) -- need to verify Dune queryability of Mento contract

**West Africa / eXOF (on Celo Uniswap V3)**
- ~$12K TVL
- eXOF covers WAEMU zone (8 countries)
- Remittance flows exist but fragmented across countries

#### Tier 3: Not Feasible Now (insufficient on-chain data)

**Nigeria (cNGN)**
- Highest remittance dependency among large African economies (~4.5%)
- THE most economically compelling corridor for this instrument
- But: "very thin" on-chain liquidity in Uniswap pools
- Primary liquidity through Mento exchange contract
- Critical unknown: is Mento exchange contract swap data queryable on Dune? If not, need direct Celo RPC indexing

**Philippines (PUSO)**
- Highest remittance % GDP (~10%) in the candidate set
- "Minimal DEX" -- PUSO exists on Mento exchange but no meaningful Uniswap pool
- PHPC on Ronin/Katana is a separate token/chain entirely

**Colombia (cCOP)**
- cCOP/USDT ~$15K TVL, ~$7K daily volume (from ARCHITECTURE.md)
- New (2025), no established pool history
- Remittance dependency ~2.8% of GDP

**El Salvador**: ~24% remittance/GDP but no stablecoin exists. Highest economic need, zero on-chain infrastructure.

**Ghana (cGHS)**: Minimal Mento exchange presence, no meaningful DEX pool.

### The Fundamental Data Tension

The countries with the STRONGEST economic case for this instrument (Nigeria, Philippines, El Salvador) have the WEAKEST on-chain data. The countries with the best data (Brazil, South Africa) have the weakest economic case (low remittance dependency).

Mexico may be the best compromise: meaningful remittance dependency (4.2% GDP) AND growing on-chain stablecoin activity (MXNe).

Kenya is interesting if the Mento exchange data proves queryable, because M-Pesa integration could eventually bridge the stablecoin-to-household gap.

### Stabull Relevance

Stabull is NOT a viable venue for building the variance swap itself (Panoptic-style options are FATAL incompatible due to lack of concentrated liquidity). However, Stabull pools (BRZ/USDC, COPM/USDC, MXNe/USDC, PHPC/USDC, ZARP/USDC) are additional sources of **swap event data** for measuring net directional flows. Their oracle-anchored pricing means the FX rate data is cleaner (less noise from AMM mechanics), though the endogenous price discovery information is lost.

---

## 5. Research Plan: Sequenced Exercises

### Exercise 0: Literature Foundation (1-2 weeks, desk work only)

**Purpose**: Establish Arrow 3 (remittance income -> household income variation) from existing literature and identify the best IV strategy for Arrow 1.

**Tasks**:
- [ ] Literature search: remittance income as fraction of household income, by country (World Bank, Ratha et al., development economics journals)
- [ ] Literature search: stablecoin flows as remittance proxy (IMF working papers already referenced in STABLECOIN_FLOWS.md)
- [ ] Literature search: variance of remittance flows and household welfare volatility
- [ ] Document the IMF IV strategy: "idiosyncratic shocks to stablecoin net inflows in OTHER currencies" as instrument. Assess applicability to the variance (not level) case.

**Data needed**: None (literature only)
**Identification strategy**: N/A (establishing priors)
**Feasibility**: Fully feasible now

### Exercise 1: Data Feasibility Probe (1 week, Dune queries)

**Purpose**: Determine which corridors have enough on-chain swap data to attempt econometric analysis.

**Tasks**:
- [ ] Query Dune for swap events on cNGN/USDC, cKES/USDC, eXOF/cUSD pools (Celo Uniswap V3)
- [ ] Query Dune for swap events on BRLA/USDC, BRZ/USDC (Polygon Uniswap)
- [ ] Query Dune for swap events on MXNe/USDC (Base Aerodrome/Uniswap)
- [ ] For each: count swaps/day, compute size distribution, test directional asymmetry
- [ ] Determine if Mento exchange contract swap data is queryable on Dune (Celo)
- [ ] All Dune queries must be permanent (non-temp) with verifiable IDs/URLs

**Data needed**: On-chain swap event data
**Identification strategy**: Descriptive statistics only
**Feasibility**: Feasible now, budget ~15-40 Dune credits per query

### Exercise 2: Migration Shock -> Var(Net USDT -> FX)

**Purpose**: Test whether exogenous migration shocks (policy changes, visa restrictions, deportation events) predict spikes in the variance of net stablecoin flows in affected corridors.

**Data needed**:
- On-chain: net directional flow time series from Exercise 1 (daily or weekly)
- Off-chain: migration policy event dates (visa changes, deportation orders, border closures) -- these are exogenous shocks to remittance-sending populations

**Identification strategy**:
- Event study / difference-in-differences
- Treatment: corridors affected by migration shock
- Control: corridors NOT affected (e.g., a US policy change affects US-Nigeria corridor but not UK-Nigeria corridor)
- If on-chain data has insufficient history, use World Bank quarterly remittance data as the dependent variable and match to known migration events

**What's feasible now**: Only if Exercise 1 reveals sufficient swap data history (ideally 12+ months daily observations). If data starts mid-2025 for a given corridor, the window may be too short for event studies.

**What's feasible later**: As on-chain stablecoin adoption grows, more events will fall within the data window. This exercise improves with time.

### Exercise 3: Local Recession -> Var(Net USDT -> FX)

**Purpose**: Test whether recessions in the HOST country (where migrants work) predict variance spikes in corridor flows.

**Data needed**:
- On-chain: same as Exercise 2
- Off-chain: host-country unemployment data (monthly), GDP growth (quarterly), sector-specific employment (e.g., US construction employment for corridors where migrants concentrate in construction)

**Identification strategy**:
- The challenge is that host-country recession affects ALL corridors from that host, so cross-corridor variation must come from differential migrant concentration by sector/region
- Potential IV: sector-specific employment shocks in the host country, interacted with the sectoral composition of the diaspora for each corridor
- This is a harder identification problem than Exercise 2

**What's feasible now**: Reduced-form correlations between host-country macro indicators and on-chain flow variance. Proper identification requires more data and careful IV construction.

**What's feasible later**: Full structural estimation once corridor-level data accumulates.

### Exercise 4: Capital Controls / Corruption

**Purpose**: Test whether capital control announcements or corruption events in the RECEIVING country predict variance in corridor flows.

**Data needed**:
- On-chain: same as Exercise 2
- Off-chain: capital control policy events (CBN announcements, FX restriction changes, Naira flotation events), corruption indices or events (anti-corruption enforcement changes)
- The parallel market premium (on-chain vs. official rate spread from MACRO_RISKS.md) is a key observable here

**Identification strategy**:
- Capital control events are relatively exogenous to individual corridor flows (they are government policy choices)
- Event study design: before/after capital control announcement
- The parallel market premium (cNGN/USDC on-chain rate vs. CBN official rate via Chainlink) is both an outcome variable and a potential predictor of flow variance
- Natural experiment potential: Nigeria's Naira flotation events in 2023-2024 provide testable episodes

**What's feasible now**: If Nigerian on-chain data exists (from Exercise 1), the Naira flotation events are well-documented and can be tested. This may be the MOST immediately testable exercise because the policy events are large, well-dated, and Nigeria-specific.

**What's feasible later**: Systematic analysis across multiple countries with different capital control regimes.

### Exercise 5: Inflation Spikes

**Purpose**: Test whether local inflation spikes predict variance in corridor flows (through demand for USD/USDT as store of value).

**Data needed**:
- On-chain: same as Exercise 2, plus AMPL/local-stable spreads (from ARCHITECTURE.md, AMPL = CPI-targeting token = real purchasing power)
- Off-chain: local CPI data (monthly), official and parallel FX rates

**Identification strategy**:
- Inflation spikes in the receiving country may increase BOTH the level and variance of flows (households demand more USD + uncertainty increases)
- The AMPL numeraire from the universal measurement basis (Layer 2) can isolate real vs. nominal effects
- Challenge: inflation is endogenous to many other macro variables. Need exclusion restriction.
- Potential IV: commodity price shocks for commodity-dependent countries (oil price for Nigeria, copper for Zambia) as exogenous inflation drivers

**What's feasible now**: Reduced-form correlation with CPI data. The AMPL/local-stable measurement apparatus from the architecture is not yet implemented.

**What's feasible later**: Full structural estimation with AMPL-based real purchasing power measurement, once Layer 2 is operational.

### Sequencing Summary

| Order | Exercise | Feasibility Now | Blocking Dependencies |
|-------|----------|----------------|----------------------|
| 0 | Literature foundation | Fully feasible | None |
| 1 | Data feasibility probe | Fully feasible | None |
| 2 | Migration shock | Conditional on Exercise 1 data | Exercise 1 |
| 3 | Local recession | Conditional; harder identification | Exercise 1 |
| 4 | Capital controls | Best near-term candidate (Nigeria events) | Exercise 1 |
| 5 | Inflation spikes | Requires Layer 2 for full treatment | Exercise 1 + architecture |

Recommended order: 0 and 1 in parallel, then 4 (capital controls, exploiting Nigeria's well-documented policy events), then 2 (migration shocks, if event dates align with data window), then 3 and 5 (harder identification, more data needed).

---

## 6. Open Questions Requiring Human Decisions

The following are economic and methodological decisions that must be made by the researcher. Per project protocol (Phase -1 must be interactive), these are flagged but NOT resolved.

### 6.1 Country Selection

Which corridor to prioritize first? The tradeoff is:
- **Brazil**: Best data, weakest economic case (0.3% remittance/GDP)
- **Mexico**: Good and growing data, strong economic case (4.2% remittance/GDP)
- **Nigeria**: Strongest economic case, weakest data (thin on-chain liquidity)
- **Kenya**: Moderate on both axes, M-Pesa integration potential

Decision needed: start with the best data (Brazil) as proof-of-concept and transfer methodology, or go directly to the strongest economic case (Nigeria/Mexico)?

### 6.2 What Exactly Is "Income" in This Context?

The PRE_REQ says "household income driven by cross-border transfers." But this could mean:
- (a) Total remittance inflow to the country (aggregate)
- (b) Per-household remittance income for receiving households (micro)
- (c) Variation in (a) or (b) relative to trend (detrended)
- (d) The VARIANCE of any of the above

For the variance swap, (d) is the payoff-relevant quantity. But to establish the PRE_REQ, you need to decide which of (a)-(c) the on-chain observable is being linked to.

### 6.3 Prediction vs. Hedging

The spec asks whether net_flow "predicts or explains" household income. These have different econometric implications:
- **Prediction**: Granger causality test. Requires temporal precedence. Useful if the instrument is meant to provide early warning.
- **Explanation / co-movement**: Contemporaneous correlation. Requires the variance swap to settle over the SAME period as the income variation. Useful if the instrument is meant to hedge realized risk.

Decision needed: is the variance swap an early-warning instrument or a contemporaneous hedge?

### 6.4 Contamination Strategy

On-chain flows include remittances, speculation, arbitrage, yield-seeking, and capital flight. How to handle this:
- (a) Filter by transaction size ($200-$2000 = likely remittance)
- (b) Filter by frequency (monthly patterns = likely remittance)
- (c) Address clustering (repeat small senders = likely remittance)
- (d) Use net flow (cancels round-trip arb) as noisy proxy, bound attenuation bias
- (e) Accept total net flow as the observable and argue it is BETTER than just remittances (it captures net purchasing power transfer, including capital flight)

Option (e) is the most intellectually interesting because it redefines the instrument: the variance swap hedges against volatility of NET cross-border purchasing power transfer, which includes but is not limited to remittances.

Decision needed: pure remittance extraction, or embrace the broader "net purchasing power transfer" definition?

### 6.5 The "Predicts/Explains" Ambiguity in the PRE_REQ

The spec itself marks this as uncertain. The choice between "predicts" and "explains" determines:
- The lag structure of the econometric specification
- Whether the instrument is a leading indicator or a contemporaneous hedge
- The relevant specification tests (Granger causality vs. contemporaneous regression)

Decision needed before writing the full Reiss-Wolak specification.

### 6.6 Variance Computation Method

"Var(Net USDT -> FX)" requires choices:
- Rolling window length (7d? 30d? 90d?)
- Realized variance vs. EWMA vs. GARCH conditional variance
- Annualization convention
- Treatment of weekends/low-activity periods
- Whether to use log returns of the flow or absolute deviations

These are not just technical choices -- they affect the economic interpretation and the hedging horizon.

### 6.7 Who Are the Shorts?

The EXPECTED_SHORTS section is explicitly contingent on PRE_REQ. But even after PRE_REQ, the question of who takes the other side of this trade is an economic judgment:
- Is there a natural short (someone who benefits from remittance volatility)?
- Or does this require a speculative short (variance risk premium sellers)?
- If the latter, is there evidence that a variance risk premium exists in remittance flows?

### 6.8 Settlement Mechanism

The architecture provides two options: Panoptic and Voltaire. But the variance swap does not obviously map to either:
- Panoptic settles options/perpetuals on Uniswap V3 positions
- A variance swap on FLOW data is not an option on a PRICE

Decision needed: is this settled as a custom Layer 3 instrument (new settlement contract reading flow data), or does it decompose into existing primitives (e.g., a strip of options on the Remittance Health Index)?

### 6.9 Time Granularity

The econometric spec raises this: hourly? daily? weekly? The choice depends on:
- The frequency of actual remittance-relevant flows
- The minimum observations needed for variance estimation
- The hedging horizon of the target users (fintechs plan monthly, payment apps need daily awareness)

---

## Appendix: File Reference Index

| File | Role in This Research |
|------|----------------------|
| `notes/REMITTANCE_VOLATILITY_SWAP/REMITTANCE_VOLATILITY_SWAP.md` | Core instrument spec |
| `notes/REMITTANCE_VOLATILITY_SWAP/STABLECOIN_FLOWS.md` | IMF empirical evidence on stablecoin-FX nexus |
| `notes/INCOME_SETTLEMENT.md` | Settlement theory, instrument taxonomy, Shiller-CFMM mapping |
| `notes/PRICE_SETTLEMENT.md` | When price settlement applies (illiquid cash markets) |
| `notes/SIGNAL_TO_INDEX.md` | Signal -> Index -> Settlement pipeline |
| `notes/MACRO_RISKS.md` | Macro risk taxonomy, psychology of framing |
| `notes/MACRO_DERIVATIVES.md` | CDS analogy, MacroDefaultSwap construct |
| `notes/MACRO_RISKS_CHECKPOINT.md` | Literature references (Shiller, macro derivatives papers) |
| `notes/structural-econometrics/specs/SIGMOID_VOLATILITY_SWAP/2026-04-01-usdc-dai-volume-fee-elasticity.md` | Methodological template (Reiss-Wolak spec) |
| `notes/structural-econometrics/specs/INCOME_SETTLEMENT/2026-04-02-net-trading-volume-remittance-income.md` | Direct PRE_REQ econometric brainstorm |
| `refs/pensionFunds/mento_research.md` | On-chain EM FX data availability |
| `refs/pensionFunds/stabull_deep_dive.md` | Alternative FX AMM venue assessment |
| `refs/macro-risk/ARCHITECTURE.md` | Three-layer architecture, index engine, RHI definition |
| `notes/ECONOMETRICS_NOTES.md` | Methodological references (Heckman, diff-in-diff) |
| `notes/PENSION_FUNDS.md` | Institutional demand context (PutWrite, short-vol users) |
| `notes/SIGMOID_VOLATILITY_SWAP.md` | Sibling instrument (fee-based vol swap), USDC/WETH results |
