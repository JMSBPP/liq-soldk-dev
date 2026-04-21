# Currency Selection for Remittance Volatility Swap: Data-Driven Ranking

*Date: 2026-04-02*
*Source: Dune queries 6939814, 6939820 (permanent, verifiable)*

---

## Selection Criteria

A currency is viable for the first exercise if it scores well on ALL of:

1. **Sample Size** -- enough swap/transfer events to estimate variance
2. **Trader Breadth** -- many unique addresses (not 3 bots)
3. **Remittance Signal** -- high ratio of remittance-sized ($10-$2000) vs whale (>$10k) transfers
4. **Recency** -- active in last 30 days (not a dead market)
5. **Economic Significance** -- remittances matter for this country's households
6. **Directional Asymmetry** -- more flow one way than the other (suggests real use, not round-trip arb)

---

## Data: Mento Broker Swaps (Dune #6939814)

These are ON-CHAIN SWAPS through Mento's broker contract (the primary liquidity venue).

| Currency | Pair | Swaps (1yr) | Unique Traders | Days Active | Swaps Last 30d | Traders Last 30d |
|----------|------|-------------|----------------|-------------|----------------|------------------|
| **PUSO (PHP)** | cUSD→PUSO | 8,905 | 2,531 | 363 | 463 | 18 |
| **PUSO (PHP)** | PUSO→cUSD | 8,192 | 2,736 | 361 | 442 | 18 |
| **cREAL (BRL)** | cUSD→cREAL | 6,652 | 110 | 260 | 1,272 | 22 |
| **cREAL (BRL)** | cREAL→cUSD | 5,812 | 72 | 261 | 1,075 | 19 |
| **cKES (KES)** | cKES→cUSD | 5,391 | 1,692 | 351 | 44 | 2 |
| **cKES (KES)** | cUSD→cKES | 5,282 | 1,490 | 357 | 87 | 1 |
| **eXOF (XOF)** | eXOF→cUSD | 786 | 14 | 263 | 163 | 1 |
| **eXOF (XOF)** | cUSD→eXOF | 245 | 42 | 255 | 1 | 1 |
| **cNGN (NGN)** | -- | **ABSENT** | -- | -- | -- | -- |
| **cCOP (COP)** | -- | **ABSENT** | -- | -- | -- | -- |

NOTE: cNGN and cCOP have ZERO Mento broker swaps in the last year.

---

## Data: All Stablecoin Transfers on Celo (Dune #6939820)

Broader view including all ERC-20 transfers (not just swaps).

| Token | Currency | Transfers (1yr) | Unique Senders | Unique Receivers | USD Volume | Last 30d Transfers | Remittance-Sized | Whale-Sized | Remittance Ratio |
|-------|----------|-----------------|----------------|------------------|------------|-------------------|------------------|-------------|-----------------|
| cKES | KES | 876,602 | 2,595 | 2,849 | $108.6M | 0* | 591,964 | 2,786 | 67.5% |
| cGHS | GHS | 924,838 | 3,833 | 3,929 | $48.0M | 0* | 781,865 | 213 | 84.5% |
| PUSO | PHP | 147,276 | 3,027 | 3,210 | $44.0M | 0* | 118,748 | 231 | 80.6% |
| cCOP | COP | 173,931 | 4,533 | 5,903 | $31.0M | 0* | 118,848 | 66 | 68.3% |
| cREAL | BRL | 1,153,741 | 11,929 | 1,034 | $130.9M | 0* | 793,952 | 1,366 | 68.8% |
| eXOF | XOF | 521,810 | 355 | 407 | $34.9M | 0* | 357,958 | 36 | 68.6% |
| cZAR | ZAR | 60,974 | 146 | 185 | $71.8M | 0* | 41,477 | 2,463 | 68.0% |
| cNGN | NGN | 8,815 | 206 | 265 | $3.0M | 0* | 4,967 | 8 | 56.3% |
| BRLA | BRL | 1,235,128 | 195 | 217 | $1.41B | 41,379 | 656,523 | 7,315 | 53.2% |

*NOTE: cKES, cGHS, PUSO, cCOP, cREAL, eXOF, cZAR, cNGN all show 0 transfers in last 30d in the OLD token contracts. 
Mento migrated to NEW token contracts (KESm, GHSm, PHPm, COPm, etc.) around 2026-01-25.*

### Post-Migration Tokens (active NOW):

| Token | Currency | Transfers (since Jan 25) | Unique Senders | Last 30d Transfers | Last 30d USD Vol | Remittance-Sized |
|-------|----------|--------------------------|----------------|-------------------|------------------|------------------|
| KESm | KES | 154,763 | 177 | 49,980 | $2.39M | 41,223 (26.6%) |
| GHSm | GHS | 197,755 | 100 | 64,759 | $551K | 81,714 (41.3%) |
| PHPm | PHP | 50,403 | 96 | 12,233 | $1.41M | 31,587 (62.7%) |
| COPm | COP | 54,020 | 178 | 21,627 | $686K | 36,053 (66.7%) |
| XOFm | XOF | 91,715 | 72 | 33,278 | $833K | 18,642 (20.3%) |
| BRLm | BRL | 265,504 | 204 | 85,714 | $11.4M | 87,496 (33.0%) |
| NGNm | NGN | 1,570 | 58 | 750 | $191K | 634 (40.4%) |
| ZARm | ZAR | 3,827 | 44 | 579 | $614 | 1,263 (33.0%) |

---

## Composite Scoring

### Criterion 1: Sample Size (transfers + swaps, recent activity)

| Rank | Currency | Recent 30d Activity | Historical Depth |
|------|----------|-------------------|------------------|
| 1 | BRL (BRLm+BRLA) | 127,093 transfers | 1.2M+ historical |
| 2 | GHS (GHSm) | 64,759 transfers | 924K historical |
| 3 | KES (KESm) | 49,980 transfers | 876K historical |
| 4 | XOF (XOFm) | 33,278 transfers | 521K historical |
| 5 | COP (COPm+COPM) | 29,419 transfers | 269K historical |
| 6 | PHP (PHPm) | 12,233 transfers | 147K historical |
| 7 | NGN (NGNm) | 750 transfers | 10K historical |
| 8 | ZAR (ZARm) | 579 transfers | 64K historical |

### Criterion 2: Trader Breadth (unique senders + receivers)

| Rank | Currency | Unique Participants (old + new combined) |
|------|----------|----------------------------------------|
| 1 | COP | 5,903 receivers, 4,533 senders (old) + 245 new |
| 2 | GHS | 3,929 receivers, 3,833 senders (old) |
| 3 | PHP | 3,210 receivers, 3,027 senders (old) + 96 new |
| 4 | KES | 2,849 receivers, 2,595 senders (old) + 177 new |
| 5 | BRL | 11,929 senders but only 1,034 receivers (asymmetric!) |
| 6 | XOF | 407 receivers, 355 senders |
| 7 | NGN | 265 receivers, 206 senders |
| 8 | ZAR | 185 receivers, 146 senders |

### Criterion 3: Remittance Signal (% of transfers in $10-$2000 range)

| Rank | Currency | Remittance-Sized % | Whale % |
|------|----------|-------------------|---------|
| 1 | GHS (old) | 84.5% | 0.02% |
| 2 | PHP (old) | 80.6% | 0.16% |
| 3 | BRL (old cREAL) | 68.8% | 0.12% |
| 4 | COP (old) | 68.3% | 0.04% |
| 5 | KES (old) | 67.5% | 0.32% |
| 6 | PHP (new PHPm) | 62.7% | 0.12% |
| 7 | COP (new COPm) | 66.7% | 0.00% |
| 8 | NGN | 56.3% | 0.09% |

### Criterion 4: Economic Significance (Remittances as % GDP)

| Rank | Country | Remittances % GDP | Annual Remittance (est) |
|------|---------|------------------|------------------------|
| 1 | Philippines | ~10% | ~$38B |
| 2 | Ghana | ~5.3% | ~$4.5B |
| 3 | Nigeria | ~4.5% | ~$20B |
| 4 | Kenya | ~3.4% | ~$4B |
| 5 | Mexico | ~4.2% | ~$60B |
| 6 | Colombia | ~2.8% | ~$10B |
| 7 | West Africa (WAEMU) | varies | varies |
| 8 | Brazil | ~0.3% | ~$4B |
| 9 | South Africa | ~0.3% | ~$1B |

### Criterion 5: Directional Asymmetry (Mento broker swaps)

| Currency | cUSD→Local | Local→cUSD | Ratio | Interpretation |
|----------|-----------|-----------|-------|----------------|
| PUSO | 8,905 | 8,192 | 1.09 | Slight net inflow (remittance direction) |
| cKES | 5,282 | 5,391 | 0.98 | Nearly symmetric |
| cREAL | 6,652 | 5,812 | 1.14 | Net inflow |
| eXOF | 245 | 786 | 0.31 | Net OUTFLOW (capital flight?) |

---

## COMPOSITE RANKING

| Rank | Currency | Sample | Breadth | Remittance Signal | Econ Significance | Recency | VERDICT |
|------|----------|--------|---------|-------------------|-------------------|---------|---------|
| **1** | **KES (Kenya)** | HIGH (876K hist, 50K/30d new) | HIGH (2,595 senders) | 67.5% | 3.4% GDP | Active (KESm) | **BEST OVERALL** |
| **2** | **PHP (Philippines)** | MED (147K hist, 12K/30d new) | HIGH (3,027 senders) + **best Mento swap breadth (2,700)** | 80.6% | **10% GDP** | Active (PHPm) | **BEST ECONOMIC STORY** |
| **3** | **GHS (Ghana)** | HIGH (924K hist, 65K/30d new) | HIGH (3,833 senders) | **84.5%** | 5.3% GDP | Active (GHSm) | **BEST REMITTANCE SIGNAL** |
| 4 | COP (Colombia) | MED (269K hist, 29K/30d) | HIGHEST (5,903 receivers) | 68.3% | 2.8% GDP | Active (COPm+COPM) | Good all-around |
| 5 | BRL (Brazil) | HIGHEST volume | LOW breadth (195 senders new) | 53.2% | 0.3% GDP | Most active | Volume but not remittance |
| 6 | XOF (West Africa) | MED (521K hist) | LOW (355 senders) | 68.6% | varies | Active (XOFm) | Few participants |
| 7 | NGN (Nigeria) | **VERY LOW (10K total)** | LOW (206 senders) | 56.3% | 4.5% GDP | Barely active (750/30d) | **INSUFFICIENT DATA** |
| 8 | ZAR (South Africa) | LOW | LOW | 68% | 0.3% GDP | Nearly dead | Not viable |

---

## Recommendation (data-driven, subject to economic judgment)

**Top 3 candidates, each with different strengths:**

1. **KES (Kenya)**: Best balance of sample size, trader breadth, and recency. KESm has 50K transfers/month currently. 3.4% GDP remittance dependency is meaningful. The old cKES had 2,595 unique senders — real usage breadth. Mento broker swaps showed 1,692 unique traders.

2. **PHP (Philippines)**: Strongest economic case (10% GDP from remittances). Best Mento broker swap breadth (2,700 unique traders). 80.6% remittance-sized transfers. Lower total volume than KES but potentially cleaner signal.

3. **GHS (Ghana)**: Highest remittance signal purity (84.5% in $10-$2000 range, only 0.02% whale). 5.3% GDP from remittances. Massive transfer count but needs verification that this isn't bot activity (3,833 senders for 924K transfers = ~241 transfers per sender average).

**Eliminated:**
- **NGN (Nigeria)**: Despite being the original target country, the data is simply not there. 10K total transfers, 750/month, no Mento broker swaps. Cannot estimate variance from this.
- **BRL (Brazil)**: Highest volume but lowest remittance dependency (0.3% GDP), lowest remittance-sized ratio (53%), and concentrated in few senders. This is a trading/arbitrage market, not remittance.
- **ZAR (South Africa)**: Dead market.

---

## Open Decision

The user must decide: optimize for **data quality** (KES), **economic story** (PHP), or **signal purity** (GHS)?

This is an economic judgment, not a statistical one.
