# cKES Behavioral Fingerprints: What the Data Actually Shows

*Date: 2026-04-02*
*Status: QUERIES WRITTEN -- awaiting Dune MCP execution*
*SQL file: CKES_BEHAVIORAL_QUERIES.sql (5 queries, all permanent, is_temp: false)*
*Dune queries: PENDING -- run via Dune MCP or paste into dune.com*

---

## 0. Context and Methodology

### Why cKES?

From CURRENCY_SELECTION.md (Dune queries #6939814, #6939820):
- cKES has **10,673 Mento broker swaps** (5,282 buy + 5,391 sell) with **~1,690 unique traders** -- comparable to PUSO
- **876,602 ERC-20 transfers** historically with $108.6M volume -- actually larger than PUSO's 147K transfers
- Post-migration token (KESm) has **154,763 transfers since Jan 25, 2026** with 49,980 in last 30d
- **Remittance-sized ratio: 67.5%** (591,964 of 876K transfers between $10-$2000)
- Kenya receives **$4.1B/yr in remittances** (World Bank 2023), 2.8% of GDP -- meaningful but not Philippines-scale (9.3% of GDP)

### Key question: Does cKES show more organic income-conversion behavior than PUSO?

PUSO was revealed as campaign-driven (July 2025 spike, no December seasonality, 83.7% occasional users, modal trade $10-50). If cKES shows:
- Steady growth without campaign spikes
- Transaction sizes clustering at $50-$500 (Kenya's typical remittance range)
- Timezone signature matching East Africa (UTC+3)
- Higher proportion of regular/returning users
- December or end-of-month seasonality

...then cKES is a stronger candidate for the remittance volatility swap.

### Token Details
- **cKES**: `0x456a3D042C0DbD3db53D5489e98dFb038553B0d0` (18 decimals)
- **cUSD**: `0x765DE816845861e75A25fCA122bb6898B8B1282a` (18 decimals)
- **Source table**: `mento_celo.Broker_evt_Swap`
- **USD sizing**: Uses cUSD side of each swap (amountIn or amountOut) divided by 1e18

### PUSO Comparison Baseline (from PUSO_BEHAVIORAL_FINGERPRINTS.md)
| Metric | PUSO Value |
|---|---|
| Total broker swaps | ~19,128 |
| Unique traders | ~2,818 |
| Modal trade bucket | $10-50 (50.8% of trades) |
| Median trade | ~$20 |
| Hourly peak (UTC) | 1-7 (9am-3pm PHT) |
| DoW anomaly | Thursday 56% of all trades |
| Monthly spike | July 2025 (9,142 trades, 1,617 new traders) |
| December seasonality | NONE |
| Power users (>50 trades) | 22 (0.8% of addresses, 77.6% of volume) |
| Regular users (3+ months) | 2 (0.07% of addresses) |
| One-shot users | 435 (15.4% of addresses) |
| Occasional users | 2,359 (83.7% of addresses) |

---

## 1. Transaction Size Distribution (Query #PENDING)

| Bucket | Trades | % Trades | Unique Traders | Avg Size | Median Size | % Volume |
|---|---|---|---|---|---|---|
| $0-10 | -- | -- | -- | -- | -- | -- |
| $10-50 | -- | -- | -- | -- | -- | -- |
| $50-100 | -- | -- | -- | -- | -- | -- |
| $100-200 | -- | -- | -- | -- | -- | -- |
| $200-500 | -- | -- | -- | -- | -- | -- |
| $500-1000 | -- | -- | -- | -- | -- | -- |
| $1000-2000 | -- | -- | -- | -- | -- | -- |
| $2000-5000 | -- | -- | -- | -- | -- | -- |
| $5000+ | -- | -- | -- | -- | -- | -- |

### What to look for (vs PUSO):
- **PUSO** had 50.8% of trades at $10-50, median ~$20. NOT consistent with remittance use.
- **Kenyan remittance signature** would show clustering at $50-$500 (average remittance to Kenya ~$200-$300/month per World Bank data).
- If cKES modal bucket is $50-200, that is far more consistent with income conversion.
- Volume concentration: PUSO had 57.4% of volume in $1000+ bucket (intermediary-dominated). Lower concentration here = more retail.

### Interpretation
[FILL AFTER QUERY EXECUTION]

---

## 2. Temporal Patterns (Query #PENDING)

### Hour of Day (UTC)

| UTC Hour | EAT Equivalent | Trades | Traders | Interpretation |
|---|---|---|---|---|
| 0 | 3am EAT | -- | -- | |
| 1 | 4am EAT | -- | -- | |
| 2 | 5am EAT | -- | -- | |
| 3 | 6am EAT | -- | -- | |
| 4 | 7am EAT | -- | -- | |
| 5 | 8am EAT | -- | -- | |
| 6 | 9am EAT | -- | -- | |
| 7 | 10am EAT | -- | -- | |
| 8 | 11am EAT | -- | -- | |
| 9 | 12pm EAT | -- | -- | |
| 10 | 1pm EAT | -- | -- | |
| 11 | 2pm EAT | -- | -- | |
| 12 | 3pm EAT | -- | -- | |
| 13 | 4pm EAT | -- | -- | |
| 14 | 5pm EAT | -- | -- | |
| 15 | 6pm EAT | -- | -- | |
| 16 | 7pm EAT | -- | -- | |
| 17 | 8pm EAT | -- | -- | |
| 18 | 9pm EAT | -- | -- | |
| 19 | 10pm EAT | -- | -- | |
| 20 | 11pm EAT | -- | -- | |
| 21 | 12am EAT | -- | -- | |
| 22 | 1am EAT | -- | -- | |
| 23 | 2am EAT | -- | -- | |

**Kenya timezone signature**: East Africa Time = UTC+3. Business hours peak expected at UTC 5-14 (8am-5pm EAT).
- PUSO showed strong PHT signature (UTC 1-7 peak = 9am-3pm PHT). Timezone alignment confirms local usage.
- If cKES peaks at UTC 5-14, users are Kenya-based (not US/UK diaspora).
- US East Coast diaspora would peak at UTC 12-21 (8am-4pm EST).
- UK diaspora would peak at UTC 8-17 (8am-5pm GMT).

### Day of Week

| Day | Trades | Traders | % of Total |
|---|---|---|---|
| Monday | -- | -- | -- |
| Tuesday | -- | -- | -- |
| Wednesday | -- | -- | -- |
| Thursday | -- | -- | -- |
| Friday | -- | -- | -- |
| Saturday | -- | -- | -- |
| Sunday | -- | -- | -- |

**What to look for**:
- PUSO had extreme Thursday anomaly (56% of trades). This screamed batch processing or campaign artifact.
- Organic income conversion would show relatively flat weekday distribution, possibly with Monday/Friday slight peaks (payday-adjacent).
- Strong weekend drop-off = business use. Flat weekend = personal use.

### Monthly Trend

| Month | Trades | Unique Traders | Phase |
|---|---|---|---|
| [2024 months] | -- | -- | -- |
| [2025 months] | -- | -- | -- |
| [2026 months] | -- | -- | -- |

**What to look for**:
- PUSO had no December seasonality (evidence AGAINST remittance use, since OFW remittances peak in December).
- Kenyan remittances peak in December (Christmas/year-end) and to some extent August (school fees).
- If cKES shows December peak relative to adjacent months, that is STRONG evidence for remittance-linked usage.
- Campaign spikes (like PUSO's July 2025) would indicate artificial growth.

### Interpretation
[FILL AFTER QUERY EXECUTION]

---

## 3. Daily Net Flow Time Series (Query #PENDING)

### Summary Statistics
| Metric | Value |
|---|---|
| Total days with activity | -- |
| Total gross inflow (cUSD to cKES) | -- |
| Total gross outflow (cKES to cUSD) | -- |
| Cumulative net flow | -- |
| Avg daily net flow | -- |
| Net flow standard deviation | -- |
| Buy/sell ratio | -- |

### What to look for:
- **Persistent net inflow** (more cUSD-to-cKES than reverse) = demand-side signal, consistent with income conversion (people converting USD earnings to local currency).
- **Balanced flow** = two-way market, could be trading/arb.
- **Net outflow** = people exiting cKES for cUSD, could be savings or capital flight.
- **Variance of net flow** is the key input for the variance swap. Higher variance with identifiable seasonal structure = viable instrument.

### Interpretation
[FILL AFTER QUERY EXECUTION]

---

## 4. Address Behavior Clustering (Query #PENDING)

| Class | Addresses | % Addresses | % Trades | % Volume | Avg Volume/User | Avg Trades | Avg Active Months |
|---|---|---|---|---|---|---|---|
| power_user (>50 trades) | -- | -- | -- | -- | -- | -- | -- |
| regular (3+ trades, 3+ months) | -- | -- | -- | -- | -- | -- | -- |
| occasional (2-10 trades) | -- | -- | -- | -- | -- | -- | -- |
| one_shot (1 trade) | -- | -- | -- | -- | -- | -- | -- |

### What to look for (vs PUSO):
- PUSO had **only 2 regular users** out of 2,818 total. This was damning evidence against sustained use.
- If cKES has >20 regular users (3+ trades across 3+ months), that represents meaningful habitual usage.
- PUSO power users (22) controlled 77.6% of volume. If cKES has lower power-user volume concentration, the market is more retail-driven.
- One-shot ratio: PUSO had 15.4%. Higher one-shot = more experimentation. Lower one-shot = more intentional usage.

### Interpretation
[FILL AFTER QUERY EXECUTION]

---

## 5. Spike Investigation - New vs Returning Traders (Query #PENDING)

### Days with >50 new traders
| Date | Total Traders | New | Returning | Retention Rate | 7d Retention |
|---|---|---|---|---|---|
| [FILL] | -- | -- | -- | -- | -- |

### What to look for:
- PUSO's July 2025 spike brought 1,617 new traders in one month, with almost no retention. Classic campaign artifact.
- If cKES has no single-day spike above 50 new traders, growth was organic.
- If spikes exist but retention is >20%, the campaign actually drove lasting adoption.
- Gradual daily new-trader counts (1-5/day consistently) = organic discovery, not campaign.

### Interpretation
[FILL AFTER QUERY EXECUTION]

---

## 6. Comparative Assessment: cKES vs PUSO

| Dimension | PUSO | cKES | Better for Variance Swap? |
|---|---|---|---|
| Total broker swaps | ~19,128 | ~10,673 | [FILL] |
| Unique traders | ~2,818 | ~1,690 | [FILL] |
| Modal trade size | $10-50 (micro) | [FILL] | [FILL] |
| Timezone signature | PHT confirmed | [FILL] | [FILL] |
| DoW distribution | Thursday 56% (anomalous) | [FILL] | [FILL] |
| December seasonality | NONE | [FILL] | [FILL] |
| Campaign spikes | July 2025 (1,617 new traders) | [FILL] | [FILL] |
| Regular users | 2 (0.07%) | [FILL] | [FILL] |
| Power user volume share | 77.6% | [FILL] | [FILL] |
| ERC-20 transfer volume | $44M / 147K transfers | $108.6M / 876K transfers | cKES larger |
| Post-migration activity | 12,233 transfers/30d | 49,980 transfers/30d | cKES 4x more active |

---

## 7. Implications for Variance Swap Design

### If cKES shows organic income-conversion behavior:
1. **Variance swap on cKES net flow** becomes the leading candidate instrument
2. **Settlement observable**: daily net flow through Mento broker (Query 1 time series)
3. **Variance estimation**: use realized variance of daily net flow, annualized
4. **Seasonality structure**: if December/August peaks exist, the variance swap has predictable term structure
5. **Next step**: formal identification strategy (Phase -1) for the variance swap parameters

### If cKES shows campaign-driven behavior similar to PUSO:
1. Both PHP and KES stablecoins on Mento are infrastructure proofs, not usage proofs
2. The variance swap needs a different underlying -- possibly FX rate directly, or wait for Mento V2 growth
3. Consider cCOP (Colombia) or cGHS (Ghana) as alternatives, though both have fewer broker swaps

### Independent of behavioral fingerprint:
- cKES has **4x more post-migration transfer activity** than PUSO (49,980 vs 12,233 per 30d)
- This suggests the broader Celo-Kenya ecosystem (MiniPay, Valora) drives more organic cKES usage than shows up in Mento broker swaps alone
- A more complete picture would also analyze KESm ERC-20 transfers (not just broker swaps)

---

## 8. Execution Instructions

The Dune MCP server was not available when this report was scaffolded. To complete it:

1. Connect the Dune MCP server to this Claude Code session
2. Create all 5 queries from `CKES_BEHAVIORAL_QUERIES.sql` using `mcp__dune__createDuneQuery` with `is_temp: false`
3. Execute each query using `mcp__dune__executeQueryById`
4. Retrieve results using `mcp__dune__getExecutionResults`
5. Fill in all [FILL] and -- placeholders in this report
6. Write final interpretation sections

### Query creation parameters:
| # | Name | Description |
|---|---|---|
| 1 | cKES Daily Net Flow Time Series (Mento Broker) | Daily inflow/outflow/net with trade counts and unique traders |
| 2 | cKES Transaction Size Distribution (Mento Broker) | USD-sized buckets with trade counts, volume, percentiles |
| 3 | cKES Temporal Patterns Combined (Mento Broker) | UNION ALL of hourly, day-of-week, monthly breakdowns |
| 4 | cKES Address Behavior Clustering (Mento Broker) | Per-trader stats classified into power/regular/occasional/one-shot |
| 5 | cKES Spike Investigation New vs Returning (Mento Broker) | Daily new vs returning traders with retention rates |

---

## Permanent Dune Queries

| # | Query ID | Description |
|---|---|---|
| 1 | PENDING | cKES Daily Net Flow Time Series |
| 2 | PENDING | cKES Transaction Size Distribution |
| 3 | PENDING | cKES Temporal Patterns Combined |
| 4 | PENDING | cKES Address Behavior Clustering |
| 5 | PENDING | cKES Spike Investigation New vs Returning |
