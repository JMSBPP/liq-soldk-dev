-- ============================================================
-- cCOP / COPM / COPm Behavioral Fingerprint Queries
-- Target: Colombian Peso stablecoins on Celo
-- cCOP (Mento): 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
-- COPM/COPm: from stablecoins_multichain.transfers where currency = 'COP'
-- All queries: is_temp = false, DuneSQL dialect
-- Date: 2026-04-02
-- ============================================================


-- ============================================================
-- QUERY 1: COP Tokens Mento Broker and DEX Check
-- Name: "COP Tokens Mento Broker and DEX Check (Celo)"
-- Purpose: Does cCOP exist in Mento Broker swaps? Where do COP tokens trade?
-- ============================================================
WITH mento_swaps AS (
    SELECT
        COUNT(*) AS total_swaps,
        COUNT(DISTINCT evt_tx_hash) AS unique_txs
    FROM mento_celo.Broker_evt_Swap
    WHERE tokenIn = 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
       OR tokenOut = 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
),
dex_cop AS (
    SELECT
        project,
        COUNT(*) AS trades,
        COUNT(DISTINCT tx_hash) AS unique_txs,
        COUNT(DISTINCT taker) AS unique_traders,
        SUM(amount_usd) AS total_usd_volume,
        MIN(block_date) AS first_trade,
        MAX(block_date) AS last_trade
    FROM dex.trades
    WHERE blockchain = 'celo'
      AND (
        token_bought_symbol LIKE '%COP%'
        OR token_sold_symbol LIKE '%COP%'
        OR token_bought_address = 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
        OR token_sold_address = 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
      )
    GROUP BY project
)
SELECT
    'mento_broker' AS source,
    'Mento Broker Swaps' AS detail,
    total_swaps AS count_val,
    unique_txs,
    CAST(NULL AS bigint) AS unique_traders,
    CAST(NULL AS double) AS total_usd_volume,
    CAST(NULL AS date) AS first_trade,
    CAST(NULL AS date) AS last_trade
FROM mento_swaps

UNION ALL

SELECT
    'dex_trades' AS source,
    project AS detail,
    trades AS count_val,
    unique_txs,
    unique_traders,
    total_usd_volume,
    first_trade,
    last_trade
FROM dex_cop
ORDER BY source, count_val DESC
;


-- ============================================================
-- QUERY 2: All COP Stablecoins Transfer Overview
-- Name: "COP Stablecoins Monthly Transfer Overview (Celo)"
-- Purpose: Monthly breakdown by token_symbol for all COP tokens
-- ============================================================
SELECT
    date_trunc('month', block_date) AS month,
    token_symbol,
    token_address,
    COUNT(*) AS transfer_count,
    COUNT(DISTINCT sender) AS unique_senders,
    COUNT(DISTINCT receiver) AS unique_receivers,
    SUM(amount_usd) AS total_usd_volume,
    AVG(amount_usd) AS avg_usd_per_transfer,
    APPROX_PERCENTILE(amount_usd, 0.5) AS median_usd_per_transfer
FROM stablecoins_multichain.transfers
WHERE blockchain = 'celo'
  AND currency = 'COP'
  AND block_date >= DATE '2024-01-01'
GROUP BY 1, 2, 3
ORDER BY 1, 4 DESC
;


-- ============================================================
-- QUERY 3: COP Transaction Size Distribution
-- Name: "COP Transaction Size Distribution (Celo)"
-- Purpose: Bucket analysis to identify remittance-sized transfers
-- ============================================================
SELECT
    CASE
        WHEN amount_usd < 10 THEN '01: $0-10'
        WHEN amount_usd < 50 THEN '02: $10-50'
        WHEN amount_usd < 100 THEN '03: $50-100'
        WHEN amount_usd < 200 THEN '04: $100-200'
        WHEN amount_usd < 500 THEN '05: $200-500'
        WHEN amount_usd < 1000 THEN '06: $500-1000'
        WHEN amount_usd < 2000 THEN '07: $1000-2000'
        WHEN amount_usd < 5000 THEN '08: $2000-5000'
        ELSE '09: $5000+'
    END AS size_bucket,
    token_symbol,
    COUNT(*) AS transfers,
    COUNT(DISTINCT sender) AS unique_senders,
    SUM(amount_usd) AS total_usd_volume,
    AVG(amount_usd) AS avg_usd,
    APPROX_PERCENTILE(amount_usd, 0.5) AS median_usd
FROM stablecoins_multichain.transfers
WHERE blockchain = 'celo'
  AND currency = 'COP'
  AND block_date >= DATE '2024-01-01'
  AND amount_usd > 0
GROUP BY 1, 2
ORDER BY 1, 2
;


-- ============================================================
-- QUERY 4: COP Temporal Patterns
-- Name: "COP Temporal Patterns - Hour/DOW/Month (Celo)"
-- Purpose: Identify Colombia (UTC-5) vs US timezone signatures
-- ============================================================

-- 4a: Hourly distribution
SELECT
    'hourly' AS granularity,
    CAST(hour(block_time) AS varchar) AS period,
    COUNT(*) AS transfers,
    COUNT(DISTINCT sender) AS unique_senders,
    SUM(amount_usd) AS total_usd_volume
FROM stablecoins_multichain.transfers
WHERE blockchain = 'celo'
  AND currency = 'COP'
  AND block_date >= DATE '2024-01-01'
GROUP BY 1, 2

UNION ALL

-- 4b: Day of week (1=Mon, 7=Sun)
SELECT
    'day_of_week' AS granularity,
    CAST(day_of_week(block_time) AS varchar) AS period,
    COUNT(*) AS transfers,
    COUNT(DISTINCT sender) AS unique_senders,
    SUM(amount_usd) AS total_usd_volume
FROM stablecoins_multichain.transfers
WHERE blockchain = 'celo'
  AND currency = 'COP'
  AND block_date >= DATE '2024-01-01'
GROUP BY 1, 2

UNION ALL

-- 4c: Monthly
SELECT
    'monthly' AS granularity,
    CAST(date_trunc('month', block_date) AS varchar) AS period,
    COUNT(*) AS transfers,
    COUNT(DISTINCT sender) AS unique_senders,
    SUM(amount_usd) AS total_usd_volume
FROM stablecoins_multichain.transfers
WHERE blockchain = 'celo'
  AND currency = 'COP'
  AND block_date >= DATE '2024-01-01'
GROUP BY 1, 2

ORDER BY granularity, period
;


-- ============================================================
-- QUERY 5: COP Address Clustering
-- Name: "COP Sender Clustering Analysis (Celo)"
-- Purpose: Classify senders by behavior pattern
-- ============================================================
WITH sender_stats AS (
    SELECT
        sender,
        COUNT(*) AS total_transfers,
        COUNT(DISTINCT date_trunc('month', block_date)) AS active_months,
        SUM(amount_usd) AS total_usd_volume,
        AVG(amount_usd) AS avg_transfer_usd,
        APPROX_PERCENTILE(amount_usd, 0.5) AS median_transfer_usd,
        MIN(block_date) AS first_transfer,
        MAX(block_date) AS last_transfer,
        COUNT(DISTINCT receiver) AS unique_receivers
    FROM stablecoins_multichain.transfers
    WHERE blockchain = 'celo'
      AND currency = 'COP'
      AND block_date >= DATE '2024-01-01'
    GROUP BY 1
)
SELECT
    CASE
        WHEN total_transfers >= 50 AND active_months >= 6 THEN 'power_user'
        WHEN total_transfers >= 10 AND active_months >= 3 THEN 'regular'
        WHEN total_transfers >= 3 THEN 'occasional'
        ELSE 'one_shot'
    END AS user_class,
    COUNT(*) AS num_senders,
    SUM(total_transfers) AS total_transfers,
    SUM(total_usd_volume) AS total_usd_volume,
    AVG(total_transfers) AS avg_transfers_per_sender,
    AVG(active_months) AS avg_active_months,
    AVG(avg_transfer_usd) AS avg_per_transfer_usd,
    AVG(unique_receivers) AS avg_unique_receivers
FROM sender_stats
GROUP BY 1
ORDER BY 1
;


-- ============================================================
-- QUERY 6: COP Spike Investigation
-- Name: "COP Daily New vs Returning Senders (Celo)"
-- Purpose: Detect mass onboarding events and organic growth
-- ============================================================
WITH first_seen AS (
    SELECT
        sender,
        MIN(block_date) AS first_date
    FROM stablecoins_multichain.transfers
    WHERE blockchain = 'celo'
      AND currency = 'COP'
    GROUP BY 1
),
daily_breakdown AS (
    SELECT
        t.block_date,
        COUNT(*) AS total_transfers,
        COUNT(DISTINCT t.sender) AS total_senders,
        COUNT(DISTINCT CASE WHEN t.block_date = f.first_date THEN t.sender END) AS new_senders,
        COUNT(DISTINCT CASE WHEN t.block_date > f.first_date THEN t.sender END) AS returning_senders,
        SUM(t.amount_usd) AS total_usd_volume
    FROM stablecoins_multichain.transfers t
    JOIN first_seen f ON t.sender = f.sender
    WHERE t.blockchain = 'celo'
      AND t.currency = 'COP'
      AND t.block_date >= DATE '2024-01-01'
    GROUP BY 1
)
SELECT
    block_date,
    total_transfers,
    total_senders,
    new_senders,
    returning_senders,
    CAST(new_senders AS double) / NULLIF(total_senders, 0) AS new_sender_ratio,
    total_usd_volume,
    -- Flag days with unusual new sender counts (>2x 7-day avg)
    CASE
        WHEN new_senders > 2.0 * AVG(new_senders) OVER (
            ORDER BY block_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) THEN 'SPIKE'
        ELSE 'normal'
    END AS onboarding_flag
FROM daily_breakdown
ORDER BY block_date
;


-- ============================================================
-- QUERY 7: COPM on DEX - Where Does It Trade?
-- Name: "COP Tokens DEX Trading Analysis (Celo)"
-- Purpose: Identify DEX venues, pairs, volume for COP tokens
-- ============================================================
SELECT
    project,
    project_contract_address,
    token_bought_symbol,
    token_sold_symbol,
    token_bought_address,
    token_sold_address,
    COUNT(*) AS trades,
    COUNT(DISTINCT tx_hash) AS unique_txs,
    COUNT(DISTINCT taker) AS unique_traders,
    SUM(amount_usd) AS total_usd_volume,
    AVG(amount_usd) AS avg_trade_usd,
    MIN(block_date) AS first_trade,
    MAX(block_date) AS last_trade
FROM dex.trades
WHERE blockchain = 'celo'
  AND (
    token_bought_symbol LIKE '%COP%'
    OR token_sold_symbol LIKE '%COP%'
    OR token_bought_address = 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
    OR token_sold_address = 0xC8604A749Ef02b530A8F3bDB5dDe498bE1AB528c
  )
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY trades DESC
;
