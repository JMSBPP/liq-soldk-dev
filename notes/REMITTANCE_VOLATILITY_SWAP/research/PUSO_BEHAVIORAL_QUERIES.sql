-- ============================================================
-- PUSO Behavioral Fingerprint Queries
-- All queries target: mento_celo.Broker_evt_Swap
-- PUSO: 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
-- cUSD: 0x765DE816845861e75A25fCA122bb6898B8B1282a
-- All queries: is_temp = false, DuneSQL dialect
-- ============================================================

-- ============================================================
-- QUERY 1: PUSO Daily Net Flow Time Series
-- Name: "PUSO Daily Net Flow Time Series (Mento Broker)"
-- ============================================================
SELECT
  date_trunc('day', evt_block_time) AS trade_date,
  SUM(CASE WHEN tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    THEN CAST(amountOut AS double) / 1e18 ELSE 0 END) AS gross_inflow_puso,
  SUM(CASE WHEN tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    THEN CAST(amountIn AS double) / 1e18 ELSE 0 END) AS gross_outflow_puso,
  SUM(CASE WHEN tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    THEN CAST(amountOut AS double) / 1e18 ELSE 0 END)
  - SUM(CASE WHEN tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    THEN CAST(amountIn AS double) / 1e18 ELSE 0 END) AS net_flow_puso,
  COUNT(CASE WHEN tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B THEN 1 END) AS trade_count_buy,
  COUNT(CASE WHEN tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B THEN 1 END) AS trade_count_sell,
  COUNT(DISTINCT trader) AS unique_traders
FROM mento_celo.Broker_evt_Swap
WHERE (
  tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
)
AND evt_block_time >= TIMESTAMP '2024-09-01'
GROUP BY 1
ORDER BY 1
;


-- ============================================================
-- QUERY 2: PUSO Transaction Size Distribution
-- Name: "PUSO Transaction Size Distribution (Mento Broker)"
-- ============================================================
WITH puso_swaps AS (
  SELECT
    trader,
    evt_block_time,
    -- Get the cUSD side amount for USD sizing
    -- cUSD has 6 decimals
    CASE
      WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountIn AS double) / 1e6
      WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountOut AS double) / 1e6
      ELSE 0
    END AS trade_size_usd
  FROM mento_celo.Broker_evt_Swap
  WHERE (
    tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  )
  AND evt_block_time >= TIMESTAMP '2024-09-01'
),
bucketed AS (
  SELECT
    *,
    CASE
      WHEN trade_size_usd < 10 THEN '01_$0-10'
      WHEN trade_size_usd < 50 THEN '02_$10-50'
      WHEN trade_size_usd < 100 THEN '03_$50-100'
      WHEN trade_size_usd < 200 THEN '04_$100-200'
      WHEN trade_size_usd < 500 THEN '05_$200-500'
      WHEN trade_size_usd < 1000 THEN '06_$500-1000'
      WHEN trade_size_usd < 2000 THEN '07_$1000-2000'
      WHEN trade_size_usd < 5000 THEN '08_$2000-5000'
      ELSE '09_$5000+'
    END AS size_bucket
  FROM puso_swaps
)
SELECT
  size_bucket,
  COUNT(*) AS trade_count,
  COUNT(DISTINCT trader) AS unique_traders,
  SUM(trade_size_usd) AS total_volume_usd,
  AVG(trade_size_usd) AS avg_size_usd
FROM bucketed
GROUP BY 1
ORDER BY 1
;

-- Percentiles subquery (run separately or as UNION)
-- Name: "PUSO Trade Size Percentiles (Mento Broker)"
SELECT
  COUNT(*) AS total_trades,
  AVG(trade_size_usd) AS mean_usd,
  approx_percentile(trade_size_usd, 0.25) AS p25_usd,
  approx_percentile(trade_size_usd, 0.50) AS median_usd,
  approx_percentile(trade_size_usd, 0.75) AS p75_usd,
  approx_percentile(trade_size_usd, 0.90) AS p90_usd,
  approx_percentile(trade_size_usd, 0.99) AS p99_usd,
  MIN(trade_size_usd) AS min_usd,
  MAX(trade_size_usd) AS max_usd
FROM (
  SELECT
    CASE
      WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountIn AS double) / 1e6
      WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountOut AS double) / 1e6
      ELSE 0
    END AS trade_size_usd
  FROM mento_celo.Broker_evt_Swap
  WHERE (
    tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  )
  AND evt_block_time >= TIMESTAMP '2024-09-01'
)
;


-- ============================================================
-- QUERY 3: PUSO Temporal Patterns - Hour of Day
-- Name: "PUSO Hourly Trading Pattern (Mento Broker)"
-- ============================================================
SELECT
  hour(evt_block_time) AS hour_utc,
  COUNT(*) AS trade_count,
  COUNT(DISTINCT trader) AS unique_traders,
  SUM(
    CASE
      WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountIn AS double) / 1e6
      WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountOut AS double) / 1e6
      ELSE 0
    END
  ) AS total_volume_usd,
  -- Philippine time = UTC+8
  -- hour_utc 0 = PH 8am, hour_utc 8 = PH 4pm, etc.
  CASE
    WHEN hour(evt_block_time) BETWEEN 22 AND 23 THEN 'PH morning (6-8am)'
    WHEN hour(evt_block_time) BETWEEN 0 AND 3 THEN 'PH morning-midday (8am-12pm)'
    WHEN hour(evt_block_time) BETWEEN 4 AND 7 THEN 'PH afternoon (12-4pm)'
    WHEN hour(evt_block_time) BETWEEN 8 AND 11 THEN 'PH evening (4-8pm)'
    WHEN hour(evt_block_time) BETWEEN 12 AND 15 THEN 'PH night (8pm-12am)'
    WHEN hour(evt_block_time) BETWEEN 16 AND 21 THEN 'PH sleeping (12am-6am)'
    ELSE 'other'
  END AS ph_period
FROM mento_celo.Broker_evt_Swap
WHERE (
  tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
)
AND evt_block_time >= TIMESTAMP '2024-09-01'
GROUP BY 1, 5
ORDER BY 1
;


-- ============================================================
-- QUERY 4: PUSO Temporal Patterns - Day of Week
-- Name: "PUSO Day-of-Week Pattern (Mento Broker)"
-- ============================================================
SELECT
  day_of_week(evt_block_time) AS dow_number,
  CASE day_of_week(evt_block_time)
    WHEN 1 THEN 'Monday'
    WHEN 2 THEN 'Tuesday'
    WHEN 3 THEN 'Wednesday'
    WHEN 4 THEN 'Thursday'
    WHEN 5 THEN 'Friday'
    WHEN 6 THEN 'Saturday'
    WHEN 7 THEN 'Sunday'
  END AS day_name,
  COUNT(*) AS trade_count,
  COUNT(DISTINCT trader) AS unique_traders,
  SUM(
    CASE
      WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountIn AS double) / 1e6
      WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountOut AS double) / 1e6
      ELSE 0
    END
  ) AS total_volume_usd,
  AVG(
    CASE
      WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountIn AS double) / 1e6
      WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountOut AS double) / 1e6
      ELSE 0
    END
  ) AS avg_trade_size_usd
FROM mento_celo.Broker_evt_Swap
WHERE (
  tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
)
AND evt_block_time >= TIMESTAMP '2024-09-01'
GROUP BY 1, 2
ORDER BY 1
;


-- ============================================================
-- QUERY 5: PUSO Monthly Seasonality
-- Name: "PUSO Monthly Seasonality (Mento Broker)"
-- ============================================================
SELECT
  date_trunc('month', evt_block_time) AS month,
  COUNT(*) AS total_trades,
  COUNT(DISTINCT trader) AS unique_traders,
  SUM(
    CASE
      WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountIn AS double) / 1e6
      WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
        THEN CAST(amountOut AS double) / 1e6
      ELSE 0
    END
  ) AS gross_volume_usd,
  SUM(CASE WHEN tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    THEN CAST(amountOut AS double) / 1e18 ELSE 0 END)
  - SUM(CASE WHEN tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    THEN CAST(amountIn AS double) / 1e18 ELSE 0 END) AS net_flow_puso,
  COUNT(CASE WHEN tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B THEN 1 END) AS buy_count,
  COUNT(CASE WHEN tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B THEN 1 END) AS sell_count,
  COUNT(DISTINCT date_trunc('day', evt_block_time)) AS active_days
FROM mento_celo.Broker_evt_Swap
WHERE (
  tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
)
AND evt_block_time >= TIMESTAMP '2024-09-01'
GROUP BY 1
ORDER BY 1
;


-- ============================================================
-- QUERY 6: PUSO Address Behavior Clustering
-- Name: "PUSO Address Behavior Clustering (Mento Broker)"
-- ============================================================
WITH per_trader AS (
  SELECT
    trader,
    COUNT(*) AS total_trades,
    COUNT(DISTINCT date_trunc('day', evt_block_time)) AS distinct_days,
    COUNT(DISTINCT date_trunc('month', evt_block_time)) AS distinct_months,
    SUM(
      CASE
        WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountIn AS double) / 1e6
        WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountOut AS double) / 1e6
        ELSE 0
      END
    ) AS total_volume_usd,
    AVG(
      CASE
        WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountIn AS double) / 1e6
        WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountOut AS double) / 1e6
        ELSE 0
      END
    ) AS avg_trade_size_usd,
    MIN(evt_block_time) AS first_trade,
    MAX(evt_block_time) AS last_trade
  FROM mento_celo.Broker_evt_Swap
  WHERE (
    tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  )
  AND evt_block_time >= TIMESTAMP '2024-09-01'
  GROUP BY 1
),
classified AS (
  SELECT
    *,
    CASE
      WHEN total_trades > 50 THEN 'power_user'
      WHEN total_trades >= 3 AND distinct_months >= 3 THEN 'regular'
      WHEN total_trades BETWEEN 2 AND 10 AND distinct_months <= 2 THEN 'occasional'
      WHEN total_trades = 1 THEN 'one_shot'
      ELSE 'other'
    END AS user_category
  FROM per_trader
)
SELECT
  user_category,
  COUNT(*) AS address_count,
  SUM(total_trades) AS total_trades,
  SUM(total_volume_usd) AS total_volume_usd,
  AVG(avg_trade_size_usd) AS avg_trade_size_usd,
  AVG(total_trades) AS avg_trades_per_address,
  AVG(distinct_days) AS avg_active_days,
  AVG(distinct_months) AS avg_active_months
FROM classified
GROUP BY 1
ORDER BY 2 DESC
;

-- Detailed per-address view for top traders (supplementary)
-- Name: "PUSO Top Traders Detail (Mento Broker)"
WITH per_trader AS (
  SELECT
    trader,
    COUNT(*) AS total_trades,
    COUNT(DISTINCT date_trunc('day', evt_block_time)) AS distinct_days,
    COUNT(DISTINCT date_trunc('month', evt_block_time)) AS distinct_months,
    SUM(
      CASE
        WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountIn AS double) / 1e6
        WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountOut AS double) / 1e6
        ELSE 0
      END
    ) AS total_volume_usd,
    AVG(
      CASE
        WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountIn AS double) / 1e6
        WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
          THEN CAST(amountOut AS double) / 1e6
        ELSE 0
      END
    ) AS avg_trade_size_usd,
    MIN(evt_block_time) AS first_trade,
    MAX(evt_block_time) AS last_trade,
    CASE
      WHEN COUNT(*) > 50 THEN 'power_user'
      WHEN COUNT(*) >= 3 AND COUNT(DISTINCT date_trunc('month', evt_block_time)) >= 3 THEN 'regular'
      WHEN COUNT(*) BETWEEN 2 AND 10 AND COUNT(DISTINCT date_trunc('month', evt_block_time)) <= 2 THEN 'occasional'
      WHEN COUNT(*) = 1 THEN 'one_shot'
      ELSE 'other'
    END AS user_category
  FROM mento_celo.Broker_evt_Swap
  WHERE (
    tokenIn = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
    OR tokenOut = 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B
  )
  AND evt_block_time >= TIMESTAMP '2024-09-01'
  GROUP BY 1
)
SELECT * FROM per_trader
ORDER BY total_volume_usd DESC
LIMIT 50
;
