# Dune Queries: USDC/WETH Algebra Pool Hourly Data (Q1 2026)

*Generated: 2026-04-01*
*Pool: Quickswap V3 Algebra USDC/WETH (`0xa6aedf7c4ed6e821e67a6bfd56fd1702ad9a9719`, Polygon)*
*Period: 2026-01-01 to 2026-03-31*

---

## Query 1: Pool Hourly Data (MAIN)

- **Query ID**: 6937696
- **URL**: https://dune.com/queries/6937696
- **Status**: Executed successfully
- **Execution cost**: 0.211 credits
- **Total rows**: ~2,156 hourly observations (Jan 1 00:00 to Mar 31 19:00 UTC)

### Source Tables
- `dex.trades` (partition: `block_month`, `blockchain`, `project`) -- hourly USD volume
- `quickswap_v3_polygon.algebrapool_evt_fee` (partition: `evt_block_date`) -- fee events
- `quickswap_v3_polygon.algebrapool_evt_swap` (partition: `evt_block_date`) -- swap events (liquidity, price, tick)

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `hour` | timestamp | Hour bucket (UTC) |
| `volume_usd` | double | Total swap volume in USD from `dex.trades` (SUM of `amount_usd`) |
| `trade_count` | bigint | Number of trades from `dex.trades` |
| `avg_fee` | double | Simple average of fee events per hour (hundredths of bip) |
| `min_fee` | integer | Minimum fee event value in the hour |
| `max_fee` | integer | Maximum fee event value in the hour |
| `stddev_fee` | double | Standard deviation of fee within the hour |
| `median_fee` | bigint | Approximate median fee (via APPROX_PERCENTILE) |
| `fee_event_count` | bigint | Number of Fee events emitted in the hour |
| `vwap_fee` | double | Volume-weighted average fee: SUM(fee_i * abs(amount0_i)/1e6) / SUM(abs(amount0_i)/1e6), joined on tx_hash |
| `avg_liquidity` | double | Average active liquidity from swap events (uint256 cast to double) |
| `avg_sqrtPriceX96` | double | Average sqrtPriceX96 from swap events |
| `avg_tick` | double | Average tick from swap events |
| `swap_count` | bigint | Number of swap events in the hour |
| `fee_regime` | varchar | Classification: 'low' (<200), 'mid' (200-599), 'high' (>=600) based on avg_fee |

### SQL

```sql
-- USDC/WETH Algebra Pool: Hourly Volume, Fee, Liquidity, Price
-- Pool: 0xa6aedf7c4ed6e821e67a6bfd56fd1702ad9a9719 (Polygon)
-- Period: 2026-01-01 to 2026-03-31

WITH pool_address AS (
    SELECT 0xa6aedf7c4ed6e821e67a6bfd56fd1702ad9a9719 AS addr
),

hourly_volume AS (
    SELECT
        date_trunc('hour', block_time) AS hour,
        SUM(amount_usd) AS volume_usd,
        COUNT(*) AS trade_count
    FROM dex.trades
    WHERE blockchain = 'polygon'
      AND project = 'quickswap'
      AND block_month >= DATE '2026-01-01'
      AND block_month < DATE '2026-04-01'
      AND block_date >= DATE '2026-01-01'
      AND block_date < DATE '2026-04-01'
      AND project_contract_address = (SELECT addr FROM pool_address)
    GROUP BY 1
),

hourly_fee AS (
    SELECT
        date_trunc('hour', evt_block_time) AS hour,
        AVG(fee) AS avg_fee,
        MIN(fee) AS min_fee,
        MAX(fee) AS max_fee,
        STDDEV(fee) AS stddev_fee,
        COUNT(*) AS fee_event_count,
        APPROX_PERCENTILE(fee, 0.5) AS median_fee
    FROM quickswap_v3_polygon.algebrapool_evt_fee
    WHERE contract_address = (SELECT addr FROM pool_address)
      AND evt_block_date >= DATE '2026-01-01'
      AND evt_block_date < DATE '2026-04-01'
    GROUP BY 1
),

hourly_swap AS (
    SELECT
        date_trunc('hour', s.evt_block_time) AS hour,
        AVG(CAST(s.liquidity AS DOUBLE)) AS avg_liquidity,
        AVG(CAST(s.price AS DOUBLE)) AS avg_sqrtPriceX96,
        AVG(CAST(s.tick AS DOUBLE)) AS avg_tick,
        COUNT(*) AS swap_count
    FROM quickswap_v3_polygon.algebrapool_evt_swap s
    WHERE s.contract_address = (SELECT addr FROM pool_address)
      AND s.evt_block_date >= DATE '2026-01-01'
      AND s.evt_block_date < DATE '2026-04-01'
    GROUP BY 1
),

vwap_fee AS (
    SELECT
        date_trunc('hour', s.evt_block_time) AS hour,
        SUM(
            CAST(f.fee AS DOUBLE)
            * (ABS(CAST(s.amount0 AS DOUBLE)) / 1e6)
        ) / NULLIF(SUM(ABS(CAST(s.amount0 AS DOUBLE)) / 1e6), 0) AS vwap_fee
    FROM quickswap_v3_polygon.algebrapool_evt_swap s
    INNER JOIN quickswap_v3_polygon.algebrapool_evt_fee f
        ON s.evt_tx_hash = f.evt_tx_hash
        AND s.contract_address = f.contract_address
    WHERE s.contract_address = (SELECT addr FROM pool_address)
      AND s.evt_block_date >= DATE '2026-01-01'
      AND s.evt_block_date < DATE '2026-04-01'
      AND f.evt_block_date >= DATE '2026-01-01'
      AND f.evt_block_date < DATE '2026-04-01'
    GROUP BY 1
)

SELECT
    COALESCE(v.hour, f.hour, sw.hour, vf.hour) AS hour,
    v.volume_usd,
    v.trade_count,
    f.avg_fee,
    f.min_fee,
    f.max_fee,
    f.stddev_fee,
    f.median_fee,
    f.fee_event_count,
    vf.vwap_fee,
    sw.avg_liquidity,
    sw.avg_sqrtPriceX96,
    sw.avg_tick,
    sw.swap_count,
    CASE
        WHEN f.avg_fee < 200 THEN 'low'
        WHEN f.avg_fee < 600 THEN 'mid'
        ELSE 'high'
    END AS fee_regime
FROM hourly_volume v
FULL OUTER JOIN hourly_fee f ON v.hour = f.hour
FULL OUTER JOIN hourly_swap sw ON COALESCE(v.hour, f.hour) = sw.hour
FULL OUTER JOIN vwap_fee vf ON COALESCE(v.hour, f.hour, sw.hour) = vf.hour
ORDER BY 1
```

---

## Query 2: Total Polygon DEX Volume Hourly

- **Query ID**: 6937702
- **URL**: https://dune.com/queries/6937702
- **Status**: Executed successfully
- **Execution cost**: 0.127 credits
- **Total rows**: ~2,156 hourly observations
- **Note**: Replaces query 6937698 (had missing GROUP BY)

### Source Tables
- `dex.trades` (partition: `block_month`, `blockchain`, `project`)

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `hour` | timestamp | Hour bucket (UTC) |
| `total_polygon_dex_volume_usd` | double | Sum of all DEX volume on Polygon in USD |
| `total_polygon_trade_count` | bigint | Total trade count across all Polygon DEXes |

### SQL

```sql
SELECT
    date_trunc('hour', block_time) AS hour,
    SUM(amount_usd) AS total_polygon_dex_volume_usd,
    COUNT(*) AS total_polygon_trade_count
FROM dex.trades
WHERE blockchain = 'polygon'
  AND block_month >= DATE '2026-01-01'
  AND block_month < DATE '2026-04-01'
  AND block_date >= DATE '2026-01-01'
  AND block_date < DATE '2026-04-01'
GROUP BY 1
ORDER BY 1
```

---

## Query 3: ETH Hourly Price

- **Query ID**: 6937699
- **URL**: https://dune.com/queries/6937699
- **Status**: Executed successfully
- **Execution cost**: 0.213 credits
- **Total rows**: ~2,018+ hourly observations (full Q1 2026 coverage confirmed)

### Source Tables
- `prices.hour` (no partition columns -- filtered by timestamp)

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `hour` | timestamp | Hour bucket (UTC) |
| `eth_price_usd` | double | Hourly ETH price in USD (from Ethereum WETH) |
| `log_return` | double | ln(price_t / price_{t-1}), hourly log return for realized vol computation |
| `eth_volume` | double | Trading volume (currently null in prices.hour) |

### SQL

```sql
SELECT
    timestamp AS hour,
    price AS eth_price_usd,
    LN(price / LAG(price) OVER (ORDER BY timestamp)) AS log_return,
    volume AS eth_volume
FROM prices.hour
WHERE blockchain = 'ethereum'
  AND symbol = 'WETH'
  AND timestamp >= TIMESTAMP '2026-01-01 00:00:00'
  AND timestamp < TIMESTAMP '2026-04-01 00:00:00'
ORDER BY 1
```

---

## Query 4: Fee Distribution Analysis

- **Query ID**: 6937700
- **URL**: https://dune.com/queries/6937700
- **Status**: Executed successfully
- **Execution cost**: 0.027 credits

### Output
Combined result set with `analysis_type` discriminator column:
- `'summary'` row: full distribution statistics (count, distinct, mean, stddev, percentiles)
- `'histogram'` rows: fee bucket counts (buckets of 50 hundredths-of-bip)

### Key Findings
- 142,422 total fee events in Q1 2026
- 511 distinct fee values
- Range: 400--910 (hundredths of bip)
- Mean: 784.6, Median: 888, StdDev: 182.7
- Heavily right-skewed (p25=729, p75=899)
- Default regime thresholds (200/600) place nearly all observations in "high" -- regime boundaries need recalibration

---

## Credit Usage Summary

| Item | Credits |
|------|---------|
| Pre-existing usage | 1.162 |
| Query 1 (pool hourly) | 0.211 |
| Query 2 (Polygon DEX vol) | 0.127 |
| Query 3 (ETH price) | 0.213 |
| Query 4 (fee distribution) | 0.027 |
| Coverage check (temp) | 0.328 |
| **Total after pull** | **2.068** |
| **Remaining budget** | **~430** |

---

## How to Get Full Results

The Dune API returns max 100 rows per call. For full datasets (~2,156 rows each):

1. **Dune Web UI**: Visit the query URL and click "Run" or view cached results. Export as CSV.
2. **Dune Python SDK**:
   ```python
   from dune_client.client import DuneClient
   dune = DuneClient(api_key="YOUR_KEY")
   results = dune.get_latest_result(6937696)  # returns all rows
   df = results.get_dataframe()
   ```
3. **Direct API**: `GET https://api.dune.com/api/v1/query/6937696/results?limit=5000`
