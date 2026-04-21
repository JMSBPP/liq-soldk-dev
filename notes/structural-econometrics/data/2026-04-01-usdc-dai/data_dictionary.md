# Data Dictionary: Volume-Fee Elasticity Variables

*Date: 2026-04-01*
*Pool: Quickswap V3 Algebra USDC/DAI (0xbc8f3da0bd42e1f2509cd8671ce7c7e5f7fd39c8, Polygon)*
*Period: 2026-01-01 through 2026-03-31*

---

## Variable Definitions

### V_A(t) -- Algebra Pool Hourly Volume

| Property | Value |
|----------|-------|
| **Variable name** | `hourly_volume_usd` (hourly), `daily_volume_usd` (daily) |
| **Definition** | Total swap volume in the Algebra USDC/DAI pool per hour |
| **Unit** | USD |
| **Source table** | `quickswap_v3_polygon.algebrapool_evt_swap` |
| **Aggregation** | SUM over hour of per-swap volume |
| **Per-swap volume** | `GREATEST(ABS(amount0) / 1e6, ABS(amount1) / 1e18)` |
| **Token0** | USDC (PoS), 6 decimals, contract `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` |
| **Token1** | DAI (PoS), 18 decimals, contract `0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063` |
| **Cleaning** | Deduplication via ROW_NUMBER on (evt_tx_hash, evt_block_time, amount0, amount1) |
| **Known issues** | Volume is computed from raw token amounts, not from external price feeds. For a stablecoin pair at ~1:1, this is equivalent to USD volume. |
| **Measurement error** | Negligible -- on-chain data is exact. Minor deviation from true USD only from USDC/DAI spread. |

### phi_t -- Volume-Weighted Average Fee

| Property | Value |
|----------|-------|
| **Variable name** | `vwap_fee` |
| **Definition** | Volume-weighted average of per-swap fees in the hour |
| **Unit** | Hundredths of a basis point (1 unit = 0.0001% = 0.01bp) |
| **Source table** | `quickswap_v3_polygon.algebrapool_evt_fee` |
| **Aggregation** | SUM(fee * volume_usd) / SUM(volume_usd) per hour |
| **Per-swap fee** | Emitted by the `Fee` event, joined to swap via evt_tx_hash |
| **Join logic** | Fee event fires before swap event in same tx; joined on evt_tx_hash with evt_index <= swap's evt_index, then deduplicated to closest match |
| **CRITICAL FINDING** | Fee is CONSTANT at 10 (= 0.1 bp = 0.001%) for the entire Q1 2026 period. See validation.md. |

### D_low, D_mid, D_high -- Fee Regime Dummies

| Property | Value |
|----------|-------|
| **Definition** | Binary indicators for volatility regime based on Algebra AdaptiveFee.sol sigmoid parameters |
| **NOT COMPUTABLE** | Fee is constant at 10 for entire sample. No regime variation exists. All observations are in the lowest fee regime. |
| **Algebra parameters** | baseFee=100, alpha1=2900, alpha2=12000, beta1=360, beta2=60000, gamma1=59, gamma2=8500 |
| **Note** | The observed fee of 10 is BELOW the baseFee parameter of 100. This suggests the pool may be using different fee parameters than the defaults, or the fee was overridden by governance. |

### TotalDEXVol_t -- Total Polygon DEX Volume

| Property | Value |
|----------|-------|
| **Variable name** | `total_polygon_dex_volume_usd` |
| **Definition** | Sum of all DEX swap volume on Polygon across all pairs and protocols |
| **Unit** | USD |
| **Source table** | `dex.trades` (Dune Spellbook) |
| **Aggregation** | SUM(amount_usd) per hour |
| **Partition filters** | `blockchain = 'polygon'`, `block_month >= '2026-01-01'`, `block_date >= '2026-01-01'` |
| **Coverage** | 14-16 DEX protocols active per day |

### DSR_t -- MakerDAO DAI Savings Rate

| Property | Value |
|----------|-------|
| **Variable name** | `dsr_annualized` |
| **Definition** | Annualized Dai Savings Rate set by MakerDAO governance |
| **Unit** | Decimal (e.g., 0.0125 = 1.25%) |
| **Source table** | `maker_ethereum.pot_call_file` on Ethereum mainnet |
| **Computation** | `EXP(31536000 * LN(data / 1e27)) - 1` where data is RAY-format per-second rate |
| **FINDING** | Constant at 1.25% for entire Q1 2026 (last change: 2025-10-27) |
| **Treatment in regression** | Drops out as constant -- absorbed by intercept |

### |USDC/DAI - 1| -- Price Deviation from Peg

| Property | Value |
|----------|-------|
| **Variable name** | `avg_price_deviation`, `max_price_deviation` |
| **Definition** | Absolute deviation of USDC/DAI exchange rate from 1.0 |
| **Unit** | Dimensionless (e.g., 0.001 = 0.1% deviation) |
| **Computation** | Price derived from sqrtPriceX96: `(sqrtPriceX96 / 2^96)^2 * 10^(6-18)` gives DAI per USDC |
| **Aggregation** | Mean (avg) and max of |price - 1.0| per hour |

### Liquidity_t -- Active Liquidity

| Property | Value |
|----------|-------|
| **Variable name** | `vwap_liquidity`, `avg_liquidity` |
| **Definition** | Active liquidity at current tick during each swap |
| **Unit** | Raw uint128 liquidity units (Uniswap V3 / Algebra concentrated liquidity) |
| **Source** | `liquidity` field from algebrapool_evt_swap |
| **Aggregation** | Volume-weighted average (vwap) and simple average per hour |

### Aggregator Fraction

| Property | Value |
|----------|-------|
| **Variable name** | `aggregator_volume_fraction`, `aggregator_trade_count` |
| **Definition** | Fraction of volume routed through known DEX aggregator contracts |
| **Identification** | `evt_tx_from` matched against known router addresses (1inch v4/v5, Paraswap v5, 0x, KyberSwap, Odos v2) |
| **FINDING** | Aggregator fraction is 0% for entire Q1 2026. See validation.md. |

---

## Token Addresses (Polygon PoS)

| Token | Address | Decimals |
|-------|---------|----------|
| USDC (PoS) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | 6 |
| DAI (PoS) | `0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063` | 18 |

---

## Known Aggregator Router Addresses

| Protocol | Address |
|----------|---------|
| 1inch v5 | `0x1111111254EEB25477B68fb85Ed929f73A960582` |
| 1inch v4 | `0x1111111254fb6c44bAC0beD2854e76F90643097d` |
| Paraswap v5 | `0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57` |
| 0x Exchange Proxy | `0xDef1C0ded9bec7F1a1670819833240f027b25EfF` |
| KyberSwap | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |
| Odos v2 | `0xf5b4F3CE32d8B0660F328bD8247B05bceF87CE3B` |
