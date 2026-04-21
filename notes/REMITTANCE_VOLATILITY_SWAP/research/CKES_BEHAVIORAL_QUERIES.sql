-- ============================================================
-- cKES Behavioral Fingerprint Queries
-- All queries target: mento_celo.Broker_evt_Swap
-- cKES: 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0
-- cUSD: 0x765DE816845861e75A25fCA122bb6898B8B1282a
-- Both tokens have 18 decimals on Celo
-- All queries: is_temp = false, DuneSQL dialect
-- ============================================================


-- ============================================================
-- QUERY 1: cKES Daily Net Flow Time Series
-- Dune name: "cKES Daily Net Flow Time Series (Mento Broker)"
-- ============================================================
WITH swaps AS (
    SELECT
        DATE_TRUNC('day', evt_block_time) AS trade_date,
        CASE
            WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
             AND tokenOut = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0
            THEN 'buy_ckes'
            WHEN tokenIn = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0
             AND tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN 'sell_ckes'
        END AS direction,
        CASE
            WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN CAST(amountIn AS DOUBLE) / 1e18
            WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN CAST(amountOut AS DOUBLE) / 1e18
        END AS usd_amount,
        trader
    FROM mento_celo.Broker_evt_Swap
    WHERE evt_block_time >= TIMESTAMP '2024-01-01'
      AND (
          (tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a AND tokenOut = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0)
          OR
          (tokenIn = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0 AND tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a)
      )
)
SELECT
    trade_date,
    COALESCE(SUM(CASE WHEN direction = 'buy_ckes' THEN usd_amount END), 0) AS gross_inflow,
    COALESCE(SUM(CASE WHEN direction = 'sell_ckes' THEN usd_amount END), 0) AS gross_outflow,
    COALESCE(SUM(CASE WHEN direction = 'buy_ckes' THEN usd_amount END), 0)
      - COALESCE(SUM(CASE WHEN direction = 'sell_ckes' THEN usd_amount END), 0) AS net_flow,
    COUNT(CASE WHEN direction = 'buy_ckes' THEN 1 END) AS trade_count_buy,
    COUNT(CASE WHEN direction = 'sell_ckes' THEN 1 END) AS trade_count_sell,
    COUNT(DISTINCT trader) AS unique_traders
FROM swaps
GROUP BY 1
ORDER BY 1
;


-- ============================================================
-- QUERY 2: cKES Transaction Size Distribution
-- Dune name: "cKES Transaction Size Distribution (Mento Broker)"
-- ============================================================
WITH swaps AS (
    SELECT
        CASE
            WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN CAST(amountIn AS DOUBLE) / 1e18
            WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN CAST(amountOut AS DOUBLE) / 1e18
        END AS usd_amount,
        trader
    FROM mento_celo.Broker_evt_Swap
    WHERE evt_block_time >= TIMESTAMP '2024-01-01'
      AND (
          (tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a AND tokenOut = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0)
          OR
          (tokenIn = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0 AND tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a)
      )
),
bucketed AS (
    SELECT
        CASE
            WHEN usd_amount < 10 THEN '$0-10'
            WHEN usd_amount < 50 THEN '$10-50'
            WHEN usd_amount < 100 THEN '$50-100'
            WHEN usd_amount < 200 THEN '$100-200'
            WHEN usd_amount < 500 THEN '$200-500'
            WHEN usd_amount < 1000 THEN '$500-1000'
            WHEN usd_amount < 2000 THEN '$1000-2000'
            WHEN usd_amount < 5000 THEN '$2000-5000'
            ELSE '$5000+'
        END AS size_bucket,
        CASE
            WHEN usd_amount < 10 THEN 1
            WHEN usd_amount < 50 THEN 2
            WHEN usd_amount < 100 THEN 3
            WHEN usd_amount < 200 THEN 4
            WHEN usd_amount < 500 THEN 5
            WHEN usd_amount < 1000 THEN 6
            WHEN usd_amount < 2000 THEN 7
            WHEN usd_amount < 5000 THEN 8
            ELSE 9
        END AS bucket_order,
        usd_amount,
        trader
    FROM swaps
),
totals AS (
    SELECT COUNT(*) AS total_trades FROM bucketed
)
SELECT
    b.size_bucket,
    b.bucket_order,
    COUNT(*) AS trade_count,
    COUNT(DISTINCT b.trader) AS unique_traders,
    SUM(b.usd_amount) AS total_volume_usd,
    AVG(b.usd_amount) AS avg_size_usd,
    APPROX_PERCENTILE(b.usd_amount, 0.5) AS median_size_usd,
    ROUND(100.0 * COUNT(*) / MAX(t.total_trades), 2) AS pct_of_trades
FROM bucketed b
CROSS JOIN totals t
GROUP BY 1, 2
ORDER BY b.bucket_order
;


-- ============================================================
-- QUERY 3: cKES Temporal Patterns (Hour + DoW + Monthly)
-- Dune name: "cKES Temporal Patterns Combined (Mento Broker)"
-- ============================================================
WITH base_swaps AS (
    SELECT
        evt_block_time,
        trader
    FROM mento_celo.Broker_evt_Swap
    WHERE evt_block_time >= TIMESTAMP '2024-01-01'
      AND (
          (tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a AND tokenOut = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0)
          OR
          (tokenIn = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0 AND tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a)
      )
),
hourly AS (
    SELECT
        'hourly' AS granularity,
        CAST(HOUR(evt_block_time) AS VARCHAR) AS period_key,
        HOUR(evt_block_time) AS sort_key,
        COUNT(*) AS trade_count,
        COUNT(DISTINCT trader) AS unique_traders
    FROM base_swaps
    GROUP BY 1, 2, 3
),
daily_dow AS (
    SELECT
        'day_of_week' AS granularity,
        CASE DAY_OF_WEEK(evt_block_time)
            WHEN 1 THEN '1_Monday'
            WHEN 2 THEN '2_Tuesday'
            WHEN 3 THEN '3_Wednesday'
            WHEN 4 THEN '4_Thursday'
            WHEN 5 THEN '5_Friday'
            WHEN 6 THEN '6_Saturday'
            WHEN 7 THEN '7_Sunday'
        END AS period_key,
        DAY_OF_WEEK(evt_block_time) AS sort_key,
        COUNT(*) AS trade_count,
        COUNT(DISTINCT trader) AS unique_traders
    FROM base_swaps
    GROUP BY 1, DAY_OF_WEEK(evt_block_time)
),
monthly AS (
    SELECT
        'monthly' AS granularity,
        CAST(DATE_TRUNC('month', evt_block_time) AS VARCHAR) AS period_key,
        CAST(EXTRACT(YEAR FROM evt_block_time) * 100 + EXTRACT(MONTH FROM evt_block_time) AS BIGINT) AS sort_key,
        COUNT(*) AS trade_count,
        COUNT(DISTINCT trader) AS unique_traders
    FROM base_swaps
    GROUP BY 1, DATE_TRUNC('month', evt_block_time), EXTRACT(YEAR FROM evt_block_time), EXTRACT(MONTH FROM evt_block_time)
)
SELECT * FROM hourly
UNION ALL
SELECT * FROM daily_dow
UNION ALL
SELECT * FROM monthly
ORDER BY granularity, sort_key
;


-- ============================================================
-- QUERY 4: cKES Address Behavior Clustering
-- Dune name: "cKES Address Behavior Clustering (Mento Broker)"
-- ============================================================
WITH swaps AS (
    SELECT
        trader,
        evt_block_time,
        CASE
            WHEN tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN CAST(amountIn AS DOUBLE) / 1e18
            WHEN tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a
            THEN CAST(amountOut AS DOUBLE) / 1e18
        END AS usd_amount
    FROM mento_celo.Broker_evt_Swap
    WHERE evt_block_time >= TIMESTAMP '2024-01-01'
      AND (
          (tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a AND tokenOut = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0)
          OR
          (tokenIn = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0 AND tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a)
      )
),
per_trader AS (
    SELECT
        trader,
        COUNT(*) AS total_trades,
        COUNT(DISTINCT DATE_TRUNC('month', evt_block_time)) AS active_months,
        COUNT(DISTINCT DATE_TRUNC('day', evt_block_time)) AS active_days,
        SUM(usd_amount) AS total_volume_usd,
        MIN(evt_block_time) AS first_trade,
        MAX(evt_block_time) AS last_trade
    FROM swaps
    GROUP BY 1
),
classified AS (
    SELECT
        *,
        CASE
            WHEN total_trades > 50 THEN 'power_user'
            WHEN total_trades >= 3 AND active_months >= 3 THEN 'regular'
            WHEN total_trades BETWEEN 2 AND 10 THEN 'occasional'
            ELSE 'one_shot'
        END AS user_class
    FROM per_trader
),
totals AS (
    SELECT
        COUNT(*) AS total_addresses,
        SUM(total_trades) AS total_all_trades,
        SUM(total_volume_usd) AS total_all_volume
    FROM classified
)
SELECT
    c.user_class,
    COUNT(*) AS address_count,
    SUM(c.total_trades) AS total_trades,
    ROUND(100.0 * COUNT(*) / MAX(t.total_addresses), 2) AS pct_of_addresses,
    ROUND(100.0 * SUM(c.total_trades) / MAX(t.total_all_trades), 2) AS pct_of_trades,
    ROUND(100.0 * SUM(c.total_volume_usd) / MAX(t.total_all_volume), 2) AS pct_of_volume,
    ROUND(AVG(c.total_volume_usd), 2) AS avg_volume_per_user,
    ROUND(AVG(c.total_trades), 1) AS avg_trades_per_user,
    ROUND(AVG(c.active_months), 1) AS avg_active_months,
    ROUND(AVG(c.active_days), 1) AS avg_active_days
FROM classified c
CROSS JOIN totals t
GROUP BY 1
ORDER BY total_trades DESC
;


-- ============================================================
-- QUERY 5: cKES Spike Investigation - New vs Returning Traders
-- Dune name: "cKES Spike Investigation New vs Returning (Mento Broker)"
-- ============================================================
WITH swaps AS (
    SELECT
        trader,
        DATE_TRUNC('day', evt_block_time) AS trade_date
    FROM mento_celo.Broker_evt_Swap
    WHERE evt_block_time >= TIMESTAMP '2024-01-01'
      AND (
          (tokenIn = 0x765DE816845861e75A25fCA122bb6898B8B1282a AND tokenOut = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0)
          OR
          (tokenIn = 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0 AND tokenOut = 0x765DE816845861e75A25fCA122bb6898B8B1282a)
      )
),
first_appearance AS (
    SELECT
        trader,
        MIN(trade_date) AS first_trade_date
    FROM swaps
    GROUP BY 1
),
daily_breakdown AS (
    SELECT
        s.trade_date,
        COUNT(DISTINCT s.trader) AS total_traders,
        COUNT(DISTINCT CASE WHEN s.trade_date = f.first_trade_date THEN s.trader END) AS new_traders,
        COUNT(DISTINCT CASE WHEN s.trade_date > f.first_trade_date THEN s.trader END) AS returning_traders
    FROM swaps s
    JOIN first_appearance f ON s.trader = f.trader
    GROUP BY 1
),
new_trader_retention AS (
    SELECT
        f.first_trade_date,
        COUNT(DISTINCT f.trader) AS new_traders_that_day,
        COUNT(DISTINCT CASE WHEN s2.trade_date > f.first_trade_date THEN f.trader END) AS returned_later,
        COUNT(DISTINCT CASE WHEN s2.trade_date > f.first_trade_date
            AND s2.trade_date >= f.first_trade_date + INTERVAL '7' DAY THEN f.trader END) AS returned_after_7d
    FROM first_appearance f
    LEFT JOIN swaps s2 ON f.trader = s2.trader AND s2.trade_date > f.first_trade_date
    GROUP BY 1
    HAVING COUNT(DISTINCT f.trader) >= 3
)
SELECT
    d.trade_date,
    d.total_traders,
    d.new_traders,
    d.returning_traders,
    ROUND(100.0 * d.new_traders / NULLIF(d.total_traders, 0), 1) AS pct_new,
    r.returned_later,
    r.returned_after_7d,
    ROUND(100.0 * r.returned_later / NULLIF(r.new_traders_that_day, 0), 1) AS retention_rate,
    ROUND(100.0 * r.returned_after_7d / NULLIF(r.new_traders_that_day, 0), 1) AS retention_7d_rate
FROM daily_breakdown d
LEFT JOIN new_trader_retention r ON d.trade_date = r.first_trade_date
ORDER BY d.trade_date
;
