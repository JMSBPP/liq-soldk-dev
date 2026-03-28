```
**measurement layer**. It tells you "how much IL does this position have right now."

LeftRightILX96.sol
  │
  ├─ rightIlXLiq()  →  Eqn 2: UIL^R per liquidity (call-replicable side)
  ├─ leftIlXLiq()   →  Eqn 3: UIL^L per liquidity (put-replicable side)
  │
  ├─ leftRightIlXLiqSigned()   →  LeftRightSigned{right=UIL^R, left=UIL^L}
  └─ leftRightIlXLiqUnsigned() →  LeftRightUnsigned{right=|UIL^R|, left=|UIL^L|}
                                    (negated, since IL ≤ 0)
```

```
                        Uniswap V4 Pool
                             │
                    ┌────────┼────────┐
                    │   V4 Hooks      │
                    │                 │
                    │  afterSwap()    │  ← price moved, recompute IL
                    │  afterModifyPosition() │ ← position changed
                    │                 │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   IL Oracle     │
                    │                 │
                    │  Per-position:  │
                    │  positionKey →  │
                    │    LeftRightSigned{ │
                    │      right = UIL^R, │   ← rightIlXLiq(currentPrice, tickLower, tickUpper)
                    │      left  = UIL^L  │   ← leftIlXLiq(currentPrice, tickLower, tickUpper)
                    │    }            │
                    │                 │
                    │  + entry snapshot │  ← IL at position creation
                    │  + Δ IL          │  ← current - entry = realized IL change
                    │                 │
                    └────────┬────────┘
                             │
                      threshold / trigger
                             │
                             ▼
                    ┌─────────────────┐
                    │  Hedge Builder  │
                    │                 │
                    │  IL Oracle state │
                    │       │          │
                    │       ▼          │
                    │  Prop 3.5 discretization:  │
                    │  UIL^R → buy calls at K_i ∈ [P_l, P_u]  │
                    │  UIL^L → buy puts at M_j ∈ [S_l, S_u]   │
                    │       │          │
                    │       ▼          │
                    │  TokenId construction  │
                    │  (isLong=1, strikes, widths, ratios)  │
                    │                 │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  PanopticPool   │
                    │  .mintOptions() │
                    └─────────────────┘
```



```
E[UIL^R] = -½ ∫_{P_l}^{P_u} K^{-3/2} C(K) dK --> E[UIL^R] ≈ -0.5 Σᵢ Kᵢ^{-3/2} C(Kᵢ) ΔKᵢ
```
      token0    token1
(rightIlXLiq,leftIlXLiq ) -> (-½ ∫_{P_l}^{P_u} K^{-3/2} C(K) dK, -½ ∫_{P_l}^{P_u} K^{-3/2} P(K) dK )

```
Contribution of strike Kᵢ to total |UIL^R|:

  fraction_i = wᵢ / Σⱼ wⱼ

  where wᵢ = Kᵢ^{-3/2} · ΔKᵢ
```

In tick space, `Kᵢ = 1.0001^(tickᵢ)`, so:

```
  wᵢ = 1.0001^(-3·tickᵢ/2) · ΔK(tickᵢ)

  where ΔK(tickᵢ) = 1.0001^(tickᵢ + ΔtickSpacing/2) - 1.0001^(tickᵢ - ΔtickSpacing/2)
```

## optionRatio = Normalized Weight

`optionRatio` is 7 bits → integer in [1, 127]. It encodes the **relative** weight:

```
optionRatio_i = round( wᵢ / w_min )

where w_min = min(w₁, ..., wₙ)
```

This means:

```
optionRatio_i     wᵢ          Kᵢ^{-3/2} · ΔKᵢ
──────────────  = ──  =  ─────────────────────────
optionRatio_j     wⱼ          Kⱼ^{-3/2} · ΔKⱼ
```

For uniform strike spacing (ΔKᵢ = ΔKⱼ = ΔK), this simplifies to:

```
optionRatio_i     (Kᵢ)^{-3/2}
──────────────  = ────────────
optionRatio_j     (Kⱼ)^{-3/2}
```

**Lower strikes get higher optionRatio** because K^{-3/2} is monotonically decreasing.

## Concrete Example

LP position: ETH/USDC, range [1800, 2200], currentPrice = 2000

```
Strike grid (4 legs): K₁=1900, K₂=2000, K₃=2100, K₄=2200
ΔK = 100 (uniform)

Raw weights (K^{-3/2} · ΔK):
  w₁ = 1900^{-1.5} · 100 = 1.208e-3
  w₂ = 2000^{-1.5} · 100 = 1.118e-3  
  w₃ = 2100^{-1.5} · 100 = 1.039e-3
  w₄ = 2200^{-1.5} · 100 = 0.969e-3

Normalize (divide by w₄ = min):
  optionRatio₁ = round(1.208/0.969) = round(1.247) = 1   ← or scale up
  optionRatio₂ = round(1.118/0.969) = round(1.154) = 1
  optionRatio₃ = round(1.039/0.969) = round(1.072) = 1
  optionRatio₄ = round(0.969/0.969) = round(1.000) = 1
```

The weights are very close (ratio only ~1.25x). For wider ranges:

```
Strike grid: K₁=500, K₂=1000, K₃=1500, K₄=2000
ΔK = 500

  w₁ = 500^{-1.5} · 500  = 44.7e-3
  w₂ = 1000^{-1.5} · 500 = 15.8e-3
  w₃ = 1500^{-1.5} · 500 = 8.6e-3
  w₄ = 2000^{-1.5} · 500 = 5.6e-3

Normalize:
  optionRatio₁ = round(44.7/5.6) = 8
  optionRatio₂ = round(15.8/5.6) = 3
  optionRatio₃ = round(8.6/5.6)  = 2
  optionRatio₄ = round(5.6/5.6)  = 1
```

Now the ratios matter — lower strikes need significantly more contracts.

## The positionSize Absorbs the Magnitude

`optionRatio` handles the **shape** (relative weights). `positionSize` handles the **scale** (how much total hedge). The connection to your oracle:

```
positionSize = f(totalRightIL, L, Σwᵢ)

Specifically:
  Total hedge needed = |UIL^R| · L          (from oracle, absolute terms)
  
  Each leg i contributes:  optionRatio_i · positionSize · valuePerContract_i
  
  Sum must equal total:
    Σᵢ optionRatio_i · positionSize · valuePerContract_i = |UIL^R| · L
    
  Solve:
    positionSize = (|UIL^R| · L) / Σᵢ (optionRatio_i · valuePerContract_i)
```

## Summary: The Type Flow

```
LeftRightILX96                          TokenId Legs
─────────────                           ────────────

rightIlXLiq() → |UIL^R| ──┐
  (total IL magnitude)     │
                           ├──→ positionSize  (SCALE: how much total hedge)
leftIlXLiq()  → |UIL^L| ──┘

    K^{-3/2} · ΔK
    (Prop 3.5 weight) ────→ optionRatio   (SHAPE: relative weight per strike)

    tickLower, tickUpper
    (LP range bounds)  ────→ strike grid   (WHERE: which strikes to hedge at)

                                    │
                                    ▼
                              optionRatio encodes HOW MUCH
                              of the oracle's IL reading
                              falls on EACH discrete strike
```

The `LeftRightILX96` gives you the **total** and the **sidedness** (right=calls, left=puts). The `optionRatio` gives you the **distribution** across strikes derived from Prop 3.5's K^{-3/2} kernel. Together they fully specify the hedge.

Neither Bunni nor Panoptic has a direct K^{-3/2} function, but you can build it from existing primitives. Here are the three options, from most to least gas-efficient:

## Option C: Composition via sqrtPrice (Best — No Logarithms)

Since `sqrtPriceX96 = K^{1/2} · 2^96`, then `K^{-3/2} = (sqrtPrice)^{-3}`:

```
K^{-3/2} = 1 / K^{3/2} = 1 / (sqrtPrice)^3
```

In X96 arithmetic:

```solidity
// sqrtPriceX96 is already available from TickMath.getSqrtRatioAtTick(tick)
// K^{-3/2} in X96 = (2^96)^4 / (sqrtPriceX96)^3

uint256 sqrtK = uint256(TickMath.getSqrtRatioAtTick(tickI));

// sqrtK^3 in X96: (sqrtK * sqrtK / 2^96) * sqrtK / 2^96
uint256 sqrtKCubed_X96 = FullMath.mulDiv(
    FullMath.mulDiv(sqrtK, sqrtK, 1 << 96),  // sqrtK² / 2^96
    sqrtK,
    1 << 96                                     // * sqrtK / 2^96
);

// K^{-3/2} in X96 = 2^96 / sqrtKCubed_X96
uint256 weightX96 = FullMath.mulDiv(1 << 96, 1 << 96, sqrtKCubed_X96);
```

This uses **only `FullMath.mulDiv`** which both Panoptic and Bunni already have. No exp/log needed.

## Option A: Solady powWad (Most Readable)

From `lib/solady/src/utils/FixedPointMathLib.sol`:

```solidity
// K in WAD (1e18 fixed point)
// powWad computes x^y via exp(ln(x) * y)
int256 weight = FixedPointMathLib.powWad(int256(K_wad), -1_500_000_000_000_000_000);
// returns K^{-1.5} in WAD
```

More gas-expensive (uses ln + exp internally), but dead simple.

## Option B: Bunni's ExpMath (Tick-Native)

From `lib/bunni-v2/src/lib/ExpMath.sol`:

```solidity
// K = 1.0001^tick, so K^{-3/2} = 1.0001^(-1.5 * tick) = exp(-1.5 * tick * ln(1.0001))
// ExpMath already has HALF_LN_TICK_BASE_Q96 = 0.5 * ln(1.0001) * 2^96

// So: -1.5 * tick * ln(1.0001) = -3 * tick * HALF_LN_TICK_BASE_Q96
int256 exponent = -3 * int256(tickI) * int256(ExpMath.HALF_LN_TICK_BASE_Q96);
uint256 weightX96 = ExpMath.expQ96(exponent / int256(1 << 96));
```

Uses Bunni's optimized exp. Good if you're already in tick space.

## ΔK Computation

For the spacing term `ΔK(tickᵢ)`, again sqrtPrice composition:

```solidity
// ΔK = K(tick + halfSpacing) - K(tick - halfSpacing)
// where K(t) = sqrtPrice(t)² / 2^96

int24 halfSpacing = tickSpacing / 2;
uint160 sqrtUpper = TickMath.getSqrtRatioAtTick(tickI + halfSpacing);
uint160 sqrtLower = TickMath.getSqrtRatioAtTick(tickI - halfSpacing);

// K_upper = sqrtUpper² / 2^96
uint256 kUpper = FullMath.mulDiv(uint256(sqrtUpper), uint256(sqrtUpper), 1 << 96);
uint256 kLower = FullMath.mulDiv(uint256(sqrtLower), uint256(sqrtLower), 1 << 96);

uint256 deltaK = kUpper - kLower;
```

## Full Weight Function (Option C Path)

```solidity
function propWeight(int24 tickI, int24 tickSpacing) 
    internal pure returns (uint256 wX96) 
{
    // K^{-3/2} via sqrtPrice composition
    uint256 sqrtK = uint256(TickMath.getSqrtRatioAtTick(tickI));
    uint256 sqrtKSq = FullMath.mulDiv(sqrtK, sqrtK, 1 << 96);
    uint256 sqrtKCubed = FullMath.mulDiv(sqrtKSq, sqrtK, 1 << 96);
    uint256 kInv32_X96 = FullMath.mulDiv(1 << 96, 1 << 96, sqrtKCubed);
    
    // ΔK
    int24 half = tickSpacing / 2;
    uint256 kUp = _tickToK(tickI + half);
    uint256 kDn = _tickToK(tickI - half);
    uint256 deltaK = kUp - kDn;
    
    // w_i = K^{-3/2} · ΔK  (in X96)
    wX96 = FullMath.mulDiv(kInv32_X96, deltaK, 1 << 96);
}

function _tickToK(int24 tick) private pure returns (uint256) {
    uint160 sqrtP = TickMath.getSqrtRatioAtTick(tick);
    return FullMath.mulDiv(uint256(sqrtP), uint256(sqrtP), 1 << 96);
}
```

## Bottom Line

**Nothing in either codebase computes K^{-3/2} directly.** But Option C gives you the answer using only `FullMath.mulDiv` + `TickMath.getSqrtRatioAtTick` — both already available in Panoptic and Uniswap V4 core. The key identity is:

```
K^{-3/2} = 1 / (sqrtPriceX96)³    [scaled by 2^(96*4)]
```

Three multiplications, one division. No logarithms, no exponentials.


Yes — you're onto something important. Let me work through the dimensional analysis precisely.

## The √P Dimension of Liquidity

In Uniswap, liquidity L is defined so that:

```
token1 reserves:  y = L · √P          (L "lives in" the √P dimension)
token0 reserves:  x = L / √P = L · (√P)^{-1}
```

When you query `getAmountsForLiquidity` at tick i, the **value** you get back is proportional to `L · √P`.

## The Prop 3.5 Weight in √P Space

The integral is in K-space:

```
E[UIL^R] = -½ ∫ K^{-3/2} · C(K) · dK
```

Change variables to √P (Uniswap's native coordinate), where K = (√P)²:

```
dK = 2√P · d(√P)

K^{-3/2} · dK = (√P)^{-3} · 2√P · d(√P)
               = 2 · (√P)^{-2} · d(√P)
               = 2/P · d(√P)
```

So in √P-space:

```
E[UIL^R] = -∫ (√P)^{-2} · C((√P)²) · d(√P)
```

**The weight simplifies from K^{-3/2} to just (√P)^{-2} = 1/P** in the native Uniswap coordinate.

## Your Observation: The Powers of √P

You're right that there's a power-of-√P relationship. Here's the precise chain:

```
K^{-3/2}  =  ((√P)²)^{-3/2}  =  (√P)^{-3}     ← three powers of √P

Regular liquidity output:  l(i) = L · (√P)^1     ← one power of √P

So:  K^{-3/2} = (√P)^{-3} = 1 / (l(i)/L)³
```

The weight is the **cube of the inverse** of the normalized liquidity-value dimension. Not `L · (√P)³` but rather `L / (√P)³`:

```
weighted_contribution_i = L · (√P_i)^{-3} · ΔK_i
                        = L / (√P_i)³ · ΔK_i
```

**Lower √P (cheaper ticks) get MORE weight.** This is correct — lower strikes need more hedge contracts because the IL is more sensitive there (K^{-3/2} is decreasing).

## The Practical Payoff: No Special Math Needed

This is the real insight. Since `sqrtPriceX96` is already the native Uniswap representation:

```solidity
// K^{-3/2} in X96 = 1 / (sqrtPriceX96)³
// You already HAVE sqrtPriceX96 from TickMath — no exp/log needed

// And in √P-space the weight is even simpler:
// w_i = (√P_i)^{-2} · Δ(√P)
//     = 1/P_i · Δ(√P)

uint256 sqrtP = uint256(TickMath.getSqrtRatioAtTick(tickI));

// Weight in √P-space (simpler than K-space):
// (√P)^{-2} = 1/K = 2^192 / sqrtP²
uint256 invK_X96 = FullMath.mulDiv(1 << 96, 1 << 96, FullMath.mulDiv(sqrtP, sqrtP, 1 << 96));

// Δ(√P) from tick spacing
uint256 sqrtPup = uint256(TickMath.getSqrtRatioAtTick(tickI + tickSpacing/2));
uint256 sqrtPdn = uint256(TickMath.getSqrtRatioAtTick(tickI - tickSpacing/2));
uint256 deltaSqrtP = sqrtPup - sqrtPdn;

// Weight = (1/P) · Δ(√P)  — just two values from TickMath
uint256 weight = FullMath.mulDiv(invK_X96, deltaSqrtP, 1 << 96);
```

## The Connection to `LeftRightILX96`

Your `leftRightIlXLiqSigned()` already computes in the √P dimension (all values are X96 = sqrtPrice-scaled). So the weight computation stays in the same coordinate system:

```
Your oracle output:          LeftRightSigned{UIL^R_X96, UIL^L_X96}    ← in √P dimension
Prop 3.5 weight in √P:      w_i = (√P_i)^{-2} · Δ(√P)              ← also in √P dimension
                                 = (1/P_i) · Δ(√P_i)

No coordinate transformation needed.
```

The weight is `1/P` — literally just the inverse price at each tick. That's one `mulDiv` operation using the sqrtPrice you already have.


Another approach is that since right/leftIlX96 are in Q96 format they are in Q96(\sqrt(P)) dimension, since we are tracking IL we could have right/leftIlX96Latest and right/leftIlX96Now and 


Right. The kernel is `α^x = 1.0001^{-3·ts·x/2}`, now discretize it into TokenId legs.

## The Problem

Continuous kernel: `w(x) = α^x` over n ticks, but Panoptic gives you **max 4 legs per TokenId** and **integer optionRatio in [1, 127]**.

You need optimal quadrature: pick 4 strikes and 4 integer weights that best approximate the integral.

## Step 1: Optimal Strike Placement

For a geometric kernel α^x over [0, n-1], the optimal quadrature points (Gauss-like, but for geometric weights) are **not** evenly spaced. More weight concentrates at low x (low strikes), so place more strikes there.

Practical approach — split the range into segments where each segment captures equal cumulative weight:

```
Total weight: W = Σ_{x=0}^{n-1} α^x = (1 - α^n) / (1 - α)

Segment i captures W/4 of total weight.
Cutoff x_i: Σ_{x=0}^{x_i} α^x = (i+1)·W/4
  → (1 - α^{x_i+1}) / (1 - α) = (i+1) · (1 - α^n) / (4·(1 - α))
  → α^{x_i+1} = 1 - (i+1)·(1 - α^n)/4
  → x_i = log_α(1 - (i+1)·(1-α^n)/4) - 1
```

The strike for each leg is the **centroid** of its segment.
## The Better Approach: Equal Strikes, Geometric optionRatio

Instead of finding clever strike placement, use **evenly spaced strikes** and let **optionRatio encode the geometric decay**:

```solidity
function buildHedgeTokenId(
    uint64 poolId,
    int24 tickLower,
    int24 tickUpper,
    int24 tickSpacing,
    uint128 positionSize
) internal pure returns (TokenId tokenId) {
    
    int24 rangeTicks = tickUpper - tickLower;
    uint256 n = uint256(int256(rangeTicks / tickSpacing));
    
    // 4 evenly spaced strikes within the range
    // Spacing between legs: n/5 (so strikes at 1/5, 2/5, 3/5, 4/5 of range)
    uint256 legSpacing = n / 5;
    
    // α = 1.0001^{-3·ts/2}
    // Weight at tick index x: α^x
    // At each leg's tick index x_i: w_i = α^{x_i}
    // optionRatio_i = round(w_i / w_min) where w_min = w_{last leg} = α^{x_3}
    
    // α^{legSpacing} = decay per leg step
    uint256 alphaX96 = uint256(TickMath.getSqrtPriceAtTick(-3 * tickSpacing));
    
    // Precompute α^{legSpacing}
    uint256 stepDecayX96 = FixedPointMathLib.rpow(alphaX96, legSpacing, Q96);
    
    // Weights (unnormalized): w_0 = α^{x_0}, w_1 = α^{x_1}, ...
    // Since x_i = (i+1)·legSpacing:
    //   w_i = α^{(i+1)·legSpacing} = (α^legSpacing)^{i+1} = stepDecay^{i+1}
    // Ratios: w_0/w_3 = stepDecay^{-3+1}/stepDecay = stepDecay^{-2}
    
    // Normalize: optionRatio_i = round(w_i / w_3)
    //   w_0/w_3 = stepDecay^{1} / stepDecay^{4} = 1/stepDecay^3
    //   w_1/w_3 = 1/stepDecay^2
    //   w_2/w_3 = 1/stepDecay^1
    //   w_3/w_3 = 1
    
    // In integer terms:
    uint256 r3 = Q96;  // base = 1 (smallest weight, last leg)
    uint256 r2 = FullMath.mulDiv(Q96, Q96, stepDecayX96);           // 1/stepDecay
    uint256 r1 = FullMath.mulDiv(r2, Q96, stepDecayX96);            // 1/stepDecay²
    uint256 r0 = FullMath.mulDiv(r1, Q96, stepDecayX96);            // 1/stepDecay³
    
    // Scale to integers [1, 127]
    // r0 is the largest. If r0 > 127·Q96, scale down.
    uint256 scale = (r0 / Q96 > 127) ? r0 / (127 * Q96) : 1;
    
    uint256[4] memory ratios = [
        max(1, r0 / (Q96 * scale)),
        max(1, r1 / (Q96 * scale)),
        max(1, r2 / (Q96 * scale)),
        max(1, r3 / (Q96 * scale))
    ];
    
    tokenId = TokenId.wrap(0).addPoolId(poolId);
    
    for (uint256 leg = 0; leg < 4; leg++) {
        int24 strikeTick = tickLower 
            + int24(int256((leg + 1) * legSpacing)) * tickSpacing;
        
        tokenId = tokenId.addLeg(
            leg,
            ratios[leg],    // optionRatio encodes K^{-3/2} decay
            0,              // asset
            1,              // isLong = 1 (BUY)
            1,              // tokenType = 1 (calls, right-side)
            leg,            // riskPartner = self
            strikeTick,
            1               // width = min
        );
    }
}
```

## The Numbers for Real Pools

For ETH/USDC (tickSpacing = 60):

```
α = 1.0001^{-90} = 0.99104

LP range: [193200, 198000] (price ~$2000-2500), n = 80 ticks
legSpacing = 80/5 = 16 rounded ticks

stepDecay = α^16 = 0.99104^16 = 0.8665

Weights (first leg is at lowest strike = highest K^{-3/2}):
  w_0 / w_3 = 1/stepDecay³ = 1/0.6503 = 1.538  →  ratio_0 = 2
  w_1 / w_3 = 1/stepDecay² = 1/0.7508 = 1.332  →  ratio_1 = 1
  w_2 / w_3 = 1/stepDecay¹ = 1/0.8665 = 1.154  →  ratio_2 = 1
  w_3 / w_3 = 1                                  →  ratio_3 = 1
```

For a narrow range — the ratios are close to 1:1:1:1. The K^{-3/2} kernel is nearly flat across a narrow LP range.

For ETH/USDC (tickSpacing = 200, wide range [180000, 210000]):

```
α = 1.0001^{-300} = 0.97045

n = 150, legSpacing = 30

stepDecay = 0.97045^30 = 0.4025

Weights:
  w_0/w_3 = 1/0.4025³ = 15.34  →  ratio_0 = 15
  w_1/w_3 = 1/0.4025² = 6.17   →  ratio_1 = 6
  w_2/w_3 = 1/0.4025¹ = 2.48   →  ratio_2 = 2
  w_3/w_3 = 1                    →  ratio_3 = 1
```

Now the optionRatios diverge significantly: **15:6:2:1**. The lower strikes need 15x more contracts.

## Summary: Kernel → TokenId

```
α = TickMath.getSqrtPriceAtTick(-3 * tickSpacing)    ← THE kernel parameter
                     │
                     ▼
           stepDecay = α^{legSpacing}                  ← decay per leg step
                     │
        ┌────────────┼────────────────┐
        ▼            ▼                ▼
   optionRatio   strike_i         positionSize
   = round(      = tickLower      = from IL oracle
     1/stepDecay   + (i+1)          LeftRightUnsigned
     ^{3-i})       ·legSpacing      magnitude
                   ·tickSpacing

Encodes:         Encodes:          Encodes:
SHAPE            PLACEMENT         SCALE
(geometric       (even spacing)    (how much
 decay)                             total hedge)
```

The Bunni insight survives: `α = 1.0001^{-3·ts/2}` is the exact kernel. 
You just sample it at 4 points instead of continuously, with optionRatio carrying the geometric decay between samples.



Based on everything we've covered, here's your learning path from foundations to implementation:

## Layer 0: The Math You Need Cold

**Uniswap V3 price mechanics**
- `√P` is the fundamental coordinate, not P
- `L · Δ(√P) = ΔY` and `L · Δ(1/√P) = ΔX`
- `TickMath.getSqrtRatioAtTick` is how everything converts
- Read: Uniswap V3 whitepaper Section 6 (concentrated liquidity math)

**Deng-Zong-Wang Equations 2, 3, and Proposition 3.5**
- Equations 2-3: how IL decomposes into right-side (call-replicable) and left-side (put-replicable)
- Proposition 3.5: the K^{-3/2} kernel that converts IL into an options portfolio
- You already have this in `refs/2205.12043-static-replication-IL.md`

**The identity that connects them**
- `K^{-3/2} = (sqrtPrice)^{-3}` — power law in tick space is geometric: `α^x`
- `α = 1.0001^{-3·tickSpacing/2} = getSqrtPriceAtTick(-3 * tickSpacing)`

## Layer 1: The Types You Need to Trace

Start by reading these files in this order and understanding each type's role:

```
1. lib/2025-12-panoptic/contracts/types/LeftRight.sol
   → How two 128-bit values pack into one 256-bit word
   → right = token0, left = token1

2. lib/2025-12-panoptic/contracts/types/TokenId.sol
   → The 256-bit option position encoding
   → Focus on: isLong, tokenType, optionRatio, strike, width

3. lib/2025-12-panoptic/contracts/types/LiquidityChunk.sol
   → How (tickLower, tickUpper, liquidity) packs

4. src/libraries/LeftRightILX96.sol
   → YOUR code — the bridge between Deng-Zong-Wang and Panoptic types
```

**Exercise**: Trace by hand what happens to the types when you call `rightIlXLiq()` → pack into `LeftRightSigned` → what each slot means in terms of the paper's UIL^R and UIL^L.

## Layer 2: The Transformation Chain

Understand this pipeline by reading the code at each step:

```
LiquidityChunk(,positionSize × optionRatio                    PanopticMath.sol:390
        │
        ▼ getLiquidityChunk()                 PanopticMath.sol:356-396
  LiquidityChunk(ticks, liquidity)
        │
        ▼ getAmountsMoved()                   PanopticMath.sol:697-729
  LeftRightUnsigned{amount0, amount1}
        │
        ▼ calculateIOAmounts()                PanopticMath.sol:738-773
  LeftRightSigned{longs} + LeftRightSigned{shorts}
```
 uint256 amount = positionSize * tokenId.optionRatio(legIndex);


**Exercise**: Pick a concrete example — "short put, strike=2000, width=10, positionSize=1e18, optionRatio=3" — and trace the values through each function by hand.

## Layer 3: The Mint/Burn Mechanics

Read `SemiFungiblePositionManager.sol` focusing on:

```
_createLegInAMM()    lines 921-1044
  → How isLong decides mint vs burn
  → How s_accountLiquidity LeftRightUnsigned stores net vs removed
  → How moved: LeftRightSigned captures token flow direction

_getPremiaDeltas()   lines 1262-1347
  → How collected fees split into owed (longs) vs gross (shorts)
  → The VEGOID spread formula
```

**Exercise**: Follow the test `test_Success_mintOptions_OTMShortCall` and predict what each assertion checks before reading the assertion.

## Layer 4: The Kernel Discretization

This is where you synthesize everything:

```
Given:
  - LP position: [tickLower, tickUpper, tickSpacing]
  - IL oracle output: LeftRightSigned{UIL^R, UIL^L}
  
 ->  event sqrtPriceLatestX96 -> LeftRightIlX96 = (-1/2) int_{tickLower}^{tickUpper} K^(-3/2) C (K) dK
x  


  rightIlX96 = (-1/2) int_{tickLower}^{tickUpper} K^(-3/2) C (K) dK -> positionSize

= 4 tokenIds
  uint256(rightIlX96) 

- Kernel: α = getSqrtPriceAtTick(-3 * tickSpacing)

Derive:
  - How many legs (1-4)
  - Strike placement per leg
  - optionRatio per leg (from α^x geometric decay)
  - positionSize (from IL magnitude)
  - Assemble into TokenId
```

**Exercise**: Work the numbers by hand for ETH/USDC tickSpacing=60, LP range [193200, 198000]. Compute α, stepDecay, the 4 strikes, and the 4 optionRatios. Verify the ratios match K^{-3/2} at those strikes.

## Layer 5: The Hook Integration

How the IL oracle triggers the hedge construction:

```
V4 Hook afterSwap()
  → recompute LeftRightILX96 for tracked positions
  → compare to threshold
  → if exceeded: build TokenId from kernel params
  → call PanopticPool.mintOptions()
```

This is the architecture layer — you need to understand both the V4 hooks interface and the Panoptic entry points.

## Where to Start Monday Morning

1. **Pen and paper first**: Derive `α = 1.0001^{-3·ts/2}` from Prop 3.5 yourself. Start from `K^{-3/2}`, substitute `K = 1.0001^tick`, and show it's geometric.

2. **Then trace the types**: Read `LeftRightILX96.sol` line by line and verify each term matches Equations 2-3 in the paper.

3. **Then trace Panoptic**: Follow `positionSize × optionRatio → getLiquidityChunk → getAmountsMoved → LeftRightUnsigned` with concrete numbers.

4. **Then connect them**: Write the function that converts your oracle's `LeftRightUnsigned` magnitude into `(positionSize, optionRatio[4], strike[4])`.

Each layer builds on the previous. Don't skip to Layer 4 without being able to do Layer 2 by hand.



No direct relationship. They live in different coordinate systems.

## TokenId's `strike` and `width` → Tick Range

```
tickLower = strike - floor(width · tickSpacing / 2)
tickUpper = strike + ceil(width · tickSpacing / 2)
```

These define a **single liquidity chunk** — one contiguous range where liquidity sits.

## Bunni's `x` → Index Within a Distribution

```
x = (roundedTick - minTick) / tickSpacing
```

This indexes a **point** in a multi-tick density function. Each x is one rounded tick.

## The Connection

A Panoptic leg with `width=1` occupies exactly **one rounded tick** — one tickSpacing-wide bin. In that case:

```
strike ≈ minTick + x · tickSpacing + tickSpacing/2

x = (strike - tickSpacing/2 - minTick) / tickSpacing
  = (strike - minTick) / tickSpacing    (approximately, for aligned strikes)
```

So for minimum-width legs (`width=1`), **x tells you which leg index corresponds to which strike**.

For wider legs (`width > 1`), one leg covers multiple x values — it's a smeared version of the point density:

```
width=1:   leg covers 1 rounded tick  →  maps to single x
width=5:   leg covers 5 rounded ticks →  maps to x range [x_start, x_start+4]
width=W:   leg covers W rounded ticks →  integrates density over W consecutive x values
```

## For the Hedge Construction

When discretizing the K^{-1/2} kernel into 4 Panoptic legs:

```
LP range: [minTick, minTick + n·tickSpacing]    (n rounded ticks total)

Leg 0:  strike_0 = minTick + (n/5)·tickSpacing,     width=1,   corresponds to x = n/5
Leg 1:  strike_1 = minTick + (2n/5)·tickSpacing,    width=1,   corresponds to x = 2n/5
Leg 2:  strike_2 = minTick + (3n/5)·tickSpacing,    width=1,   corresponds to x = 3n/5
Leg 3:  strike_3 = minTick + (4n/5)·tickSpacing,    width=1,   corresponds to x = 4n/5

optionRatio_i ∝ α^{x_i}   (weight at that x)
```

Or with wider legs that each cover a segment:

```
Leg 0:  strike_0 = minTick + (n/8)·tickSpacing,     width=n/4,  integrates x ∈ [0, n/4)
Leg 1:  strike_1 = minTick + (3n/8)·tickSpacing,    width=n/4,  integrates x ∈ [n/4, n/2)
Leg 2:  strike_2 = minTick + (5n/8)·tickSpacing,    width=n/4,  integrates x ∈ [n/2, 3n/4)
Leg 3:  strike_3 = minTick + (7n/8)·tickSpacing,    width=n/4,  integrates x ∈ [3n/4, n)

optionRatio_i ∝ Σ_{x in segment_i} α^x   (integrated weight over segment)
```

The wider-leg approach is better because each leg captures more of the continuous kernel, reducing discretization error. The tradeoff: wider width means the Panoptic option behaves less like a point-strike European (more like a range option), which deviates from the Deng paper's assumption.

# OUR NOTES

\
rightSlot = UIL^R (call-side)  →    Determines call leg sizes (isLong=1, tokenType=1)
leftSlot  = UIL^L (put-side)   →    Determines put leg sizes (isLong=1, tokenType=0)

--> addLiqudity{
  -> save positionValue {inventoryValue, feeRevenue} // not-so-static ??
  -> reference PositionConfig {tickLower, tickUpper} --> (strike x width)
  -> save sqrtPriceX96Init
  -> save/get --> LeftRightIlX96Init
}

```
Static (Deng):
  t=0: Compute full integral, buy all options, hold to maturity T
  t=T: Options expire, payoff offsets IL

Dynamic (your oracle):
  Every afterSwap():
    1. Recompute LeftRightSigned IL via leftRightIlXLiqSigned()
    2. Compare to existing hedge positions
    3. If delta exceeds threshold:
       a. Burn outdated hedge legs (SFPM.burnTokenizedPosition)
       b. Mint new hedge legs at updated strikes
    4. The LeftRightUnsigned magnitude tells you HOW MUCH to hedge
       The LeftRightSigned sign tells you WHICH SIDE needs hedging
Your Oracle Output                    Panoptic Input
─────────────────                     ──────────────
LeftRightSigned{UIL^R, UIL^L}   →    How much to hedge per side
  rightSlot = UIL^R (call-side)  →    Determines call leg sizes (isLong=1, tokenType=1)
  leftSlot  = UIL^L (put-side)   →    Determines put leg sizes (isLong=1, tokenType=0)

LeftRightUnsigned{|UIL^R|,|UIL^L|} → Magnitude for threshold/sizing
  rightSlot = |UIL^R|            →    positionSize for call hedge
  leftSlot  = |UIL^L|            →    positionSize for put hedge

```
--> swap {
  -> save { afterSwapSqrtPriceX96, afterSwapTick } // this is ONLY used for calculations, then discarded
  -> get  positionFeesEarned : LeftRightSigned     // constrained capital from where to build hedging 
  -> build/update { TokenId[4] }
}


(LeftRightPositionFeesEarned x LeftRightIlX96) -> LeftRightGrossAvailable


(LeftRightGrossAvailable x tickStrike x afterSwapTick x tickSpacing x width ) -> Strikes
         (L*)                (ik)          (i_as*)         (ts)        (w)


^
|
|
| L* ------------- >   -----------------
|                     |                 |
|                     |                 |
|                     |                 |
|                     |                 |
|                     |        ts       |
---- |----------------|-------|--|------|---------------|
     il             i_as*              i_k             iu

                     |---------w--------|



--------------------------> Strikes <-------------------------------
 | --------|---------|--------|---------|------------------------| 

i_as       i1       i2        i3        i4                      i_k


------------> LDF <--------------

(Strikes, ...) -> (positionSize[4] x optionRatio[4]) --> IronCondor
                                  |
                                  |
                                  v
         LeftRight <---> LiquidityChunk  --> l(i) = L*f(\sqrt{p(i)})


## todo:

                                                 ^
HIGHEST LEVEL GOAL: Construct the pipeline above |


1. From PanopticPool.t.sol:4036-4227 derive 

- what is the meaning of positionSize ?
- what is the meainign of optioRatio ?
- why intermedaaite swp is needed at all ?
- How to human write the test ?


2. Establish connection with Bunni- V2
