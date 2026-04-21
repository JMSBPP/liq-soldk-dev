# EulerSwap Deep Dive

**Date:** 2026-04-03
**Status:** Research report -- live protocol, early-stage TVL
**Author:** Papa Bear analysis

---

## Executive Summary

EulerSwap is a lending-integrated AMM built on top of Euler V2 (EVK + EVC), where each pool is a single-LP operator account that borrows just-in-time from Euler lending vaults to amplify swap depth up to 50x. It launched on Ethereum mainnet in June 2025 with a $500K live CTF (no funds lost). It is compatible with Uniswap V4 hooks for routing. Fees are fixed per pool (set at deploy time, immutable). The curve is a parameterized constant-product variant with a concentration factor that interpolates between Uniswap V2 (c=0) and zero-slippage constant-sum (c=1). Current TVL on DeFiLlama reads near zero across two chains, indicating the protocol is live but in early adoption. There is no native TWAP oracle, no plugin/hook extensibility system of its own (it IS a hook on Uniswap V4), and no emerging-market stablecoin pairs.

---

## 1. Architecture

### 1.1 Core Design: Lending-Integrated AMM

EulerSwap is NOT a standalone AMM. It is an **operator** installed on an Euler V2 lending position. The architecture has three layers:

| Layer | Component | Role |
|-------|-----------|------|
| Base | Euler Vault Kit (EVK) | ERC-4626 lending vaults, interest accrual, collateral management |
| Connector | Ethereum Vault Connector (EVC) | Cross-vault account abstraction, operator permissions |
| AMM | EulerSwap Operator | Swap logic, curve math, JIT borrowing, fee collection |

When an LP "creates a pool," they:
1. Deposit assets into Euler lending vaults (earning supply APY)
2. Install the EulerSwap operator on their EVC account
3. Configure curve parameters (equilibrium price, concentration, fee)
4. The operator contract gains permission to borrow on behalf of the LP's account

### 1.2 Single-LP Pool Model

This is a fundamental architectural departure from all major AMMs:

- **No shared liquidity pools.** Each EulerSwap instance is controlled by exactly one LP entity.
- The LP has full control: withdraw liquidity, uninstall operator, change nothing (parameters are immutable after deployment).
- Multiple single-LP pools for the same pair can coexist; aggregators/routers pick the best one.
- This is structurally closer to a professional market-maker model than a community LP model.

### 1.3 Just-In-Time (JIT) Liquidity via Borrowing

The core capital efficiency mechanism:

1. Trader requests swap: give token A, receive token B
2. If the LP's vault position has insufficient token B:
   - EulerSwap automatically borrows token B from the Euler lending pool
   - Uses the incoming token A as collateral
   - Executes the swap
3. The LP now holds a borrow position (short token B, long token A)
4. This borrow position accrues interest -- cost to the LP

**Amplification claim:** Up to 50x effective depth in optimal cases (stablecoin pairs with high lending liquidity and low borrow rates).

### 1.4 Uniswap V4 Hook Compatibility

EulerSwap registers as a Uniswap V4 hook, meaning:

- Pools are discoverable through Uniswap's routing infrastructure
- Traders interact through standard Uniswap V4 swap interfaces
- The euler-swap-jslib library includes a function to mine salt values that produce Uniswap V4 hook-compatible addresses
- Third-party aggregators (1inch, Paraswap, etc.) can route through EulerSwap pools

EulerSwap does NOT implement its own hook/plugin system. It IS a hook consumer, not a hook provider.

---

## 2. Key Innovation: What Differentiates EulerSwap

### 2.1 AMM Curve: Parameterized Concentration

The curve is defined by three parameters:

| Parameter | Range | Meaning |
|-----------|-------|---------|
| Equilibrium price | Any positive value | Price point where liquidity is maximally concentrated |
| Concentration factor | [0, 1) | How tightly liquidity clusters around equilibrium |
| Fee | Fixed at deploy | Swap fee rate |

Behavior by concentration factor:

- **c = 0**: Equivalent to Uniswap V2 constant-product (x * y = k). Full-range, uniform liquidity.
- **c approaching 1**: Approaches constant-sum (x + y = k). Near-zero price impact around equilibrium. Similar to Curve StableSwap at high amplification.
- **c = 1**: No price impact at all (degenerate case, not practically used).

The jslib exposes:
- `f(x, params)` -- the fundamental curve equation, returns y given x
- `fInverse(y, params)` -- inverse function, returns x given y
- `marginalPrice(reserves)` -- returns marginal price at a given curve point
- `reservesFromPrice(price, params)` -- returns reserves for a target marginal price
- `isValid(point, params)` -- validates a point is on or above the curve

This is a custom curve, not Curve StableSwap, not Uniswap V3 concentrated liquidity. It is a single smooth curve with a tunable concentration parameter, always providing full-range liquidity but with variable density.

### 2.2 Fee Mechanism

**Fixed per pool, immutable after deployment.**

- The LP sets the fee at pool creation time
- Fee applies to the ENTIRE swap volume, including the JIT-borrowed portion
- This means: if JIT borrowing amplifies effective liquidity 10x, the LP earns fees on 10x the volume their own capital could support
- There is NO dynamic fee mechanism (unlike Algebra's volatility-adaptive fees or Uniswap V4 dynamic fee hooks)
- There is NO protocol fee (at least none documented in current sources)

Fee optimization is the LP's responsibility:
- High fee: less volume, more revenue per trade, more IL protection
- Low fee: more volume, less revenue per trade, more IL exposure

### 2.3 Lending Integration: Triple Yield

An EulerSwap LP simultaneously earns:

1. **Supply APY** -- assets in Euler vaults earn lending interest
2. **Swap fees** -- from trades routed through their pool
3. **Potential leverage** -- can borrow against LP position for other strategies

And pays:
- **Borrow interest** on JIT-borrowed amounts
- **Impermanent loss** on price divergence

### 2.4 Comparison with Competitors

| Feature | EulerSwap | Uniswap V3 | Uniswap V4 | Algebra V4 | Balancer V3 | Fluid DEX |
|---------|-----------|------------|------------|------------|-------------|-----------|
| LP model | Single-LP | Multi-LP | Multi-LP | Multi-LP | Multi-LP | Multi-LP |
| Lending integration | Native (EVK) | None | Via hooks | None | Via Aave boosted | Native (Liquidity Layer) |
| JIT borrowing | Built-in | None | Possible via hooks | None | None | Smart Debt |
| Fee type | Fixed/immutable | Fixed per pool | Dynamic via hooks | Dynamic (volatility) | Dynamic | Dynamic |
| Curve | Custom concentration | Tick-range CLMM | Tick-range CLMM | Tick-range CLMM | Weighted/Stable | Custom |
| Hook system | IS a hook (V4) | N/A | Yes (provider) | Plugin system | Hooks (V3) | None |
| Oracle | External (Chainlink etc.) | Built-in TWAP | Built-in TWAP | Built-in TWAP | None native | None native |

### 2.5 Fluid DEX: The Closest Competitor

Both EulerSwap and Fluid DEX compose AMMs with credit markets. Key differences:

- **Fluid** uses a shared Liquidity Layer -- all protocols on Fluid share one custodial pool. EulerSwap uses isolated per-vault liquidity.
- **Fluid** has "Smart Debt" (analogous to JIT liquidity). The mechanism is similar but the architecture differs.
- **Fluid** currently has deeper blue-chip liquidity on its DEX due to unified liquidity design.
- **EulerSwap** gives individual LPs more control and isolation (less systemic risk, more operational complexity).

---

## 3. Deployed Pools and Current Status

### 3.1 Launch Timeline

| Date | Event |
|------|-------|
| ~Q1 2025 | EulerSwap development, fuzzing campaign (Echidna + Foundry) since January 2025 |
| May 2025 | Announcement, multiple audit completions |
| June 2, 2025 | Mainnet beta: USDC/USDT pool deployed with $500K real liquidity as live CTF |
| June 2025 | Cantina CTF competition: 600+ participants, no funds lost, no high/medium issues found |
| Mid-2025 | Maglev UI launched for pool creation and management |
| 2025-2026 | Gradual adoption phase |

### 3.2 Chain Deployment

Per DeFiLlama, EulerSwap is tracked on **two chains** (likely Ethereum mainnet + one L2). Current TVL reads near zero, indicating minimal active liquidity.

**Known contract:**
- Ethereum Mainnet: `0xb013be1D0D380C13B58e889f412895970A2Cf228`

### 3.3 Known Pools

| Pair | Chain | Notes |
|------|-------|-------|
| USDC/USDT | Ethereum | The CTF launch pool, $500K initial liquidity |

**No confirmed evidence of:**
- wstETH or sDAI yield-bearing token pairs
- PAXG gold-backed pairs
- Emerging-market stablecoin pairs (cCOP, MXNC, PHP stablecoins, etc.)
- Significant active TVL beyond initial seeding

### 3.4 TVL and Volume

- DeFiLlama shows TVL effectively at zero across both chains as of early 2026
- Recent metrics show fee surges (+97%) alongside volume drops (-69%), suggesting sporadic activity
- Euler V2 overall has ~$4B+ in deposits, but EulerSwap specifically has negligible TVL
- The protocol is live and functional but has not achieved meaningful organic adoption yet

### 3.5 Security Posture

- **5 audit firms** engaged
- ChainSecurity audit completed
- Cantina competition (600+ participants, $500K at stake, zero exploits)
- Continuous fuzzing since Jan 2025 (Echidna + Foundry, led by Victor Martinez)
- No high or medium severity issues found across all review surfaces

---

## 4. Observable Extraction: What Can Be Read On-Chain

### 4.1 Direct On-Chain Observables

From each EulerSwap pool contract:

| Observable | Source | Macro Proxy Potential |
|------------|--------|----------------------|
| Spot price | Curve reserves / marginal price calculation | Direct asset price |
| Reserve balances | Pool state (token0, token1 amounts) | Directional flow indicator |
| Borrow position | Euler vault debt for the LP account | Credit demand / stress indicator |
| Health factor | EVK position health | Leverage stress |
| Swap fee rate | Immutable pool parameter | Market-maker confidence |
| Concentration factor | Immutable pool parameter | LP's volatility expectation at deploy time |
| Equilibrium price | Immutable pool parameter | LP's fair value estimate at deploy time |

### 4.2 Derived from Euler V2 Vaults (Underlying)

Since EulerSwap pools sit on top of EVK vaults, you can read:

| Observable | Source | Macro Proxy Potential |
|------------|--------|----------------------|
| Supply APY | Vault interest rate model | Risk-free rate proxy |
| Borrow APY | Vault interest rate model | Credit demand / cost of capital |
| Utilization rate | Vault utilization | Credit market tightness |
| Total supply / borrow | Vault state | Market depth / confidence |
| Liquidation events | EVC events | Stress events |

### 4.3 What EulerSwap Does NOT Provide

- **No native TWAP oracle.** Unlike Uniswap V2/V3, there is no cumulative price accumulator. Price must be computed from reserves.
- **No volume accumulator.** Must be tracked via event indexing.
- **No fee accumulator.** Fee revenue must be computed from swap events.
- **No implied volatility signal.** The concentration parameter is fixed at deploy, not dynamic. It does not update with market conditions.

### 4.4 Observable Extraction Strategy

To extract useful observables from EulerSwap:

1. **Index swap events** -- compute volume, fee revenue, directional flow over time
2. **Read vault state** -- supply/borrow rates, utilization, health factors via EVK view functions
3. **Compute spot price** -- use the jslib `marginalPrice()` function off-chain, or replicate the curve math in a view call
4. **Monitor borrow positions** -- track JIT borrow sizes as a proxy for swap demand exceeding LP capital
5. **Cross-reference with Euler lending rates** -- the spread between swap fee revenue and borrow cost is effectively the LP's risk premium

### 4.5 Relevance to Macro Hedging Instruments

**Low relevance currently.** The protocol has:
- No emerging-market pairs
- No stablecoin pairs beyond USDC/USDT
- Near-zero TVL (insufficient depth for meaningful price discovery)
- No dynamic observables (fees, concentration are immutable)

**Potential future relevance IF:**
- Pools are created for yield-bearing or macro-relevant pairs
- Euler lending rates for stablecoins become deep enough to serve as rate benchmarks
- The borrow rate integration (supply APY + swap fees - borrow cost) could produce a composite yield metric useful as a DeFi-native interest rate observable

---

## 5. Extensibility: Plugin/Hook System

### 5.1 EulerSwap IS a Hook, Not a Hook Provider

EulerSwap does not have its own plugin or hook extensibility system. The architecture is:

```
Uniswap V4 PoolManager
    |
    +-- EulerSwap Hook (registers as a V4 hook)
            |
            +-- Euler Vault Kit (EVK) -- lending logic
            +-- Ethereum Vault Connector (EVC) -- account abstraction
```

### 5.2 Operator System as Limited Extensibility

The EVC operator model provides some extensibility:

- An LP can install the EulerSwap operator on their account
- Operators are smart contracts that can act on behalf of the account
- In theory, custom operator contracts could wrap EulerSwap logic with additional behavior
- The Maglev UI is the primary tool for creating and managing operators

### 5.3 What This Means

- You cannot write "EulerSwap plugins" the way you write Uniswap V4 hooks or Algebra plugins
- You CAN write custom operator contracts that interact with EulerSwap pools
- You CAN build on top of EulerSwap via the EVC account abstraction layer
- The jslib and SDK provide programmatic access for off-chain automation

---

## 6. Assessment for Universal Pool / Macro Hedging Use Case

### 6.1 Strengths

1. **Lending rate integration** -- the fact that EulerSwap LPs are simultaneously in lending markets means the protocol produces composite yield signals (supply APY + swap fees - borrow cost) that are richer than pure AMM observables
2. **Single-LP model** -- allows sophisticated actors to create bespoke pools with specific curve parameters, which could include macro-relevant pairs if the right LPs participate
3. **Euler V2 vault observables** -- supply/borrow rates, utilization, and health factors across multiple asset types provide a richer observable set than pure AMMs
4. **Modular architecture** -- EVK + EVC is genuinely composable; building on top is architecturally clean

### 6.2 Weaknesses

1. **No dynamic fees** -- the immutable fee means the protocol does not produce a volatility-adaptive signal. Algebra's dynamic fee mechanism is strictly more informative for volatility extraction.
2. **No native oracle** -- no TWAP, no cumulative price. Observation requires event indexing.
3. **Near-zero adoption** -- insufficient liquidity for meaningful price discovery or observable extraction
4. **No emerging-market pairs** -- no cCOP, no PHP stablecoins, no PAXG. The pool set is limited.
5. **Single-LP fragmentation** -- liquidity is spread across isolated single-LP pools, making aggregation harder than unified-pool designs
6. **Immutable parameters** -- concentration and equilibrium price are fixed at deploy. The pool cannot adapt to changing market conditions (the LP must create a new pool).

### 6.3 Verdict

**EulerSwap is architecturally interesting but not currently useful for the macro hedging instrument project.** The lending-rate integration is the most valuable feature -- if Euler V2 vaults develop deep stablecoin markets, the supply/borrow rate observables could serve as DeFi-native interest rate proxies. However, the AMM itself produces fewer observables than Uniswap V3 (no TWAP), Algebra V4 (no dynamic fees), or even Balancer V3 (no multi-asset pools).

**Watch list items:**
- Monitor if any LP creates emerging-market stablecoin pairs on EulerSwap
- Track Euler V2 lending rate depth for USDC, DAI as potential rate benchmarks
- The composite yield metric (supply APY + swap fees - borrow cost) is a novel observable worth formalizing if pool depth materializes

---

## 7. Key Repositories and Resources

| Resource | URL |
|----------|-----|
| Euler Docs: EulerSwap Concepts | https://docs.euler.finance/concepts/advanced/euler-swap/ |
| Euler Docs: How It Works | https://docs.euler.finance/developers/euler-swap/how-it-works/ |
| Euler Docs: LP Considerations | https://docs.euler.finance/developers/euler-swap/lp-considerations/ |
| Euler Docs: Strategy Profitability | https://docs.euler.finance/concepts/financial/strategy-profitability/ |
| Euler Docs: Maglev (Pool Creator UI) | https://docs.euler.finance/creator-tools/maglev/overview/ |
| Euler Docs: Swap Audits | https://docs.euler.finance/security/swap-audits/ |
| Blog: Introducing EulerSwap | https://www.euler.finance/blog/introducing-eulerswap |
| GitHub: euler-swap-jslib | https://github.com/euler-xyz/euler-swap-jslib |
| GitHub: euler-swap-solhint-rules | https://github.com/euler-xyz/euler-swap-solhint-rules |
| GitHub: euler-maglev | https://github.com/euler-xyz/euler-maglev |
| GitHub: euler-price-oracle | https://github.com/euler-xyz/euler-price-oracle |
| GitHub: euler-sdk | https://github.com/euler-xyz/euler-sdk |
| DeFiLlama: EulerSwap | https://defillama.com/protocol/eulerswap |
| DeFiLlama: Euler (lending) | https://defillama.com/protocol/euler |
| Cantina: EulerSwap CTF | https://cantina.xyz/competitions/a188a03f-4631-4b58-82ce-a5818a6df332 |
| Cantina: Euler Bounty | https://cantina.xyz/bounties/4d285eee-602e-440a-845e-25e155cec26a |
| ChainSecurity Audit | https://www.chainsecurity.com/security-audit/eulerswap |
| OAK Research: Euler Deep Dive | https://oakresearch.io/en/analyses/fundamentals/deep-dive-into-euler-products-vaults-markets-earn-eulerswap |
| Fluid DEX Comparison | https://letsgetonchain.medium.com/fluid-dex-vs-eulerswap-part-1-comparing-the-credit-market-foundations-0319ad42c9d6 |
| The Block: Launch Announcement | https://www.theblock.co/post/356004/euler-to-launch-eulerswap-dex-with-lending-boosted-yield |
| Cyfrin: Vault Withdrawal Flow | https://www.cyfrin.io/blog/how-vault-withdrawals-work-in-eulerswap-full-flow-explained |

---

## 8. Open Questions for Further Investigation

1. **What is the exact curve equation?** The jslib has it implemented but no published whitepaper formalizes it. Reading the jslib source (`euler-xyz/euler-swap-jslib/src/`) would reveal the exact math.
2. **What is the second chain on DeFiLlama?** Likely Base or Arbitrum given Euler V2 deployments, but unconfirmed.
3. **Are there any active pools beyond USDC/USDT?** The Maglev UI or on-chain factory events would reveal this.
4. **Does the EulerSwap operator emit events for swap execution?** Critical for indexing volume and building observables. Needs contract ABI inspection.
5. **Can the euler-price-oracle system be pointed at EulerSwap pools?** If so, Euler vaults could use EulerSwap as a price source, creating a feedback loop.
