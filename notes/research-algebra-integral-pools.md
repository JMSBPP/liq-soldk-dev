
# Algebra Integral DEX Pools: Dynamic Fee Plugin Research

**Date**: 2026-04-03
**Purpose**: Identify Algebra Integral-powered DEX pools with dynamic/adaptive fee plugins where macro-economic information can be extracted from pool observables (price, volume, fees, liquidity).

---

## Executive Summary

Algebra Integral (also referred to as Algebra V4) is a modular AMM architecture deployed across 90+ DEXes on 50+ EVM chains. Its key innovation for our purposes is the **plugin architecture** that separates core pool logic from customizable modules, most critically the **adaptive fee plugin** which adjusts fees based on 24-hour TWAP-derived volatility. This makes the **fee itself a real-time volatility observable** -- exactly what we need for macro-risk hedging instrument design.

**Key findings:**

1. Three major DEXes have the most liquid Algebra-powered pools with dynamic fees: **QuickSwap V3** (Polygon), **Camelot V3** (Arbitrum), and **THENA FUSION** (BNB Chain).
2. QuickSwap V3 has the highest aggregate TVL (~$50M+ in V3 pools) with dynamic fees enabled by default on all pools.
3. THENA FUSION has the most interesting dynamic fee implementation post-V3,3 upgrade (May 2025) with plugin-based fee governance.
4. **No Algebra-powered DEX currently lists emerging-market stablecoin pairs** (cCOP, cNGN, BRZ, etc.) with meaningful liquidity. These pairs exist primarily on Celo-native DEXes or Uniswap V3 deployments.
5. Gold-backed token pools (PAXG, XAUT) are not present on Algebra-powered DEXes; they primarily trade on Uniswap V3 Ethereum mainnet.

---

## 1. Algebra Integral Architecture: What Matters for Observable Extraction

### Version History

| Version Label | Architecture | Plugin Support | Key DEX Users |
|---|---|---|---|
| Algebra V1.0 | Monolithic (like Uni V3) | No plugins, built-in adaptive fee | QuickSwap Polygon |
| Algebra V1.9 | Monolithic, improved | No plugins, built-in adaptive fee | Camelot V3, Lynex, Swapbased |
| Algebra Integral 1.0 (V4) | Modular Core + Plugins | Yes | SwapX (Sonic), Kim (Mode) |
| Algebra Integral 1.2 (V4 latest) | Modular Core + Plugins, improved | Yes | Camelot V4, THENA V3,3 |

**Important clarification on "B1, B2"**: These labels do not appear in Algebra's official documentation. The versions are v1.0, v1.9 (monolithic) and Integral 1.0, 1.2 (modular plugin). "B1/B2" may be internal designations.

### Plugin Types Relevant to Observable Extraction

| Plugin | What It Does | Observable Value |
|---|---|---|
| **Adaptive Fee (Standard Plugin)** | Adjusts fee based on 24h TWAP volatility | Fee level = realized volatility proxy |
| **Sliding Fee** | Asymmetric fee based on trade direction vs price movement | Fee spread = directional pressure indicator |
| **TWAP Oracle (Standard Plugin)** | Records price/tick history per block | Historical price path |
| **Brevis ZK Dynamic Fee** | Fee discount based on ZK-verified trading history | Volume-weighted fee = user-type segmentation |

**Critical constraint**: Only one plugin can be attached per pool at a time. The Standard Plugin bundles TWAP Oracle + Adaptive Fee + Farming Proxy together.

### How the Adaptive Fee Works (The Key Observable)

1. Uses TWAP oracle data about price changes over the last 24 hours
2. Calculates volatility as a 24-hour average (smoothed)
3. Applies a sigmoid-based fee function with tunable parameters (alpha, gamma, beta)
4. Updates fee on every swap via the `beforeSwap` hook
5. Fee increases in volatile markets, decreases in calm markets

The dynamic fee is effectively a **24-hour realized volatility oracle** updated on every swap. Combined with volume data, it captures: capital flight (sudden volume + fee spikes on stablecoin pairs), FX depreciation pressure (sustained fee elevation), and interest rate shocks (fee regime changes on yield-bearing token pairs like wstETH/ETH).

Algebra also provides `IntegralFeeSimulation` ([GitHub](https://github.com/cryptoalgebra/IntegralFeeSimulation)) for backtesting adaptive fee behavior against historical data.

---

## 2. DEX-by-DEX Pool Inventory

### 2.1 QuickSwap V3 -- Polygon PoS

- **Algebra version**: V1.0 (monolithic, built-in adaptive fee)
- **V4 upgrade**: Proposed via governance March 2025, outcome unclear
- **Overall TVL**: ~$50M+ in V3 | **Daily volume**: ~$11.5M
- **Dynamic fee**: YES -- all pools by default
- **Fee split**: 90% LPs, 6.8% QUICK stakers, 1.7% Foundation, 1.5% devs

**Major Pairs (crypto volatility proxy)**

| Pair | Pool Address | TVL | 24h Vol | Fee |
|---|---|---|---|---|
| WBTC/WETH | `0xac4494e30a85369e332bdb5230d6d694d4259dbc` | ~$1.07M | ~$139K | 0.04% dynamic |
| USDC/WETH | `0xa6aedf7c4ed6e821e67a6bfd56fd1702ad9a9719` | ~$212K | ~$402K | 0.088% dynamic |
| WPOL/WETH | `0xadbf1854e5883eb8aa7baf50705338739e558e5b` | ~$442K | ~$10K | Dynamic |
| WMATIC/USDT | `0x604229c960e5cacf2aaeac8be68ac07ba9df81c3` | ~$210K | ~$1.75M | Dynamic |

**Stablecoin Pairs**

| Pair | Pool Address | TVL | 24h Vol | Fee |
|---|---|---|---|---|
| USDC/USDT | `0x2cf7252e74036d1da831d11089d326296e64a728` | ~$1.03M | ~$15K | Dynamic |

No emerging-market stablecoin, gold-backed, or yield-bearing token pairs found.

### 2.2 Camelot V3/V4 -- Arbitrum

- **Algebra version**: V1.9 (V3), upgrading to Integral 1.2 (V4)
- **Overall TVL**: ~$30M+ | **Daily volume**: ~$41.3M
- **Dynamic fee**: YES -- directional and volatility-based
- **Fee split**: 80% LPs, 17% xGRAIL, 3% protocol

**Yield-Bearing (interest rate observable)**

| Pair | Pool Address | TVL | Fee |
|---|---|---|---|
| wstETH/WETH | `0xdeb89de4bb6ecf5bfed581eb049308b52d9b2da7` | ~$67K | 0.005% dynamic |
| wstETH/WETH (older) | `0x5201f6482eea49c90fe609ed9d8f69328bac8dda` | ~$74K | Dynamic |

**Major Pairs**

| Pair | Pool Address | TVL | Fee |
|---|---|---|---|
| WETH/USDC | `0xb1026b8e7276e7ac75410f1fcbbe21796e8f7526` | ~$2.26M | Dynamic |
| ARB/WETH | `0xe51635ae8136abac44906a8f230c2d235e9c195f` | ~$549K | Dynamic |
| ARB/USDC | `0xfae2ae0a9f87fd35b5b0e24b47bac796a7eefea1` | ~$310K | 0.075% dynamic |
| GMX/USDC | `0xb79af3dadc07e905a148b14382fe8ed7528623f2` | Variable | Dynamic |

### 2.3 THENA FUSION -- BNB Chain

- **Algebra version**: Moving to Integral 1.2 (V3,3 upgrade, May 2025)
- **Overall TVL**: ~$8.3M total | **Daily volume**: ~$9.5M (FUSION only)
- **Dynamic fee**: YES -- volatility + sliding fee plugins available

**Major Pairs**

| Pair | Pool Address | TVL | Fee |
|---|---|---|---|
| ETH/WBNB | `0x1123e75b71019962cd4d21b0f3018a6412edb63c` | ~$5.92M | 0.187% dynamic |
| BTCB/WBNB | `0x6b67112aa7b45e8cdc0a93b8d66a6a36e68ae8e5` | Variable | Dynamic |

**Stablecoin Pairs**

| Pair | Pool Address | TVL | 24h Vol | Fee |
|---|---|---|---|---|
| USDT/USDC | `0x618f9eb0e1a698409621f4f487b563529f003643` | ~$1.92M | ~$37.7M | 0.001% dynamic |
| HAY/USDT | `0x5b0baf66718caabda49a4af32eb455c3b99b5821` | ~$255K | ~$672K | 0.01% dynamic |

**Liquid Staking**

| Pair | Pool Address | TVL | Fee |
|---|---|---|---|
| ankrBNB/WBNB | `0x2f6c6e00e517944ee5efe310cd0b98a3fc61cb98` | ~$171K | 0.01% dynamic |

### 2.4-2.7 Smaller DEXes

- **SwapX (Sonic)**: Integral 1.0, $612K total TVL -- too small, skip for now
- **Kim (Mode)**: Integral 1.0, sparse data -- skip
- **Lynex (Linea)**: V1.9, ~$15M peak TVL -- monitor
- **Others** (Swapsicle, Hercules, Fenix, StellaSwap, Hydrex, TONCO, Yaka): All low TVL or pre-launch

---

## 3. Consolidated Priority Ranking

### Tier 1: Best Candidates (Use Now)

| # | Pool | DEX | Chain | TVL | Vol/Day | Macro Signal |
|---|---|---|---|---|---|---|
| 1 | USDT/USDC | THENA FUSION | BNB | $1.92M | $37.7M | USD monetary policy divergence, stablecoin stress |
| 2 | ETH/WBNB | THENA FUSION | BNB | $5.92M | Variable | Crypto/BNB value, SE Asian capital flows |
| 3 | WETH/USDC | Camelot V3 | Arbitrum | $2.26M | Variable | Primary ETH/USD volatility |
| 4 | WBTC/WETH | QuickSwap V3 | Polygon | $1.07M | $139K | BTC/ETH relative, risk-on/off |
| 5 | USDC/USDT | QuickSwap V3 | Polygon | $1.03M | $15K | USD stablecoin peg stress |

### Tier 2: Usable with Caveats

Pools 6-10: ARB/WETH ($549K), WPOL/WETH ($442K), ARB/USDC ($310K), HAY/USDT ($255K), USDC/WETH on QuickSwap ($212K)

### Tier 3: Monitor

wstETH/WETH on Camelot ($67-74K -- signal type is extremely valuable despite low TVL), ankrBNB/WBNB on THENA ($171K)

### Tier 4: Missing but Would Be Highest Priority

cCOP/cUSD, cNGN/cUSD, BRZ/USDC, PAXG/USDC, wstETH/USDC, sDAI/USDC, MXNB/USDC, PUSO/USDC -- **none exist on Algebra-powered DEXes**.

---

## 4. Technical: Reading Dynamic Fee Data On-Chain

**V1.0/V1.9 pools** (QuickSwap, Camelot V3): Call `globalState()` on the pool contract for current fee. Historical data requires indexing `Swap` events.

**Integral 1.0/1.2 pools** (THENA V3,3, SwapX, Camelot V4): Call `plugin()` on the pool to get plugin address, then query the plugin for current fee and TWAP oracle data via `timepoints()`.

**Key events to index**: `Swap(...)` for price/volume, `Fee(fee)` or `ChangeFee(fee)` for dynamic fee changes (Integral only), `Collect(...)` for fee collection.

---

## 5. Recommendations

**Immediate**: Start with THENA FUSION USDT/USDC (`0x618f9...`) -- its 19.6x daily volume/TVL ratio means extremely frequent fee updates, producing a high-resolution volatility signal. Correlate with Fed rate decisions, Tether reserve announcements, and stablecoin de-peg events.

**Medium-term**: Explore deploying a custom Algebra Integral pool with a plugin that records fee history and emits macro-relevant events. The [Algebra Plugin Template](https://github.com/cryptoalgebra/algebra-plugin-template) provides scaffolding.

**Strategic gap**: No Algebra DEX has emerging-market stablecoin liquidity. **Possible approach**: Use Algebra pools as cross-market volatility oracles (ETH/USD, BTC/USD, stablecoin stress) while using Celo Uniswap V3 pools for actual cCOP/cUSD prices. The Algebra dynamic fee provides the volatility dimension that Uniswap V3 lacks natively.
