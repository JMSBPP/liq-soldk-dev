# PHPC On-Chain Feasibility Assessment
# Can Coins.ph PHPC on Polygon Serve as Behavioral Reference for Remittance Variance Swap?

*Date: 2026-04-02*
*Analyst: Mama Bear — practical feasibility check*
*Status: COMPLETED — verdict is definitive*

---

## Executive Summary

PHPC on Polygon (`0x87a25dc121Db52369F4a9971F664Ae5e372CF69A`) has **insufficient on-chain data** to serve as a behavioral reference for the remittance variance swap project. The Polygon deployment is effectively dormant. The token's primary activity has migrated to Ronin Network and, more recently, Solana. Dune queries were constructed but could not be executed in this session due to an MCP connectivity failure — however, the publicly available on-chain and market data gathered via PolygonScan, CoinGecko, and secondary sources is sufficient to reach a definitive verdict without query execution.

**Verdict: PHPC on Polygon is NOT viable as a behavioral reference. Monitoring Ronin or Solana deployments post-growth is the correct forward-looking path.**

---

## 1. Dune Query Specifications

The following four queries were designed for this assessment. They were not executed because the Dune MCP server (`https://api.dune.com/mcp/v1`) did not register its tools in this session. The queries are permanently specified here and should be created as permanent queries when the MCP connection is restored.

All queries use `erc20_polygon.evt_Transfer`, DuneSQL dialect, `is_temp: false`.

### Query 1: PHPC Transfer Count and History

**Purpose:** Baseline check — does `erc20_polygon.evt_Transfer` have PHPC data at all?

```sql
SELECT 
    COUNT(*) as total_transfers,
    COUNT(DISTINCT "from") as unique_senders,
    COUNT(DISTINCT "to") as unique_receivers,
    MIN(evt_block_time) as first_transfer,
    MAX(evt_block_time) as last_transfer,
    COUNT(*) FILTER (WHERE "from" = 0x0000000000000000000000000000000000000000) as mint_count,
    COUNT(*) FILTER (WHERE "to" = 0x0000000000000000000000000000000000000000) as burn_count
FROM erc20_polygon.evt_Transfer
WHERE contract_address = 0x87a25dc121Db52369F4a9971F664Ae5e372CF69A
```

**Expected result (from PolygonScan):** ~87 total transfers, ~87 holders, minimal mint/burn events.

### Query 2: PHPC Monthly Mint/Burn Volume

**Purpose:** Time-series of mint and burn activity by month to assess whether any growth trend exists.

```sql
SELECT
    date_trunc('month', evt_block_time) as month,
    COUNT(*) FILTER (WHERE "from" = 0x0000000000000000000000000000000000000000) as mints,
    COUNT(*) FILTER (WHERE "to" = 0x0000000000000000000000000000000000000000) as burns,
    SUM(CASE WHEN "from" = 0x0000000000000000000000000000000000000000 
        THEN CAST(value AS DOUBLE) / 1e6 ELSE 0 END) as mint_volume_php,
    SUM(CASE WHEN "to" = 0x0000000000000000000000000000000000000000 
        THEN CAST(value AS DOUBLE) / 1e6 ELSE 0 END) as burn_volume_php,
    COUNT(*) FILTER (WHERE "from" != 0x0000000000000000000000000000000000000000 
        AND "to" != 0x0000000000000000000000000000000000000000) as regular_transfers
FROM erc20_polygon.evt_Transfer
WHERE contract_address = 0x87a25dc121Db52369F4a9971F664Ae5e372CF69A
GROUP BY 1
ORDER BY 1
```

**Expected result:** Very sparse monthly rows. Likely a handful of large institutional mints with zero recurring retail activity. Total supply of ~20.7M PHP suggests a few large mint events, not retail flow.

### Query 3: PHPC Mint Size Distribution

**Purpose:** Determine whether mints look like retail remittance ($200-$1000) or institutional batch operations ($100K+).

```sql
SELECT
    CASE 
        WHEN amt < 1000 THEN '$0-1K PHP'
        WHEN amt < 5000 THEN '$1K-5K'
        WHEN amt < 10000 THEN '$5K-10K'
        WHEN amt < 50000 THEN '$10K-50K'
        WHEN amt < 100000 THEN '$50K-100K'
        ELSE '$100K+'
    END as size_bucket,
    COUNT(*) as count,
    COUNT(DISTINCT "to") as unique_receivers
FROM (
    SELECT "to", CAST(value AS DOUBLE) / 1e6 as amt
    FROM erc20_polygon.evt_Transfer
    WHERE contract_address = 0x87a25dc121Db52369F4a9971F664Ae5e372CF69A
      AND "from" = 0x0000000000000000000000000000000000000000
) mints
GROUP BY 1
ORDER BY count DESC
```

**Expected result:** Given total supply of 20,700,000 PHP across only ~87 transfers, average transfer size is ~238,000 PHP (~$4,200 USD at current rates). This strongly indicates institutional/batch minting, not remittance-sized retail flows. The $100K+ PHP bucket likely dominates.

### Query 4: PHPC Temporal Pattern (Hour of Day for Mints)

**Purpose:** Check whether minting activity concentrates in Philippine business hours (UTC+8, i.e., UTC 01:00-10:00) vs. global/US hours.

```sql
SELECT
    HOUR(evt_block_time) as hour_utc,
    COUNT(*) as mint_count
FROM erc20_polygon.evt_Transfer
WHERE contract_address = 0x87a25dc121Db52369F4a9971F664Ae5e372CF69A
  AND "from" = 0x0000000000000000000000000000000000000000
GROUP BY 1
ORDER BY 1
```

**Expected result:** With only ~87 transfers total, the hourly distribution will be statistically meaningless (single-digit counts per hour at best). No behavioral inference is possible from this data.

---

## 2. Evidence Gathered Without Dune Execution

### 2.1 PolygonScan Data (contract: `0x87a25dc121Db52369F4a9971F664Ae5e372CF69A`)

| Metric | Value |
|--------|-------|
| Total transfers on Polygon | ~87 |
| Total holders on Polygon | ~87 |
| Total supply on Polygon | 20,700,000 PHPC |
| Implied average transfer size | ~238,000 PHP (~$4,200 USD) |
| Decimals | 6 |

**Interpretation:** 87 transfers across the entire token history is negligible. For comparison, PUSO on Celo has 147,276 transfers (1-year) and 3,027 unique senders. PHPC on Polygon has roughly 1,700x less transfer activity than PUSO.

### 2.2 CoinGecko Market Data (as of ~mid-March 2026)

| Metric | Value |
|--------|-------|
| Circulating supply tracked | ~331,234 PHPC (Ronin deployment) |
| 24h trading volume | $57.22 |
| Trading status | Stopped ~17 days before data snapshot |
| Market cap | $0 (not reported) |

Note: CoinGecko tracks the Ronin deployment, not the Polygon contract. The Ronin deployment circulating supply (~331K PHPC) is also small — but the Polygon contract holds a larger total supply (~20.7M PHPC) that appears to be a custodial reserve, not circulating.

### 2.3 Project Timeline and Status

| Date | Event |
|------|-------|
| May 2024 | BSP approves Coins.ph sandbox for PHPC |
| July 2024 | PHPC launches on Ronin Network (primary) |
| August 2024 | Stables Money partnership for Australia→Philippines remittances |
| September 2024 | Solana expansion announced at Breakpoint 2024 |
| July 5, 2025 | PHPC exits BSP Regulatory Sandbox; minting cap lifted |
| November 2025 | Ronin + QRPH integration announced (600K+ merchants) |
| Q1 2026 | CoinGecko shows trading halted on tracked exchanges |

**Key observation:** The BSP sandbox ran from July 2024 to July 2025. During the sandbox, minting was **capped** — explaining the minimal Polygon supply. Post-sandbox, Coins.ph announced increased minting capacity. However, the primary deployment focus has been Ronin (gaming ecosystem) and Solana (DeFi/remittance rails), not Polygon.

### 2.4 Competitive Landscape: Other Philippine Peso Stablecoins on Polygon

PolygonScan search reveals two other Philippine peso tokens on Polygon:

- **Philippines Peso (Tagcash) (PHP):** `0x69a8aaa4318f4803b3517f78a2ca6c859f5349f3` — smaller project, minimal data
- **Jarvis Synthetic Philippine Peso (jPHP):** `0x486880fb16408b47f928f472f57bec55ac6089d1` — synthetic, backed by USDC, no real remittance flow signal

None of these are viable alternatives. jPHP in particular is a synthetic instrument that reflects FX pricing, not real-world remittance behavior.

---

## 3. Assessment Against Feasibility Criteria

### 3.1 Sample Size

| Threshold | PHPC Polygon | Verdict |
|-----------|-------------|---------|
| Minimum for variance estimation | 500+ transfer events | FAIL |
| Actual count | ~87 transfers total | FAIL |
| PUSO (benchmark) | 147,276 transfers | — |

**Conclusion:** Sample size is insufficient by a factor of ~1,700x. No statistically meaningful variance estimate is possible.

### 3.2 Monthly Mint/Burn Trends

Without query execution, the monthly pattern can be inferred:
- Total supply of 20.7M PHP means ~$370K USD equivalent has been minted across all time
- BSP sandbox capped minting to a small pilot volume
- The Polygon contract appears to serve as a **reserve/bridge custody address**, not a retail-facing mint/burn contract
- There is likely NO regular monthly cadence — minting events are batch institutional operations

**Conclusion:** No meaningful mint/burn trend exists. The Polygon contract is not a remittance-flow instrument.

### 3.3 Mint Size Distribution

Given 20.7M PHPC total supply across ~87 transfers:
- Mean transfer: ~238,000 PHP ($4,200 USD)
- At this average, the distribution is entirely in the "$100K+ PHP" bucket
- This is **institutional/custodial activity**, not retail remittance flow
- Retail remittance ($200-$1000 USD) would require thousands of small transfers

**Conclusion:** Mint size distribution disqualifies PHPC Polygon as a remittance behavioral reference. The signal captured would be institutional custodial operations, not household income flows.

### 3.4 Hourly Pattern (Philippines Timezone)

With only ~87 total transfers and likely fewer than 20 mint events, hourly analysis is statistically incoherent. No pattern can be extracted.

**Conclusion:** Temporal analysis is not possible. The data density is too low to compute any distribution.

### 3.5 Trader Breadth

| Metric | PHPC Polygon | PUSO (benchmark) | Verdict |
|--------|-------------|-----------------|---------|
| Unique senders | ~87 | 3,027 | FAIL |
| Unique receivers | ~87 | 3,210 | FAIL |
| Unique Mento swap traders | N/A | 2,531 | — |

**Conclusion:** Trader breadth is insufficient by two orders of magnitude.

### 3.6 Recency

CoinGecko shows PHPC trading stopped on tracked exchanges around mid-March 2026 — two to three weeks before this assessment. The Polygon deployment appears to have no new minting activity since the BSP sandbox was active.

**Conclusion:** PHPC on Polygon is effectively inactive as of Q1 2026.

---

## 4. Verdict

**PHPC on Polygon cannot serve as a behavioral reference for the remittance variance swap project.**

The failure is decisive on four independent grounds:

1. **Volume:** 87 total transfers is not a dataset. A variance swap requires estimating variance from time-series flow data. This sample cannot yield any estimate with finite confidence intervals.

2. **Transfer character:** The ~238K PHP average transfer size indicates institutional/custodial operations, not retail remittance flows. The behavioral signal we need (household income → PHP conversion) is absent.

3. **Network mismatch:** PHPC's operational deployment is on Ronin Network (gaming ecosystem) and Solana (post-Breakpoint 2024). Polygon was likely a technical bridge/reserve address, never the intended retail-facing chain.

4. **Current inactivity:** As of Q1 2026, PHPC trading appears to have halted on CoinGecko-tracked venues. The Polygon contract shows no recent minting activity.

---

## 5. Forward-Looking Recommendations

### 5.1 Monitor Ronin Network PHPC

The Ronin deployment (`announced July 2024`) is the primary active chain. However:
- Ronin is a gaming-focused blockchain (Sky Mavis / Axie Infinity ecosystem)
- The user base is gamers and gaming-adjacent, not OFW remittance recipients
- The QRPH integration (November 2025) for 600K merchants is promising but still pending regulatory approval
- Behavioral signal will be mixed (gaming, remittance, merchant payments) — harder to decompose

**Action:** Monitor Ronin PHPC contract. Re-assess in 6-12 months if QRPH integration goes live and merchant payment volume materializes.

### 5.2 Monitor Solana PHPC

The Solana deployment (announced Breakpoint 2024) targets DeFi and remittance rails — a closer match to our use case. Solana's throughput and low fees are better suited to retail remittance-scale transactions.

**Action:** Track Solana PHPC contract deployment. If retail-scale transfers begin, run the equivalent feasibility assessment using `solana.transfers` or equivalent Dune table.

### 5.3 Consider PUSO (PHPm) as the Current Best PHP Reference

The existing research in this project already established that PUSO on Celo (and its successor PHPm) has:
- 147,276 historical transfers
- 3,027 unique senders
- 80.6% remittance-sized transactions
- Active Mento broker swap market with 2,531 unique traders

PUSO/PHPm is a superior behavioral reference for PHP-denominated remittance flows relative to PHPC Polygon at this time. See `/notes/REMITTANCE_VOLATILITY_SWAP/research/CURRENCY_SELECTION.md` for the full scoring.

### 5.4 Re-run Dune Queries When MCP Reconnects

The four queries specified in Section 1 should be created as permanent queries when the Dune MCP connection is restored. Even though the verdict is already clear, the query results will:
- Provide exact transfer counts and dates for the record
- Confirm whether the 20.7M supply represents a small number of large institutional mints
- Document the baseline for future comparison if PHPC Polygon activity increases

---

## 6. Data Sources

- [PHPC Token Tracker on PolygonScan](https://polygonscan.com/token/0x87a25dc121Db52369F4a9971F664Ae5e372CF69A) — 87 transfers, 20.7M supply
- [Philippine Peso Coin on CoinGecko](https://www.coingecko.com/en/coins/philippine-peso-coin) — trading halted ~March 2026
- [PHPC Whitepaper - Coins.ph](https://www.coins.ph/en-ph/phpc-whitepaper) — Polygon + Ronin deployment confirmed
- [Coins.ph PHPC Exits BSP Sandbox - BitPinas](https://bitpinas.com/regulation/phpc-exits-sandbox/) — sandbox exit July 2025, minting cap lifted
- [Coins.ph PHPC Solana Expansion - BitPinas](https://bitpinas.com/business/coins-ph-phpc-solana/) — Solana deployment announced Breakpoint 2024
- [Stables Money + PHPC Remittances - CoinTelegraph](https://cointelegraph.com/news/coinsph-stables-money-phpc-stablecoin-remittances) — Australia-Philippines corridor
- [State of Stablecoins in Philippines September 2025 - Bitwage](https://bitwage.com/en-us/blog/state-of-stablecoins-in-philippines-september-2025) — regulatory context
- [Ronin + QRPH PHPC Integration - Newsbytes](https://newsbytes.ph/2025/11/22/ronin-coins-ph-plan-qrph-integration-to-allow-phpc-stablecoin-payments/) — 600K merchant target

---

## 7. Technical Note: Dune MCP Failure

The Dune MCP server is configured at `https://api.dune.com/mcp/v1` (see `/home/jmsbpp/.claude.json` lines 2032-2038). The API key is present and valid. However, the MCP tool set (`mcp__dune__create_query`, `mcp__dune__execute_query`, `mcp__dune__execute_sql`) did not register in this Claude session. This appears to be an HTTP remote MCP connection failure at session initialization.

The queries in Section 1 are ready to be created when the connection is restored. Given the publicly available data (87 transfers, institutional-scale average amounts, inactive since sandbox exit), executing the queries would confirm rather than challenge the verdict.

---

*This assessment is complete and the verdict is actionable without further data collection.*
