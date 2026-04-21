# Dune SQL Queries for Volume-Fee Elasticity Data Pull

*Date: 2026-04-01*
*Total credits used: 0.831 (of ~2,500 budget)*

---

## Query 1: Algebra USDC/DAI Hourly Pool Data (HOURLY - canonical)

- **Query ID**: 6937636
- **URL**: https://dune.com/queries/6937636
- **Rows**: ~2,160 (hourly, Q1 2026)
- **Note**: Full hourly data must be exported from Dune web UI (API limit = 100 rows)

### SQL

```sql
-- Algebra USDC/DAI Pool: Hourly Volume, Fee, Liquidity, Price Deviation
-- Pool: 0xbc8f3da0bd42e1f2509cd8671ce7c7e5f7fd39c8 (Polygon)
-- Period: Q1 2026 (Jan 1 - Mar 31)
-- Token0 = USDC (6 decimals), Token1 = DAI (18 decimals)

WITH pool_address AS (
    SELECT 0xbc8f3da0bd42e1f2509cd8671ce7c7e5f7fd39c8 AS addr
),

swap_fees AS (
    SELECT evt_tx_hash, evt_index, fee
    FROM quickswap_v3_polygon.algebrapool_evt_fee
    WHERE contract_address = (SELECT addr FROM pool_address)
      AND evt_block_date >= DATE '2026-01-01'
      AND evt_block_date < DATE '2026-04-01'
),

aggregator_routers AS (
    SELECT addr FROM (VALUES
        (0x1111111254EEB25477B68fb85Ed929f73A960582),  -- 1inch v5
        (0x1111111254fb6c44bAC0beD2854e76F90643097d),  -- 1inch v4
        (0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57),  -- Paraswap v5
        (0xDef1C0ded9bec7F1a1670819833240f027b25EfF),  -- 0x Exchange Proxy
        (0x6131B5fae19EA4f9D964eAc0408E4408b66337b5),  -- KyberSwap
        (0xf5b4F3CE32d8B0660F328bD8247B05bceF87CE3B)   -- Odos v2
    ) AS t(addr)
),

swaps_raw AS (
    SELECT
        s.evt_block_time, s.evt_tx_hash, s.evt_tx_from,
        s.amount0, s.amount1, s.liquidity, s.price AS sqrtPriceX96, s.tick,
        f.fee,
        GREATEST(ABS(CAST(s.amount0 AS DOUBLE))/1e6, ABS(CAST(s.amount1 AS DOUBLE))/1e18) AS volume_usd,
        POWER(CAST(s.price AS DOUBLE)/POWER(2.0, 96), 2) * 1e-12 AS price_dai_per_usdc,
        CASE WHEN s.evt_tx_from IN (SELECT addr FROM aggregator_routers) THEN 1 ELSE 0 END AS is_aggregator_tx
    FROM quickswap_v3_polygon.algebrapool_evt_swap s
    INNER JOIN swap_fees f
        ON s.evt_tx_hash = f.evt_tx_hash AND f.evt_index <= s.evt_index
    WHERE s.contract_address = (SELECT addr FROM pool_address)
      AND s.evt_block_date >= DATE '2026-01-01'
      AND s.evt_block_date < DATE '2026-04-01'
),

swaps_deduped AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY evt_tx_hash, evt_block_time, amount0, amount1
        ORDER BY fee DESC
    ) AS rn FROM swaps_raw
),

swaps AS (SELECT * FROM swaps_deduped WHERE rn = 1)

SELECT
    DATE_TRUNC('hour', evt_block_time) AS hour_ts,
    SUM(volume_usd) AS hourly_volume_usd,
    COUNT(*) AS trade_count,
    SUM(fee * volume_usd) / NULLIF(SUM(volume_usd), 0) AS vwap_fee,
    MIN(fee) AS min_fee, MAX(fee) AS max_fee,
    APPROX_PERCENTILE(fee, 0.5) AS median_fee,
    SUM(CAST(liquidity AS DOUBLE)*volume_usd)/NULLIF(SUM(volume_usd),0) AS vwap_liquidity,
    AVG(CAST(liquidity AS DOUBLE)) AS avg_liquidity,
    AVG(ABS(price_dai_per_usdc - 1.0)) AS avg_price_deviation,
    MAX(ABS(price_dai_per_usdc - 1.0)) AS max_price_deviation,
    AVG(price_dai_per_usdc) AS avg_price_dai_per_usdc,
    SUM(CASE WHEN is_aggregator_tx=1 THEN volume_usd ELSE 0 END)/NULLIF(SUM(volume_usd),0) AS aggregator_volume_fraction,
    SUM(is_aggregator_tx) AS aggregator_trade_count
FROM swaps
GROUP BY DATE_TRUNC('hour', evt_block_time)
ORDER BY hour_ts
```

---

## Query 1b: Algebra USDC/DAI Daily Summary (API-exportable, 90 rows)

- **Query ID**: 6937640
- **URL**: https://dune.com/queries/6937640
- **Execution ID**: 01KN5DTGE4S7BFSJDBCSJEFS4C
- **Execution cost**: 0.24 credits
- **Rows returned**: 90 (all 90 days, full coverage)

### Columns

| Column | Type | Description |
|--------|------|-------------|
| day_date | date | Calendar date |
| daily_volume_usd | double | Total swap volume in USD |
| trade_count | bigint | Number of swaps |
| active_hours | bigint | Hours with at least 1 trade (expect 24) |
| vwap_fee | double | Volume-weighted average fee (hundredths of bip) |
| min_fee | integer | Minimum fee observed |
| max_fee | integer | Maximum fee observed |
| median_fee | bigint | Median fee |
| avg_liquidity | double | Average active liquidity (raw uint128) |
| avg_price_deviation | double | Mean |USDC/DAI - 1.0| |
| max_price_deviation | double | Max |USDC/DAI - 1.0| |
| aggregator_volume_fraction | double | Fraction of volume from known aggregator routers |
| aggregator_trade_count | bigint | Number of aggregator-routed trades |

---

## Query 2: Total Polygon DEX Volume (HOURLY - canonical)

- **Query ID**: 6937637
- **URL**: https://dune.com/queries/6937637
- **Rows**: ~2,160 (hourly)

### Tables used
- `dex.trades` (spellbook spell, partitioned on `block_month`, `blockchain`, `project`)

---

## Query 2b: Total Polygon DEX Volume Daily (API-exportable, 90 rows)

- **Query ID**: 6937641
- **URL**: https://dune.com/queries/6937641
- **Execution ID**: 01KN5DTGWVJND3ZVNW6GSVRJQC
- **Execution cost**: 0.324 credits
- **Rows returned**: 90

### Columns

| Column | Type | Description |
|--------|------|-------------|
| day_date | date | Calendar date |
| total_polygon_dex_volume_usd | double | Sum of all DEX volume on Polygon |
| total_trade_count | bigint | Number of DEX trades |
| active_projects | bigint | Distinct DEX protocols active that day |

---

## Query 3: MakerDAO DSR Changes

- **Query ID**: 6937638
- **URL**: https://dune.com/queries/6937638
- **Execution ID**: 01KN5DTH55ZBKGM65H312TACPY
- **Execution cost**: 0.007 credits
- **Rows returned**: 24 (all DSR changes from Jan 2024 to present)

### Tables used
- `maker_ethereum.pot_call_file` (decoded call table for MakerDAO Pot contract)

### DSR value during Q1 2026
The last DSR change before Q1 2026 occurred on **2025-10-27**, setting DSR to **1.25% annualized**.
No DSR changes occurred during Q1 2026. The DSR was **constant at 1.25%** for the entire sample period.

### Columns

| Column | Type | Description |
|--------|------|-------------|
| call_block_time | timestamp | When the DSR was changed |
| call_block_number | bigint | Ethereum block number |
| call_tx_hash | varbinary | Transaction hash |
| dsr_per_second | double | Per-second rate (RAY / 1e27) |
| dsr_annualized | double | (dsr_per_second)^(365*24*3600) - 1 |

---

## Data Source Tables

| Table | Category | Partition Column | Used For |
|-------|----------|-----------------|----------|
| `quickswap_v3_polygon.algebrapool_evt_swap` | decoded | evt_block_date | Swap amounts, liquidity, price, tick |
| `quickswap_v3_polygon.algebrapool_evt_fee` | decoded | evt_block_date | Per-swap fee (hundredths of bip) |
| `dex.trades` | spell | block_month, blockchain, project | Total Polygon DEX volume |
| `maker_ethereum.pot_call_file` | decoded | call_block_date | DSR governance changes |
