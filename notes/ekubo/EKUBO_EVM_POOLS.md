# Ekubo EVM Pools — Complete Inventory

**Date**: 2026-04-08
**Sources**: GeckoTerminal, CoinGecko, on-chain scan
**Core Contract (V3)**: `0x00000000000014aA86C5d3c41765bb24e11bd701` (Ethereum + Arbitrum)

---

## Ethereum Mainnet — Live Pools

**Total TVL**: ~$4.7M across all pools
**Total 24h Volume**: ~$11.5M (2.4x TVL daily turnover)

### Tier 1: Macro-Relevant Pairs

| Pair | Liquidity | 24h Volume | Vol/TVL | Macro Signal |
|---|---|---|---|---|
| **USDC/USDT** | $916K | $6.88M | 7.5x | Stablecoin peg stress, USD monetary policy |
| **EUROC/USDC** | $224K | $183K | 0.8x | **EUR/USD FX rate — direct macro observable** |
| **XAUt/USDT** | $105K | $85K | 0.8x | **Gold/USD — inflation proxy** |
| **wstETH/ETH** (pool 1) | $520K | $48K | 0.09x | ETH staking yield = risk-free rate proxy |
| **wstETH/ETH** (pool 2) | $337K | $5K | 0.01x | Same signal, different tick spacing |
| **USDe/USDC** | $64K | $387K | 6.1x | Ethena synthetic dollar health |
| **GHO/USDC** | $113K | $14K | 0.1x | Aave stablecoin health |
| **BOLD/USDC** | $370K | $79K | 0.2x | Liquity V2 stablecoin health |

### Tier 2: Crypto Major Pairs

| Pair | Liquidity | 24h Volume | Vol/TVL |
|---|---|---|---|
| **cbBTC/WBTC** (pool 1) | $715K | $1.76M | 2.5x |
| **cbBTC/WBTC** (pool 2) | $215K | $33K | 0.2x |
| **WBTC/ETH** | $373K | $301K | 0.8x |
| **USDC/ETH** (pool 1) | $299K | $1.21M | 4.0x |
| **USDC/ETH** (pool 2) | $66K | $20K | 0.3x |
| **USDC/ETH** (pool 3) | $61K | $13K | 0.2x |
| **USDT/WBTC** | $151K | $279K | 1.8x |
| **tBTC/WBTC** | $166K | $79K | 0.5x |
| **USDC/crvUSD** (pool 1) | $130K | $633K | 4.9x |
| **USDC/crvUSD** (pool 2) | small | $18K | — |
| **USDT/ETH** (pool 1) | $10K | $11K | 1.1x |
| **USDT/ETH** (pool 2) | $8K | $22K | 2.9x |

### Tier 3: Protocol Tokens

| Pair | Liquidity | 24h Volume |
|---|---|---|
| EKUBO/USDC | $30K | $4K |

---

## Arbitrum — Live Pools

| Pair | Liquidity | 24h Volume | Status |
|---|---|---|---|
| ETH/USDC | Small | $10.8K | Inactive (no trades in 3h) |

Arbitrum deployment is effectively dead.

---

## Key Findings

### 1. EUROC/USDC and XAUt/USDT Are Live

These are **directly macro-relevant** pairs on Ekubo EVM with Ekubo's dynamic fee mechanism:
- **EUROC/USDC** ($224K TVL, $183K/day): EUR/USD exchange rate with MEV-capture dynamic fees producing a volatility signal. EUROC is Circle's EUR stablecoin.
- **XAUt/USDT** ($105K TVL, $85K/day): Gold/USD price with dynamic fees. XAUt is Tether Gold (1 oz LBMA gold per token).

Neither pair exists on Algebra DEXes. This gives Ekubo a unique data advantage for inflation (gold) and FX (EUR) signals.

### 2. Stablecoin Diversity Is Exceptional

Ekubo has pools for 7 different stablecoins against each other:
- USDC, USDT (USD standard)
- USDe (Ethena synthetic)
- GHO (Aave)
- BOLD (Liquity V2)
- crvUSD (Curve)
- EUROC (Circle EUR)

Each stablecoin/stablecoin pair's fee dynamics encode different risk profiles. The MEV-capture fee on USDC/USDT captures USD peg stress differently from GHO/USDC which captures Aave protocol risk.

### 3. Volume/TVL Ratios Are Extreme

| Pool | Vol/TVL Ratio |
|---|---|
| USDC/USDT | **7.5x daily** |
| USDe/USDC | **6.1x daily** |
| USDC/crvUSD | **4.9x daily** |
| USDC/ETH (pool 1) | **4.0x daily** |

These ratios mean the MEV-capture fee updates extremely frequently per unit of TVL, producing high-resolution volatility signals despite modest absolute TVL.

### 4. Extension Type Uncertainty

GeckoTerminal does not show which extension (Base CL vs MEV-capture vs TWAMM vs Oracle vs Boosted Fees) each pool uses. To determine this, we'd need to decode the pool key from on-chain events — specifically the `extension` field in each pool's key. This requires:
- Scanning `PoolInitialized` or equivalent events on the Core contract
- Matching the extension address field against known extension addresses:
  - `0x5555fF9Ff2757500BF4EE020DcfD0210CFfa41Be` = MEV-capture
  - `0xd4F1060cB9c1A13e1d2d20379b8aa2cF7541eD9b` = TWAMM
  - `0x517E506700271AEa091b02f42756F5E174Af5230` = Oracle
  - `0xd4B54d0ca6979Da05F25895E6e269E678ba00f9e` = Boosted Fees
  - `0x0000000000000000000000000000000000000000` = Base CL (no extension)

### 5. V1 Core Status

V1 Core (`0xe0e0e08A6A4b9Dc7bD67BCB7aadE5cF48157d444`) holds ~$717K in stranded funds (EKUBO, LINK, cbBTC, DAI). 62 total lifetime transactions. Deprecated and immutable.

---

## Revised Strategic Assessment

Ekubo EVM is **more valuable than initially appeared** from the prior research:

1. **EUROC/USDC** is the only EUR/USD pair on any dynamic-fee AMM — Algebra doesn't have it, Balancer V3 doesn't have it with hooks. For our EUR cross-rate needs (Angle Transmuter is Mainnet-only mint/burn, not a pool), Ekubo provides a live trading pair with dynamic fees.

2. **XAUt/USDT** is the only gold/USD pair on a dynamic-fee AMM. PAXG/WETH on Uniswap V2 has 70x more TVL but fixed 0.3% fees. Ekubo's dynamic fee on gold captures inflation-driven volatility directly.

3. **Stablecoin diversity** (7 stablecoins) with high vol/TVL ratios means the MEV-capture fee signal updates frequently across multiple USD risk profiles.

4. **The missing piece** is still which pools use MEV-capture vs base CL. If EUROC/USDC and XAUt/USDT use MEV-capture extension, Ekubo EVM immediately becomes the #1 source for FX and inflation volatility signals.

---

## Next Steps

1. **Decode pool keys** to determine extension types — scan PoolInitialized events on Core contract
2. **Build Dune queries** for Ekubo EVM fee dynamics (tick displacement per swap)
3. **Compare EUROC/USDC fee dynamics** against Angle Transmuter agEUR/USDC to see which produces a cleaner EUR/USD signal
4. **Compare XAUt/USDT fee dynamics** against PAXG/WETH (Uniswap V2) volume as gold volatility proxy
