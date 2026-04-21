# PUSO Behavioral Fingerprints: What the Data Actually Shows

*Date: 2026-04-02*
*Status: Phase 0 complete — results challenge initial hypothesis*
*Dune queries: #6939951, #6939952, #6939953, #6939954, #6939960 (all permanent)*

---

## 1. Transaction Size Distribution (Query #6939960)

| Bucket | Trades | % Trades | Unique Traders | Avg Size | % Volume |
|---|---|---|---|---|---|
| $0-10 | 2,394 | 12.5% | 389 | $2.09 | 0.2% |
| **$10-50** | **9,718** | **50.8%** | **2,104** | **$23.64** | 7.6% |
| $50-100 | 3,443 | 18.0% | 352 | $70.94 | 8.1% |
| $100-200 | 1,691 | 8.8% | 128 | $133.81 | 7.5% |
| $200-500 | 989 | 5.2% | 42 | $311.77 | 10.3% |
| $500-1000 | 380 | 2.0% | 27 | $701.82 | 8.9% |
| $1000-2000 | 247 | 1.3% | 24 | $1,365.37 | 11.2% |
| $2000-5000 | 196 | 1.0% | 16 | $2,956.07 | 19.3% |
| $5000+ | 70 | 0.4% | 11 | $11,557.73 | 26.9% |

**Median trade: ~$20. Modal bucket: $10-50 (50.8% of all trades).**

### Interpretation

The distribution is bimodal in VOLUME terms:
- Bulk of TRADES at $10-50 (micro-transactions, 2,104 unique traders)
- Bulk of VOLUME at $1000+ (high-value flows, ~50 traders, 57.4% of dollar volume)

This does NOT match the classic OFW remittance pattern ($200-$1000 monthly). 

Possible populations:
- **$10-50 cohort** (50.8% of trades, 2,104 traders): Micro-payment users, DeFi experimenters, possibly mobile top-ups or small purchases. Too small for income conversion.
- **$200-$2000 cohort** (8.5% of trades, ~70 traders): Possible income converters — freelancers or small remittances. This is the candidate remittance signal.
- **$2000+ cohort** (1.4% of trades, ~20 traders): Intermediaries, batch processors, or high-value contractors. Drives most volume.

---

## 2. Temporal Patterns (Query #6939953)

### Hour of Day (UTC)

| UTC Hour | PHT Equivalent | Trades | Traders | Interpretation |
|---|---|---|---|---|
| 0 | 8am PHT | 906 | 399 | Morning start |
| **1** | **9am PHT** | **1,718** | **563** | Business hours begin |
| **2** | **10am PHT** | **1,834** | **720** | **PEAK** |
| **3** | **11am PHT** | **1,521** | **550** | Morning active |
| **4** | **12pm PHT** | **1,685** | **559** | Lunch hour active |
| **5** | **1pm PHT** | **1,459** | **502** | Afternoon |
| **6** | **2pm PHT** | **1,433** | **504** | Afternoon |
| **7** | **3pm PHT** | **1,499** | **483** | Afternoon |
| 8 | 4pm PHT | 959 | 263 | Winding down |
| 9 | 5pm PHT | 727 | 131 | End of business |
| 10-22 | Evening/night PHT | 240-565 | 39-119 | Low activity |
| 23 | 7am PHT | 609 | 278 | Early birds |

**Strong Philippines timezone signature: UTC 1-7 (9am-3pm PHT) accounts for ~58% of all trades.**

This is NOT US-based diaspora activity (which would peak at UTC 13-21 / 8am-4pm EST). The traders are Philippines-based.

### Day of Week

| Day | Trades | Traders | % of Total |
|---|---|---|---|
| Monday | 1,541 | 75 | 8.1% |
| Tuesday | 1,328 | 102 | 6.9% |
| **Wednesday** | **3,111** | **785** | **16.3%** |
| **Thursday** | **10,728** | **2,287** | **56.1%** |
| Friday | 1,498 | 72 | 7.8% |
| Saturday | 418 | 56 | 2.2% |
| Sunday | 505 | 57 | 2.6% |

**Thursday dominates with 56% of all trades and 2,287 unique traders.** This is anomalous and needs investigation:
- Could be a specific batch processing day for a Celo ecosystem partner
- Could be a community event / campaign day
- Could be Mento's own liquidity operations
- The spike in unique traders (2,287 on Thursday vs. ~75 on Monday) suggests coordinated activity, not organic use

### Monthly Trend

| Month | Trades | Unique Traders | Phase |
|---|---|---|---|
| Sep 2024 | 10 | 6 | Launch |
| Oct 2024 | 580 | 13 | Early |
| Nov 2024 | 119 | 7 | Quiet |
| Dec 2024 | 378 | 9 | No Christmas spike |
| Jan 2025 | 243 | 4 | Low |
| Feb 2025 | 515 | 12 | |
| Mar 2025 | 182 | 7 | |
| Apr 2025 | 288 | 7 | |
| May 2025 | 168 | 7 | |
| Jun 2025 | 239 | 8 | |
| **Jul 2025** | **9,142** | **1,617** | **Explosive spike** |
| **Aug 2025** | **2,699** | **1,086** | **Still elevated** |
| Sep 2025 | 419 | 47 | GCash USDC launch month |
| Oct 2025 | 390 | 20 | Post-GCash collapse |
| Nov 2025 | 536 | 21 | |
| Dec 2025 | 608 | 24 | **No Christmas spike** |
| Jan 2026 | 607 | 14 | |
| Feb 2026 | 980 | 13 | |
| Mar 2026 | 971 | 22 | Stable low |

Key observations:
- **No December seasonality**: OFW remittances peak in December (BSP data). PUSO shows no December effect. This is evidence AGAINST remittance use.
- **July 2025 spike**: 1,617 unique traders in one month, then collapse. Likely a Celo ecosystem campaign or airdrop, not organic growth.
- **Post-September 2025**: Stable at ~600-1000 trades/month with only 13-24 traders. The market settled to a small core of regular users.

---

## 3. Address Clustering (Query #6939954)

| Class | Addresses | % Addresses | % Trades | % Volume |
|---|---|---|---|---|
| Occasional (2-10 trades) | 2,359 | 83.7% | 47.6% | 15.4% |
| Power user (>50 trades) | 22 | 0.8% | 40.0% | 77.6% |
| One-shot (1 trade) | 435 | 15.4% | 12.2% | 6.8% |
| Regular (3+ trades, 3+ months) | 2 | 0.07% | 0.1% | 0.2% |

- **83.7% occasional**: Tried PUSO a few times, didn't return. Consistent with campaign-driven acquisition.
- **22 power users**: 77.6% of volume. These are the real market — intermediaries, bots, or committed users.
- **Only 2 regular users**: Almost nobody uses PUSO consistently across multiple months.

---

## 4. Honest Assessment

### What the data tells us PUSO IS:
- A Celo community experiment with ~2,800 addresses that tried it
- Philippines-timezone users making $10-50 micro-transactions
- Dominated by 22 power users controlling 77.6% of volume
- Subject to campaign-driven spikes (July 2025) followed by collapse
- A market of ~20 active traders post-stabilization

### What the data tells us PUSO is NOT:
- A remittance corridor (no $200-$1000 clustering, no December seasonality)
- A freelancer income conversion tool (median $20 is too small)
- A growing or sustainable market (post-spike trajectory is flat at low levels)
- Representative of the broader Filipino income-conversion population

### The $200+ segment
989 trades at $200-$500, 380 at $500-$1000, 247 at $1000-$2000 — totaling 1,616 trades from ~70 traders. This segment COULD contain income conversion activity, but:
- 70 traders is too small for statistical inference
- We can't separate income conversion from DeFi activity at this size
- The July 2025 spike likely inflates this segment too

---

## 5. Implications for the Variance Swap Project

### The interpolation strategy is CHALLENGED:
- PUSO behavioral fingerprints do NOT match expected remittance/income patterns
- Calibrating PUSO against BSP remittance seasonality would likely show NO correlation (no December peak)
- The KS test comparing PUSO tx sizes to hypothetical remittance distribution will reject

### PHPC is also dead:
- 87 transfers on Polygon, effectively dormant
- Primary activity on Ronin (gaming) — not remittance-oriented
- Cannot serve as behavioral reference

### Options:
1. **Acknowledge PUSO as proof-of-infrastructure, not proof-of-usage**: The CFMM observables exist (Uniswap v3 Celo), the Mento broker works, the data pipeline is queryable. But the user population doesn't match the target use case yet.
2. **Investigate cKES or cCOP instead**: May have different size distributions that better match remittance patterns.
3. **Wait for Ronin/Solana PHPC growth**: If Coins.ph's QRPH integration brings 600K merchants, PHPC on Ronin could become viable in 6-12 months.
4. **Pivot to pure FX-rate based settlement**: Abandon income-flow proxy, use PHP/USD exchange rate directly. Loses the Shiller income-claim framing but gains data quality.

---

## Permanent Dune Queries

| # | Query ID | Description |
|---|---|---|
| 1 | #6939951 | PUSO Daily Net Flow Time Series |
| 2 | #6939960 | PUSO Transaction Size Distribution (FIXED, 18 decimals) |
| 3 | #6939953 | PUSO Temporal Patterns (Hour + DoW + Monthly) |
| 4 | #6939954 | PUSO Address Behavior Clustering |
| 5 | #6939952 | PUSO Transaction Size Distribution (BROKEN, 6 decimal assumption) |
