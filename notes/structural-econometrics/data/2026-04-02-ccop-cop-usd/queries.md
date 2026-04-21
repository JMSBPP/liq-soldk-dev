# Dune SQL Queries: cCOP Residual Daily Flow

*Date: 2026-04-02*
*Spec: INCOME_SETTLEMENT/2026-04-02-ccop-cop-usd-flow-response.md*

---

## Query Registry

**QA FIX (M2)**: All queries were created with `is_temp: false` (permanent). They will persist on Dune indefinitely and are reproducible via the URLs below.

| ID | Name | Status | is_temp | URL |
|---|---|---|---|---|
| **#6941901** | **cCOP Residual Daily Flow v3 (PRIMARY)** | **COMPLETED** | **false** | [dune.com/queries/6941901](https://dune.com/queries/6941901) |
| #6941892 | Filter Address Lists v2 | COMPLETED | false | [dune.com/queries/6941892](https://dune.com/queries/6941892) |
| #6941902 | Diagnostic: Token Symbols | COMPLETED | false | [dune.com/queries/6941902](https://dune.com/queries/6941902) |
| #6941903 | Diagnostic: Filter Impact | COMPLETED | false | [dune.com/queries/6941903](https://dune.com/queries/6941903) |
| #6941906 | Diagnostic: Campaign Days | COMPLETED | false | [dune.com/queries/6941906](https://dune.com/queries/6941906) |
| #6941886 | Filter Addresses v1 (BROKEN) | FAILED | false | [dune.com/queries/6941886](https://dune.com/queries/6941886) |
| #6941889 | Daily Aggregation v1 (BROKEN) | FAILED | false | [dune.com/queries/6941889](https://dune.com/queries/6941889) |
| #6941894 | Daily Aggregation v2 (NOT IN pattern) | COMPLETED | false | [dune.com/queries/6941894](https://dune.com/queries/6941894) |

---

## PRIMARY QUERY: #6941901 — cCOP Residual Daily Flow v3

**Execution ID**: `01KN7SPR5JA3RCBTPVYJ1D29Q5`
**Rows**: ~499 daily observations (Oct 31 2024 - Apr 1 2026)
**Cost**: 7.09 credits

### SQL

```sql
-- cCOP Residual Daily Flow — Single-pass design
-- Pre-computes address filter flags, then joins once for aggregation

WITH address_stats AS (
    SELECT 
        "from" AS address,
        COUNT(*) AS total_txns,
        COUNT(DISTINCT "to") AS unique_counterparties,
        SUM(CASE WHEN day_of_week(block_time) = 4 THEN 1 ELSE 0 END) AS thursday_txns,
        MIN(CAST(block_time AS DATE)) AS first_date
    FROM stablecoins_multichain.transfers
    WHERE blockchain = 'celo'
      AND currency = 'COP'
      AND token_symbol IN ('cCOP', 'COPm')
      AND block_date >= DATE '2024-10-01'
    GROUP BY "from"
),

-- Identify campaign spike days (>50 new senders on same day)
campaign_days AS (
    SELECT first_date AS campaign_date
    FROM address_stats
    GROUP BY first_date
    HAVING COUNT(*) > 50
),

-- Flag addresses for exclusion
flagged_addresses AS (
    SELECT 
        a.address,
        CASE 
            WHEN a.total_txns >= 3 AND CAST(a.thursday_txns AS DOUBLE) / a.total_txns > 0.8 THEN 1
            ELSE 0
        END AS is_thursday_ubi,
        CASE 
            WHEN a.total_txns > 1000 AND a.unique_counterparties < 10 THEN 1
            ELSE 0
        END AS is_bot,
        CASE 
            WHEN c.campaign_date IS NOT NULL THEN 1
            ELSE 0
        END AS is_campaign
    FROM address_stats a
    LEFT JOIN campaign_days c ON a.first_date = c.campaign_date
),

-- Only keep addresses that pass all filters
clean_addresses AS (
    SELECT address
    FROM flagged_addresses
    WHERE is_thursday_ubi = 0 AND is_bot = 0 AND is_campaign = 0
)

SELECT 
    CAST(t.block_time AS DATE) AS day,
    SUM(t.amount_usd) AS gross_volume_usd,
    SUM(CASE WHEN t.amount_usd BETWEEN 200 AND 2000 THEN t.amount_usd ELSE 0 END) AS income_volume_usd,
    SUM(CASE WHEN t.amount_usd BETWEEN 1 AND 50 THEN t.amount_usd ELSE 0 END) AS small_volume_usd,
    SUM(CASE WHEN t.amount_usd > 2000 THEN t.amount_usd ELSE 0 END) AS whale_volume_usd,
    COUNT(*) AS total_transfers,
    SUM(CASE WHEN t.amount_usd BETWEEN 200 AND 2000 THEN 1 ELSE 0 END) AS income_count,
    COUNT(DISTINCT t."from") AS unique_senders,
    day_of_week(CAST(t.block_time AS DATE)) AS day_of_week,
    CASE WHEN DAY(CAST(t.block_time AS DATE)) = 15 
         OR CAST(t.block_time AS DATE) = LAST_DAY_OF_MONTH(CAST(t.block_time AS DATE)) 
         THEN 1 ELSE 0 END AS is_quincena,
    CASE WHEN day_of_week(CAST(t.block_time AS DATE)) = 4 THEN 1 ELSE 0 END AS is_thursday,
    CASE WHEN day_of_week(CAST(t.block_time AS DATE)) IN (6, 7) THEN 1 ELSE 0 END AS is_weekend
FROM stablecoins_multichain.transfers t
INNER JOIN clean_addresses ca ON t."from" = ca.address
WHERE t.blockchain = 'celo'
  AND t.currency = 'COP'
  AND t.token_symbol IN ('cCOP', 'COPm')
  AND t.block_date >= DATE '2024-10-01'
  AND t.amount_usd >= 1.0
  AND CAST(t.block_time AS DATE) NOT BETWEEN DATE '2025-07-07' AND DATE '2025-07-12'
GROUP BY CAST(t.block_time AS DATE)
ORDER BY CAST(t.block_time AS DATE)
```

### Filtering Definition (User-Approved)

```
cCOP_residual = stablecoins_multichain.transfers 
  WHERE blockchain = 'celo' AND currency = 'COP' AND token_symbol IN ('cCOP', 'COPm')
  MINUS thursday-only addresses (>80% of txns on Thursdays AND >=3 txns) — UBI
  MINUS bot addresses (>1000 txns AND <10 unique counterparties) 
  MINUS campaign spike addresses (first appeared on days with >50 new senders)
  MINUS dust (amount_usd < $1)
  MINUS hardfork window (block_date BETWEEN '2025-07-07' AND '2025-07-12')
```

### Token Scope

Only Mento tokens (cCOP + COPm). Excludes COPM (Minteo) per identification exercise:
- cCOP = old Mento token (227,536 transfers, 2024-10-31 to 2026-01-24)
- COPm = new Mento token after migration (55,222 transfers, 2026-01-25 to present)
- COPM = Minteo spending token (excluded — different economic function)

### Filter Impact Summary (Diagnostic #6941903)

| Filter | Addresses Flagged |
|---|---|
| Total unique senders | 4,990 |
| Thursday UBI | 588 (11.8%) |
| Bots | 26 (0.5%) |
| Campaign spike | 3,563 (71.4%) |
| **Clean (residual)** | **1,310 (26.3%)** |

Campaign days identified:
- 2025-02-19: 77 new senders
- 2025-05-23: 60 new senders
- 2025-07-30: 509 new senders (mass onboarding wave 1)
- 2025-07-31: 1,931 new senders (mass onboarding wave 1)
- 2025-08-13: 192 new senders (mass onboarding wave 2)
- 2025-08-14: 794 new senders (mass onboarding wave 2)

**NOTE**: The campaign filter removes 71% of addresses. This is by design — the July-August 2025 mass onboarding events brought in thousands of addresses that are campaign participants, not organic income converters. The Feb 19 and May 23 thresholds (77 and 60) are borderline. For sensitivity analysis S1 (no filter) vs S2 (current) vs S3 (tight), consider adjusting the campaign threshold.

---

## FILTER QUERY: #6941892 — Filter Address Lists v2

**Execution ID**: `01KN7SK8Y4C2K997QXN173CC6T`
**Rows**: 100 (all thursday_ubi; zero bots, zero campaign addresses returned)
**Note**: This query only outputs the filtered addresses. The campaign filter in the daily aggregation query uses a different pattern (INNER JOIN vs UNION ALL) so the filter addresses query shows only thursday_ubi addresses.

---

## How to Re-Execute

### Via Dune MCP:
```
executeQueryById(query_id=6941901, performance="medium")
```

### Via Dune API:
```bash
curl -X POST "https://api.dune.com/api/v1/query/6941901/execute" \
  -H "X-DUNE-API-KEY: $DUNE_API_KEY"
```

### To download results as CSV:
```bash
curl "https://api.dune.com/api/v1/query/6941901/results/csv" \
  -H "X-DUNE-API-KEY: $DUNE_API_KEY" \
  -o ccop_residual_daily.csv
```
