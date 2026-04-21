# Balancer V3 — Key References & Documentation

**Last updated**: 2026-04-03
**Status**: V3 contracts live and immutable; Balancer Labs shut down March 2026, protocol continues under OpCo

---

## Critical Context

- **Balancer Labs corporate shutdown** (March 2026) after $110-128M V2 exploit (Nov 2025)
- TVL collapsed to ~$157M from $3.5B peak
- V3 smart contracts are immutable and operational — corporate risk does NOT affect deployed code
- Leaner "OpCo" continues maintenance; development velocity reduced

---

## Core Contracts

| Contract | Address (same on all chains) | Notes |
|---|---|---|
| V3 Vault | `0xbA1333333333a1BA1108E8412f11850A5C319bA9` | Singleton, EIP-1153 transient accounting |
| CoW AMM Factory (ETH) | `0xf76c421bAb7df8548604E60deCCcE50477C10462` | |
| CoW AMM Factory (Gnosis) | `0x703Bd8115E6F21a37BB5Df97f78614ca72Ad7624` | |
| CoW AMM Factory (Arbitrum) | `0xE0e2Ba143EE5268DA87D529949a2521115987302` | |
| StableSurge Hook (ETH) | `0xbdbadc891bb95dee80ebc491699228ef0f7d6ff1` | Dynamic peg-protection fees |

**Deployed on**: Ethereum, Arbitrum, Base, Optimism, Gnosis, Avalanche, Polygon, Plasma, HyperEVM, Mode

---

## Documentation

### Official Docs (docs.balancer.fi)
- [Architecture Overview](https://docs.balancer.fi/concepts/core-concepts/architecture.html)
- [Vault Concepts](https://docs.balancer.fi/concepts/vault/)
- [Swap Fee Documentation](https://docs.balancer.fi/concepts/vault/swap-fee.html)
- [Router Overview](https://docs.balancer.fi/concepts/router/overview.html)
- [Hooks Documentation](https://docs.balancer.fi/concepts/core-concepts/hooks.html)
- [Hooks API Reference](https://docs.balancer.fi/developer-reference/contracts/hooks-api.html)
- [Weighted Pool](https://docs.balancer.fi/concepts/explore-available-balancer-pools/weighted-pool/weighted-pool.html)
- [Weighted Math](https://docs.balancer.fi/concepts/explore-available-balancer-pools/weighted-pool/weighted-math.html)
- [Boosted Pool (ERC-4626)](https://docs.balancer.fi/concepts/explore-available-balancer-pools/boosted-pool.html)
- [reCLAMM Pool](https://docs.balancer.fi/concepts/explore-available-balancer-pools/reclamm-pool/reclamm-pool.html) — suspended Feb 2026
- [Impermanent Loss (Weighted)](https://docs.balancer.fi/concepts/explore-available-balancer-pools/weighted-pool/impermanent-loss.html)
- [Create Custom AMM with Novel Invariant](https://docs.balancer.fi/build/build-an-amm/create-custom-amm-with-novel-invariant.html)
- [Extend Existing Pool Type (Hooks)](https://docs.balancer.fi/build/build-a-hook/extend-existing-pool-type.html)
- [Deployment Addresses (Mainnet)](https://docs.balancer.fi/developer-reference/contracts/deployment-addresses/mainnet.html)
- [Hook Directory](https://hooks.balancer.fi/)
- [CoW AMM Pools Browser](https://balancer.fi/pools/cow)

### GitHub
- [Balancer V3 Monorepo](https://github.com/balancer/balancer-v3-monorepo)
  - [Vault.sol](https://github.com/balancer/balancer-v3-monorepo/blob/main/pkg/vault/contracts/Vault.sol)
  - [BatchRouter.sol](https://github.com/balancer/balancer-v3-monorepo/blob/main/pkg/vault/contracts/BatchRouter.sol)
- [Balancer Deployments](https://github.com/balancer/balancer-deployments)

---

## Key Technical Concepts

### Pool Types
- **Weighted Pool**: 2-8 tokens, configurable weights, `V = product(B_i ^ w_i)` invariant
- **Stable Pool**: Correlated assets, amplification parameter (like Curve)
- **Boosted Pool**: 100% ERC-4626 wrapped, earns yield while providing swap liquidity
- **reCLAMM**: Auto-adjusting concentrated liquidity (suspended for security review)
- **Custom AMM**: Implement `IBasePool` with 3 functions: `onSwap()`, `computeInvariant()`, `computeBalance()`

### Hook System — 10 Hook Points
| Hook | Dynamic Fee? | Reentrant? |
|---|---|---|
| `onRegister` | No | No |
| `onBeforeInitialize` / `onAfterInitialize` | No | No |
| `onBeforeAddLiquidity` / `onAfterAddLiquidity` | No | Yes |
| `onBeforeRemoveLiquidity` / `onAfterRemoveLiquidity` | No | Yes |
| `onBeforeSwap` / `onAfterSwap` | No | Yes |
| **`onComputeDynamicSwapFeePercentage`** | **YES** | Yes |

- 1 hook per pool, immutable after creation (unlike Algebra plugins)
- Hooks CAN emit custom events, accumulate state, read external oracles
- Hooks CANNOT modify token balances directly or change invariant math

### Multi-Token Observables (unique to Balancer)
1. **Joint invariant value** — single scalar encoding all token states
2. **Weight-normalized relative prices** — internally arbitrage-free
3. **Divergence vector** — per-token deviation from target weights
4. **Per-pair fee revenue decomposition** — within a single pool
5. **Per-token decomposed IL** — realized volatility per token

### Notable Hooks in Production
- **StableSurge**: Exponential fee increase when token balance deviates from target weight
- **MEV-Cap** (Base/Optimism): Fee proportional to priority gas price — internalizes MEV for LPs
- **TWAMM**: Time-weighted average market maker for gradual large orders

---

## Analytics & Data

- [Balancer V3 on DeFiLlama](https://defillama.com/protocol/balancer-v3)
- [Balancer CoW AMM TVL on DeFiLlama](https://defillama.com/protocol/balancer-cow-amm)

---

## Articles & Analysis

- [Inside a Balancer V3 Swap with MEV Hook](https://medium.com/balancer-protocol/inside-a-balancer-v3-swap-a-step-by-step-walkthrough-with-the-mev-hook-f4a694928594)
- [MEV Internalization via Priority Fee Taxes](https://medium.com/balancer-protocol/mev-internalization-through-priority-fee-taxes-coming-to-balancer-v3-on-base-q1-2025-f20b3e1b7295)
- [Unlocking MEV for LPs: V3 MEV Capture Hooks](https://medium.com/balancer-protocol/unlocking-mev-for-lps-introducing-balancer-v3-mev-capture-hooks-c81da5a7c022)
- [StableSurge Hook](https://medium.com/balancer-protocol/balancers-stablesurge-hook-09d2eb20f219)
- [StableSurge: Idea to Product](https://medium.com/balancer-protocol/stablesurge-idea-to-product-c7bd5bf4fd09)
- [CoW AMM: Next Frontier of AMM Innovation](https://medium.com/balancer-protocol/cow-amm-the-next-frontier-of-amm-innovation-1718842ad066)
- [Multi-Token Pool Benefits](https://medium.com/balancer-protocol/the-benefits-of-multi-token-pools-653eea3ef03a)
- [MixBytes: Modern DEXes — Balancer V3](https://mixbytes.io/blog/modern-dex-es-how-they-re-made-balancer-v3)
- [Zealynx: Balancer V3 Security Analysis](https://www.zealynx.io/blogs/balancer-protocol-architecture)
- [Algebra Integral vs Balancer/Uniswap Comparison](https://medium.com/@crypto_algebra/integral-by-algebra-next-gen-dex-infrastructure-vs-balancer-uniswap-traderjoe-ba72d69b3431)

### News
- [Balancer Labs Shutdown (CoinDesk)](https://www.coindesk.com/tech/2026/03/24/balancer-labs-will-shut-down-as-corporate-entity-became-a-liability-after-usd110-million-exploit)
- [Balancer Labs Shutdown (Decrypt)](https://decrypt.co/362141/balancer-labs-winds-down-128m-defi-exploit)
- [V3 Expands to Avalanche (The Block)](https://www.theblock.co/post/345510/balancer-v3-expands-to-avalanche-following-governance-vote)
- [V3 on Plasma — $200M TVL First Week](https://outposts.io/article/balancer-v3-achieves-dollar200m-tvl-on-plasma-in-one-week-2947d575-e829-435b-9971-c0ff783d19f6)

---

## Relevance to This Project

**Best for**: Multi-token macro baskets under a single invariant (USDC/DAI/ETH/wstETH). Only production CFMM that can do this.

**Not suitable for**: EM stablecoin pools (none exist, bootstrapping conflicts with project constraint). Use Uniswap V3/V4 for pairwise cCOP/USDC.

**Recommended approach**: Hybrid — Balancer V3 for basket observables + Uniswap V4 for pairwise EM stablecoin observables. Read from existing pools; don't deploy new ones until OpCo stabilizes.

**CoW AMM limitation**: Only 2-token 50/50 pools. No multi-token CoW AMM exists — the cleanest signal source is limited to the simplest pool type.
