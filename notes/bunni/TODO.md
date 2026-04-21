# Bunni V2 Option Payoff Mechanism — Test Map

## Architecture: How Bunni V2 Writes Options

The option lifecycle is split across THREE execution steps, each in a different test file:

```
1. DEPOSIT (BunniHub)     → LP enters position = writes the option
2. LDF SHIFT + SWAP       → price moves, triggers rebalance = option is exercised
   (BunniHook)              FloodPlain order created
3. REBALANCE FULFILLED    → tokens exchanged at TWAP price = payoff realized
   (FloodPlain)
4. WITHDRAW (BunniHub)    → LP exits = closes the option, collects net P&L
```

No single test traces the full deposit → rebalance → withdraw → measure P&L end-to-end.

---

## Test File Map

### `BunniHub.t.sol` — LP Entry/Exit (Option Writing & Closing)

| Test | Line | What to see |
|---|---|---|
| `test_deposit` | L32 | Fuzz: deposit amounts → shares minted. How the option is opened. Tracks `amount0`, `amount1`, `shares` — the LP's capital commitment. |
| `test_withdraw` | L97 | Fuzz: deposit → withdraw lifecycle. Tracks token amounts returned vs deposited. **The P&L is here**: `wd_amount0/1` vs `dep_amount0/1`. But no swaps/rebalancing between deposit and withdraw, so P&L is only from idle balance changes. |
| `test_queueWithdraw_happyPath` | L211 | Queued withdrawal flow with time delay. Shows the withdrawal lock mechanism that prevents front-running rebalances. |
| `test_idleBalance_ldfShiftUpdatesIdleBalance` | L792 | **Key**: When LDF shifts, idle balance changes. This is the mechanism that creates excess tokens that need rebalancing — the trigger for the option payoff. |
| `test_withdraw_revertWhenRebalanceOrderIsActive` | L161 | Withdrawal blocked during active rebalance. LP cannot exit while the option is being exercised. |

### `BunniHook.t.sol` — Swap + Rebalance (Option Exercise)

| Test | Line | What to see |
|---|---|---|
| `test_rebalance_basicOrderCreationAndFulfillment` | L1197 | **THE option exercise test.** Full cycle: deploy pool with GeometricDistribution LDF → shift LDF (simulates price move) → swap triggers rebalance detection → FloodPlain order etched → order fulfilled → pool rebalanced. Verifies: order price matches TWAP with slippage bound, offer/consideration tokens correct, pool no longer needs rebalancing after. The rebalancing P&L = option payoff. |
| `test_rebalance_basicOrderCreationAndFulfillment_carpetedLDF` | L1361 | Same lifecycle with CarpetedGeometricDistribution. Shows how carpet liquidity (floor) changes the rebalancing pattern — equivalent to a different option structure (covered strangle vs pure straddle). |
| `test_rebalance_arb` | L1646 | Rebalance arbitrage test. Shows what happens when someone tries to deposit (JIT liquidity) during a rebalance fulfillment — reverts with reentrancy guard. Proves the rebalancing is atomic. |
| `test_swap_zeroForOne_noTickCrossing` | L25 | Small swap within one tick. The BunniSwapMath computes amounts using LDF density. Shows how the LDF shape determines the effective liquidity at each price point — this IS the option's gamma. |
| `test_swap_zeroForOne_oneTickCrossing` | L93 | Swap crosses a tick boundary. The LDF's `computeSwap` function determines liquidity at the new tick. **The tick crossing is the discrete delta-hedge**: the pool's token composition changes according to the LDF density at the new price. |
| `test_swap_zeroForOne_twoTickCrossing` | L131 | Larger swap crossing two ticks. Shows how the LDF-shaped liquidity creates non-uniform price impact — concentrated near the LDF peak (high gamma), thin at the tails (low gamma). |
| `test_fuzz_swapNoArb_double` | L725 | Two sequential swaps. Tests that the LDF-shaped pricing is consistent: swap A→B then B→A returns approximately the same amount (no arbitrage). This is the fundamental no-arb condition that makes the LDF a valid pricing function. |
| `test_collectProtocolFees` | L389 | Fee collection after swaps. Shows how fees are split between LP pool and protocol — the premium income channel for pools that DO have swap volume. |
| `test_idleBalance_rebalanceUpdatesIdleBalance` | L1959 | After rebalance, idle balance resets. Confirms the rebalancing consumed the excess tokens. |
| `test_curatorFees_happyPath` | L2150 | Curator fee deduction from swap fees. Relevant for fee income reconstruction in our analysis. |

### `RebalanceWithBunniLiqTest.t.sol` — Multi-Pool Rebalance (Complex Option)

| Test | Line | What to see |
|---|---|---|
| `test_rebalance_withBunniLiq` | L56 | **Most complex lifecycle.** Three pools (A: token0/token1, B: token0/token2, C: token1/token2) share the same LDF. Rebalancer fulfills pool A's order by routing through pools B and C. Shows how Bunni V2 rebalancing creates **cross-pool option exposure** — the payoff on pool A depends on liquidity in pools B and C. Analogous to a multi-leg option strategy where the hedge route matters. |

### `RebalanceAttackTest.t.sol` — Adversarial Option Exercise

| Test | Line | What to see |
|---|---|---|
| `test_rebalance_arb_setup` | L213 | Setup for attack scenario — creates a pool with known LDF params. |
| `test_rebalance_arb_rebalance` | L245 | Attack: adversary tries to extract value from the rebalance order. Shows the TWAP slippage protection — the option exercise price is bounded. This is the protocol's protection against adverse selection on the rebalancing trades. |

### `test/ldf/GeometricDistribution.t.sol` — Option Structure (Payoff Shape)

| Test | File | What to see |
|---|---|---|
| LDF query tests | `test/ldf/GeometricDistribution.t.sol` | Tests the `query()` function that returns liquidity density at each tick. The density IS the option's gamma profile. Plot `liquidityDensityX96` vs `tick` → this is the option's payoff curvature. |
| LDF shift tests | same | Tests LDF shifting with TWAP. When the LDF center moves, the strike moves — this is the rolling straddle mechanism. |
| `isValidParams` | same | Validates LDF parameter bounds. The alpha parameter controls the bell curve width = option moneyness range. |

Other LDF test files follow the same pattern for their respective distributions:
- `DoubleGeometricDistribution.t.sol` → short strangle structure
- `CarpetedGeometricDistribution.t.sol` → covered strangle structure
- `BuyTheDipGeometricDistribution.t.sol` → short put structure
- `UniformDistribution.t.sol` → full-range LP (wide straddle)

---

## What's MISSING — No End-to-End Payoff Test

No existing test does:
```
1. Deploy pool with GeometricDistribution LDF
2. LP deposits X wstETH + Y WETH → gets shares
3. Price moves (multiple swaps over time)
4. Multiple rebalances fire (FloodPlain orders fulfilled)
5. LP withdraws shares → gets X' wstETH + Y' WETH
6. Compute: net P&L = V(X',Y') - V(X,Y)
7. Assert: P&L ≈ short straddle payoff at realized price path
```

**This is the test WE need to write** to prove the option payoff mechanism empirically.

---

## Key Source Files for Understanding the Mechanism

| File | What it does |
|---|---|
| `src/lib/RebalanceLogic.sol` | Computes rebalance params: which token is excess, how much to trade, at what price. The `_computeRebalanceParams` function is the option exercise calculation. |
| `src/lib/BunniSwapMath.sol` | Computes swap amounts using LDF-shaped liquidity. The `computeSwap` function uses `inverseCumulativeAmount` to find the tick where remaining liquidity exists — this is the LDF determining the effective strike. |
| `src/lib/BunniHookLogic.sol:beforeSwap` | The hook that intercepts every swap: updates TWAP oracle, queries LDF, detects if rebalance is needed, computes dynamic fees, applies surge fees. This is the option pricing engine. |
| `src/interfaces/ILiquidityDensityFunction.sol` | The LDF interface. `query()` returns density at a tick = gamma at that price. `computeSwap()` returns the swap result shaped by the LDF = effective payoff computation. |
| `src/ldf/GeometricDistribution.sol` + `LibGeometricDistribution.sol` | The specific bell-curve LDF. The alpha parameter controls width. ShiftMode controls whether the center tracks TWAP (rolling strike). |
| `src/base/SharedStructs.sol:DecodedHookParams` | All the knobs: feeMin/Max, surgeFeeHalfLife, rebalanceThreshold, rebalanceMaxSlippage. These are the option pricing parameters. |
| `test/mocks/MockLDF.sol` | Test mock that allows manual LDF shifting via `setMinTick()`. This is how tests simulate price movement. |
| `test/BaseTest.sol` | Test harness with `_deployPoolAndInitLiquidity`, `_makeDeposit`, `_swap` helpers. |
