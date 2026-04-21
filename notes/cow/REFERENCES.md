# CoW Protocol & CoW AMM — Key References & Documentation

**Last updated**: 2026-04-03
**Status**: Live, growing (~$87B volume in 2025, $188M surplus returned to users)

---

## Critical Context

- CoW AMM implements FM-AMM (Function-Maximizing AMM) from Canidio & Fritsch (2023) — provably eliminates LVR
- Batch auctions (30s intervals) produce MEV-free clearing prices — no sandwich, no frontrunning
- **Surplus** = value that would go to MEV bots in traditional CFMMs, returned to users/LPs
- CoW AMM currently limited to **2-token 50/50 weighted pools only** (no multi-token, no concentrated liquidity)
- No EM stablecoin pools, no gold pools — same gap as other AMMs
- **Novel observable**: Surplus data measures gap between user expectations and true price — leading indicator of FX pressure

---

## Core Contracts

| Contract | Address (same on all chains) |
|---|---|
| GPv2Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` |
| GPv2VaultRelayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFe0110` |
| BCoWPool Factory (Ethereum) | `0xf76c421bAb7df8548604E60deCCcE50477C10462` |
| BCoWPool Factory (Gnosis) | `0x703Bd8115E6F21a37BB5Df97f78614ca72Ad7624` |
| BCoWPool Factory (Arbitrum) | `0xE0e2Ba143EE5268DA87D529949a2521115987302` |

**Supported chains (CoW Protocol)**: Ethereum, Gnosis, Arbitrum, Base, Optimism, Polygon, BNB Chain, Avalanche
**CoW AMM pools**: Ethereum, Gnosis, Arbitrum only

---

## Documentation

### Official Docs (docs.cow.fi)
- [CoW Protocol Overview](https://docs.cow.fi/)
- [CoW AMM Documentation](https://docs.cow.fi/cow-amm)
- [GPv2Settlement Reference](https://docs.cow.fi/cow-protocol/reference/contracts/core/settlement)
- [Programmatic Orders](https://docs.cow.fi/cow-protocol/concepts/order-types/programmatic-orders)
- [TWAP Orders](https://docs.cow.fi/cow-protocol/reference/contracts/programmatic/twap)
- [Milkman Orders](https://docs.cow.fi/cow-protocol/concepts/order-types/milkman-orders)
- [CoW Hooks](https://docs.cow.fi/cow-protocol/reference/core/intents/hooks)
- [Solver Competition Rules](https://docs.cow.fi/cow-protocol/reference/core/auctions/competition-rules)
- [Orderbook API](https://docs.cow.fi/cow-protocol/reference/apis/orderbook)

### API Endpoints
| Chain | Base URL |
|---|---|
| Ethereum | `https://api.cow.fi/mainnet/api/v1/` |
| Gnosis | `https://api.cow.fi/xdai/api/v1/` |
| Arbitrum | `https://api.cow.fi/arbitrum_one/api/v1/` |

Key endpoints: `/quote` (POST), `/orders` (POST), `/orders/{uid}` (GET), `/trades` (GET)

### GitHub
- [CoW Protocol Contracts](https://github.com/cowprotocol/contracts)
- [CoW AMM](https://github.com/cowprotocol/cow-amm)
- [Balancer CoW AMM](https://github.com/balancer/cow-amm)
- [ComposableCoW](https://github.com/cowprotocol/composable-cow)
- [Watch Tower](https://github.com/cowprotocol/watch-tower)
- [Hooks Trampoline](https://github.com/cowprotocol/hooks-trampoline)
- [Solver Template (Python)](https://github.com/cowprotocol/solver-template-py)
- [CoW SDK](https://github.com/cowprotocol/cow-sdk)

---

## Academic Papers

- **FM-AMM Paper**: Canidio & Fritsch, "Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response," arXiv:2307.02074, published at AFT 2023
  - Core theoretical result: FM-AMM eliminates LVR by maximizing the invariant function in batch clearing

---

## Key Technical Concepts

### Batch Auction Flow
```
t=0s    Orders accumulate in orderbook (off-chain, private)
t=30s   Autopilot cuts batch, sends to solvers
t=30-60s Solvers compute optimal settlements
t=60s   Winning solution selected (max surplus)
t=60-90s Winner submits settlement tx on-chain
```

### On-Chain Events
```solidity
event Trade(address indexed owner, IERC20 sellToken, IERC20 buyToken,
            uint256 sellAmount, uint256 buyAmount, uint256 feeAmount, bytes orderUid);
event Settlement(address indexed solver);
```
All `Trade` events between consecutive `Settlement` events belong to the same batch at the same clearing price.

### ComposableCoW (Programmatic Orders)
- Deploy Safe wallet + ComposableCoW module
- Register conditional order with custom `IConditionalOrderGenerator` handler
- Handler's `getTradableOrder()` encodes settlement logic
- Watch tower monitors conditions, submits orders to API
- Solver executes in batch auction
- **Viable for income-settled derivative settlement**

### Variance Swap Settlement Pattern
```
1. Deploy Safe + ComposableCoW
2. Handler: VarianceSwapSettlement contract
3. Handler reads realized variance oracle at expiry
4. Computes payoff: notional * (realized_var - strike_var)
5. Generates CoW order transferring settlement amount
6. Solver executes in MEV-protected batch
```

### CoW Hooks
- **Pre-hooks**: execute before user funds pulled (approvals, unwrapping)
- **Post-hooks**: execute after trade proceeds delivered (vault deposits, bridging, **derivative settlement**)
- Execute via HooksTrampoline contract (security isolation)
- Hook execution NOT enforced on-chain — social consensus among solvers

### Surplus as Macro Observable
- Surplus = execution_price - limit_price (per order)
- High surplus on cCOP-sell orders → cCOP weaker than expected → FX depreciation pressure
- High surplus on cCOP-buy orders → remittance inflow stronger than expected
- **Novel signal with no CFMM analogue** — in Uniswap this value is extracted by MEV bots

### Residual MEV Risks
1. Solver collusion (mitigated by bonding/slashing)
2. Solver front-running own settlement tx (mitigated by limit price enforcement)
3. Block builder MEV on settlement tx (mitigated by private mempools)
4. Genuine informed flow within batches (not MEV, legitimate)
5. Censorship by solvers/Autopilot
6. Batch timing manipulation (30s discrete windows)

---

## Analytics & Dune Dashboards

- [CoW AMM Performance](https://dune.com/cowprotocol/cowamms)
- [CoW Swap High Level Metrics](https://dune.com/cowprotocol/cowswap-high-level-metrics-dashboard)
- [CoW DAO Revenue](https://dune.com/cowprotocol/cow-revenue)
- [Solver Info](https://dune.com/cowprotocol/solver-info)
- [Balancer CoW AMM Pool Analysis](https://dune.com/balancer/balancer-cowswap-amm-pool)
- [DeFiLlama: Balancer CoW AMM](https://defillama.com/protocol/balancer-cow-amm)
- [DeFiLlama: CoW Swap](https://defillama.com/protocol/cowswap)

---

## Known Pools

| Pool | Chain | Tokens | Notes |
|---|---|---|---|
| USDC/WETH | Ethereum | Stablecoin/ETH | Flagship |
| MKR/WETH | Ethereum | Governance/ETH | |
| AAVE/WETH | Ethereum | Governance/ETH | |
| WBTC/wstETH | Ethereum | BTC/Liquid staking | `0xf25a3b5a965c59f88873da93fc2a244b00616be4` |
| COW/WETH | Ethereum | Protocol token/ETH | |
| ARB/WETH | Arbitrum | Governance/ETH | |
| GNO/xDAI | Gnosis | Governance/Stablecoin | |

No stablecoin/stablecoin, gold, or EM stablecoin pools exist.

---

## Relevance to This Project

**Best for**: 
- MEV-free settlement execution layer via ComposableCoW programmatic orders
- Clean volume/price signals as validation layer for contaminated CFMM observables
- Surplus data as novel macro observable (FX pressure detection)

**Not suitable for**:
- Primary measurement instrument (no multi-token pools, no EM pairs, no fee-rate observable)
- High-frequency volatility estimation (30s batch discretization)

**Recommended 3-layer architecture**:
1. **Observe** on Uniswap V3 / Balancer V3 multi-token pools (primary CFMM observables)
2. **Validate** using CoW batch clearing prices as MEV-free ground truth
3. **Settle** via CoW Protocol ComposableCoW for MEV-protected derivative execution

**Key novel finding**: CoW surplus data is a genuinely new information channel — measures the gap between market expectations and equilibrium clearing prices, directly relevant to FX pressure detection in the Colombia cCOP use case.
