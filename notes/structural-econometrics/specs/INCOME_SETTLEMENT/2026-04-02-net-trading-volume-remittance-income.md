# Structural Econometric Specification: Net Trading Volume as Predictor of Household Income from Cross-Border Transfers

*Date: 2026-04-02*
*Status: Phase -1 (Identification brainstorm -- requires human decisions)*
*Framework: Reiss & Wolak (2007), Handbook of Econometrics Vol 6A, Ch. 64*

---

## 0. High-Level Question

**Can net trading volume of USD-equivalent stablecoins against an underserved-country currency on-chain predict variation in household income driven by cross-border transfers (remittances)?**

More precisely: if we observe net flow(USDC -> cNGN) on Mento/Uniswap pools over time, does this observable carry information about the income received by Nigerian households from diaspora remittances?

---

## 1. Why This Exercise Matters

This is the **first feasibility test** for income-settled derivatives on underserved-country currencies. If net trading volume proxies remittance-driven income variation:
- We have an on-chain settlement oracle for income claims (no off-chain dependency)
- The signal is real-time (not quarterly GDP reports)
- It bootstraps the Shiller perpetual income claim using existing pool infrastructure

If the proxy is too noisy or contaminated, we know to look elsewhere (e.g., pure FX depreciation, fee revenue, vault yields).

---

## 2. The Economic Chain We Need to Establish

```
On-chain observable              Real-world target
─────────────────────            ──────────────────
net_flow(USDC -> cNGN, t)   -->  remittance_inflow(Nigeria, t)
                                       |
                                       v
                              household_income_from_transfers(t)
                                       |
                                       v
                              total_household_income_variation(t)
```

Each arrow is a **separate identification question** with its own assumptions:

### Arrow 1: net_flow(USDC -> cNGN) --> remittance_inflow(Nigeria)
- What fraction of USDC->cNGN swaps are actually remittances vs. speculation vs. arbitrage?
- Is the signal dominated by a few whales or distributed across many small transfers?
- Does the corridor matter? (US-based Nigerians use USDC, UK-based might use different paths)

### Arrow 2: remittance_inflow --> household_income_from_transfers
- Remittances are not income to the sender, they ARE income to the receiver
- But we observe the send-side (on-chain swap), not the receive-side (cash-out)
- Timing: does the on-chain swap precede, coincide with, or lag the actual household receipt?

### Arrow 3: household_income_from_transfers --> total_household_income_variation
- Remittances are ~4-5% of Nigerian GDP but much higher % for receiving households
- For households that receive remittances, transfers can be 30-60% of household income
- The variation in remittance income may dominate total income variation for this subpopulation

---

## 3. Candidate Countries (by on-chain FX liquidity and remittance dependency)

| Country | Remittances % GDP | Best On-Chain Token | Pool Venue | Liquidity Status |
|---------|------------------|--------------------|-----------:|-----------------|
| Nigeria | ~4.5% | cNGN (Mento) | Uniswap v3 Celo | Very thin |
| Philippines | ~10% | PUSO (Mento) | Mento exchange | Minimal DEX |
| Kenya | ~3.4% | cKES (Mento) | Uniswap v3 Celo | ~$4.8k TVL |
| Colombia | ~2.8% | cCOP (Mento) | Mento exchange | New, no pool |
| Brazil | ~0.3% | BRLA/BRZ | Uniswap Polygon | Best liquidity |
| Mexico | ~4.2% | MXNe | Aerodrome/Uni Base | Growing |
| South Africa | ~0.3% | ZARP | Uniswap/Stabull Base | Institutional backing |
| El Salvador | ~24% | - | - | No stablecoin |
| Ghana | ~5.3% | cGHS (Mento) | Mento exchange | Minimal |
| West Africa (WAEMU) | varies | eXOF (Mento) | Uniswap v3 Celo | ~$12k TVL |

**Selection criteria for first exercise**: Need BOTH (a) meaningful remittance dependency AND (b) observable on-chain flows.

---

## 4. Identification Challenges (OPEN -- require human decisions)

### 4.1 What counts as "remittance" in on-chain flow data?

**The contamination problem**: A USDC->cNGN swap could be:
- (a) Diaspora Nigerian sending money home (REMITTANCE)
- (b) Trader speculating on NGN appreciation (SPECULATION)
- (c) Arbitrageur correcting a price discrepancy (ARBITRAGE)
- (d) DeFi user farming yield (YIELD SEEKING)
- (e) Capital flight from Nigeria (REVERSE FLOW -- not remittance)

**Question for identification**: Can we separate these? Possible strategies:
1. **Size filter**: Remittances tend to be $200-$2000. Whale trades are larger. Filter by tx size.
2. **Frequency filter**: Remittance senders have regular patterns (monthly). Arbs are high-frequency.
3. **Address clustering**: Repeat addresses with regular small transfers → likely remittance
4. **Directional filter**: Net USDC→cNGN flow (not round-trip) more likely remittance
5. **Accept contamination**: Use total net flow as a noisy proxy and bound the attenuation bias

### 4.2 Which direction tells the story?

For Nigerian remittances, the expected flow is:
```
US-based Nigerian earns USD → buys USDC → swaps USDC for cNGN → sends cNGN to family
```

So the **directional** observable is: net_buy(cNGN, paid_in_USDC)

But there's also the reverse: Nigerians converting cNGN to USDC for:
- Paying for US services/education
- Capital flight
- Saving in USD

**The NET flow is the margin**: net = remittance_in - capital_flight_out

This is actually MORE interesting than gross remittance -- it captures the net transfer of purchasing power.

### 4.3 Counterfactual: what is the "no remittance" baseline?

To claim net_flow predicts VARIATION in income, we need a counterfactual:
- What would household income be without the remittance flow?
- Is the variation we're measuring driven by shocks to the SENDER (US recession → less remittance) or shocks to the RECEIVER (Nigerian crisis → more remittance requested)?

### 4.4 Temporal structure

- Remittance sending likely has weekly/monthly patterns (payday cycles)
- On-chain swaps are continuous
- Is the unit of observation hourly? Daily? Weekly?
- What lag structure do we expect?

---

## 5. Data Requirements (to be specified after identification decisions)

### 5.1 On-chain data (Dune queries needed)
- [ ] Swap events on cNGN/USDC pools (Mento exchange + any Uniswap v3 Celo pools)
- [ ] Swap events on BRLA/USDC, BRZ/USDC (Polygon Uniswap) -- comparison country
- [ ] Transaction-level data: sender, amount, timestamp, direction
- [ ] Address clustering: repeat senders, transaction size distribution
- [ ] Pool-level: TVL, volume, fee revenue time series

### 5.2 Off-chain validation data
- [ ] World Bank remittance data (quarterly, by corridor)
- [ ] CBN (Central Bank of Nigeria) BOP data
- [ ] Western Union / MoneyGram volume reports (if available)
- [ ] Mobile money transfer volumes (M-Pesa for Kenya, OPay for Nigeria)

### 5.3 Macro controls
- [ ] USD/NGN official rate (CBN)
- [ ] USD/NGN parallel market rate
- [ ] Nigeria CPI
- [ ] US unemployment rate (affects sender capacity)
- [ ] Oil price (Nigeria is oil-dependent)

---

## 6. Feasibility Pre-Check (BEFORE writing the full spec)

Before committing to a full Reiss-Wolak specification, we need to answer:

### 6.1 Is there enough on-chain data?
- How many cNGN/USDC swaps occur per day? Per week?
- What's the transaction size distribution?
- How far back does the data go?

### 6.2 Is the signal plausibly separable from noise?
- What fraction of volume looks like remittance-sized transfers?
- Is there a clear directional asymmetry (more USDC->cNGN than reverse)?

### 6.3 Is there a validation target?
- Can we get monthly/quarterly remittance data for the same period?
- Is there any existing research linking on-chain stablecoin flows to remittance corridors?

---

## 7. Research Tasks

### Phase -1: Feasibility (current)
- [ ] Query Dune for cNGN/USDC swap event data (volume, count, size distribution)
- [ ] Query Dune for directional flow asymmetry
- [ ] Literature search: stablecoin remittance corridor research
- [ ] Literature search: remittance as income proxy (development economics)
- [ ] Identify best country candidate based on data availability

### Phase 0: Identification (after feasibility confirmed)
- [ ] Specify exclusion restrictions
- [ ] Define the contamination decomposition strategy
- [ ] Define unit of observation and time granularity
- [ ] Write identification assertions (with Aristotle formalization)

### Phase 1: Data collection
- [ ] Build Dune queries (permanent, non-temp, with verifiable IDs)
- [ ] Collect off-chain validation data
- [ ] Exploratory data analysis

### Phase 2: Estimation
- [ ] Implement estimator
- [ ] Run specification tests
- [ ] Robustness checks

---

## 8. Open Questions for Discussion

1. **Country selection**: Should we start with Nigeria (high remittance dependency, thin on-chain liquidity) or Brazil (lower remittance dependency, better on-chain liquidity)?

2. **What exactly is the "income" we're trying to predict?** Is it:
   - (a) Total remittance inflow to the country?
   - (b) Per-household remittance income for receiving households?
   - (c) Variation in (a) or (b) relative to trend?

3. **Is the goal prediction or hedging?** These are different:
   - Prediction: can we forecast next month's remittance flow from this month's on-chain data?
   - Hedging: can a Nigerian household buy a claim whose payoff correlates with their remittance income variation?

4. **Multiple corridors**: Nigerian diaspora is in US (35%), UK (20%), Canada (10%), UAE (8%). Each corridor would use different stablecoins/chains. Do we need corridor decomposition?

5. **The Mento exchange contract vs. Uniswap pool**: Most cNGN liquidity routes through Mento's own AMM (reserve-as-counterparty), not Uniswap v3. Is Mento exchange contract swap data queryable on Dune? If not, we may need direct Celo RPC indexing.
