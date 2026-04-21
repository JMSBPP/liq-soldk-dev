# Ekubo Protocol Deep Dive

**Date**: 2026-04-08
**Context**: Ranked #1 in VeloraDEX adapter hierarchy for macro-risk signal extraction
**Purpose**: Full technical assessment for hedging instrument settlement on CFMM observables

---

## Executive Summary

Ekubo is a singleton-architecture concentrated liquidity AMM founded by Moody Salem (Uniswap Labs employee #5, chief engineer April 2020 -- May 2022, contributor to Uniswap V3, led V4 design). 
It originated on Starknet (mainnet August 2023), commands 60-70% of Starknet DeFi TVL, and expanded to EVM chains (Ethereum mainnet + Arbitrum) in 2025 as V2/V3. It is the same team -- NOT a fork.

The protocol's core innovation is its **extension system** -- external contracts callable at lifecycle hooks (beforeSwap, afterPositionUpdate) that can re-enter the core contract. This predates and inspired Uniswap V4 hooks. First-party extensions include: Oracle (TWAP), TWAMM (DCA orders), MEV-capture/MEV-resist (dynamic fees proportional to tick displacement), and Boosted Fees (donate-rate mechanics).

**Critical finding for our project**: The MEV-capture fee formula `fee = |tick_displacement| * base_fee / tick_spacing` is confirmed in the VeloraDEX adapter source. This produces a per-swap fee that scales linearly with price movement magnitude -- a direct discrete approximation of the continuous-time LVR integral (sum of delta_tick^2 terms). The fee trajectory IS a realized volatility signal without any additional computation.

**Risk assessment**: Ekubo EVM TVL is still small (~$20M on Ethereum), though volume/TVL ratio exceeds 
30x on peak days. The protocol is young on EVM (live since early 2025). The Starknet deployment is mature but Starknet itself has limited liquidity. For macro signal extraction, 
the signal quality is excellent but the TVL depth means the signal may be noisy for illiquid pairs.

---

## 1. Protocol Overview

### History and Team

- **Founder**: Moody Salem. 5th employee and Chief Engineer at Uniswap Labs (April 2020 -- May 2022). Wrote much of the Uniswap web interface, created the token-lists standard, built the first V2/V3 routing algorithm. Contributed to V3, led V4 design.
- **Company**: Ekubo, Inc. Intentionally small, engineering-focused. Under contract with the Ekubo DAO to continue development until at least July 28, 2026.
- **Advisors**: Uri Kolodny (StarkWare co-founder), Sylve Chevet (Briq CEO), Itamar Lesuisse (Argent co-founder), Mentor Reka (AVNU CEO).
- **Funding**: 6 million STRK grant (~$3.1M) from Starknet Foundation. Uniswap community approved a $12M investment (3M UNI tokens, $60M valuation), but Ekubo ultimately declined the deal, choosing independence.
- **Starknet launch**: August 26, 2023 (mainnet).
- **EVM expansion**: 2025. V2 launched on Ethereum first, V3 followed on Ethereum + Arbitrum.

### Starknet vs EVM Relationship

**Same team, same protocol.** Ekubo originated on Starknet (Cairo contracts). The EVM deployment is a port of the same architecture by the same team. The codebase was made EVM-compatible and can be deployed to any major EVM chain. The official interface at ekubo.org serves Ethereum, Arbitrum, and Starknet.

### Current Status and TVL

- **Starknet**: 60-70% of Starknet AMM TVL (~$85M post-rewards). $18M daily volume. Dominant DEX on the chain.
- **Ethereum**: ~$20M TVL but extraordinary capital efficiency -- daily volume has topped $700M, placing it in top 3 AMMs by 24h volume behind Uniswap and Fluid. Volume/TVL ratio above 30x on peak days.
- **Arbitrum**: First EVM L2 deployment. Nascent but growing.
- **Planned chains**: Base, BSC, HyperEVM (Hyperliquid), Sonic, Monad.

### Governance

- **EKUBO token**: ERC-20 on Ethereum L1, bridged to Starknet. Total supply: 10,000,000.
- **Distribution**: 1/3 airdrop, 1/3 team (Ekubo Inc.), 1/3 sold by DAO for ETH/USDC/STRK via DCA orders.
- **DAO**: Fully on-chain governance (OpenZeppelin Governor standard). Core contract ownership irrevocably transferred to DAO. Over 40% of governance proposals come from the community.
- **Revenue model**: Withdrawal fees (see Section 2) accumulate in core contract, withdrawable by DAO. Currently 100% directed to EKUBO buyback program.

---

## 2. Architecture

### Core Design: Singleton + Flash Accounting

Ekubo uses a **singleton architecture** -- one core contract for ALL pools on a given chain. This is the same design pattern as Uniswap V4's PoolManager, but Ekubo shipped it first.

**Key contracts (V3 EVM -- same address on all EVM chains)**:
- Core: `0x00000000000014aA86C5d3c41765bb24e11bd701`
- Oracle extension: `0x517E506700271AEa091b02f42756F5E174Af5230`
- MEV-capture extension: `0x5555fF9Ff2757500BF4EE020DcfD0210CFfa41Be`
- TWAMM extension: `0xd4F1060cB9c1A13e1d2d20379b8aa2cF7541eD9b`
- Boosted Fees extension: `0xd4B54d0ca6979Da05F25895E6e269E678ba00f9e`

**Key contracts (V2 EVM -- Ethereum only, predecessor)**:
- Core: `0xe0e0e08A6A4b9Dc7bD67BCB7aadE5cF48157d444`
- Oracle: `0x51d02A5948496a67827242EaBc5725531342527C`
- TWAMM: `0xD4279c050DA1F5c5B2830558C7A08E57e12b54eC`
- MevResist: `0x553a2EFc570c9e104942cEC6aC1c18118e54C091`

**Till pattern (flash accounting)**: When you swap or update a position, token transfers are deferred until the end of the transaction. You can execute many actions across many pools and only make the minimum number of token transfers at settlement. This is identical to Uniswap V4's flash accounting.

Benefits:
- Pool creation ~99% cheaper (no new contract deployment)
- Swaps ~50% cheaper (fewer storage writes, no inter-pool transfers)
- Multi-hop routes settle with only 2 token transfers total

### Concentrated Liquidity

Ekubo implements concentrated liquidity with the x*y=k formula within regions of constant liquidity, identical in principle to Uniswap V3. However:

- **Tick size**: 1.000001 (1/100th of a basis point) -- 100x finer than Uniswap V3's 1.0001.
- **Price formula**: `sqrt_ratio_x128 = 1.000001^(tick/2) * 2^128` (64.128 fixed point number).
- **Tick spacing**: Configurable per pool. Higher tick_spacing for volatile pairs (cheaper swaps, fewer boundary crossings).
- **Capital efficiency claim**: $1,000 in Ekubo works as well as $100,000 in the next best AMM, due to finer ticks.

### Pool Key Structure

A pool is identified by a **pool key** tuple:
- `token0`, `token1`: The token pair (sorted)
- `fee`: 0.128 fixed point number. E.g., 0.05% = `floor(0.0005 * 2^128)`
- `tick_spacing`: Minimum space between position boundaries
- `extension`: Address of the extension contract (or zero for vanilla pools)

The extension field in the pool key is what makes the system powerful -- different extensions create fundamentally different pool types while sharing the same liquidity infrastructure.

### Pool State

Each pool's state consists of:
- `sqrt_ratio`: Square root of current price (token1/token0), as 64.128 fixed point
- `liquidity`: Amount of tokens available for trading at the current price
- `tick`: Current tick derived from sqrt_ratio

### Extension System (vs Uniswap V4 Hooks)

Extensions are external contracts callable at pool lifecycle hooks:
- `beforeSwap`
- `afterSwap` (implied by the re-entrancy capability)
- `beforeUpdatePosition` / `afterPositionUpdate`

**Critical difference from Uniswap V4**: Extensions can **re-enter the core contract** to perform their own actions within lifecycle events. This means an extension triggered by a swap can itself perform swaps, update positions, or interact with other pools -- enabling far richer composability than simple hook callbacks.

**Permissionless deployment**: Anyone can deploy a new extension contract and create pools that use it. No governance approval needed. The extension integrates into the same ecosystem of aggregators and interfaces.

### Anti-JIT Withdrawal Fee

Unique to Ekubo: when removing liquidity, you pay a fee equal to the pool's swap fee, taken from your principal (not from earned fees). Example: 0.3% pool fee means removing $10,000 costs $30.

This makes JIT liquidity attacks economically unviable -- the withdrawal fee exactly cancels the swap fee a JIT provider would earn, resulting in zero profit minus gas. Long-term LPs amortize this cost over many periods of fee collection.

Withdrawal fees are collected by the core contract and directed to the DAO.

### Comparison to Uniswap V3/V4

| Feature | Ekubo V3 | Uniswap V3 | Uniswap V4 |
|---------|----------|------------|------------|
| Architecture | Singleton | Factory (1 contract/pool) | Singleton |
| Flash Accounting | Yes (till pattern) | No | Yes |
| Tick Granularity | 1.000001 (1/100 bp) | 1.0001 (1 bp) | 1.0001 (1 bp) |
| Extension/Hook System | Yes (re-entrant) | No | Yes (non-re-entrant) |
| Dynamic Fees | Via extensions (MEV-capture, etc.) | No (fixed tiers) | Via hooks |
| TWAMM | First-party extension | N/A | Community hooks |
| Oracle | First-party extension | Built-in (removed in V4) | Via hooks |
| Anti-JIT | Withdrawal fee | None | Via hooks |
| Stableswap | Yes (native pool type) | No | Via hooks |

---

## 3. MEV-Capture Fee Mechanism (CRITICAL)

### The Formula

From the VeloraDEX paraswap-dex-lib adapter:

```
fee = |tick_displacement| * base_fee / tick_spacing
```

Capped at uint64 max.

### How It Works

The MEV-capture extension (address `0x5555fF9Ff2757500BF4EE020DcfD0210CFfa41Be` on V3) implements a dynamic fee that is **proportional to the magnitude of price movement caused by the swap**.

- **tick_displacement**: The absolute difference between the tick before and after the swap. This measures how far the price moved.
- **base_fee**: A configurable parameter for the pool, set at pool creation.
- **tick_spacing**: The pool's tick spacing parameter.

### Per-Swap vs Cumulative

The tick_displacement is computed **per swap** -- it is the absolute change in tick from the start to the end of that specific swap. It is NOT cumulative across blocks.

### Why This Is a Realized Volatility Proxy

The LVR (Loss-Versus-Rebalancing) integral in continuous time is:

```
LVR = integral of (sigma^2 / 8) * L * S dt
```

In discrete time, this becomes a sum of squared price changes. The Ekubo MEV-capture fee captures |delta_tick| per swap. While LVR is quadratic in price change, the fee is linear in |delta_tick|. However:

1. **The fee trajectory over time** (sequence of per-swap fees) encodes the magnitude of each price movement.
2. **Squaring the fee** (after dividing out base_fee/tick_spacing) gives you the per-swap contribution to realized variance.
3. **Summing squared fees over a window** gives you realized variance directly.

Formula for realized variance extraction:

```
RV(T) = sum over swaps in [0,T] of (fee_i * tick_spacing / base_fee)^2
```

This is fundamentally different from Algebra's approach (24h TWAP of some volatility estimator used to SET fees) or Uniswap V4 hooks (arbitrary logic, no standard). Ekubo's MEV-capture fee is not trying to estimate volatility to set an optimal fee -- it is literally measuring the per-swap price impact and charging proportionally. The fee IS the measurement.

### Comparison to Algebra Dynamic Fees

| Aspect | Ekubo MEV-Capture | Algebra v1.1/v1.9 |
|--------|-------------------|---------------------|
| Fee computation | `|delta_tick| * base_fee / tick_spacing` | TWAP-based volatility estimator over 24h window |
| Granularity | Per-swap, real-time | Smoothed over hours |
| Directionality | Magnitude only | v1.9: bidirectional (feeZto, feeOtz) |
| Signal type | Instantaneous price impact | Smoothed realized volatility |
| Observable for us | Raw per-swap delta_tick -> realized variance | Fee level -> smoothed vol estimate |
| Latency | Zero (fee = measurement) | Hours (TWAP lag) |

**Verdict**: For building a realized volatility oracle, Ekubo MEV-capture is strictly superior in signal granularity. Algebra's bidirectional fees add directional information Ekubo lacks, but for volatility measurement, Ekubo's instantaneous per-swap tick displacement is the atomic observable we need.

### Comparison to Uniswap V4 Hook-Based Dynamic Fees

Uniswap V4 hooks CAN implement any fee logic, including MEV-capture. But currently only one production hook exists (Arena on Avalanche). Ekubo ships MEV-capture as a first-party production extension. The theoretical ceiling is equal; the practical deployment is not.

### On-Chain Fee Storage and Queryability

The fee is applied during the swap and reflected in the swap output amounts. The per-swap fee is NOT stored separately on-chain as a historical time series. However:

1. **Events**: The swap event emits the tick before and after, from which tick_displacement can be reconstructed.
2. **Indexer**: Ekubo provides an open-source indexer (https://github.com/EkuboProtocol/indexer) that stores all events in Postgres. The indexer runs on both Starknet and EVM chains.
3. **On-chain state**: The current sqrt_ratio and tick are readable from the Core contract at any time.

To build a historical fee/volatility series, you would index swap events and compute `|tick_after - tick_before|` for each swap.

---

## 4. TWAMM Extension

### How It Works

TWAMM (Time-Weighted Average Market Maker) shows up in the Ekubo interface as "DCA orders" and "DCA-enabled pools."

- A DCA order is an order to sell a token at a **specified rate** between a start and end time.
- The TWAMM extension breaks the large order into infinitely small virtual orders executed continuously over the specified period.
- In practice, execution happens up to once per block (~30 seconds on Starknet, ~12 seconds on Ethereum).
- Orders on both sides of a DCA-enabled pool are **netted against each other**, and only the difference is swapped against the pool to compute the resulting price.

### Extension Address

- V3 EVM: `0xd4F1060cB9c1A13e1d2d20379b8aa2cF7541eD9b`
- V2 EVM: `0xD4279c050DA1F5c5B2830558C7A08E57e12b54eC`

### Virtual Order Sale Rates

Each DCA-enabled pool tracks:
- **Sale rate per direction**: How many tokens per unit time are being sold from token0->token1 and token1->token0.
- **Deltas**: Changes in sale rates at specific future timestamps (when orders start or end).

These are the "virtual order sale rates" referenced in the VeloraDEX adapter. They represent the aggregate intent to buy/sell over time, which is distinct from spot order flow.

### Observables from TWAMM State

1. **Net sale rate imbalance**: `sale_rate_0to1 - sale_rate_1to0` encodes directional buying/selling pressure over the medium term (hours to weeks).
2. **Sale rate deltas at future timestamps**: Tells you when large DCA orders begin and end -- forward-looking order flow information.
3. **Execution prices**: The realized execution price of TWAMM orders vs spot price shows the cost of TWAMM execution and informs about pool liquidity depth.
4. **Total DCA volume**: Aggregate capital being DCA'd through the pool signals sustained directional conviction.

### Comparison to Uniswap V4 TWAMM

Uniswap V4 has a community TWAMM hook, but it is not a first-party production extension. Ekubo's TWAMM was the first extension deployed (April 2024 on Starknet) and is production-grade. The design is architecturally similar but Ekubo's is more mature and integrated into aggregator routing.

### Macro Signal Value

TWAMM sale rates are one of the most unique observables in all of DeFi. No other major DEX produces on-chain, time-weighted aggregate order flow data. For macro hedging instruments:

- A rising sale rate of USDC->ETH in TWAMM pools signals sustained ETH accumulation (bullish flow).
- Net imbalance in stablecoin DCA pools could encode capital flight signals for EM stablecoin pairs.
- The time profile of future deltas reveals when large players are scheduling their exits/entries.

---

## 5. Oracle Extension

### Mechanism

The Oracle extension implements a **permissionless, manipulation-resistant TWAP oracle** for any pair tradeable on Ekubo.

- **One oracle pool per pair** with parameters: fee = 0, tick_spacing = MAX_TICK_SPACING.
- **Only full-range positions** are allowed (to support all possible prices).
- These parameters maximize oracle precision and cost-to-manipulate.

### Accumulator

The oracle collects snapshots of a **cumulative tick accumulator** (identical in concept to Uniswap V3's tick accumulator). The arithmetic mean of tick values over a time period corresponds to the **geometric mean price** (TWAP).

### Extension Address

- V3 EVM: `0x517E506700271AEa091b02f42756F5E174Af5230`
- V2 EVM: `0x51d02A5948496a67827242EaBc5725531342527C`

### If an `oracle_token` is defined

All oracle pools must be paired with that token, and price fetching methods use it as an intermediate for computing all prices. This creates a hub-and-spoke oracle topology.

### Comparison to Uniswap V3 Oracle

Functionally equivalent (cumulative tick accumulator -> TWAP). Uniswap V3's oracle was built into the core; Ekubo separates it as an extension. Uniswap V4 removed the built-in oracle entirely (moved to hooks). Ekubo's approach is architecturally cleaner -- the oracle is a first-class extension, not embedded in core or relegated to a community hook.

### On-Chain Queryability

External contracts can compute TWAP prices over custom time periods by querying the accumulated tick values from the extension's snapshots. The Starknet oracle extension code is open source at https://github.com/EkuboProtocol/oracle-extension.

---

## 6. Boosted Fees Extension

### Extension Address (V3 EVM)

`0xd4B54d0ca6979Da05F25895E6e269E678ba00f9e`

### Mechanism

The Boosted Fees extension allows external parties to **donate tokens** to a pool's fee distribution, boosting the effective APR for LPs beyond what swap fees alone provide.

Key characteristics:
- **Donate rate**: External parties can deposit tokens at a configurable rate that gets distributed to LPs proportionally.
- **Zero-fee pools**: The existence of zero-fee pools (fee = 0) enables extensions like TWAMM and limit orders without additional swap fees. Boosted Fees can make these zero-fee pools attractive to LPs by providing external fee injection.
- **Incentive alignment**: Protocols can bootstrap liquidity in specific pools by donating tokens, effectively creating a targeted liquidity mining program without modifying the core AMM.

### Observables

1. **Donate rate per pool**: Measures external capital inflow to incentivize liquidity -- higher donate rates signal protocol-level demand for that pool's liquidity.
2. **Donate rate changes over time**: Rising/falling donation rates signal changing liquidity demand.
3. **Ratio of donated fees to swap fees**: High ratio means the pool is externally subsidized (fragile liquidity); low ratio means organically profitable.

### Macro Signal Value

Limited direct macro value. Boosted fees primarily encode protocol-level incentive dynamics rather than market-level price/volatility information. However, a sudden drop in boosted fee rates could signal protocol stress or reduced commitment to maintaining liquidity in a pair.

---

## 7. Deployed Pools

### Starknet (Primary Chain)

Ekubo dominates with 60-70% of Starknet AMM TVL. Major pairs:
- **ETH/USDC**: ~21.38% APR, highest volume
- **USDC/USDT**: ~18.84% APR, stablecoin base
- **DAI/USDC**: Active stablecoin pair
- **rETH/wstETH**: Yield-bearing pair
- **STRK/ETH**: Native Starknet token pair
- **EKUBO/ETH**: Governance token pair

### Ethereum (EVM V3)

~$20M TVL but $700M+ daily volume on peak days (top 3 by volume).
- **USDC/USDT**: Stablecoin pair with stableswap curve
- **ETH/USDC**: Major trading pair
- Key positions visible at ekubo.org/evm/positions

### Arbitrum (EVM V3)

First EVM L2. Nascent liquidity, growing.

### Pool Creation

**Fully permissionless.** Anyone can create a pool with any token pair, fee, tick_spacing, and extension combination. No governance approval needed.

### Macro-Relevant Pairs

- **Stablecoin pairs** (USDC/USDT, DAI/USDC): Depeg detection
- **Yield-bearing pairs** (rETH/wstETH): Yield differential signals
- **No EM stablecoins** found on Ekubo (no cCOP, cUSD, cEUR, agEUR on Ekubo -- agEUR is on Angle Transmuter instead)
- **No gold tokens** found on Ekubo currently

---

## 8. Observable Extraction for Macro Signals

### Complete Inventory of On-Chain Readable State

**From Core contract (per pool)**:
1. `sqrt_ratio` (64.128 fixed point) -- current price
2. `tick` -- current tick index
3. `liquidity` -- active liquidity at current price
4. `call_points` -- extension callback configuration

**From Oracle extension (per oracle pool)**:
5. Cumulative tick accumulator snapshots -- for computing TWAP over any window

**From TWAMM extension (per DCA-enabled pool)**:
6. Sale rate token0->token1
7. Sale rate token1->token0
8. Future deltas (sale rate changes at scheduled timestamps)

**From MEV-capture extension (derived from swap events)**:
9. Per-swap tick_displacement = |tick_after - tick_before|
10. Effective fee = tick_displacement * base_fee / tick_spacing

**From Boosted Fees extension (per boosted pool)**:
11. Donate rate per token direction

### Events Emitted Per Swap

The Core contract emits swap events containing:
- Pool key (token0, token1, fee, tick_spacing, extension)
- sqrt_ratio before and after
- tick before and after (from which tick_displacement is derived)
- Amount0 and amount1 deltas
- Liquidity at time of swap

### Events Emitted Per Position Change

Position update events containing:
- Pool key
- Owner / position ID
- Lower tick, upper tick
- Liquidity delta (positive = add, negative = remove)

### How to Build a Realized Volatility Oracle from MEV-Capture Fees

**Step-by-step pipeline**:

1. **Index swap events** for MEV-capture pools (extension = `0x5555fF9Ff2757500BF4EE020DcfD0210CFfa41Be`).
2. **Extract tick_displacement** = |tick_after - tick_before| for each swap.
3. **Convert to log-price change**: Since tick = log_{1.000001}(price), delta_tick * ln(1.000001) ~= delta_tick * 1e-6 gives the log-return.
4. **Compute rolling realized variance**: RV(T) = sum(delta_tick_i^2) * (1e-6)^2 over window T.
5. **Annualize**: Multiply by (seconds_per_year / window_seconds).
6. **Alternatively**: Use the fee directly. fee_i = delta_tick_i * base_fee / tick_spacing. Then RV(T) = sum((fee_i * tick_spacing / base_fee)^2) * (1e-6)^2.

This is functionally equivalent to computing realized variance from high-frequency trade data, but the data comes from on-chain swap events rather than centralized exchange ticks.

### How TWAMM Sale Rates Encode Order Flow

- **Net directional flow** = sale_rate_0to1 - sale_rate_1to0 (in token-normalized units).
- **Time-weighted**: Sale rates are sustained over hours/days/weeks, filtering out noise.
- **Forward-looking**: Future deltas reveal scheduled order starts/ends.
- **Aggregated**: All DCA orders for the same pair are netted, providing a clean aggregate signal.

### Comparison of Observable Richness

| Observable Type | Ekubo | Uniswap V3 | Algebra | Balancer V3 |
|----------------|-------|------------|---------|-------------|
| Spot price (sqrt_ratio/tick) | Yes | Yes | Yes | Yes (via balances) |
| Active liquidity | Yes | Yes | Yes | Yes (balancesLiveScaled18) |
| TWAP oracle | Extension | Built-in | No | No |
| Per-swap tick displacement | Yes (MEV-capture) | Derivable from events | No (fee is smoothed) | No |
| Dynamic fee level | Yes (= tick displacement) | No (fixed) | Yes (smoothed) | Yes (hooks: StableSurge, DirectionalFee) |
| TWAMM sale rates | Yes (extension) | No | No | No |
| TWAMM future deltas | Yes | No | No | No |
| Directional fee split | No | No | Yes (v1.9: feeZto/feeOtz) | Yes (DirectionalFee hook) |
| Multi-token pool state | No (pairs only) | No | No | Yes (2-8 tokens) |
| Withdrawal fee | Yes (= swap fee) | No | No | No |
| Boosted/donated fee rate | Yes (extension) | No | No | No |

---

## 9. Strategic Assessment

### Is Ekubo Actually Better Than Algebra for Volatility Signal Extraction?

**Yes, for instantaneous realized volatility. No, for directional flow.**

Ekubo advantages:
- Per-swap tick displacement is the atomic unit of realized variance. No smoothing, no lag.
- The fee formula mechanically encodes |delta_tick| -- no estimation, no oracle dependency.
- TWAMM adds a unique order flow dimension no other DEX provides.
- Oracle extension provides clean TWAP baseline.

Algebra advantages:
- Bidirectional fees (feeZto vs feeOtz) encode directional flow asymmetry. Ekubo MEV-capture is magnitude-only.
- Algebra is deployed on more chains via more brands (QuickSwap, Camelot, SwaprV3).
- Algebra pools have deeper liquidity on Arbitrum (Camelot) than Ekubo currently.
- More mature on EVM -- Ekubo EVM is still early.

**Recommendation**: Use BOTH. Ekubo for realized variance extraction (MEV-capture fee decomposition). Algebra for directional flow signals (bidirectional fee spread). They are complementary, not substitutes.

### Risks

1. **TVL depth (HIGH)**: Ekubo EVM TVL is ~$20M. Signal quality depends on sufficient trade volume. The 30x volume/TVL ratio helps but thin periods will produce noisy signals.

2. **Protocol maturity (MEDIUM)**: EVM deployment is ~1 year old. Core contract is ownerless and immutable, which reduces upgrade risk but means bugs are permanent.

3. **Team concentration (LOW-MEDIUM)**: Ekubo Inc. is small and engineering-focused. Moody Salem is the key person risk. However, contracts are immutable and DAO-owned.

4. **Starknet dependency (LOW for us)**: We care about EVM deployment. Starknet performance is irrelevant for our integration. The EVM contracts are independent.

5. **Extension security (MEDIUM)**: Extensions are permissionless and can re-enter the core. A malicious extension could create pools that behave unexpectedly. For signal extraction, we only read from known first-party extensions, so this risk is limited.

6. **Aggregator routing (LOW)**: Most Ekubo volume comes via aggregators (VeloraDEX/ParaSwap, AVNU on Starknet). If aggregator support drops, volume drops and signals degrade. Current aggregator integration is strong.

### Integration Complexity

**Can we read Ekubo state from Solidity contracts?**

Yes. The Core contract at `0x00000000000014aA86C5d3c41765bb24e11bd701` is a standard EVM contract with view functions. You can:

1. **Read pool price**: Call the Core contract with the pool key to get sqrt_ratio and tick.
2. **Read oracle TWAP**: Call the Oracle extension to get cumulative tick snapshots, compute TWAP in your contract.
3. **Read TWAMM state**: Call the TWAMM extension to get sale rates and deltas.
4. **Index swap events**: Use the Ekubo indexer (open source, Postgres) or your own event listener to capture tick displacement per swap.

The pool key structure (token0, token1, fee, tick_spacing, extension) must be known in advance. The extension address is part of the pool key, so you must specify which pool type you're querying.

SDKs available:
- **TypeScript**: https://github.com/EkuboProtocol/evm-typescript-sdk
- **Rust**: https://github.com/EkuboProtocol/evm-rust-sdk
- **ABIs**: https://github.com/EkuboProtocol/abis

### Integration Priority for Our Project

**Phase 1 (Immediate)**:
1. Deploy an ILTracker-style hook that reads Ekubo Core contract state (sqrt_ratio, tick) for ETH/USDC and USDC/USDT pools on Ethereum.
2. Build a swap event indexer for MEV-capture pools to extract tick_displacement series.
3. Compute rolling realized variance from tick_displacement^2 sums.

**Phase 2 (Short-term)**:
4. Query Oracle extension for TWAP baseline.
5. Query TWAMM extension for sale rate imbalance as directional order flow signal.
6. Compare Ekubo RV signal to Algebra bidirectional fee spread signal for the same pairs.

**Phase 3 (Medium-term)**:
7. Build on-chain realized volatility oracle contract that reads from Ekubo MEV-capture events.
8. Use TWAMM sale rates as forward-looking signal for hedging instrument pricing.

---

## Key References

- Ekubo Documentation: https://docs.ekubo.org/
- Ekubo GitHub: https://github.com/EkuboProtocol
- Ekubo EVM Contracts V3 Docs: https://docs.ekubo.org/integration-guides/reference/evm-contracts-v3
- Ekubo Extensions Docs: https://docs.ekubo.org/integration-guides/extensions
- Ekubo Math 1-Pager: https://docs.ekubo.org/integration-guides/reference/math-1-pager
- Ekubo Key Concepts: https://docs.ekubo.org/integration-guides/reference/key-concepts
- Ekubo Reading Pool Price: https://docs.ekubo.org/integration-guides/reference/reading-pool-price
- Ekubo Oracle Extension (Starknet): https://github.com/EkuboProtocol/oracle-extension
- Ekubo Indexer: https://github.com/EkuboProtocol/indexer
- Ekubo EVM TypeScript SDK: https://github.com/EkuboProtocol/evm-typescript-sdk
- Ekubo EVM Rust SDK: https://github.com/EkuboProtocol/evm-rust-sdk
- Ekubo ABIs: https://github.com/EkuboProtocol/abis
- Starknet Blog -- "Ekubo: The AMM Endgame": https://www.starknet.io/blog/ekubo-the-amm-endgame/
- DeFiLlama Ekubo: https://defillama.com/protocol/ekubo
- VeloraDEX Adapter Hierarchy: /home/jmsbpp/apps/liq-soldk-dev/notes/velora/VELORA_DEX_HIERARCHY.md
- "The Price of Liquidity: Implied Volatility of AMM Fees" (arXiv): https://arxiv.org/pdf/2509.23222
