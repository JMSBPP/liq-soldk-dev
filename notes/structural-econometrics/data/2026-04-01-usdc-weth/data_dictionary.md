# Data Dictionary: USDC/WETH Volume-Fee Elasticity Estimation

*Generated: 2026-04-01*
*Pool: Quickswap V3 Algebra USDC/WETH on Polygon*

---

## Unit of Observation

One hour. Each row represents a one-hour window [hour, hour+1h) in UTC.

Expected observation count: 90 days * 24 hours = 2,160. Actual: ~2,156 (4 missing hours likely due to zero-activity gaps).

---

## Variable Definitions

### Outcome Variable

| Variable | Query | Column | Definition | Units | Aggregation |
|----------|-------|--------|------------|-------|-------------|
| `V_A(t)` | Q1 | `volume_usd` | Hourly swap volume in the USDC/WETH Algebra pool | USD | SUM(`amount_usd`) from `dex.trades` where `project_contract_address` = pool |
| `ln(V_A(t))` | Derived | -- | Log of hourly volume | log-USD | `LN(volume_usd)` -- compute in estimation code |

### Endogenous Variable (Fee)

| Variable | Query | Column | Definition | Units | Aggregation |
|----------|-------|--------|------------|-------|-------------|
| `phi_t` (baseline) | Q1 | `vwap_fee` | Volume-weighted average fee per hour | hundredths of bip | SUM(fee_i * \|amount0_i\|) / SUM(\|amount0_i\|), joined swap+fee events on tx_hash |
| `phi_t` (simple) | Q1 | `avg_fee` | Simple arithmetic mean of fee events per hour | hundredths of bip | AVG(fee) from `algebrapool_evt_fee` |
| `ln(phi_t)` | Derived | -- | Log of hourly fee | log(hundredths-bip) | `LN(vwap_fee)` -- compute in estimation code |

**Fee units**: The Algebra `Fee` event emits fee in "hundredths of a basis point". Fee value 100 = 1 bip = 0.01%. Fee value 900 = 9 bips = 0.09%. To convert to percentage: `fee / 1e6`.

### Fee Variation Variables

| Variable | Query | Column | Definition |
|----------|-------|--------|------------|
| `min_fee_t` | Q1 | `min_fee` | Minimum fee event value in the hour |
| `max_fee_t` | Q1 | `max_fee` | Maximum fee event value in the hour |
| `stddev_fee_t` | Q1 | `stddev_fee` | Within-hour standard deviation of fee events |
| `median_fee_t` | Q1 | `median_fee` | Approximate median fee (APPROX_PERCENTILE) |
| `fee_range_t` | Derived | -- | `max_fee - min_fee` -- intra-hour fee dispersion |

### Regime Dummies

| Variable | Query | Column | Definition |
|----------|-------|--------|------------|
| `D_low(t)` | Q1 | `fee_regime='low'` | 1 if avg_fee < 200 |
| `D_mid(t)` | Q1 | `fee_regime='mid'` | 1 if 200 <= avg_fee < 600 |
| `D_high(t)` | Q1 | `fee_regime='high'` | 1 if avg_fee >= 600 |

**IMPORTANT NOTE**: The default regime thresholds (200/600) from AdaptiveFee.sol defaults are WRONG for this pool. The observed fee range is 400--910 with mean 785. Almost all observations fall in "high". Regime thresholds MUST be recalibrated based on this pool's actual fee distribution.

**Recommended data-driven thresholds** (from Q4 fee distribution analysis):
- Low: fee < p33 = 851 (roughly: fee < 730)
- Mid: p33 <= fee < p67 (roughly: 730 <= fee < 896)
- High: fee >= p67 = 896

Alternatively, use the fee histogram natural breaks:
- Low: 400--699 (lower mass cluster)
- Mid: 700--849 (transition zone)
- High: 850--910 (upper mass cluster, where >50% of observations live)

### Exogenous Controls

| Variable | Query | Column | Definition | Units |
|----------|-------|--------|------------|-------|
| `TotalDEXVol_t` | Q2 | `total_polygon_dex_volume_usd` | Total hourly DEX volume on Polygon (all pairs, all DEXes) | USD |
| `ln(TotalDEXVol_t)` | Derived | -- | Log of total Polygon DEX volume | log-USD |
| `ETH_price_t` | Q3 | `eth_price_usd` | Hourly ETH/USD price | USD |
| `r_t` | Q3 | `log_return` | Hourly log return: ln(P_t / P_{t-1}) | dimensionless |
| `RV_t` | Derived | -- | Realized volatility: sqrt(sum of squared log returns over trailing 24h window) | annualized if multiplied by sqrt(8760) |

**Note**: The original spec's DSR and USDC/DAI deviation controls are replaced by:
- `ETH_price_t` -- serves as the external price exogenous variable (ETH price drives pool activity)
- `RV_t` (derived from `log_return`) -- replaces pair-specific vol measure

### Pool Microstructure Variables

| Variable | Query | Column | Definition | Units |
|----------|-------|--------|------------|-------|
| `Liquidity_t` | Q1 | `avg_liquidity` | Average active liquidity at current tick (from swap events) | raw uint256 (Algebra liquidity units) |
| `ln(Liquidity_t)` | Derived | -- | Log of average liquidity | log-units |
| `sqrtPriceX96_t` | Q1 | `avg_sqrtPriceX96` | Average sqrtPriceX96 from swap events | raw Q64.96 |
| `tick_t` | Q1 | `avg_tick` | Average tick from swap events | tick units |
| `trade_count_t` | Q1 | `trade_count` | Number of trades in dex.trades per hour | count |
| `swap_count_t` | Q1 | `swap_count` | Number of swap events per hour | count |
| `fee_event_count_t` | Q1 | `fee_event_count` | Number of Fee events per hour | count |

### Derived Price from sqrtPriceX96

For USDC (token0, 6 decimals) / WETH (token1, 18 decimals):

```
raw_price = (sqrtPriceX96 / 2^96)^2         -- token1 per token0 in raw units
ETH_per_USDC = raw_price * 10^(6-18)        -- adjust for decimals
USDC_per_ETH = 1 / ETH_per_USDC             -- invert for familiar units
```

Or equivalently: `USDC_per_ETH = 10^12 / (sqrtPriceX96 / 2^96)^2`

---

## Data Sources

| Source Table | Blockchain | Partition Columns | Filter Applied |
|---|---|---|---|
| `dex.trades` | polygon | `block_month`, `blockchain`, `project` | `block_month >= '2026-01-01'`, `block_date >= '2026-01-01'`, `project = 'quickswap'`, `project_contract_address = pool` |
| `quickswap_v3_polygon.algebrapool_evt_fee` | polygon | `evt_block_date` | `evt_block_date >= '2026-01-01'`, `contract_address = pool` |
| `quickswap_v3_polygon.algebrapool_evt_swap` | polygon | `evt_block_date` | `evt_block_date >= '2026-01-01'`, `contract_address = pool` |
| `prices.hour` | ethereum | (none) | `blockchain = 'ethereum'`, `symbol = 'WETH'`, `timestamp >= '2026-01-01'` |

---

## Join Strategy

- **Q1 internal join (vwap_fee CTE)**: `evt_swap` INNER JOIN `evt_fee` ON `evt_tx_hash` AND `contract_address`. Rationale: the Fee event is emitted in the same transaction as the Swap event by the `beforeSwap` hook.
- **Q1 hourly aggregation**: FULL OUTER JOIN across hourly_volume, hourly_fee, hourly_swap, vwap_fee on `hour`. This preserves hours where one source has data but another does not (e.g., fee events without matching dex.trades rows).
- **Cross-query join** (in estimation code): JOIN Q1, Q2, Q3 on `hour`. Inner join recommended -- only estimate on hours where all three sources have data.

---

## Known Limitations

1. **Volume measurement**: `dex.trades.amount_usd` depends on Dune's token pricing. Small tokens or during flash crashes, USD valuation may be noisy.
2. **Fee-swap join**: The INNER JOIN on `evt_tx_hash` may miss fee events in transactions that do not produce a Swap event (e.g., fee changes from governance). This is correct behavior -- we only want fees associated with actual swaps.
3. **Liquidity**: `avg_liquidity` is the mean of the `liquidity` field across all swap events in the hour. This is the active liquidity at the moment of each swap, not a time-weighted average. Hours with many small swaps at the same liquidity level will be accurate; hours with large liquidity changes may have noisy averages.
4. **ETH price**: Sourced from `prices.hour` on Ethereum (WETH). This is a CEX-derived aggregate, not the pool's own price. This is intentional -- we want an exogenous price, not the endogenous pool price.
5. **sqrtPriceX96 precision**: Cast to DOUBLE loses precision for very large uint256 values. Sufficient for average-level analysis but not for tick-level reconstruction.
