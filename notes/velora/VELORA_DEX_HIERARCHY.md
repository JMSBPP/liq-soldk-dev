# VeloraDEX Adapter Hierarchy for Macro-Risk Signal Extraction

**Generated**: 2026-04-08
**Source**: paraswap-dex-lib adapter source analysis (71 adapters, 20 analyzed in detail)
**Note**: VeloraDEX = ParaSwap (rebranded March 2026, same repo)

Ranking criteria (descending priority): (A) Dynamic fees / novel observables, (B) Multi-token pools, (C) EM stablecoins / gold / EUR / yield-bearing tokens, (D) TVL for clean signals, (E) MEV protection.

---

## Adapter Inventory

### 1. Ekubo V3 (Ethereum + Arbitrum)

- **DEX Key**: `EkuboV3`
- **Chains**: Ethereum Mainnet, Arbitrum
- **AMM Types**: Concentrated liquidity, Full-range (oracle), Stableswap, TWAMM, MEV-capture, Boosted Fees
- **Core Contracts**: Core `0x00000000000014aA86C5d3c41765bb24e11bd701`, Oracle `0x517E506700271AEa091b02f42756F5E174Af5230`, MEV-capture `0x5555fF9Ff2757500BF4EE020DcfD0210CFfa41Be`, TWAMM `0xd4F1060cB9c1A13e1d2d20379b8aa2cF7541eD9b`, Boosted Fees `0xd4B54d0ca6979Da05F25895E6e269E678ba00f9e`
- **Fee Mechanism**: Dynamic MEV-capture fees -- `fee = |tick_displacement| * base_fee / tick_spacing`, capped at uint64 max. Plus boosted fee pools with donate-rate mechanics.
- **Observable Types**: sqrtRatio, tick, liquidity, TWAMM virtual order sale rates + deltas (time-weighted), boosted fee donate rates, MEV-capture tick displacement metrics, oracle snapshots

### 2. Ekubo (Ethereum Mainnet predecessor)

- **DEX Key**: `Ekubo`
- **Chains**: Ethereum Mainnet only
- **AMM Types**: Base concentrated liquidity, Oracle (full-range), TWAMM, MEV-resist
- **Core Contracts**: Core `0xe0e0e08A6A4b9Dc7bD67BCB7aadE5cF48157d444`, Oracle `0x51d02A5948496a67827242EaBc5725531342527C`, TWAMM `0xD4279c050DA1F5c5B2830558C7A08E57e12b54eC`, MevResist `0x553a2EFc570c9e104942cEC6aC1c18118e54C091`
- **Fee Mechanism**: Same tick-displacement dynamic fee as V3 but called "MevResist"

### 3. Balancer V3

- **DEX Key**: `BalancerV3`
- **Chains**: Mainnet, Gnosis, Arbitrum, Base, Optimism, Sonic, Avalanche, Plasma, Sepolia
- **AMM Types**: Weighted, Stable, GyroE (concentrated), QUANT_AMM_WEIGHTED (time-varying weights), RECLAMM (rebalancing CL)
- **Universal Vault**: `0xbA1333333333a1BA1108E8412f11850A5C319bA9` (all chains)
- **Hooks**: StableSurge (dynamic fee surge on stablecoin depeg, V1-V3 variants with up to 50k amp), DirectionalFee (direction-dependent fees), Akron (Arbitrum + Base)
- **QuantAMM**: Time-varying weights updated by `quantAmmUpdateWeightRunnerAddress` on Mainnet (`0x21Ae9576a393413D6d91dFE2543dCb548Dbb8748`) and Arbitrum/Base (`0x8Ca4e2a74B84c1feb9ADe19A0Ce0bFcd57e3f6F7`)
- **reCLAMM**: Rebalancing CL with `dailyPriceShiftBase`, `centerednessMargin`, fourth-root price ratio parameters
- **Observable Types**: balancesLiveScaled18, swapFee, aggregateSwapFee, tokenRates, erc4626Rates, totalSupply, amp factor (stable), weight multipliers + update times (QuantAMM), virtual balances + price shift base (reCLAMM), StableSurge threshold/max fee
- **Multi-token**: YES -- pools support 2-8 tokens

### 4. Balancer V2 + BeetsFi

- **DEX Key**: `BalancerV2`, `BeetsFi`
- **Chains**: Mainnet, Polygon, Arbitrum, Avalanche, Base, Gnosis (V2); Sonic, Optimism (BeetsFi)
- **AMM Types**: Weighted, Stable, PhantomStable, Linear, GyroE, Gyro3
- **Universal Vault**: `0xBA12222222228d8Ba445958a75a0704d566BF2C8`
- **Multi-token**: YES -- weighted pools up to 8 tokens

### 5. Algebra (v1.1, v1.9, v1.9-bidirectional-fee)

- **DEX Key**: `QuickSwapV3` (Polygon), `CamelotV3` (Arbitrum), `SwaprV3` (Gnosis)
- **Chains**: Polygon, Arbitrum, Gnosis
- **AMM Type**: Concentrated liquidity with dynamic fees
- **Fee Mechanism**: v1.1 single dynamic fee; v1.9 directional fees (`feeZto`, `feeOtz` -- separate for zero-to-one and one-to-zero directions); v1.9-bidirectional-fee (SwaprV3) fully bidirectional
- **Observable Types**: sqrtPrice, tick, dynamic fee (single or bidirectional), communityFee (token0/token1), liquidity, tickBitmap, balance0/balance1

### 6. Algebra Integral

- **DEX Key**: `QuickSwapV4` (Base), `BlackholeCL` (Avalanche), `Supernova` (Mainnet)
- **AMM Type**: Concentrated liquidity with plugin-based dynamic fees
- **Fee Mechanism**: Plugin-configurable (pluginConfig field), lastFee tracks current fee, communityFee + communityVault

### 7. Uniswap V4

- **DEX Key**: `UniswapV4`
- **Chains**: Mainnet, Base, Optimism, Arbitrum, Polygon, Avalanche, BSC, Unichain (8 chains)
- **AMM Type**: Concentrated liquidity with hooks architecture
- **PoolManager**: Singleton `0x000000000004444c5dc75cB358380D2e3dE08A90` (Mainnet)
- **Hooks**: Arena hook on Avalanche `0xe32a5d788c568fc5a671255d17b618e70552e044` with feeHelper `0x537505da49b4249b576fc8d00028bfddf6189077`
- **Fee Mechanism**: Per-pool lpFee + protocolFee in slot0. Fee `0x800000` signals dynamic (hook-determined)
- **Observable Types**: sqrtPriceX96, tick, lpFee, protocolFee, feeGrowthGlobal0X128/1X128, liquidity, hook address
- **Notable Pools**: GHO/USDC (Base), USDC/USDT, ETH/USDC, cbBTC/USDC

### 8. Curve (V1 + V1 Factory + V1 Stable NG)

- **DEX Key**: `CurveV1StableNg`, `CurveV1Factory`, `CurveV1`
- **Chains**: StableNG on 8 chains (Mainnet, Polygon, Sonic, Arbitrum, Optimism, Base, Plasma, Gnosis). Factory/V1 on 6 chains.
- **AMM Types**: Stable (StableSwap invariant), Meta pools (USD/BTC base), Plain pools (2/3/4 coins), EMA pools
- **Multi-token**: YES -- up to 4 tokens in plain pools
- **Key Pools**: 3pool, sUSD, sETH, stETH, **EURS**, hBTC, renBTC, sBTC, GUSD, HUSD, sLINK

### 9. Angle Transmuter

- **DEX Key**: `AngleTransmuter`
- **Chains**: Mainnet only
- **AMM Type**: Transmuter (mint/burn against collateral at oracle price with piecewise-linear fees)
- **EUR Stablecoin**: agEUR `0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8`, transmuter `0x00253582b2a3FE112feEC532221d9708c64cEFAb`
- **USD Stablecoin**: USDA `0x0000206329b97DB379d5E1Bf586BbDB969C63274`, transmuter `0x222222fD79264BBE280b4986F6FEfBC3524d0137`
- **Oracle System**: Chainlink + Pyth `0x4305FB66699C3B2702D4d05CF36551390A4c69C6` + Morpho vault + Backed + Redstone (11 OracleReadType variants)
- **Observable Types**: Oracle prices (multi-source), stablecoinsIssued, totalStablecoinIssued, redemption curves, piecewise fee curves, stablecoinCap, whitelist status

### 10. Fluid DEX

- **DEX Key**: `FluidDex`
- **Chains**: Mainnet, BSC, Arbitrum, Polygon, Base, Plasma (6 chains)
- **AMM Type**: Dual-reserve (collateral + debt reserves with imaginary reserves)
- **Contracts**: LiquidityProxy `0x52aa899454998be5b000ad077a46bbe360f4e497`, DexFactory `0x91716C4EDA1Fb55e84Bf8b4c7085f84285c19085`
- **Observable Types**: centerPrice, collateralReserves (real + imaginary per token), debtReserves, dexLimits (available/expandsTo/expandsDuration), fee

### 11. Maverick V2

- **DEX Key**: `MaverickV2`
- **Chains**: Base, Mainnet, BSC, Arbitrum
- **AMM Type**: Directional liquidity bins (4 kinds: static, right, left, both)
- **Fee Mechanism**: Asymmetric fees (feeAIn, feeBIn), lookback parameter for TWA
- **Observable Types**: activeTick, binCounter, reserveA/reserveB, lastTwaD8 (TWA price), lastLogPriceD8, lastTimestamp, bin states

### 12. Solidly Forks

- **DEX Keys**: `Velodrome`, `VelodromeV2`, `Aerodrome`, `Thena`, `Ramses`, `PharaohV1`, `Equalizer`, `Blackhole`
- **Chains**: Optimism, Base, BSC, Arbitrum, Avalanche
- **AMM Type**: xy=k (volatile) + x^3y+xy^3 (stable)
- **Fee Mechanism**: Fixed or dynamic. Blackhole/Aerodrome use dynamic (feeCode=0). Thena: 1bps stable/20bps volatile.

### 13. Uniswap V3 + All Forks

- **DEX Keys**: `UniswapV3`, `SushiSwapV3`, `RamsesV2`, `VelodromeSlipstream`, `AerodromeSlipstream`, `PharaohV3`, `PangolinV3`, `SpookySwapV3`, `AlienBaseV3`, `OkuTradeV3`
- **Chains**: All major chains (11+)
- **Fee Mechanism**: Fixed tiers. Some forks add non-standard tiers.

### 14. PancakeSwap V3 + SwapBasedV3

- **Chains**: Mainnet, BSC, Arbitrum, Base
- **Fee Tiers**: 100, 500, 2500, 10000 bps (SwapBasedV3 adds 35 bps)

### 15. Trader Joe V2.1

- **Chains**: Avalanche only
- **AMM Type**: Liquidity Book (discretized bins with volatility-based variable fees)

### 16. ERC4626 Vaults

- **DEX Keys**: `sDAI`, `wUSDL`, `sUSDe`, `yoETH`, `yoUSD`, `stcUSD`, `fUSDT0`, `eUSDT0`, `waPlaUSDT0`, `wOETH`, `wOUSD`, `wOS`, `wsuperOETHb`
- **Macro-relevant**: sUSDe (Ethena yield), sDAI (MakerDAO DSR), stcUSD (cUSD wrapper -- Celo EM stablecoin). No yoGOLD or yoEUR found yet.

### 17. Camelot V2 (Solidly fork)

- **Chains**: Arbitrum
- **AMM Type**: xy=k with dynamic fees (feeCode 0)

### 18. Solidly V3

- **Chains**: Mainnet only
- **AMM Type**: Concentrated liquidity with tick-spacing-based fees

---

## FINAL RANKED HIERARCHY

### #1 -- Ekubo V3

Ekubo V3 is the most valuable adapter for macro-risk signal extraction. It natively implements four distinct pool extension types beyond vanilla concentrated liquidity: (A) MEV-capture pools with tick-displacement-proportional dynamic fees that directly quantify arbitrage pressure and serve as a realized volatility proxy; (B) TWAMM pools exposing time-weighted average sale rates and future execution deltas -- effectively on-chain order flow data; (C) Oracle pools providing canonical price feeds; (D) Boosted-fee pools with donate-rate token mechanics. The MEV-capture fee formula (`fee = |tick_displacement| * base_fee / tick_spacing`) is a direct analog of the LVR path-dependent integral. Available on Mainnet and Arbitrum.

### #2 -- Balancer V3

Balancer V3 provides the richest multi-dimensional observable set. Its hook architecture produces three novel fee types: StableSurge (dynamic fees that spike during stablecoin depegs -- a direct depeg stress indicator), DirectionalFee (asymmetric fees by swap direction -- reveals directional flow pressure), and Akron hooks. QuantAMM pools have algorithmically time-varying weights, making them the closest on-chain analog to dynamic portfolio rebalancing. reCLAMM pools auto-shift concentrated liquidity ranges with `dailyPriceShiftBase`. Multi-token pools (up to 8 tokens) enable basket-level observables. Boosted pool integration wraps ERC4626 yield-bearing tokens. Deployed on 9 chains.

### #3 -- Algebra + Algebra Integral (Dynamic Fee CL)

Algebra provides the most mature dynamic fee concentrated liquidity implementation across 6 DEX brands. Version 1.9 introduced bidirectional fees (`feeZto`/`feeOtz`) where each swap direction has its own dynamically adjusted fee -- a direct observable of directional flow asymmetry not available in standard UniV3. The bidirectional fee spread (`feeZto - feeOtz`) is a novel signal for directional pressure. Algebra Integral adds a plugin architecture where fee logic is externally configurable via `pluginConfig`.

### #4 -- Angle Transmuter

Despite being Mainnet-only, Angle Transmuter is irreplaceable for EUR stablecoin exposure. It operates agEUR and USDA with piecewise-linear fee curves that reshape based on collateral ratio -- the fee curve shape itself is a macro observable encoding protocol stress. The multi-oracle setup (Chainlink + Pyth + Morpho + Backed + Redstone, 11 OracleReadType variants) provides redundant price feeds. The redemption curve, `stablecoinCap`, and `totalStablecoinIssued` create a rich picture of EUR/USD stablecoin health.

### #5 -- Fluid DEX

Fluid DEX has the most unconventional AMM architecture. Its dual-reserve model (collateral + debt reserves with imaginary components) creates observables no other DEX produces: borrowing demand (`debtReserves`), credit expansion limits (`expandsTo`/`expandsDuration`), and imaginary reserves reflecting synthetic depth. The `centerPrice` tracking across 6 chains makes it valuable for cross-chain credit stress monitoring.

### #6 -- Maverick V2

Maverick V2 exposes directional liquidity positioning through its 4-kind bin system (static, right, left, both) and asymmetric fees (`feeAIn` vs `feeBIn`). The built-in TWA price oracle (`lastTwaD8`/`lastLogPriceD8`) and `lookback` parameter provide native time-weighted pricing without external oracles.

### #7 -- Uniswap V4

Uniswap V4's hooks architecture has the highest theoretical ceiling for novel observables but currently only one production hook is deployed (Arena on Avalanche). The `0x800000` dynamic fee flag enables hook-determined fees. Deployed on 8 chains. Enormous potential but limited current observable richness.

### #8 -- Curve (V1 + V1 Factory + V1 Stable NG)

Curve provides the deepest stablecoin liquidity with multi-token pools (up to 4 coins), meta-pools, and the amplification factor. The EURS pool provides EUR exposure. Virtual price changes encode accumulated fees. Stable NG adds `isStoreRateSupported` for yield-bearing token tracking. Deployed across 8 chains.

### #9 -- Solidly Forks

The Solidly family provides dominant L2 DEX coverage with the stable pool invariant (x^3y + xy^3) that is sensitive to stablecoin depegs. Some forks use dynamic fees. Wide coverage ensures signal availability across chains.

### #10 -- Uniswap V3 + All Forks

Deepest concentrated liquidity coverage. Standard observables are the baseline for any CFMM measurement instrument. No dynamic fees but unmatched TVL.

### #11 -- ERC4626 Vaults

Yield-rate observables encoding monetary policy signals. sUSDe tracks synthetic dollar yield, sDAI tracks DSR, stcUSD wraps cUSD (Celo EM stablecoin relevant).

### #12-18 -- PancakeSwap V3, Trader Joe V2.1, Balancer V2, Maverick V1, Solidly V3, Uniswap V2, Camelot V2

Standard or legacy implementations with diminishing marginal value for macro signal extraction.

---

## Summary Matrix

| Rank | Adapter | Dynamic Fees | Multi-Token | EM/EUR/Gold/Yield | TVL | MEV Protection |
|------|---------|-------------|-------------|-------------------|-----|---------------|
| 1 | Ekubo V3 | MEV-capture + TWAMM + Boosted | No | -- | Med | **YES** |
| 2 | Balancer V3 | StableSurge + DirectionalFee + Hooks | **YES (2-8)** | Yield (boosted) | High | -- |
| 3 | Algebra/Integral | Bidirectional dynamic | No | -- | High | -- |
| 4 | Angle Transmuter | Piecewise-linear on collateral | Multi-collateral | **EUR (agEUR), USD (USDA)** | Med | -- |
| 5 | Fluid DEX | Dynamic + center price | No | -- | Med | -- |
| 6 | Maverick V2 | Asymmetric (feeA/feeB) | No | -- | Med | -- |
| 7 | Uniswap V4 | Hook-based (potential) | No | GHO/USDC | High | Hook-dep. |
| 8 | Curve | Governance + rate store | **YES (2-4)** | **EUR (EURS)**, yield | Highest | -- |
| 9 | Solidly forks | Some dynamic | No | -- | High (L2) | -- |
| 10 | Uniswap V3 | Fixed tiers | No | -- | Highest | -- |
| 11 | ERC4626 | N/A | N/A | sUSDe, sDAI, **stcUSD** | N/A | N/A |

---

## Implementation Priority

**Phase 1 (Immediate)**: Ekubo V3 MEV-capture fee extraction, Balancer V3 hook state monitoring, Algebra bidirectional fee tracking

**Phase 2 (Short-term)**: Angle Transmuter EUR observable pipeline, Fluid DEX debt-reserve monitoring, Maverick V2 directional bin analysis

**Phase 3 (Medium-term)**: Uniswap V4 hook expansion tracking, Curve rate-store integration, Solidly fork L2 coverage

**Phase 4 (Baseline)**: Uniswap V3/V2 price/volume/liquidity baseline across all chains

---

## Key Open PRs (New Integrations)

- **#1098/#1096**: yoGOLD (gold-backed vault) and yoEUR -- directly macro-relevant (inflation proxy + EUR exposure)
- **#1034**: Aegis UniswapV4 hooked stablecoin pool
- **#1160**: Wasabi Prop AMM -- novel "sample-based pricing"
- **#1139**: TrebleSwap -- Algebra v1.2.2 on Base
- **#1151**: RamsesV3 -- CL fork on Arbitrum
- **#1100**: Renegade -- dark pool / privacy DEX
- **#1042**: Pendle PT sUSDe/USDe/eUSDe to USDC -- yield token unwrapping
