# Baseline Markets -- Deep Dive Research Report

**Date**: 2026-04-08
**Analyst**: Papa Bear (automated research)
**Purpose**: Evaluate Baseline Markets for macro-risk hedging architecture relevance

---

## Executive Summary

Baseline Markets is NOT an AMM, NOT a derivatives protocol, and NOT a lending protocol in the traditional sense. It is an **automated tokenomics engine** -- a permissionless factory for launching ERC-20 tokens ("bTokens") that self-manage their own liquidity on Uniswap V3 pools via an on-chain algorithmic market maker. Each bToken has a monotonically-increasing floor price (the "Baseline Value" or BLV) enforced by protocol-owned concentrated liquidity positions.

**Bottom line for our project**: Baseline Markets produces very few observables relevant to macro-risk hedging. It is a token-launch infrastructure protocol, not a measurement instrument. It has no stablecoin pools, no multi-token pools, no emerging-market exposure, and no dynamic fee component extractable for hedging. **It is not a useful building block for our architecture.**

---

## 1. Protocol Overview

### What IS Baseline Markets?

Baseline is an automated tokenomics engine for ERC-20 tokens. It gives newly-launched tokens:
- **Protocol-owned liquidity** seeded automatically into a Uniswap V3 pool at launch
- **A guaranteed, monotonically-increasing floor price** (the BLV)
- **Non-liquidatable borrowing** against the BLV
- **Automated market making** via the Baseline Market Maker (BMM), which runs 24/7 on-chain
- **Fee capture and redistribution** to stakers

It is best understood as a **token issuance framework with built-in reflexivity dampening**: it replaces external market makers with protocol-managed concentrated liquidity that programmatically defends a floor price.

### Problem It Solves

Traditional token launches suffer from:
- Dependence on external market makers (often adversarial)
- Liquidity fragility after initial hype fades
- No floor price guarantee, leading to reflexive death spirals
- Rug-pull risk from LP withdrawal

Baseline makes the token itself the owner and manager of its liquidity, with programmatic guarantees that the floor price can only increase.

### Team, History, and Status

- **Predecessor**: Jimbos Protocol (Arbitrum), which suffered a **$7.5M flash loan attack** in May 2023 due to lack of slippage control on liquidity-shifting operations. On July 28, 2023, Jimbos was renamed to Baseline Protocol.
- **Team origin**: Connected to the Olympus DAO (OHM) ecosystem. The key figure "Indigo" co-authored the Olympus Bonds whitepaper with Zeus. The team has tried to distance from OHM branding.
- **Launch**: The first bToken, $YES, launched on February 15, 2024 via an "Initial Baseline Value" (IBLV) event that raised ~311 ETH (~$1M).
- **Current version**: V3 (codename "Mercury") -- in development or recently deployed. V2 was audited by Guardian Audits.
- **Funding**: No public VC funding rounds found. Appears bootstrapped/community-funded.
- **Status**: Live but small. TVL ~$1.2M per DeFiLlama as of early 2026.

### Chain Deployments

- **Primary deployment**: Blast L2 (Ethereum L2)
- **No evidence of**: Ethereum mainnet, Arbitrum, Base, or other L2 deployments
- The docs reference "Baseline Mercury" as in development, suggesting future multi-chain plans

---

## 2. Architecture

### Core Mechanism

Baseline's core innovation is managing three distinct concentrated liquidity positions on a Uniswap V3 pool for each bToken, paired against a reserve asset (typically wETH):

#### The Three Liquidity Positions

1. **Floor Position**: Narrow-range single-sided liquidity at the bottom of the order book. Defends the BLV floor price. The lowest tick in this position IS the BLV. Can never be moved down, only up via "bumps."

2. **Anchor Position**: Broader-range liquidity from BLV up to the current market price. Provides liquid trading conditions and absorbs sell pressure. Range: up to ~10 tick spacings below current price.

3. **Discovery Position**: Single-sided token liquidity above the current market price. Enables upward price discovery by distributing supply as price rises. Sits right above the current active tick spacing.

#### Key Operations

- **Rebalance()**: The V3 core function. Adjusts all three positions in response to market changes. Replaces the V2 fragmented operations (sweep, slide, bump).

- **Bump**: When excess reserves accumulate (from fees + loan interest + afterburner), the Floor position is moved up one full tick spacing (~2% increase in BLV). This is irreversible -- BLV can only increase.

- **Slide**: When price drops, Anchor and Discovery positions are re-adapted to center around the new active price. Ensures adequate liquidity near the market price.

- **Afterburner**: A randomized leveraged buy-back and burn mechanism. Uses leverage to repurchase tokens from the market and burns them, reducing circulating supply.

### Smart Contract Architecture

- **Factory pattern**: Permissionless -- anyone (including AI agents) can deploy a bToken via the Baseline Factory
- **Each bToken is an independent deployment** with its own Uniswap V3 pool and BMM
- **Token standard**: ERC-420 (custom Baseline extension of ERC-20, not a widely adopted standard)

### GitHub

- Organization: https://github.com/0xbaseline
- Only 2 public repositories found:
  - `baseline-docs` (MDX, MIT license, last updated March 2025)
  - `docker-pnpm` (Dockerfile for Fleek)
- **Core contracts are NOT open-sourced** (or are in private repos)
- No public members visible on the org

### Contract Addresses

- The docs reference a contracts page at https://docs.baseline.markets/contracts and a deployments page, but specific addresses were not surfaced in web search
- Deployed on Blast L2; contracts verifiable on Blastscan

### Integration with Other Protocols

- **Built on top of Uniswap V3** -- uses Uniswap V3 concentrated liquidity pools as the execution layer
- **Does NOT use Chainlink or any external oracle** -- the Uniswap V3 pool IS the price oracle (the BLV tick is the floor)
- No integration with Balancer, Curve, or other AMMs
- No cross-protocol composability documented

---

## 3. Token/Asset Model

### Token Types

- **bTokens**: Any ERC-420 token deployed via the Baseline Factory. Each bToken has its own BMM and Uniswap V3 pool.
- **Reserve asset**: Typically wETH (the pair asset in the Uniswap V3 pool)
- **$YES**: The flagship/first bToken, launched as a demonstration of the system

### Native Token

- There is no Baseline protocol governance token documented
- $YES is the first bToken but is specific to the YES community, not a protocol governance token

### Pools

- Each bToken has exactly ONE pool: bToken/wETH on Uniswap V3
- **No multi-token pools**
- **No stablecoin pools** (no bToken/USDC, bToken/DAI, etc.)
- **No emerging-market currency pairs**

### Yield/Staking

- bToken stakers receive trading fees from the Uniswap V3 pool
- Borrowers can borrow against BLV at 0% interest (loan fees contribute to BLV growth)
- No external yield integrations (no Aave, no Compound)

---

## 4. Fee/Pricing Mechanism

### Trading Fees

- Standard Uniswap V3 swap fees apply to all bToken trades
- 100% of LP fees are captured by the protocol (since it owns all liquidity)
- Fee revenue is distributed to stakers
- A portion of excess reserves from fees goes to the team during BLV bumps

### No Dynamic Fee Component

- Baseline does NOT implement dynamic fees
- It uses Uniswap V3's standard fee tier for the pool
- No surge pricing, no volatility-adjusted fees, no directional fee asymmetry
- This is a critical difference from protocols like Algebra, Ekubo, or Balancer V3

### Pricing/Oracle

- **No external oracle** (no Chainlink, no TWAP oracle)
- Price discovery occurs entirely through the Uniswap V3 pool
- The BLV (floor price) is encoded as the lowest tick in the Floor position
- The "oracle" is the Uniswap V3 pool's own tick/price state

---

## 5. Observable Extraction

### What On-Chain State Can Be Read

From the Uniswap V3 pool:
- Current tick/price of the bToken
- Liquidity at each tick range (Floor, Anchor, Discovery positions)
- Cumulative swap volume and fees
- Standard Uniswap V3 slot0, tick, position data

From Baseline contracts:
- Current BLV (floor tick)
- Circulating supply vs total supply
- Outstanding borrows ("virtual reserves")
- Staking balances and accumulated rewards
- Afterburner state

### Events Emitted

Not documented in public sources, but likely includes:
- BLV bump events (floor tick increase)
- Rebalance events
- Borrow/repay events
- Afterburner execution events
- Standard ERC-20 Transfer events

### Novel Observables (Compared to Standard AMMs)

1. **BLV tick trajectory**: A monotonically-increasing floor price observable. This is unique -- standard AMMs have no concept of a one-directional price floor.

2. **Circulating supply dynamics**: The relationship between circulating supply, total supply, and burned supply after afterburner events.

3. **Borrow utilization**: The ratio of borrowed reserves to Floor position reserves. This is a unique credit metric.

4. **Premium over BLV**: The ratio of market price to BLV, which measures speculative premium. This is analogous to a "premium to NAV" in traditional finance.

5. **Bump frequency**: How often BLV increases, which reflects protocol health and fee generation.

---

## 6. Macro Hedging Relevance Assessment

### FX Depreciation / Inflation / Capital Flight / Interest Rate Shocks / Remittance Corridor Risk

**Rating: NOT RELEVANT**

Baseline Markets produces NONE of the observables needed for measuring:
- FX depreciation: No fiat-pegged or EM stablecoin pools exist
- Inflation: No CPI-linked tokens or real-yield instruments
- Capital flight: No cross-border flow tracking
- Interest rate shocks: Borrowing is at 0% with no market-driven rate
- Remittance corridor risk: No remittance-related pairs or corridors

### Emerging-Market Stablecoin Pools

**None.** Baseline operates exclusively with bToken/wETH pairs on Blast. No cCOP, cUSD, USDT, DAI, or any stablecoin integration.

### Multi-Token Pools

**None.** Each bToken has exactly one pool with one pair (bToken/wETH).

### MEV Protection

**None documented.** Baseline relies on standard Uniswap V3 execution with no MEV mitigation (no private mempools, no batch auctions, no CoW-style coincidence of wants).

### Comparison to Our Target Protocols

| Feature | Baseline | Ekubo | Balancer V3 | Algebra | CoW Protocol |
|---------|----------|-------|-------------|---------|--------------|
| Multi-token pools | No | No | Yes | No | N/A (solver) |
| Dynamic fees | No | Yes | Yes (hooks) | Yes | N/A |
| Stablecoin pools | No | Yes | Yes | Yes | Yes |
| EM currency exposure | No | No | No | No | No |
| MEV protection | No | Partial | No | No | Yes |
| Custom observables for hedging | Limited | Moderate | High | Moderate | Low |
| TVL | ~$1.2M | ~$100M+ | ~$1B+ | ~$500M+ | N/A |

**Verdict**: Baseline is the LEAST relevant protocol of any we have evaluated for our macro-risk hedging architecture. It operates in a completely different problem space (token launch infrastructure) and produces no observables useful for measuring macro-economic risk in underserved countries.

---

## 7. Risks and Open Questions

### Protocol Maturity

- **Immature**: TVL of ~$1.2M is extremely small
- **Predecessor hacked**: Jimbos Protocol lost $7.5M in a flash loan attack in May 2023
- **V2 had 22 high-severity vulnerabilities** found by Guardian Audits before launch
- V3 ("Mercury") is in development -- maturity unknown

### Audit Status

- **Guardian Audits**: Conducted multiple security reviews of V2. Found 22 high-severity issues including complete DoS vectors, risk-free arbitrages, and system invalidation. All reported as resolved.
- Auditors used Echidna invariant testing with 100+ invariants over tens of millions of randomized runs
- Post-audit, the protocol has operated for over a year without reported incidents
- V3 audit status: Unknown

### TVL Trajectory

- ~$1.2M TVL is effectively negligible in DeFi terms
- Single-chain deployment (Blast) limits growth
- Blast itself has declining TVL relative to 2024 hype period

### Team/Governance Risk

- **Anonymous/pseudonymous team** with roots in Olympus DAO ecosystem
- **Previous project (Jimbos) was hacked and rebranded** -- this is a red flag
- **Closed-source contracts** (no public GitHub for core contracts)
- No governance token or DAO structure documented
- Team takes a portion of reserves during BLV bumps -- extractive economics

### Ponzi Risk Assessment

Baseline has faced persistent "ponzi" criticism because:
- The "up-only" floor price framing creates FOMO dynamics
- Revenue comes from new buyers paying a premium over BLV
- The afterburner (leveraged buyback + burn) creates reflexive upward pressure
- 0% interest borrowing against BLV is economically unusual
- The system works well in growing markets but behavior in prolonged drawdowns is untested at scale

This is NOT necessarily a ponzi, but the mechanism shares structural similarities with reflexive token designs (OHM, etc.) that have historically experienced severe drawdowns when net new capital inflows stop.

### Novel Risks

1. **Blast chain risk**: Single-chain deployment on a relatively new L2 with uncertain long-term viability
2. **Uniswap V3 dependency**: Entirely dependent on Uniswap V3's concentrated liquidity infrastructure
3. **BLV bump gaming**: Sophisticated actors could time trades around BLV bumps for guaranteed profit
4. **Virtual reserves accounting**: Borrowed reserves are tracked as "virtual" -- if borrows exceed actual reserves in the Floor position, the floor guarantee could be stressed
5. **Closed source**: Cannot independently verify contract behavior

---

## 8. Conclusion and Recommendation

### For Our Project

**SKIP.** Baseline Markets is not relevant to our macro-risk hedging architecture. Specifically:

1. It produces no observables for FX, inflation, capital flight, interest rates, or remittance risk
2. It has no stablecoin pools, no multi-token pools, no emerging-market exposure
3. It has no dynamic fee component to extract volatility signals from
4. It operates on a single chain (Blast) with ~$1.2M TVL
5. The core contracts are closed-source

### What Baseline IS Good For (Not Our Use Case)

- Token creators who want automated liquidity management with floor price guarantees
- Projects that want protocol-owned liquidity without external market maker dependency
- Communities that want "up-only" tokenomics with built-in reflexivity dampening

### Protocols to Prioritize Instead

For our CFMM-observable-based hedging instruments, we should focus on:
- **Algebra** (dynamic fees as volatility signal)
- **Balancer V3** (multi-token weighted pools as index measurement instruments)
- **Ekubo** (StarkNet native with dynamic fees and deep stablecoin liquidity)
- **Uniswap V4 hooks** (custom observable extraction)

---

## Sources

- [Baseline Docs - Main](https://docs.baseline.markets/)
- [Baseline Docs - How It Works](https://docs.baseline.markets/how-baseline-works)
- [Baseline Docs - BLV Theory](https://docs.baseline.markets/theory)
- [Baseline Docs - Dynamic Liquidity](https://docs.baseline.markets/btokenomics/dynamic_liquidity)
- [Baseline Docs - Contracts](https://docs.baseline.markets/contracts)
- [Baseline Docs - Audits](https://docs.baseline.markets/contracts/security)
- [Baseline Docs - Links](https://docs.baseline.markets/resources/links)
- [Baseline Docs - FAQ](https://docs.baseline.markets/resources/faq)
- [Baseline Docs - Launch a Token](https://docs.baseline.markets/creator)
- [Baseline Homepage](https://www.baseline.markets/)
- [DeFiLlama - Baseline Protocol](https://defillama.com/protocol/baseline-protocol)
- [GitHub - 0xbaseline](https://github.com/0xbaseline)
- [Guardian Audits - Baseline Vulnerabilities](https://guardianaudits.com/blog/baseline-markets-vulnerabilities-reported-and-resolved)
- [Mirror.xyz - Case Study: $YES](https://mirror.xyz/0xe7AD459A24A10C5E94B76CcD24da62A8394eBf5f/Q9pBLoPxjgg6SatMnkojs5faAyBwlhEQAKFh3jfDFjI)
- [Mirror.xyz - Introducing Baseline](https://mirror.xyz/0x371076D033849C014a3eF37f1a63c44916604cac/DrpUgLaSfNGQqjr8ixTxRMoOazG7asQAaDBTLx93olA)
- [Gate.io - YES Token Analysis](https://www.gate.com/learn/articles/unraveling-the-mystery-of-baseline-and-yes-token-s-up-only-price/2037)
- [YourCryptoLibrary - Baseline Overview](https://yourcryptolibrary.com/blockchain/a-new-era-of-stability-in-defi-markets-what-is-baseline-and-yes-protocol-in-defi/)
- [Medium - Baseline Deep Dive](https://medium.com/@jjimny99/unlocking-liquidity-a-deep-dive-into-baseline-protocols-revolutionary-erc20-token-economics-ce2129b5a0ac)
- [Substack - Introducing Baseline Markets](https://basedboo.substack.com/p/introducing-baseline-a-dex-that-makes)
- [Baseline on X/Twitter](https://x.com/baselinemarkets)
