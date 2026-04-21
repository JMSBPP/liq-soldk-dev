# Structural Exercise: cCOP/COPM Net Volume as Predictor of Colombian USD→COP Income Conversion

*Date: 2026-04-02*
*Status: Phase -1 (structure laid out, identification decisions pending agent outputs)*
*Framework: Reiss & Wolak (2007)*
*Tokens: cCOP/COPm (Mento, Uniswap v3) + COPM (Minteo, 100K users)*
*Depends on: COLOMBIAN_ECONOMY_CRYPTO.md, COPM_MINTEO_DEEP_DIVE.md (pending)*

---

## 0. How the Picture Changed

### Original Framing (from Shiller)
```
Claim :: Flow(Forward(Income, futureTime))
Settlement :: CashMarket(PerpetualClaim(Index(Income)))

PRE_REQ: Net(USDT → FX) predicts d(household income from cross-border transfers)
```

### What the Data Revealed
```
The "cross-border transfer" taxonomy is richer than remittance:

USD → COP conversion on-chain {
    (A) UBI recipients           ~$12/week, ImpactMarket, scheduled claims
    (B) Celo DAO community       developers, governance, test txns
    (C) Minteo/COPM users        100K users, fintech product, USE CASES TBD
    (D) MiniPay → El Dorado      cUSD→COP via fiat off-ramp
    (E) Remittance receivers     traditional cross-border, US/Spain→CO
    (F) Freelancer income        USD-denominated contract work
    (G) Speculative/arb          bots, arbitrageurs (0x2021...1271)
}
```

The "representative household" is NOT a single type. It's a mixture whose composition we partially know from the data:
- (A) and (B) are identifiable and must be CONTROLLED FOR (not the target population)
- (C) is the key unknown — agent output will reveal if Minteo users are income converters
- (D), (E), (F) are the target populations for the hedging instrument
- (G) is noise to be filtered

### Revised PRE_REQ
```
OLD: Net(USDT → FX) predicts d(household income from cross-border transfers)

NEW: Net(USD → COP) on Mento/Uniswap, AFTER controlling for (A) UBI, (B) community, 
     (G) arb, predicts d(USD-denominated income converted to COP)
     
     where "income" includes: remittance (E), freelancer (F), fintech-mediated (C+D)
```

This is a WEAKER but MORE HONEST claim. We don't need to prove it's specifically remittance. We need to prove the RESIDUAL (after filtering known non-income activity) carries income information.

---

## 1. The Hedging Argument (Who Wants This Instrument?)

### Primary: Colombian Fintechs (Minteo, El Dorado, etc.)
```
Minteo {
    serves: 100K Colombian users
    product: COP stablecoin (COPM) for payments/transfers
    risk: Var(Net USD → COP flow) through their platform
    
    WHEN flow spikes unpredictably:
        → operational stress (liquidity management)
        → FX exposure (if holding USD reserves backing COPM)
        → credit risk (if lending against COP-denominated positions)
    
    HEDGE: Long variance swap on cCOP/cUSD CFMM
           → pays out when conversion flow variance increases
           → offsets operational/liquidity risk
}
```

### Secondary: Colombian Remote Workers / Freelancers
```
ColombianFreelancer {
    earns: USD (via Deel, Payoneer, or crypto)
    converts: USD → COP for living expenses
    risk: Var(COP/USD rate) + Var(income flow timing)
    
    WHEN COP depreciates sharply:
        → purchasing power drops before next paycheck conversion
        → may delay conversion (strategic waiting)
        → income stream in COP terms becomes volatile
    
    HEDGE: Protective position on cCOP/cUSD
           → compensates when COP purchasing power drops
}
```

### Tertiary: Remittance-Dependent Households
```
RemittanceHousehold {
    receives: USD from diaspora (US, Spain)
    converts: USD → COP for rent, food, education
    risk: Var(remittance amount) + Var(COP/USD at conversion time)
    
    HEDGE: Same instrument, different user journey
           → accessed via Minteo/MiniPay frontend, not directly
}
```

---

## 2. The Instrument Architecture

```
┌─────────────────────────────────────────────────┐
│  LAYER 3: HEDGING INSTRUMENT                    │
│  Variance swap / perpetual option on cCOP/cUSD  │
│  Read from CFMM observables (Uniswap v3 Celo)  │
│  NO liquidity bootstrapping (borrow from pool)  │
│  Convex payoff: pays more in stress             │
└───────────────────┬─────────────────────────────┘
                    │ settles against
┌───────────────────┴─────────────────────────────┐
│  LAYER 2: CFMM SETTLEMENT ORACLE                │
│  cCOP/cUSD Uniswap v3 pool on Celo              │
│  Observables: price, feeGrowthGlobal, liquidity │
│  96,660 trades, 276 takers, 10K/month           │
│  THIS is where Panoptic-style options work       │
└───────────────────┬─────────────────────────────┘
                    │ prices reflect
┌───────────────────┴─────────────────────────────┐
│  LAYER 1: INCOME CONVERSION SIGNAL              │
│  Mento broker: 3,578 traders (mixed population) │
│  COPM/Minteo: 100K users (real fintech)         │
│  MiniPay + El Dorado: cUSD→COP off-ramp         │
│                                                  │
│  AFTER FILTERING: UBI (A), community (B),        │
│  arb (G) → residual = income signal             │
└─────────────────────────────────────────────────┘
```

### The No-Bootstrapping Constraint
The instrument reads from the EXISTING cCOP/cUSD Uniswap v3 pool. It does not create a new pool. Liquidity already exists (96,660 trades). The instrument borrows from this liquidity (Panoptic V2 / SFPM pattern per project architecture).

### The Convexity
The CFMM fee revenue is convex in variance (from the SIGMOID_VOLATILITY_SWAP work). In stress:
- Volume increases (more urgent conversions)
- Fee revenue increases more than proportionally
- The instrument payoff is convex — pays more when it's needed most

---

## 3. The Econometric Exercises

### Exercise 0: Population Decomposition (DESCRIPTIVE)
**Question**: What fraction of cCOP/COPm Mento broker activity is (A) UBI, (B) community, (G) arb vs. (C-F) potential income conversion?

**Method**:
- Use CELO_EVENT_CONTROL_VARIABLES.md to flag UBI claim days (Thursday), governance days
- Identify known bot addresses (0x2021...1271 and others from top sender analysis)
- Identify known ImpactMarket contracts
- Residual = candidate income conversion population

**Data**: Already have top sender/receiver data (queries #6940020, #6940021)
**Status**: Can begin now

### Exercise 1: Sanity Check (REDUCED FORM)
**Question**: Does the RESIDUAL weekly net flow (after filtering A, B, G) correlate with COP/USD exchange rate movements?

**Method**:
```
ln(ResidualNetFlow_t) = α + β₁ d(COP/USD_t) + β₂ Controls + u_t
```

**Why this works**: If β₁ ≠ 0, the residual flow responds to macro conditions. COP depreciation should increase USD→COP conversion (people converting to buy more COP while it's cheap, or receiving more COP per dollar of remittance).

**Data needed**:
- Residual net flow from Exercise 0
- COP/USD daily rate (Coins.ph API or Chainlink)
- Controls: total Celo DEX volume, COPM trading volume, Thursday dummy

**Unit of observation**: Weekly (aggregate daily to weekly to smooth noise)
**Time period**: Oct 2024 - Apr 2026 (~78 weeks)
**Status**: Conditional on Exercise 0 and COP/USD price data

### Exercise 2: Behavioral Calibration — COPM vs cCOP
**Question**: Do COPM users (Minteo, 100K real users) show the same behavioral patterns as the residual cCOP population?

**Method**: 
- Compute COPM behavioral fingerprints (same pipeline as PUSO: size distribution, temporal, clustering)
- Compare against cCOP RESIDUAL (after filtering A, B, G)
- KS test on size distributions
- Correlation of temporal patterns

**Why this matters**: If COPM users ≈ cCOP residual users → interpolation is justified. COPM has more users and cleaner signal; cCOP has CFMM integration.

**Data needed**: COPM behavioral fingerprints (NOT YET COMPUTED — need Dune queries)
**Status**: Conditional on COPM_MINTEO_DEEP_DIVE.md for understanding what to look for

### Exercise 3: Variance Response to Macro Shocks (EVENT STUDY)
**Question**: Does Var(Residual Net Flow) increase when macro shocks hit Colombia?

**Method**: Event study around dated shocks:
- COP major depreciation events (2022 spike to 4,800+, 2024 election uncertainty)
- US Fed rate decisions (affect USD/COP via interest differential)
- Colombian inflation spikes (2022-2023, peaked at 13.3%)
- Venezuelan migration surges
- Oil price shocks (Colombia is oil-dependent)

Compare: Var(flow) in [-30d, -1d] before shock vs. [+1d, +30d] after shock

**Why this matters**: This directly tests whether the variance swap payoff responds to the RIGHT events. If Var spikes during COP depreciation but NOT during Celo-specific events (after controlling), the instrument carries macro content.

**Data needed**: 
- Residual net flow from Exercise 0
- Dated macro events (from COLOMBIAN_ECONOMY_CRYPTO.md)
- CELO_EVENT_CONTROL_VARIABLES.md for filtering

**Status**: Conditional on Exercises 0-1 passing

### Exercise 4: Income Validation (LOW FREQUENCY)
**Question**: Does monthly aggregate USD→COP on-chain flow correlate with Banco de la República monthly remittance data?

**Method**:
```
ln(BanRep_Remittance_t) = α + β ln(OnChain_COP_Flow_t) + u_t
```

**Frequency**: Monthly (~18 observations if Oct 2024 - Apr 2026)
**Power**: Very low. This is a sanity check, not a precision estimate.
**Why it matters**: If β > 0 even with 18 observations, there's a real connection between on-chain and off-chain income flows.

**Data needed**: BanRep monthly remittance data (manual download from Banco de la República website)
**Status**: Conditional on BanRep data availability

---

## 4. Sequencing

```
PHASE 0 (NOW — can begin with current data):
├── Exercise 0: Population decomposition 
│   (use top sender/receiver data to identify UBI, bots, community)
├── COP/USD historical price collection (Coins.ph API or Chainlink)
└── BanRep monthly remittance data download

PHASE 1 (after COPM_MINTEO_DEEP_DIVE.md):
├── Exercise 2: COPM behavioral fingerprints
├── Exercise 1: Sanity check regression
└── Update population decomposition with Minteo insights

PHASE 2 (after COLOMBIAN_ECONOMY_CRYPTO.md):
├── Exercise 3: Macro shock event study
├── Exercise 4: BanRep validation
└── Identification assertions (Aristotle formalization)

PHASE 3 (after Exercises 1-3 pass):
├── Full Reiss-Wolak structural specification
├── Variance estimation with proper controls
└── Instrument pricing specification
```

---

## 5. AGENT OUTPUTS — What We Now Know (2026-04-02)

### COPM/Minteo (from COPM_MINTEO_DEEP_DIVE.md)
- **COPM is income-conversion-driven, not speculative.** Users convert salary/freelance income to COP stablecoin.
- Flow pattern: Salary → COP fiat → Littio → COPM (or USDC for dollar savings)
- 100K users via Littio, 50+ B2B clients for corporate treasury
- $200M/month volume but mostly through Minteo's mint/redeem API, NOT DEX
- DEX liquidity is thin (~$22K on Celo Uniswap V3 COPM pool)
- Founded by Wompi team (acquired by Bancolombia) — serious fintech pedigree

### Colombian Economy (from COLOMBIAN_ECONOMY_CRYPTO.md)
- Remittances: $11.85B (2024), all-time high, US corridor = 53%
- COP volatility: 3,450→5,133→4,050 per USD (2020-2025) — EXTREME
- 56% informal employment, 49% below minimum wage
- Littio: 200K+ users, 100%+ growth during Jan 2025 tariff crisis
- MoneyGram USDC launched Colombia as first market (Sept 2025)
- Regulatory: SFC does NOT supervise crypto (permissive by omission)

### The Bidirectional Flow Discovery
Colombia has TWO opposing populations creating variance:

```
INFLOW (USD → COP):                    OUTFLOW (COP → USD):
  Remittance receivers                    Littio savers (200K users)
  Freelancers/contractors                 Crypto-native hedgers
  COPM mint (salary→COP stablecoin)      USDC flight during COP depreciation

  Driven by: income, spending need        Driven by: COP depreciation fear
  Shock response: UP when COP weak        Shock response: UP when COP weak
  (more COP per USD)                      (flee to USD)
```

Both directions INCREASE during macro stress → net flow oscillates → VARIANCE SPIKES.
This is the structural source of the variance the swap would trade.

### The COPM vs cCOP Architecture (RESOLVED)
```
COPM (Minteo):                        cCOP/COPm (Mento):
  100K real users                       3,578 Mento broker traders
  $200M/month volume                    Small but growing
  Mint/redeem API (NOT DEX)             Uniswap v3 CFMM pool (96K trades)
  Behavioral reference                  Settlement oracle
  
  COPM tells us WHO and WHY             cCOP tells us the PRICE and VARIANCE
```

The interpolation: COPM behavioral patterns validate that the cCOP CFMM captures 
real income-conversion dynamics. The instrument SETTLES on cCOP/cUSD Uniswap v3.
COPM provides the population-level calibration.

---

## 6. Open Questions (require human decisions)

1. **Settlement token confirmed**: cCOP/COPm Uniswap v3 pool = settlement oracle. COPM = behavioral reference for interpolation. This mirrors the original (a)+(c) strategy but both tokens are ALIVE.

2. **Is the PRE_REQ "predicts" or "explains"?** 
   - "Predicts" = forecasting (harder, needs temporal ordering)
   - "Explains" = contemporaneous correlation (easier, weaker claim)
   - For a hedging instrument, "explains" may be sufficient — the hedge pays when the flow is volatile, regardless of prediction direction

3. **What is the "income" we're measuring? — NOW ANSWERED**
   - COPM users are CONVERTING SALARY INCOME through Littio
   - The flow IS income: salary → COP fiat → Littio → COPM
   - But Littio also enables COP→USDC (savings/hedging) — this is the OUTFLOW
   - The NET = income conversion MINUS savings flight
   - This NET is itself a macro variable: high NET = confidence in COP; low NET = capital flight

4. **Should we control for ImpactMarket UBI or INCLUDE it?**
   - UBI IS income for recipients (real $12/week)
   - But it's protocol-scheduled, not market-driven — variance is artificial
   - **Recommendation**: CONTROL for it (Thursday dummy + known addresses)
   - The macro signal lives in the RESIDUAL after removing scheduled distributions

5. **The representative household — REVISED**
   > TWO representative households:
   > 
   > **Household A (Income Converter)**: Colombian receiving USD-denominated income 
   > (freelancing, remittance, or fintech-mediated). Converts USD→COP for daily expenses.
   > Uses Minteo/COPM, Littio, MiniPay/El Dorado. Risk: income flow volatility + FX.
   > 
   > **Household B (Savings Hedger)**: Colombian converting COP→USD to preserve 
   > purchasing power during depreciation. Uses Littio USDC yield accounts.
   > Risk: COP depreciation eroding savings before conversion.
   >
   > The VARIANCE of net flow between these two populations is the settlement variable.
   > The instrument hedges BOTH: A hedges income disruption, B hedges depreciation risk.
   > Both benefit from the same convex payoff structure.

6. **Composite index vs. single observable?**
   - COPM_MINTEO_DEEP_DIVE.md recommends a composite: COPM flow + COP/USD rate + BanRep data
   - Should the settlement oracle be purely the cCOP CFMM? Or a weighted index?
   - Pure CFMM is simpler and composable with Panoptic
   - Composite is richer but requires custom oracle infrastructure
