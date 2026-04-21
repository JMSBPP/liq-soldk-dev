# Data Strategy: Three-Source Interpolation for Colombia Variance Swap

*Date: 2026-04-02 (UPDATED — originally PUSO-focused, now Colombia-primary)*
*Depends on: CROSS_CURRENCY_COMPARISON.md, COLOMBIAN_ECONOMY_CRYPTO.md, COPM_MINTEO_DEEP_DIVE.md, CELO_EVENT_CONTROL_VARIABLES.md*

---

## REVISION HISTORY
- v1 (2026-04-02 early): PUSO/Philippines as primary target, PHPC as reference
- **v2 (2026-04-02 late): PIVOTED TO COLOMBIA** after behavioral fingerprints revealed:
  - PUSO = campaign/UBI activity, not income conversion (~20 organic users)
  - PHPC on Polygon = dead (87 transfers)
  - cKES = same campaign as PUSO (identical Thursday spike)
  - cGHS = 99% bot-driven
  - **cCOP = most organic market (4,913 senders, Colombia timezone, flat size distribution)**
  - **COPM/Minteo = 100K real Colombian users, income-conversion-driven**
  - **Colombia has bidirectional USD↔COP flow creating higher variance than Philippines**

---

## The Strategy (REVISED)

```
(a) cCOP/COPm (Mento, Uniswap v3)  = CFMM settlement oracle
     ↕ behavioral calibration
(c) COPM (Minteo, 100K users)       = income conversion signal
     ↕ aggregate calibration  
(b) BanRep remittance data + COP/USD rate = population-level reference
```

### Why Colombia over Philippines
| Dimension | Philippines (PUSO) | Colombia (cCOP/COPM) |
|---|---|---|
| Organic users | ~20 (after campaign filter) | 4,913+ senders |
| Behavioral reference | PHPC DEAD (87 transfers) | COPM ALIVE (100K users, $200M/mo) |
| Flow direction | Mostly USD→PHP (unidirectional) | USD↔COP (bidirectional) |
| Variance generation | Low (stable PHP) | High (extreme COP volatility) |
| Fintech layer | None (PUSO = community experiment) | Minteo, Littio, El Dorado, MoneyGram USDC |
| Remittance relevance | 10% GDP but no on-chain signal | 2.8% GDP, growing 17% YoY, all-time high |

---

## Source (a): cCOP/COPm (Mento + Uniswap v3) — SETTLEMENT LAYER

| Property | Status |
|---|---|
| Mento broker traders | 3,578 unique (24,577 trades) |
| Uniswap v3 trades | 96,660 (276 takers, 10K/month) |
| Carbon DeFi | 70,915 (37 takers, bots) |
| CFMM observables | YES (Uniswap v3: price, fees, ticks, liquidity) |
| Dune coverage | Full — dex.trades, mento_celo.broker_evt_swap, stablecoins_multichain.transfers |
| Cost | FREE |
| Known contamination | UBI claims (ImpactMarket), Celo governance (Thursdays), hardfork (July 2025) |
| Control variables | CELO_EVENT_CONTROL_VARIABLES.md |
| Permanent queries | #6939996, #6939997, #6940019, #6940020, #6940021, #6940688, #6940691 |

## Source (c): COPM (Minteo) — BEHAVIORAL REFERENCE

| Property | Status |
|---|---|
| Users | 100K via Littio + 50+ B2B clients |
| Volume | $200M/month (mint/redeem API, NOT DEX) |
| Dune coverage | stablecoins_multichain.transfers (104,775 transfers, 1,033 senders) |
| DEX activity | 5,872 Uniswap trades + 69,064 Carbon DeFi |
| User behavior | Salary → COP fiat → Littio → COPM (income conversion confirmed) |
| Key signal | Mint/redeem flow = income entering/leaving COP stablecoin |
| Limitation | Thin DEX liquidity (~$22K on Uni V3); most volume through Minteo API |

## Source (b): BanRep + COP/USD — MACRO CALIBRATION

| Property | Status |
|---|---|
| BanRep remittance | Monthly, by corridor, from banrep.gov.co |
| COP/USD rate | Coins.ph API (free), Chainlink, TradingEconomics |
| Frequency | Monthly (BanRep), daily (COP/USD) |
| Cost | FREE |
| Macro events | Petro election (2022), tariff crisis (Jan 2025), economic emergency (Dec 2025) |

---

## Interpolation Method (UPDATED)

### Step 1: Clean the cCOP signal
- Remove known UBI addresses (ImpactMarket)
- Remove bot addresses (0x2021...1271 and top senders with <10 counterparties)
- Apply Thursday dummy for governance/claim scheduling
- Apply hardfork window exclusion (July 7-12, 2025)
- Residual = candidate income conversion population

### Step 2: Compute COPM behavioral fingerprints
- Mint/redeem size distribution
- Temporal patterns (Colombia timezone expected)
- Address clustering (regular vs one-shot)

### Step 3: Compare cCOP residual ≈ COPM fingerprint
- KS test on size distributions
- Correlation of temporal patterns
- If match → cCOP residual captures same population as COPM → CFMM settlement is valid

### Step 4: Validate against BanRep macro data
- Monthly cCOP net flow vs BanRep monthly remittance
- Weekly cCOP net flow vs COP/USD weekly change
- Var(cCOP net flow) response to dated macro shocks

---

## Execution Order (UPDATED)

### PHASE 0 — NOW
- [x] Currency selection (data-driven) → Colombia wins
- [x] cCOP market structure analysis → Uniswap + Mento + Carbon
- [x] Top sender/receiver identification → app addresses found
- [x] Event control variables documented
- [x] Colombian economy research complete
- [x] COPM/Minteo deep dive complete
- [ ] COPM behavioral fingerprints (Dune queries needed)

### PHASE 1 — Population decomposition
- [ ] Exercise 0: Classify cCOP addresses (UBI, bot, community, income)
- [ ] COPM behavioral fingerprints
- [ ] KS test: cCOP residual vs COPM

### PHASE 2 — Sanity checks
- [ ] Exercise 1: Weekly cCOP residual net flow vs COP/USD
- [ ] Exercise 4: Monthly vs BanRep remittance

### PHASE 3 — Variance response
- [ ] Exercise 3: Event study — Var(flow) around macro shocks
- [ ] Full Reiss-Wolak specification

---

## Cost Summary (UNCHANGED)
All data sources remain FREE. No paid APIs required.
