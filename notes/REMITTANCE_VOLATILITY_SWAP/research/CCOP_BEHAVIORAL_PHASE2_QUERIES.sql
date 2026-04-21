-- ============================================================
-- cCOP Behavioral Fingerprints Phase 2: Remaining 4 Queries
-- Target: Colombian Peso stablecoins on Celo
-- Source: stablecoins_multichain.transfers (currency = 'COP') + dex.trades
-- All queries: is_temp = false, DuneSQL dialect
-- Date: 2026-04-02
-- Prior queries: #6939996 (size distribution), #6939997 (temporal patterns)
-- ============================================================


-- ============================================================
-- QUERY P2-1: cCOP Address Clustering
-- Name: "cCOP Address Clustering - User Classification (Celo)"
-- is_temp: false
-- Purpose: Classify 4,533 cCOP senders into power/regular/occasional/one-shot
-- Key question: How many of the 4,533 senders are regular users?
-- ============================================================
WITH sender_stats AS (
  SELECT
    "from" as sender,
    token_symbol,
    COUNT(*) as total_transfers,
    COUNT(DISTINCT date_trunc('month', block_time)) as active_months,
    COUNT(DISTINCT block_date) as active_days,
    SUM(amount_usd) as total_volume_usd,
    AVG(amount_usd) as avg_transfer_usd,
    MIN(block_time) as first_transfer,
    MAX(block_time) as last_transfer
  FROM stablecoins_multichain.transfers
  WHERE blockchain = 'celo' AND currency = 'COP'
    AND block_date >= DATE '2024-01-01'
  GROUP BY 1, 2
),
classified AS (
  SELECT *,
    CASE
      WHEN total_transfers > 50 THEN 'power_user'
      WHEN total_transfers >= 3 AND active_months >= 3 THEN 'regular'
      WHEN total_transfers BETWEEN 2 AND 10 THEN 'occasional'
      ELSE 'one_shot'
    END AS user_class
  FROM sender_stats
)
SELECT
  token_symbol, user_class,
  COUNT(*) as address_count,
  SUM(total_transfers) as total_transfers,
  ROUND(AVG(total_transfers), 1) as avg_transfers_per_user,
  ROUND(AVG(total_volume_usd), 2) as avg_volume_per_user,
  ROUND(SUM(total_volume_usd), 2) as total_volume_usd,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY token_symbol), 2) as pct_of_addresses,
  ROUND(100.0 * SUM(total_transfers) / SUM(SUM(total_transfers)) OVER (PARTITION BY token_symbol), 2) as pct_of_transfers
FROM classified
GROUP BY 1, 2
ORDER BY 1, total_transfers DESC
;


-- ============================================================
-- QUERY P2-2: cCOP Spike Investigation
-- Name: "cCOP Daily Spike Investigation - New vs Returning (Celo)"
-- is_temp: false
-- Purpose: Detect July 2025 campaign contamination + organic growth patterns
-- Key question: Does cCOP share the PUSO/cKES July 2025 spike?
-- ============================================================
WITH all_cop AS (
  SELECT "from" as sender, block_time, block_date, amount_usd, token_symbol
  FROM stablecoins_multichain.transfers
  WHERE blockchain = 'celo' AND currency = 'COP'
    AND block_date >= DATE '2024-01-01'
),
first_seen AS (
  SELECT sender, MIN(block_date) as first_day FROM all_cop GROUP BY 1
),
daily AS (
  SELECT
    a.block_date as day,
    a.token_symbol,
    COUNT(*) as transfers,
    COUNT(DISTINCT a.sender) as unique_senders,
    COUNT(DISTINCT CASE WHEN f.first_day = a.block_date THEN a.sender END) as new_senders,
    COUNT(DISTINCT CASE WHEN f.first_day < a.block_date THEN a.sender END) as returning_senders,
    ROUND(AVG(a.amount_usd), 2) as avg_size,
    ROUND(APPROX_PERCENTILE(a.amount_usd, 0.5), 2) as median_size
  FROM all_cop a
  JOIN first_seen f ON a.sender = f.sender
  GROUP BY 1, 2
  HAVING COUNT(*) > 100
)
SELECT * FROM daily ORDER BY day
;


-- ============================================================
-- QUERY P2-3: COPM on DEX - Where Does It Trade?
-- Name: "COP Tokens DEX Trading Venues (Celo)"
-- is_temp: false
-- Purpose: Identify CFMM pools where COPM trades
-- Key question: Are there any DEX pools with COP tokens?
-- ============================================================
SELECT
  project as venue,
  token_bought_symbol, token_sold_symbol,
  COUNT(*) as trade_count,
  COUNT(DISTINCT taker) as unique_takers,
  SUM(amount_usd) as total_volume_usd,
  MIN(block_time) as first_trade,
  MAX(block_time) as last_trade,
  COUNT(*) FILTER (WHERE block_time >= NOW() - INTERVAL '30' DAY) as trades_last_30d
FROM dex.trades
WHERE blockchain = 'celo'
  AND block_date >= DATE '2024-01-01'
  AND (token_bought_symbol LIKE '%COP%' OR token_sold_symbol LIKE '%COP%')
GROUP BY 1, 2, 3
ORDER BY trade_count DESC
;


-- ============================================================
-- QUERY P2-4: cCOP Monthly Overview with Seasonality
-- Name: "cCOP Monthly Overview with Income Seasonality (Celo)"
-- is_temp: false
-- Purpose: Monthly breakdown with income-sized transfer ratio
-- Key question: Any monthly seasonality (December, end-of-quarter)?
-- ============================================================
SELECT
  token_symbol,
  date_trunc('month', block_time) as month,
  COUNT(*) as transfers,
  COUNT(DISTINCT "from") as unique_senders,
  COUNT(DISTINCT "to") as unique_receivers,
  SUM(amount_usd) as total_usd_volume,
  COUNT(*) FILTER (WHERE amount_usd BETWEEN 100 AND 2000) as income_sized,
  ROUND(100.0 * COUNT(*) FILTER (WHERE amount_usd BETWEEN 100 AND 2000) / COUNT(*), 2) as income_pct
FROM stablecoins_multichain.transfers
WHERE blockchain = 'celo' AND currency = 'COP'
  AND block_date >= DATE '2024-01-01'
GROUP BY 1, 2
ORDER BY 1, 2
;
