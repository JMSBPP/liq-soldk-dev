# Architecture Discovery: Bunni V2's Option Payoff Mechanism

**Date**: 2026-04-03
**Finding**: Bunni V2 realizes option payoffs through a fundamentally different mechanism than Panoptic. The bridge to traditional LP-as-option theory exists but runs through **portfolio rebalancing theory**, not through swap fee/IL dynamics.

---

## 1. The Three Option-Writing Channels in AMMs

### Channel A: Swap Fee/IL (Panoptic, Uniswap V3 LP)
```
Swaps flow through LP's tick range
  → Fees earned (option premium)
  → Price movement causes IL (option payout)
  → Net P&L = fees - IL ≈ short straddle
```
**Mechanism**: The AMM's constant-product/concentrated-liquidity math mechanically converts price movement into token rebalancing. Each swap that crosses the LP's range forces a trade at a worse price than market — this IS the option payout. Fees compensate.

**Key property**: Requires organic swap volume through the specific pool.

### Channel B: Rebalancing at Oracle Price (Bunni V2)
```
LDF defines target token distribution at each tick
  → Oracle/TWAP updates external price
  → Rebalancer sells excess token via FloodPlain order
  → Token composition adjusts to match LDF at new price
  → Value change = f(LDF shape, price path)
```
**Mechanism**: The rebalancer acts as a **portfolio insurance program**. The LDF defines the desired portfolio composition at every possible price. When price moves, the rebalancer trades to maintain the LDF-shaped distribution. This trading pattern IS the option replication.

**Key property**: Does NOT require organic swap volume through the pool. The option payoff comes from the rebalancing trades executed via FloodPlain (external order flow), not from in-pool AMM swaps.

### Channel C: Dynamic Fee Repricing (Algebra Adaptive Fee)
```
Standard concentrated liquidity position (like Uniswap V3)
  → Swaps generate fees + IL normally
  → But fee level adjusts with realized vol
  → Premium scales with vol → automatic vol surface
```
**Mechanism**: The fee IS the premium, and it reprices in real-time based on a volatility measure.

**Key property**: Requires organic swap volume, but the fee adjustment means the premium tracks vol.

---

## 2. Bunni V2 as Dynamic Portfolio Rebalancing

### The Perold-Sharpe Framework (1988)

Perold & Sharpe showed that **any rebalancing rule maps to a specific payoff function**:

| Rebalancing Rule | Equivalent Payoff | Finance Name |
|---|---|---|
| **Constant-mix** (rebalance to fixed % weights) | Concave (sells rallies, buys dips) | **Short straddle / variance swap** |
| **Buy-and-hold** (never rebalance) | Linear | No option exposure |
| **CPPI** (increase risky asset as it rises) | Convex (buys rallies, sells dips) | **Long straddle / portfolio insurance** |
| **Constant-proportion with mean reversion** | Concave near strike, convex at tails | **Short butterfly** |

### Bunni V2's LDF as a Rebalancing Rule

The LDF defines a **target portfolio composition at every price level**. This IS a rebalancing rule:

```
f(tick) = LDF density at tick
          ↕
"At price p, the pool should hold X% token0 and Y% token1"
          ↕
When price moves from p₁ to p₂:
  Rebalancer sells token that's in excess
  Buys token that's in deficit
  To match f(tick) at the new price
```

**GeometricDistribution LDF** → single-peaked bell curve → the rebalancing rule is:
- Near the peak: hold balanced amounts (delta ≈ 0)
- Price moves away from peak: sell the appreciating token, buy the depreciating token
- This is a **constant-mix strategy around the peak** → **concave payoff** → **short straddle**

**The short straddle payoff emerges NOT from AMM math, but from the rebalancing pattern.**

### The Key Equation

For a Bunni V2 position with LDF `f(tick)`, the value at terminal price `S_T` is:

```
V(S_T) = V₀ + ∫₀ᵀ Δ(S_t, f) dS_t + rebalancing_friction
```

Where:
- `Δ(S_t, f)` is the portfolio delta implied by the LDF at price S_t
- The integral captures the path-dependent rebalancing P&L
- `rebalancing_friction` = slippage + gas costs of FloodPlain orders

For a GeometricDistribution centered at K with width σ:
```
Δ(S, f) = ∫ f(tick) × δ(tick, S) d(tick)
```

Where `δ(tick, S)` is the delta of a unit of liquidity at that tick. The density-weighted delta creates a smooth delta profile that looks like:
- Δ → -1 as S → ∞ (fully in depreciating token)
- Δ → +1 as S → 0 (fully in appreciating token)  
- Δ ≈ 0 at S = K (balanced at the peak)

This delta profile is exactly the delta of a **short straddle at strike K**.

---

## 3. The Bridge: Three Architectures, One Payoff

| Dimension | Panoptic (Channel A) | Bunni V2 (Channel B) | Algebra (Channel C) |
|---|---|---|---|
| **How option is written** | AMM concentrated liquidity math | LDF-shaped portfolio rebalancing | AMM concentrated liquidity math |
| **Premium source** | Swap fees through LP range | Rebalancing profit (buy low, sell high in mean-revert regimes) | Dynamic swap fees |
| **Payout mechanism** | IL from swaps crossing range | Rebalancing loss (buy high, sell low in trending regimes) | IL from swaps crossing range |
| **Price discovery** | In-pool (AMM price moves from swaps) | External (oracle/TWAP drives rebalancing) | In-pool (AMM price moves from swaps) |
| **Volume requirement** | Needs organic swap volume | Needs rebalance execution (FloodPlain) | Needs organic swap volume |
| **What determines strike** | Midpoint of LP tick range | LDF center tick | Midpoint of LP tick range |
| **What determines width** | LP tick range width | LDF sigma parameter | LP tick range width |
| **Payoff formula** | `premium - α|√S - √K|` | `V₀ + ∫Δ(S,f)dS + friction` | `premium - α|√S - √K|` (with dynamic premium) |

### The Convergence

All three converge to the same payoff shape (short straddle for single-peaked distributions) because:

1. **Panoptic**: Concentrated liquidity at tick range [a,b] = selling a straddle at geometric mean of [a,b]
2. **Bunni V2**: LDF-shaped rebalancing with GeometricDistribution = Perold-Sharpe constant-mix around peak → concave payoff → short straddle
3. **Algebra**: Same as Panoptic but with dynamically-priced premium

The bridge is: **concentrated liquidity IS a rebalancing rule, and rebalancing rules ARE options.**

Uniswap V3's AMM automates the rebalancing via the constant-product formula within tick ranges. Bunni V2 separates the rebalancing into an explicit step (FloodPlain orders) governed by the LDF. Both produce the same payoff — just through different execution channels.

---

## 4. Observable Differences for Empirical Analysis

Although the payoff shape converges, the **execution channel** creates observable differences:

### Bunni V2 (Rebalancing Channel)
- **P&L is path-dependent**: The rebalancing P&L depends on WHEN rebalancing happens, not just terminal price
- **Discrete rebalancing**: FloodPlain orders execute at discrete intervals, creating rebalancing drag
- **Slippage matters**: Each rebalance trade has slippage, eating into the "premium"
- **No fee income from swaps**: Premium comes from the rebalancing profit itself
- **Observable**: Rebalance order execution prices vs oracle prices → rebalancing P&L

### Panoptic/Algebra (Swap Channel)  
- **P&L is path-dependent too**: But through continuous AMM swaps, not discrete rebalancing
- **Continuous rebalancing**: Every swap through the range is a micro-rebalance
- **Swap fee income**: Explicit premium from fee collection
- **Observable**: Fee accrual rate + IL → option P&L decomposition

### Measurable Bridge
To compare Bunni V2 and Algebra empirically:

| Metric | Bunni V2 Analog | Algebra Analog |
|---|---|---|
| **Premium** | Rebalancing profit (sold high, bought low) | Swap fee income |
| **Payout** | Rebalancing loss (sold low, bought high) | Impermanent loss |
| **Implied vol** | Breakeven vol where rebalancing profit = rebalancing loss | Breakeven vol where fee income = IL |
| **Gamma** | d²V/dS² from LDF curvature | d²V/dS² from tick range concentration |
| **Observable** | FloodPlain order fills, BunniToken share price changes | Swap events, position value changes |

---

## 5. Revised Data Strategy

### For Bunni V2 (Arbitrum)
Instead of swap events (which don't exist), analyze:

1. **BunniToken share price over time**: The ERC4626 share price captures all rebalancing P&L
2. **Rebalance order executions**: FloodPlain fill events show when and at what price rebalancing happened
3. **Deposit/withdrawal token ratios**: The ratio of (amount0_out/amount0_in) at withdrawal vs deposit reflects the cumulative rebalancing impact

### For Algebra (Arbitrum)
Standard swap-based analysis as originally planned:
1. Swap events for price + fee reconstruction
2. Position Mint/Burn for lifecycle tracking

### For Cross-Architecture Comparison
Compare **BunniToken share price returns** (Bunni V2) against **position value returns** (Algebra) on the same underlying pair, testing whether both exhibit short-straddle-like concavity in their return-vs-price relationship.

---

## 6. Implications for Protocol Design

This finding directly informs the universal pool architecture:

1. **Borrowing vs creating pools**: Panoptic's approach (borrow from active pool) gives the swap-channel option payoff "for free." Bunni V2's approach (create new pool + rebalance) gives the same payoff but requires active rebalancing infrastructure.

2. **For macro hedging**: If the instrument needs to track an external price (like COP/USD via oracle), Bunni V2's rebalancing channel is actually MORE natural — the option payoff tracks an external reference price rather than requiring in-pool swap volume for a potentially illiquid pair.

3. **LDF as instrument design**: The LDF shape directly determines the option type without needing swap volume. A GeometricDistribution LDF with cCOP/cUSD could create a short straddle on the COP/USD exchange rate, settled through rebalancing at oracle prices.

4. **The bridge to Algebra**: For pairs with organic volume (ETH/USDC), Algebra's adaptive fee channel is more capital-efficient (no rebalancing slippage). For pairs without volume (EM stablecoins), Bunni V2's rebalancing channel is the only viable path.
