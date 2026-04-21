# CoW Protocol & CoW AMM: Deep Dive Research Report

**Date:** 2026-04-03
**Context:** Evaluation of CoW Protocol as settlement infrastructure and MEV-free observable source for macro-risk hedging instruments targeting underserved countries.
**Relevance:** Our macro hedging instruments use CFMM pool observables (price, volume, fees, liquidity) as proxies for FX depreciation, inflation, capital flight, and interest rate shocks. MEV/toxic flow contamination of volume signals is a major identified concern. CoW Protocol's batch auction mechanism potentially eliminates this noise.

---

## Executive Summary

CoW Protocol is an intent-based trading protocol that uses batch auctions to settle orders, producing MEV-free execution and cleaner price signals than traditional CFMMs. Its AMM product (CoW AMM) implements the Function-Maximizing AMM (FM-AMM) design from Canidio & Fritsch (2023), which provably eliminates LVR and sandwich attacks. For our macro hedging use case, CoW Protocol offers three critical advantages over traditional CFMMs:

1. **Clean volume signals** -- batch auction volume is free of sandwich attack inflation and front-running noise
2. **Single clearing prices** -- each batch produces a uniform clearing price, not a path-dependent price curve, enabling manipulation-resistant TWAP construction
3. **Surplus as information** -- the surplus (price improvement over limit price) contains information about true market price vs. quoted price, a novel observable with no CFMM analogue

However, CoW AMM has significant limitations for our specific architecture: it does not yet support multi-token pools (only 2-token pairs), TVL remains modest (~$30-50M range), and there are no emerging-market stablecoin pools. The protocol is strongest as a supplementary signal source and potential settlement venue, not as a replacement for the universal multi-token pool design.

---

## 1. CoW Protocol Architecture

### 1.1 Batch Auction Mechanism: End-to-End

The CoW Protocol operates on a three-layer off-chain/on-chain architecture:

**Layer 1 -- Orderbook (Off-chain)**
Users sign EIP-712 typed data messages expressing trading intents (not transactions). These signed intents are submitted to the CoW Protocol orderbook API, an off-chain database that collects, validates, and stores pending orders. Validation includes: well-formed field encoding, sufficient balance/allowance checks, signature verification (EOA via ECDSA, smart contracts via ERC-1271).

**Layer 2 -- Autopilot (Off-chain)**
The Autopilot service aggregates pending orders into batches at approximately 30-second intervals. It organizes the auction by:
- Grouping orders into a batch
- Broadcasting the batch to all registered solvers
- Receiving proposed solutions from solvers within a fixed time window
- Scoring solutions by surplus maximization
- Selecting the winning solver
- Storing all auction metadata (proposals, scores, surplus fees, execution results)

**Layer 3 -- Settlement (On-chain)**
The winning solver submits a single transaction to the GPv2Settlement contract that executes all trades in the batch atomically. This is the only on-chain footprint -- users never submit transactions themselves.

**Batch auction timeline:**
```
t=0s    Orders accumulate in orderbook
t=30s   Autopilot cuts batch, sends to solvers
t=30-60s Solvers compute optimal settlements
t=60s   Winning solution selected (max surplus)
t=60-90s Winner submits settlement tx on-chain
```

The key insight: because all orders in a batch execute at the same uniform clearing price, there is no sequential ordering within a batch. Front-running and sandwich attacks require transaction ordering -- batch auctions eliminate the attack surface entirely.

### 1.2 Solvers

Solvers are bonded third-party optimization engines that compete to find the best settlement for each batch. They have three strategies available:

1. **Coincidence of Wants (CoW):** Direct peer-to-peer matching of opposing orders within the batch. If Alice sells ETH for USDC and Bob sells USDC for ETH, the solver matches them directly, bypassing all on-chain liquidity and paying zero LP fees.

2. **On-chain liquidity routing:** Solvers route through AMMs (Uniswap, Balancer, Curve, etc.), DEX aggregators (1inch, Paraswap), and any other on-chain liquidity source.

3. **Private market maker liquidity:** Solvers can access off-chain liquidity from private market makers willing to fill orders.

**Solver auction mechanics:**
- Each solver submits a proposed settlement (a complete solution for all fillable orders in the batch)
- Solutions are scored by total surplus: sum of (execution price - limit price) across all orders
- The solver with the highest surplus score wins
- The winning solver must give users their signed limit price or better -- they absorb all price risk from MEV

**Bonding requirements:**
- Bonding pool: $500,000 USD in yield-bearing stablecoins + 1,500,000 COW tokens
- Bond can be slashed for misconduct detected by CoW DAO
- Service fee of 15% of weekly COW rewards begins 6 months after joining
- Only approved solvers on the allowlist can participate

**Combinatorial auctions (recent):**
The protocol introduced combinatorial auctions allowing multiple solvers to collaborate on a single batch settlement, targeting ~33% increase in transaction handling capacity.

### 1.3 Intent-Based Trading vs. AMM Trading

| Dimension | AMM Trading | Intent-Based (CoW) |
|-----------|------------|-------------------|
| User action | Submit transaction | Sign message (gasless) |
| Execution | Immediate, sequential | Batched, simultaneous |
| Price | Path-dependent (slippage) | Uniform clearing price |
| MEV exposure | Full (front-run, sandwich) | None (batch eliminates ordering) |
| Counterparty | LP pool | Other traders (CoW) or LP pool |
| Gas cost | User pays | Solver pays (embedded in spread) |
| Information leakage | Mempool visible | Private until settlement |

The fundamental difference: AMM trading requires submitting a transaction to the mempool where it becomes visible to MEV searchers. Intent-based trading keeps order information private (off-chain) until the batch settles atomically on-chain.

### 1.4 The Settlement Contract (GPv2Settlement)

The GPv2Settlement contract is the sole on-chain component of CoW Protocol. It:
- Holds no user funds (users approve the GPv2VaultRelayer, not the settlement contract)
- Executes batch settlements submitted by winning solvers
- Emits `Trade` events for each executed order
- Emits a `Settlement` event per batch
- Manages interactions with on-chain liquidity (AMM swaps, Balancer vault interactions)

**Trade event signature:**
```solidity
event Trade(
    address indexed owner,
    IERC20 sellToken,
    IERC20 buyToken,
    uint256 sellAmount,
    uint256 buyAmount,
    uint256 feeAmount,
    bytes orderUid
);
```

**Settlement event:**
```solidity
event Settlement(address indexed solver);
```

Each `Settlement` event marks the boundary of a batch. All `Trade` events between consecutive `Settlement` events belong to the same batch and were executed at the same uniform clearing price.

### 1.5 Contract Addresses

The GPv2Settlement contract is deployed at the **same address** on all supported chains:

| Contract | Address |
|----------|---------|
| GPv2Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` |
| GPv2VaultRelayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFe0110` |

**Supported chains (same addresses):**
- Ethereum Mainnet (1)
- Gnosis Chain (100)
- Arbitrum One (42161)
- Base (8453)
- Optimism (10)
- Polygon (137)
- BNB Chain (56)
- Avalanche (43114)
- Sepolia testnet (11155111)

### 1.6 Programmatic Order Framework (ComposableCoW)

ComposableCoW is a framework for building conditional orders that execute programmatically via CoW Protocol. It enables smart contracts to define custom order logic that the protocol evaluates at settlement time.

**Architecture:**
```
Smart Contract Wallet (Safe)
    |
    +-- ComposableCoW (registry of conditional orders)
         |
         +-- IConditionalOrder handler (custom logic)
         |
         +-- Watch Tower (off-chain indexer)
              |
              +-- CoW Protocol Orderbook API
```

**Four customizable parameters per conditional order:**
1. `handler` -- smart contract that verifies order parameters (the custom logic)
2. `salt` -- enables multiple conditional orders of the same type
3. `staticData` -- data available to ALL discrete orders from this conditional order
4. `offchainData` -- data optionally provided from off-chain to a discrete order

**Interfaces:**
- `IConditionalOrder` -- verifies a proposed discrete order against conditions
- `IConditionalOrderGenerator` -- generates discrete orders (the more common pattern)

The `getTradableOrder()` method returns order parameters the contract would accept. A watch tower service monitors on-chain state, calls `getTradableOrder()` when conditions are met, and forwards the resulting order to the CoW Protocol API for solver pickup.

**Key insight for our use case:** ComposableCoW enables building settlement logic that triggers based on on-chain conditions (e.g., oracle price crosses a threshold, a variance swap expires). The programmatic order can encode the settlement payoff function directly.

---

## 2. CoW AMM

### 2.1 FM-AMM Theory

CoW AMM implements the Function-Maximizing AMM (FM-AMM) design from the paper "Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response" by Andrea Canidio and Robin Fritsch (arXiv:2307.02074, published at AFT 2023).

**Core idea:** Instead of executing trades sequentially (as in Uniswap), the FM-AMM batches all trades and executes them simultaneously at a single uniform clearing price. The clearing price is chosen to maximize the AMM's invariant function (e.g., x*y=k).

**Formal mechanism:**
- Let f(x,y) be the AMM invariant (e.g., f(x,y) = x*y for constant product)
- Given a batch of orders, find the clearing price p* such that the post-trade state (x', y') maximizes f(x', y')
- All trades execute at p*
- Competition between arbitrageurs guarantees p* equals the true market price

**Why LVR is eliminated:**
In a traditional CFMM, arbitrageurs extract value by trading against stale pool prices. The profit they extract IS the LVR. In the FM-AMM:
- Arbitrageurs still submit orders, but they compete with each other within the batch
- Competition drives the clearing price to the true market price
- The surplus (difference between naive CFMM price and true price) stays in the pool
- Arbitrageurs earn zero profit in equilibrium -- all "arbitrage value" accrues to LPs

**Simulation results from the paper:**
Using Binance price data for 11 token pairs, the FM-AMM lower bound on LP returns was slightly higher than empirical Uniswap V3 LP returns -- meaning FM-AMM LPs earn more even without fees, solely from capturing LVR.

### 2.2 How CoW AMM Works in Practice

CoW AMM pools are deployed on Balancer infrastructure (BCoWPool contracts). The pool acts as a "conditional order" within the CoW Protocol batch auction:

1. **Pool state:** The pool holds reserves of two tokens (e.g., WETH and USDC)
2. **Arbitrage opportunity:** When the external price diverges from the pool's implied price, an arbitrage opportunity exists
3. **Solver competition:** Solvers bid to rebalance the pool. Each solver proposes a trade (amount in, amount out) that moves the pool to a new state
4. **Surplus maximization:** The winning solver is the one whose proposed trade maximizes the pool's invariant function -- i.e., moves the pool curve highest
5. **Settlement:** The winning rebalancing trade executes as part of the CoW Protocol batch auction, atomically with all other trades in the batch
6. **Zero swap fee:** The CoW Protocol settlement contract trades with the pool at zero fee. The surplus from rebalancing replaces traditional swap fees as LP compensation

**Critical difference from traditional AMMs:** In Uniswap, arbitrageurs extract value from the pool. In CoW AMM, the competitive solver auction captures that same value and returns it to the pool (LPs).

### 2.3 Comparison to Traditional CFMMs

| Feature | CoW AMM | Uniswap V3 | Balancer V3 |
|---------|---------|------------|-------------|
| LVR | Eliminated | Full exposure | Full exposure |
| Sandwich attacks | Impossible | Common | Common |
| Swap fees | Zero (surplus replaces) | 0.01-1% tiers | Dynamic |
| Price mechanism | Batch clearing price | Continuous curve | Continuous curve |
| Rebalancing | Solver competition | Arbitrageur extraction | Arbitrageur extraction |
| LP yield source | Captured surplus | Swap fees minus LVR | Swap fees minus LVR |
| Capital efficiency | Uniform (50/50 weighted) | Concentrated liquidity | Weighted/Stable |

### 2.4 The Surplus Mechanism

Surplus in CoW AMM has a dual role:

**For traders:** Surplus = (execution price) - (limit price). The positive difference between what you asked for and what you got. This is the measure of execution quality.

**For LPs:** Surplus = the value that would have been extracted as LVR by arbitrageurs in a traditional AMM. In CoW AMM, solvers compete to offer the most surplus to the pool, and this surplus stays with LPs.

**Quantitative:** CoW AMM has captured over $100,000 in surplus for LPs since launch (early figure; growing with TVL). The protocol-wide surplus across all CoW Protocol trading exceeded $188 million cumulative as of early 2026.

### 2.5 CoW AMM on Balancer V3

CoW AMM pools are deployed using Balancer's BCoWPool factory contracts:

| Chain | BCoWPool Factory Address |
|-------|------------------------|
| Ethereum Mainnet | `0xf76c421bAb7df8548604E60deCCcE50477C10462` |
| Gnosis Chain | `0x703Bd8115E6F21a37BB5Df97f78614ca72Ad7624` |
| Arbitrum One | `0xE0e2Ba143EE5268DA87D529949a2521115987302` |

**Integration mechanics:**
- BCoWPool immutably stores CoW Protocol's SolutionSettler and VaultRelayer addresses at deployment
- Stores CoW Protocol's EIP-712 domain separator (replay attack prevention)
- Stores approved `appData` for swap authorization
- Gives infinite ERC20 approval to VaultRelayer at finalization
- Implements `IERC1271.isValidSignature()` for swap validation
- Implements `commit()` to prevent conflicting simultaneous swaps

**Pool creation flow:**
1. Call `IBCoWFactory.newBPool(name, symbol)` on factory
2. Approve tokens to pool address
3. Call `bind()` for each token with initial amounts
4. Optionally call `setSwapFee()` (for permissionless non-batch trades)
5. Call `finalize()` to activate the pool

### 2.6 Pool Types

**Currently supported:**
- **50/50 Weighted pools** -- constant product (x*y=k) invariant with equal weights. This is the only pool type currently live.

**Planned/roadmap:**
- Stable pools (constant-sum-like invariant for correlated assets)
- Concentrated liquidity within CoW AMM ranges
- Multi-token pools (3+ tokens)

### 2.7 Multi-Token Pool Support

**Current status: NOT supported.** Each CoW AMM pool trades exactly two tokens. The BCoWPool factory enforces this constraint.

Multi-token CoW AMM is on the roadmap but not yet implemented. This is a significant limitation for our universal multi-token pool architecture (USDC/DAI/AMPL base + ETH/wstETH extension), which requires 3+ tokens in a single pool.

### 2.8 Concentrated Liquidity

CoW AMM documentation mentions concentrated liquidity as a planned feature that would allow LPs to focus capital within targeted price ranges. However, this is **not yet live** -- current pools operate as uniform 50/50 weighted pools (full-range liquidity).

---

## 3. Deployed Pools & Liquidity

### 3.1 Deployment Chains

CoW AMM factory contracts are deployed on:
- **Ethereum Mainnet** (primary, highest TVL)
- **Gnosis Chain**
- **Arbitrum One**

CoW Protocol (the swap protocol, not the AMM) is additionally deployed on Base, Optimism, Polygon, BNB Chain, and Avalanche -- but CoW AMM pools exist only on the three chains above.

### 3.2 Known Pools with Meaningful TVL

Based on available data (Balancer app, Dune dashboards, DeFiLlama):

**Ethereum Mainnet:**
| Pool | Tokens | Notes |
|------|--------|-------|
| USDC/WETH | Stablecoin/ETH | Flagship pair |
| MKR/WETH | Governance/ETH | |
| AAVE/WETH | Governance/ETH | |
| WBTC/wstETH | BTC/Liquid staking | Address: `0xf25a3b5a965c59f88873da93fc2a244b00616be4` |
| COW/WETH | Protocol token/ETH | |

**Arbitrum One:**
| Pool | Tokens | Notes |
|------|--------|-------|
| ARB/WETH | Governance/ETH | |

**Gnosis Chain:**
| Pool | Tokens | Notes |
|------|--------|-------|
| GNO/xDAI | Governance/Stablecoin | |

### 3.3 Specific Pool Categories

**Stablecoin/Stablecoin pools (USDC/USDT, USDC/DAI):** No evidence of meaningful CoW AMM stablecoin-stablecoin pools. This makes sense -- FM-AMM's advantage is LVR elimination, and stablecoin pairs have minimal LVR due to tight correlation. The value proposition is weak for stable pairs.

**Yield-bearing token pools (wstETH/WETH, rETH/WETH):** The WBTC/wstETH pool exists. No dedicated wstETH/WETH or rETH/WETH CoW AMM pools were found -- another case where the correlated nature of the pair reduces LVR and thus the CoW AMM advantage.

**Gold-backed pools (PAXG):** None found.

**Emerging-market stablecoin pools:** None found. No cCOP, cPHP, BRZ, or similar.

THe Optimal Exit by Capponi and also teh panotpic architecture map expiration to the width of the position price Range or so is that feasible 

### 3.4 TVL Trajectory


Note also the patterns where the pattern were used in parent loss tracking So essentially one of the goals of this That must be aware of the must be aware of the specification is that if we cannot use this bit if we cannot use data yet because of API constraints We can use these trackers and instruments to build like models such as the ones on the papers that we can essentially do Testing or Differential testing or or things like that modeling on equations the behavior of LPs that interact with this build system So what are some requirements that come up on in terms of liquidity? How is the quality being gathered? What is this how the success of The protocol looks like in terms of what is needed and when it fails things so these things are need to be considered deeply

Yes, note that we must leverage all the already built code. So we definitely need to adapt to unused their Armstrong pattern and also the panoptic pattern for tokenizing and for collateral tracking.
DeFiLlama tracks CoW AMM under "Balancer CoW AMM" (https://defillama.com/protocol/balancer-cow-amm). Based on available data:

- TVL has been in the **$30-50M range** through late 2025/early 2026
- CoW AMM achieves close to 5% more TVL compared to equivalent reference pools (suggesting mild LP preference for MEV protection)
- Growth has been steady but not explosive -- constrained by:
  - Only 50/50 weighted pools (no concentrated liquidity)
  - Only 2-token pairs
  - Limited chain deployment
  - Relatively new product

**Assessment:** TVL is modest compared to Uniswap V3 (~$4-5B) or Balancer V3 overall. CoW AMM is still an early-stage product gaining traction.

---

## 4. Observable Extraction for Macro Signals

### 4.1 On-Chain Data Produced

Every CoW Protocol settlement produces the following on-chain data:

**Per-batch:**
- `Settlement(address indexed solver)` event -- marks batch boundary and winning solver

**Per-trade within batch:**
- `Trade(address indexed owner, IERC20 sellToken, IERC20 buyToken, uint256 sellAmount, uint256 buyAmount, uint256 feeAmount, bytes orderUid)` event

**Derivable from Trade events:**
- Effective execution price: `buyAmount / sellAmount` (or inverse)
- Fee paid: `feeAmount`
- Order identity: `orderUid` (links to off-chain order metadata)
- Trader identity: `owner`
- Token pair: `sellToken`, `buyToken`
- Batch membership: all Trades between consecutive Settlement events

### 4.2 Surplus Data as Signal

Surplus data is available off-chain through the CoW Protocol API and Autopilot records. For each order:
- `limitPrice`: the price the user signed (their minimum acceptable)
- `executionPrice`: the actual batch clearing price
- `surplus = executionPrice - limitPrice`

**Surplus as a macro signal:**
Surplus contains information about the gap between the "naive" or "stale" price (what users expect) and the "true" or "discovered" price (what the competitive solver auction finds). For a USDC/cCOP pair, high surplus on cCOP-sell orders would indicate that cCOP is weaker than users expected -- a leading indicator of FX depreciation pressure.

This is a **novel observable** with no analogue in traditional CFMMs. In Uniswap, this value is extracted by MEV bots and is invisible in on-chain data.

### 4.3 Volume Data Quality

**CoW Protocol volume is structurally cleaner than Uniswap volume:**

| Contamination Source | Uniswap V3 | CoW Protocol |
|---------------------|------------|--------------|
| Sandwich attack volume | ~10-30% of volume on popular pairs | 0% (impossible in batch auction) |
| Front-running volume | Present | 0% (order info private until settlement) |
| Back-running volume | Present | 0% |
| Wash trading | Possible but costly | Possible but costly |
| Genuine arbitrage | Mixed with toxic arb | Clean (arb happens via solver competition, not on-chain) |
| CEX-DEX arb | Visible as toxic flow | Internalized by solvers, invisible on-chain |

**Quantitative evidence:** CoW Protocol claims $87B in volume for 2025 with $188M in surplus returned. The absence of sandwich inflation means this volume figure is closer to "true" informed + uninformed trading volume. Uniswap volume figures, by contrast, include substantial MEV-inflated volume.

**No formal academic comparison** of CoW vs. Uniswap volume quality has been published. However, the structural argument is strong: batch auctions eliminate the sandwich attack vector entirely, and sandwich attacks are estimated to account for a meaningful share of DEX volume.

### 4.4 Price Discovery Quality

**Batch clearing price properties:**
- Single uniform clearing price per batch (not path-dependent)
- Determined by competitive solver optimization (not sequential trading)
- Incorporates all order information in the batch simultaneously
- Resistant to single-order manipulation (manipulator would need to outbid all solvers)

**TWAP construction from CoW data:**
A TWAP built from CoW batch clearing prices would differ fundamentally from a Uniswap TWAP:
- Uniswap TWAP: time-weighted average of a continuously manipulable price
- CoW TWAP: time-weighted average of discrete batch clearing prices, each determined by competitive auction

The CoW TWAP would have:
- **Lower manipulation surface:** each price point requires winning a competitive solver auction
- **Discrete sampling:** ~2 prices per minute (30-second batches) vs. continuous
- **No path-dependency:** each batch price is independent of previous batches

**Limitation:** CoW Protocol does not natively produce a TWAP oracle. You would need to construct one from Trade events, which requires indexing the settlement contract.

### 4.5 Volatility Oracle Construction

A realized volatility oracle from CoW data would use the sequence of batch clearing prices:

```
sigma_realized = std(log(p_{t+1}/p_t)) * sqrt(N)
```

where p_t are successive batch clearing prices and N is the annualization factor.

**Advantages over CFMM-based vol:**
- Each p_t is an MEV-free clearing price, not contaminated by sandwich-induced price spikes
- The variance of batch prices reflects genuine supply/demand volatility, not MEV-induced noise
- Suitable for Shiller-style variance swap settlement

**No existing implementation** -- this would need to be built. The raw data (Trade events) is available on-chain.

### 4.6 Order Flow Toxicity Metrics

CoW Protocol's architecture inherently separates flow types:

- **CoW-matched volume:** purely uninformed (peer-to-peer matching of opposing retail orders)
- **On-chain liquidity volume:** mix of informed and uninformed
- **Solver surplus:** measures the information gap between user expectations and market prices

The CoW-matched percentage provides a direct measure of uninformed flow proportion. This is unavailable from any traditional AMM.

---

## 5. Programmatic Orders & Custom Instruments

### 5.1 ComposableCoW for Derivative-Like Instruments

ComposableCoW can encode custom settlement logic via the `IConditionalOrderGenerator` interface. A derivative-like instrument would:

1. Deploy a Safe wallet with ComposableCoW module
2. Register a conditional order with custom handler logic
3. Handler's `getTradableOrder()` encodes the derivative payoff as a trade
4. Watch tower monitors on-chain conditions (expiry, oracle price, etc.)
5. When conditions trigger, watch tower submits order to CoW API
6. Solver executes the settlement trade in a batch auction

**This is viable for income-settled derivatives:** The handler can read an oracle (Chainlink, Uniswap TWAP, custom) and compute the settlement amount, then generate an order that transfers the correct payoff.

### 5.2 Native Order Types

| Order Type | Status | Mechanism |
|-----------|--------|-----------|
| Market order | Live | Standard CoW swap |
| Limit order | Live | Persistent until fill or expiry |
| TWAP | Live | ComposableCoW: splits large order into n parts at t-second intervals |
| Stop-loss | Live | ComposableCoW: triggers when price crosses threshold |
| Good-after-time | Live | ComposableCoW: order becomes valid after timestamp |
| Milkman | Live | Price-protected orders using oracle reference |

**TWAP implementation details:**
- User signs a single gasless intent for the entire TWAP strategy
- Order is divided into n equal parts at frequency t seconds
- Each sub-order has a validity window defined by the `span` parameter
- Solvers find optimal execution for each sub-order within its window
- Full MEV protection on each sub-order

### 5.3 Variance Swap Settlement via Programmatic Orders

A CoW-native variance swap could be implemented as follows:

```
1. Deploy Safe with ComposableCoW module
2. Register conditional order:
   - handler: VarianceSwapSettlement contract
   - staticData: {strike_vol, notional, observation_period, settlement_token}
3. Handler logic:
   - Read realized variance from on-chain oracle (or compute from stored observations)
   - Compute payoff: notional * (realized_variance - strike_variance)
   - Generate a CoW order that transfers payoff amount of settlement_token
4. Watch tower monitors: block.timestamp >= expiry
5. On expiry: getTradableOrder() returns settlement order
6. Solver executes settlement in batch auction
```

**Challenges:**
- Requires a realized variance oracle (does not exist natively in CoW)
- Settlement is a single-direction transfer, not a swap -- may not fit CoW's bilateral trade model cleanly
- Could use a "swap" where one side is the variance token and the other is the settlement token

### 5.4 Milkman (Price-Protected Orders)

Milkman was developed by Yearn Finance with CoW DAO grant funding. It solves the delayed-execution problem for DAO governance trades.

**How it works:**
- Instead of specifying a fixed `minOut` (which becomes stale if execution is delayed), the user specifies an **on-chain price checker** (oracle reference)
- At execution time, `minOut` is dynamically computed from the oracle price
- Price checkers exist for: Chainlink, Curve, SushiSwap, Uniswap V2, Uniswap V3, and combinations

**Usage:** Over $20M traded by DAOs including Aave and ENS. Particularly suited for large governance-delayed trades.

**Relevance to our use case:** Milkman's dynamic price reference pattern could be adapted for macro derivative settlement -- the oracle reference could be a macro indicator rather than a spot price.

### 5.5 CoW Hooks

CoW Hooks are arbitrary Ethereum calls that execute before (pre-hooks) and/or after (post-hooks) an order within a batch settlement.

**Pre-hooks:** Execute before user funds are pulled. Use cases:
- Token approvals batched with the trade
- Unwrapping yield-bearing tokens before selling
- Withdrawing from a vault before trading

**Post-hooks:** Execute after trade proceeds are delivered. Use cases:
- Depositing proceeds into a vault
- Bridging to another chain
- Triggering a downstream contract call
- **Settling a derivative payoff**

**Execution via HooksTrampoline:**
Hooks execute through a dedicated trampoline contract (not the settlement contract) to prevent hooks from accessing settlement contract privileges (e.g., stealing accumulated fees).

**Important limitation:** Hook execution is NOT guaranteed on-chain. It is enforced by social consensus among solvers, not by the smart contract. If a solver omits hooks, the trade may still execute.

**Relevance:** Post-hooks could trigger variance swap settlement, income distribution, or other downstream contract interactions after a CoW trade executes.

---

## 6. MEV Protection Analysis

### 6.1 Quantitative Evidence

| Metric | Value | Source |
|--------|-------|--------|
| Total volume (2025) | $87 billion | CoW DAO 2025 Review |
| Total surplus returned | $188 million+ | CoW Protocol stats |
| Monthly volume (peak) | $10B+ (late 2025) | CoW DAO |
| Monthly surplus (May 2024 snapshot) | $16.5M | Dune |

**Interpretation:** $188M in surplus means users received $188M more than their limit prices -- value that in a traditional DEX would have been partially or fully extracted by MEV bots.

### 6.2 Execution Quality vs. DEX Aggregators

CoW Protocol claims top-3 DEX aggregator market share across all networks. The surplus mechanism provides a direct, verifiable execution quality metric -- unlike DEX aggregators where "best price" is claimed but hard to verify.

**Key structural advantages over aggregators:**
- Aggregators route through existing liquidity; CoW can match peer-to-peer (CoW)
- Aggregators submit on-chain transactions visible in mempool; CoW orders are private
- Aggregators compete on quoted price; CoW solvers compete on realized surplus

**No rigorous independent academic study** comparing CoW execution quality vs. 1inch or other aggregators has been published as of this writing.

### 6.3 Coincidence of Wants (CoW) Statistics

The CoW matching rate (percentage of volume matched peer-to-peer without touching on-chain liquidity) varies by:
- Market conditions (busy markets have more opposing orders)
- Token pair popularity (high-volume pairs have more CoW opportunities)
- Batch timing (30-second windows may miss opportunities)

**Multidimensional CoW:** Three or more users can be matched in a ring. Alice: ETH->USDC, Bob: USDC->DAI, Charlie: DAI->ETH. The solver finds this ring trade and matches all three peer-to-peer.

Exact CoW percentages are tracked on the Dune dashboard (https://dune.com/cowprotocol/cowswap-high-level-metrics-dashboard) but were not available in current search results. Historical estimates suggest CoW matching rates of approximately 5-15% of volume on popular pairs.

### 6.4 Residual MEV Risks

Even with CoW Protocol, the following MEV vectors remain:

1. **Solver collusion:** If solvers collude rather than compete, they can extract value by offering suboptimal prices. Mitigation: bonding/slashing, open competition.

2. **Solver front-running the settlement tx:** The winning solver submits the on-chain transaction and could theoretically front-run their own settlement. Mitigation: the settlement must match or exceed all signed limit prices.

3. **Block builder MEV on the settlement tx:** The settlement transaction itself can be sandwiched by block builders/proposers. Solvers can use private mempools (e.g., MEV Blocker, Flashbots Protect) to mitigate.

4. **Informed order flow within batches:** If a sophisticated trader places orders based on private information that moves prices, they can profit within the batch. This is "genuine" information asymmetry, not MEV.

5. **Censorship:** Solvers or the Autopilot could censor specific orders. Mitigation: multiple solvers, transparency.

6. **Batch timing manipulation:** The 30-second batch window creates a discrete sampling that could theoretically be manipulated by timing order submission relative to batch boundaries.

---

## 7. Integration Patterns

### 7.1 Protocol Integration for Settlement

A protocol integrating CoW for settlement would use one of:

**Pattern A -- ERC-1271 Smart Contract Orders:**
1. Deploy a smart contract wallet (Safe) that implements `isValidSignature()`
2. Register with ComposableCoW
3. Contract generates orders programmatically via `getTradableOrder()`
4. Watch tower submits to CoW API
5. Solver includes in batch settlement

**Pattern B -- Direct API Integration:**
1. Backend service monitors conditions
2. When triggered, signs an order (EOA) or generates ERC-1271 order (smart contract)
3. POSTs to CoW Orderbook API
4. Monitors order status via API polling

**Pattern C -- CoW Hooks:**
1. Integrate as a post-hook on an existing CoW trade
2. When the trade settles, the hook calls your settlement contract

### 7.2 Smart Contract Order Placement

Smart contracts can place orders on CoW Protocol permissionlessly via ERC-1271:
- No private key required (the contract's `isValidSignature()` method validates)
- Anyone can submit the order to the API on behalf of the contract
- The watch tower service handles this automatically for ComposableCoW orders

### 7.3 API Endpoints

**Base URLs:**
- Ethereum: `https://api.cow.fi/mainnet/api/v1/`
- Gnosis: `https://api.cow.fi/xdai/api/v1/`
- Arbitrum: `https://api.cow.fi/arbitrum_one/api/v1/`

**Key endpoints:**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/quote` | POST | Get price quote for a trade |
| `/orders` | POST | Submit signed order |
| `/orders/{uid}` | GET | Check order status |
| `/orders/{uid}/cancel` | DELETE | Cancel pending order |
| `/trades` | GET | Query executed trades |
| `/native_price/{token}` | GET | Token price estimate (cached) |

**OpenAPI documentation:** Available at docs.cow.fi for orderbook, driver, and solver APIs.

### 7.4 Event Monitoring

Settlement monitoring uses standard EVM event indexing:
- Subscribe to `Settlement` and `Trade` events on GPv2Settlement (`0x9008...0ab41`)
- Each `Settlement` event marks a batch boundary
- `Trade` events between boundaries belong to the same batch
- The Autopilot stores full auction metadata (solver proposals, scores, surplus fees) -- accessible via CoW API

### 7.5 Cross-Chain CoW

CoW Swap supports cross-chain swaps via bridge aggregation (Bungee, Near Intents). The user submits a single intent; CoW Protocol:
1. Finds optimal bridge route
2. Executes source-chain swap
3. Bridges tokens
4. Executes destination-chain swap

This is bridge aggregation, not cross-chain batch auctions. Each chain's batch auction operates independently.

---

## 8. Comparison Table

| Feature | CoW AMM | Uniswap V3 | Uniswap V4 | Balancer V3 | Algebra Integral |
|---------|---------|------------|------------|-------------|-----------------|
| **AMM Type** | FM-AMM (batch) | CPMM (continuous) | CPMM + hooks | Weighted/Stable/Custom | CPMM + plugins |
| **Fee Mechanism** | Zero fee (surplus) | Fixed tiers (0.01-1%) | Dynamic via hooks | Dynamic | Dynamic via plugins |
| **MEV Protection** | Full (batch auction) | None native | Via hooks (partial) | None native | None native |
| **LVR Protection** | Eliminated | None | Possible via hooks | None | None |
| **Multi-Token Pools** | No (2 tokens only) | No (2 tokens) | No (2 tokens) | Yes (up to 8) | No (2 tokens) |
| **Concentrated Liquidity** | Planned, not live | Yes (core feature) | Yes | No (uniform weights) | Yes (core feature) |
| **Hooks/Plugins** | CoW Hooks (pre/post) | None | Yes (14 hook points) | Yes (Balancer hooks) | Yes (plugin system) |
| **Oracle/TWAP** | No native oracle | Built-in observations | Configurable | No native | No native |
| **Observable Quality** | Excellent (MEV-free) | Poor (MEV-contaminated) | Depends on hooks | Poor (MEV-contaminated) | Poor (MEV-contaminated) |
| **Price Mechanism** | Uniform clearing price | Path-dependent curve | Path-dependent + hooks | Path-dependent curve | Path-dependent curve |
| **Volume Signal Quality** | Clean (no sandwich) | Inflated (sandwich) | Depends on hooks | Inflated (sandwich) | Inflated (sandwich) |
| **TVL (approx.)** | $30-50M | $4-5B | Early stage | $500M-1B | $50-200M |
| **Chains** | ETH, Gnosis, Arbitrum | 10+ chains | ETH + expanding | 8+ chains | 20+ chains |
| **Composability** | Via ComposableCoW | Direct contract calls | Via hooks | Via Balancer hooks | Via plugin interface |
| **Smart Contract Orders** | ERC-1271 native | No | No | No | No |
| **Governance Token Pools** | Yes (MKR, AAVE, COW) | Yes | Yes | Yes | Yes |
| **Stablecoin Pools** | Limited | Extensive | Growing | Extensive | Moderate |

---

## 9. Strategic Assessment for Macro Hedging

### 9.1 CoW AMM as Settlement Venue for Income-Settled Derivatives

**Viability: PARTIAL.**

**For:**
- MEV-free execution means derivative settlement is not front-run
- Batch auction ensures fair settlement price
- ComposableCoW enables encoding derivative payoff logic as programmatic orders
- Surplus mechanism captures value that would otherwise leak to MEV

**Against:**
- No multi-token pools -- cannot replicate our USDC/DAI/AMPL + ETH/wstETH universal pool
- No emerging-market stablecoin pools
- Modest TVL limits settlement liquidity
- Zero-fee model means no swap fee observable (our models use fee accumulation as a signal)
- 30-second batch windows create discrete settlement timing

**Recommendation:** CoW Protocol (not CoW AMM specifically) is better suited as a settlement execution layer via ComposableCoW programmatic orders. Use Uniswap V3 or Balancer V3 pools as the observation/measurement instrument, but route settlement trades through CoW Protocol for MEV protection.

### 9.2 Batch Auction Price as Manipulation-Resistant Oracle

**Viability: HIGH.**

The batch clearing price has strong manipulation resistance properties:
- Requires winning a competitive solver auction (not just submitting a single transaction)
- All orders in the batch contribute to price discovery simultaneously
- No sequential manipulation (no front-running or sandwich within a batch)
- Private order flow prevents information leakage before settlement

**Construction method:**
1. Index `Trade` events from GPv2Settlement for the target token pair
2. Compute effective price per trade: `buyAmount / sellAmount`
3. Group by batch (between consecutive `Settlement` events)
4. Weight-average to get batch clearing price
5. Time-weight across batches for TWAP

**Limitations:**
- Not all token pairs have sufficient batch frequency (depends on trading volume)
- Discrete 30-second sampling vs. continuous Uniswap observations
- Requires custom indexing infrastructure (no native oracle contract)

### 9.3 Surplus Mechanism and Shiller-Style Income Claims

The surplus mechanism creates an interesting interaction with income-based valuation:

**Traditional CFMM income:** LP income = swap fees - LVR. This is what we use as a Shiller "dividend" observable.

**CoW AMM income:** LP income = captured surplus (no separate fee). The surplus is economically equivalent to (swap fees + LVR recovery), meaning CoW AMM LP income is structurally higher than CFMM LP income for the same pool.

**Implication for Shiller claims:**
- A Shiller-style income claim on a CoW AMM pool would have higher yield than one on an equivalent Uniswap pool
- The surplus captures "true" market clearing information -- the gap between stale prices and equilibrium
- This surplus stream could itself be a macro observable: high surplus on USDC/cCOP indicates FX pressure

**Challenge:** CoW AMM's zero-fee model means there is no fee-rate parameter to observe. In our current models, the swap fee rate is an observable that proxies for risk appetite. CoW AMM eliminates this signal channel.

### 9.4 CoW-Native Variance Swap Design

A variance swap could be built on CoW infrastructure:

**Observation phase:**
1. Deploy an indexer that records batch clearing prices for the target pair
2. Compute rolling realized variance from the price series
3. Store observations on-chain (or use a commit-reveal scheme)

**Settlement phase:**
1. ComposableCoW programmatic order encodes:
   - Strike variance (agreed at inception)
   - Realized variance (computed from stored observations)
   - Notional in settlement token
   - Payoff: `notional * (realized_var - strike_var)`
2. At expiry, `getTradableOrder()` generates an order transferring the payoff
3. Solver executes the settlement trade in a batch auction

**Advantages over traditional DeFi variance swaps:**
- Settlement trade is MEV-protected
- Observation prices are MEV-free (if sourced from CoW batches)
- No oracle manipulation risk on settlement price

**Open questions:**
- Who provides the opposing liquidity for settlement? (Needs a market maker or liquidity pool)
- How to handle negative payoffs (one party owes the other)?
- How to fund the programmatic order wallet with sufficient collateral?

### 9.5 Risks

**Solver centralization:**
The $500K+ bonding requirement creates a high barrier to entry. In practice, a small number of sophisticated solvers (estimated 10-20 active) handle the majority of volume. Solver collusion would undermine price quality. The DAO governance model for solver approval adds a political dimension.

**Censorship:**
The Autopilot (off-chain) controls batch composition. A compromised or coerced Autopilot could exclude specific orders. Solvers can also choose not to fill certain orders. Neither censorship vector has on-chain enforcement -- it relies on social consensus and DAO governance.

**Latency:**
30-second batch windows introduce settlement latency. For macro hedging instruments where settlement timing matters (e.g., FX fixing times), this latency must be accounted for. The discrete nature of batches means you cannot settle at an arbitrary timestamp -- only at batch boundaries.

**Solver quality degradation:**
If solver competition weakens (fewer solvers, less sophisticated optimization), the quality of clearing prices degrades. The surplus metric provides a real-time monitor for this risk.

**Regulatory risk:**
Intent-based protocols where third parties execute on behalf of users may face regulatory scrutiny as "broker-dealers" in some jurisdictions. The CoW DAO structure adds complexity.

**Smart contract risk:**
GPv2Settlement handles billions in volume. A vulnerability in the settlement contract, VaultRelayer, or BCoWPool factory would be catastrophic. The contracts have been audited but the attack surface is non-trivial.

---

## Appendix A: Key References

### Academic Papers
- Canidio, A. & Fritsch, R. (2023). "Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response." arXiv:2307.02074. Published at AFT 2023 (Advances in Financial Technologies).

### Documentation
- CoW Protocol docs: https://docs.cow.fi/
- CoW AMM docs: https://docs.cow.fi/cow-amm
- GPv2Settlement reference: https://docs.cow.fi/cow-protocol/reference/contracts/core/settlement
- ComposableCoW: https://github.com/cowprotocol/composable-cow
- CoW Hooks: https://docs.cow.fi/cow-protocol/reference/core/intents/hooks
- Programmatic Orders: https://docs.cow.fi/cow-protocol/concepts/order-types/programmatic-orders
- Milkman: https://docs.cow.fi/cow-protocol/concepts/order-types/milkman-orders
- TWAP: https://docs.cow.fi/cow-protocol/reference/contracts/programmatic/twap
- Solver competition rules: https://docs.cow.fi/cow-protocol/reference/core/auctions/competition-rules
- API docs: https://docs.cow.fi/cow-protocol/reference/apis/orderbook

### GitHub Repositories
- CoW Protocol contracts: https://github.com/cowprotocol/contracts
- CoW AMM: https://github.com/cowprotocol/cow-amm
- Balancer CoW AMM: https://github.com/balancer/cow-amm
- ComposableCoW: https://github.com/cowprotocol/composable-cow
- Watch Tower: https://github.com/cowprotocol/watch-tower
- Hooks Trampoline: https://github.com/cowprotocol/hooks-trampoline
- Solver template: https://github.com/cowprotocol/solver-template-py
- CoW SDK: https://github.com/cowprotocol/cow-sdk

### Dune Dashboards
- CoW AMM Performance: https://dune.com/cowprotocol/cowamms
- CoW Swap High Level Metrics: https://dune.com/cowprotocol/cowswap-high-level-metrics-dashboard
- CoW DAO Revenue: https://dune.com/cowprotocol/cow-revenue
- Solver Info: https://dune.com/cowprotocol/solver-info
- Balancer CoW AMM Pool Analysis: https://dune.com/balancer/balancer-cowswap-amm-pool

### Analytics
- DeFiLlama Balancer CoW AMM: https://defillama.com/protocol/balancer-cow-amm
- DeFiLlama CoW Swap: https://defillama.com/protocol/cowswap

### Contract Addresses Summary
| Contract | Address | Chains |
|----------|---------|--------|
| GPv2Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` | All 9 chains |
| GPv2VaultRelayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFe0110` | All 9 chains |
| Eth Flow | `0x40A50cf069e992AA4536211B23F286eF88752187` | Ethereum |
| BCoWPool Factory (ETH) | `0xf76c421bAb7df8548604E60deCCcE50477C10462` | Ethereum |
| BCoWPool Factory (Gnosis) | `0x703Bd8115E6F21a37BB5Df97f78614ca72Ad7624` | Gnosis |
| BCoWPool Factory (Arbitrum) | `0xE0e2Ba143EE5268DA87D529949a2521115987302` | Arbitrum |

---

## Appendix B: Implications for Our Architecture

### What CoW Protocol Changes for Our Design

1. **Signal extraction:** CoW batch prices should be used as a secondary/validation signal alongside Uniswap V3 pool observations. The MEV-free price series provides a ground truth for calibrating MEV contamination in our primary CFMM observables.

2. **Settlement routing:** Income-settled derivative settlement trades should be routed through CoW Protocol (via ComposableCoW) rather than directly through AMM pools. This prevents settlement MEV extraction.

3. **Surplus as new observable:** The surplus distribution across batches is a novel macro indicator. High surplus on USDC-sell / cCOP-buy orders indicates cCOP demand pressure (remittance inflow); high surplus on cCOP-sell / USDC-buy indicates capital flight.

4. **Oracle design:** A CoW batch price oracle (custom-built from Trade events) would be more manipulation-resistant than a Uniswap TWAP for derivative settlement reference prices.

### What CoW Protocol Does NOT Solve

1. **Multi-token pool measurement:** Our core architecture requires a single multi-token pool where cross-token observables (USDC vs. DAI vs. AMPL relative prices) encode macro information. CoW AMM cannot provide this.

2. **Continuous observation:** 30-second batch windows produce discrete observations. High-frequency volatility estimation requires the continuous price curve that CFMMs provide.

3. **Fee-rate observable:** CoW AMM's zero-fee model eliminates the fee-rate signal channel. We need fee accumulation rates as a proxy for trading activity composition.

4. **Emerging-market liquidity:** No cCOP, BRZ, or similar pools exist. We would need to create them, and bootstrap liquidity (which we cannot do per our architectural constraints).

### Recommended Integration Strategy

```
Primary Observation Layer:     Uniswap V3 / Balancer V3 multi-token pools
                               (price, volume, fees, liquidity depth)

Signal Validation Layer:       CoW Protocol batch clearing prices
                               (MEV-free price reference, surplus distribution)

Settlement Execution Layer:    CoW Protocol via ComposableCoW
                               (MEV-protected derivative settlement)

Oracle Layer:                  Custom indexer on GPv2Settlement Trade events
                               (manipulation-resistant TWAP for derivative reference)
```
