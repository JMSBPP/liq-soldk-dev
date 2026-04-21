# PUSO Population Decomposition: Who Is Converting USDC → PUSO?

*Date: 2026-04-02*
*Status: Hypothesis — requires empirical validation*

---

## 1. The Assumption We Must NOT Make

**Wrong assumption:** USDC → PUSO flow = US-based Filipino sending remittance to family in Philippines.

**Reality:** The population converting USDC to PUSO includes at least 5 distinct groups with different economic profiles:

```
USDC → PUSO converters {

    (A) DIASPORA_REMITTANCE {
        location: US, Gulf states, Singapore, Japan, UK
        income_source: employment in host country
        conversion_purpose: transfer to dependent household in PH
        frequency: monthly (payday-aligned)
        size: $200-$1000 typical
        economic_meaning: cross-border income transfer
    }
    
    (B) REMOTE_CONTRACTOR {
        location: Philippines (or anywhere)
        income_source: contract work paid in USD/USDC
        conversion_purpose: pay rent, food, daily expenses in PHP
        frequency: biweekly or monthly (invoice cycles)
        size: $500-$5000 typical
        economic_meaning: local income, foreign-denominated
        NOTE: may have HIGHER income than diaspora workers
    }
    
    (C) DEFI_EARNER {
        location: Philippines
        income_source: yield farming, trading profits, airdrops
        conversion_purpose: realize gains in local currency
        frequency: irregular
        size: varies widely
        economic_meaning: capital gains, not wage income
    }
    
    (D) BUSINESS_OPERATOR {
        location: Philippines or abroad
        income_source: cross-border business (exports, services)
        conversion_purpose: pay local suppliers/employees
        frequency: irregular, larger amounts
        size: $1000-$10000+
        economic_meaning: business revenue conversion
    }
    
    (E) SAVINGS_ROTATOR {
        location: Philippines
        income_source: none (converting existing savings)
        conversion_purpose: FX speculation or hedging
        frequency: irregular
        size: varies
        economic_meaning: portfolio allocation, NOT income
    }
}
```

---

## 2. Why This Matters for the Remittance Volatility Swap

The instrument is: Payoff ∝ Var(Net USDC → PUSO flow)

**If the flow is dominated by (A) Diaspora Remittance:**
- Variance is driven by host-country employment shocks (US recession, Gulf oil crash)
- The instrument hedges household income dependency on foreign labor markets
- Expected longs: Filipino fintech lenders, payment apps

**If the flow is dominated by (B) Remote Contractors:**
- Variance is driven by global demand for Filipino tech/BPO labor
- Still an income flow, still convertible to hedging instrument
- But the population is higher-income, crypto-native, less "underserved"
- Shocks: tech layoffs, AI displacement of BPO, crypto winter

**If the flow is mixed (A) + (B):**
- Both are USD-denominated income → PHP conversion
- Both contribute to Var(Net USDC → PUSO)
- The variance captures a BROADER income vulnerability than pure remittance
- This might be BETTER for the instrument — wider user base, more liquidity

**If (C), (D), (E) dominate:**
- The flow is not primarily income-driven
- Variance reflects speculation/business cycles, not household income
- The instrument would be mispriced as an income hedge

---

## 3. What the Philippines Demographic Data Says

Philippines is one of the largest sources of:
- **OFW (Overseas Filipino Workers)**: ~10M Filipinos abroad, ~$38B/year remittances
- **BPO/remote workers**: Philippines is #1 global BPO destination, ~1.3M workers
- **Freelancers paid in crypto**: Growing rapidly — Philippines ranked top 5 globally for crypto freelance payments (per Triple-A, Chainalysis reports)

The contractor population (B) is economically significant and growing:
- Platforms: Upwork, Fiverr, OnlineJobs.ph — many pay in USDC via crypto rails
- Average monthly income: $800-$3000 (higher than average OFW remittance)
- English proficiency: near-universal in this group
- Crypto literacy: high

The "underserved" population that lacks English/tech access:
- More likely to use traditional remittance channels (Western Union, GCash, bank transfer)
- Less likely to appear in on-chain data at all
- On-chain PUSO users are BIASED toward the tech-enabled population

---

## 4. Empirical Tests to Decompose the Population

### Test 1: Transaction Size Distribution
- Diaspora remittance: cluster $200-$1000 (monthly household support)
- Contractor pay: cluster $500-$5000 (biweekly/monthly invoices)  
- DeFi earner: bimodal (many small + occasional large)
- If we see a clear bimodal distribution with peaks at ~$500 and ~$2000, that suggests mixed (A) + (B)

### Test 2: Temporal Patterns
- Remittance: monthly periodicity, aligned to US/Gulf paydays (1st, 15th of month)
- Contractor: biweekly or monthly, may align to different pay cycles
- DeFi: no periodicity, event-driven
- Autocorrelation analysis of daily USDC→PUSO flow can reveal periodicity

### Test 3: Address Behavior Clustering
- Repeat addresses with consistent monthly amounts → likely (A) or (B)
- Addresses with irregular, varying amounts → likely (C), (D), or (E)
- Addresses that also interact with lending/yield protocols → likely (C)
- Addresses that only do USDC→PUSO and nothing else → likely (A) or (B)

### Test 4: Day-of-Week and Hour-of-Day Patterns
- Philippines-based users: active during PHT business hours (UTC+8)
- US-based diaspora: active during US hours (UTC-5 to UTC-8)
- Gulf-based diaspora: active during Gulf hours (UTC+3 to UTC+4)
- Can identify geographic concentration from temporal activity patterns

### Test 5: Cross-reference with GCash/Maya (if data available)
- GCash and Maya (PayMaya) are the dominant Filipino mobile wallets
- Some have crypto integration — if PUSO on-ramps/off-ramps through these, we may see patterns

---

## 5. Revised Framing for the Instrument

Instead of "remittance volatility swap" we may need to think of this as:

**USD-denominated income volatility swap for PHP-dependent households**

This captures BOTH:
- Diaspora remittance income (cross-border)
- Contractor/freelancer income (local but USD-denominated)

Both populations:
- Earn in USD
- Convert to PHP for daily expenses
- Are exposed to PHP/USD exchange rate risk
- Are exposed to income flow volatility (employment shocks, demand shocks)

The Var(Net USDC → PUSO) captures the aggregate volatility of this combined income flow.

---

## 6. What This Changes About the PRE_REQ

Original PRE_REQ: 
```
(Net USDT → FX) predicts (d household income from cross-border transfers)
```

Revised PRE_REQ should be:
```
(Net USDC → PUSO) predicts (d USD-denominated income converted to PHP)
```

This is a WEAKER claim (we don't restrict to cross-border) but a MORE DEFENSIBLE one. And it may be more useful — the contractor population is growing faster than traditional remittance and is more crypto-native (natural users of the instrument).

---

## 7. Open Decision for User

Should the instrument target:
- (a) Pure remittance flows (narrower, harder to isolate, more "underserved" narrative)
- (b) All USD→PHP income conversion (broader, easier to measure, includes contractors)
- (c) Let the data decide — run the decomposition tests first, then define the target population based on what we actually see

This is an economic judgment about who the instrument serves.
