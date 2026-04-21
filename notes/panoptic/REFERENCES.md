# Panoptic Pricing: Reference Papers

## Core Papers

### [1] Panoptic: the perpetual, oracle-free options protocol
- **Authors**: Guillaume Lambert, Jesper Kristensen
- **Published**: 2022-04-27 (v1.3.1, June 2023)
- **arXiv**: [2204.14232](https://arxiv.org/abs/2204.14232)
- **Categories**: q-fin.PR
, cs.CE, cs.CR, cs.GT, q-fin.CP
- **Local copy**: `refs/2204.14232-panoptic-protocol.md`

**Key results for pricing convergence:**

1. **Streaming premium model** (Section III.A): Instead of upfront payment, option premium is path-dependent and grows at each block proportional to the proximity of spot price to strike. Formally, this is continuously integrating theta:

   ```
   Premium = integral_0^T theta(S(t), sigma, K, t) dt
   ```

2. **Convergence to Black-Scholes** (Section III.B): Monte Carlo simulation over GBM paths shows the average streaming premium converges to Black-Scholes price. However, the distribution is wide -- ~33% of call options held 7 days cost zero (never ITM), ~16% cost 2x BS price. Coefficient of variation approaches 82% after 10+ days.

3. **Implied volatility from fees** (Section III.C): As dt -> 0, theta approximates a Dirac delta with width = tickSpacing (tS). Cumulative premium = K^2 * sigma^2 / (2*tS) * (time in range). Equating to Uni v3 fees gives:

   ```
   sigma_implied = 2 * feeRate * sqrt(Volume / (tickLiquidity * Time))
   ```

   This IV depends on traded volume and liquidity at the tick, not on realized market volatility.

4. **VEGOID spread** (Section III.D in code): The parameter modulates the premium split between longs (owed) and shorts (gross), functioning as an on-chain bid-ask spread replacement.

---

### [2] Automated Market Making and Loss-Versus-Rebalancing
- **Authors**: Jason Milionis, Ciamac C. Moallemi, Tim Roughgarden, Anthony Lee Zhang
- **Published**: 2022-08-11
- **arXiv**: [2208.06046](https://arxiv.org/abs/2208.06046)
- **Categories**: q-fin.MF, math.OC, q-fin.PM, q-fin.PR, q-fin.TR

**Key results:**

The "Black-Scholes formula for AMMs." Identifies **Loss-Versus-Rebalancing (LVR)** as the main adverse selection cost for LPs:

```
LVR_rate = sigma^2 * S^2 / (2 * marginal_liquidity)
```

This is exactly the instantaneous theta of a vanilla option. The paper derives closed-form LVR expressions for all CFMMs and shows the model matches empirical LP returns. Critical link: **LVR is the cost that funds the streaming premium in Panoptic's model** -- what shorts earn (minus LVR) and what longs pay (the streaming premium) are two sides of the same fee flow.

---

### [3] Automated Market Making and Arbitrage Profits in the Presence of Fees
- **Authors**: Jason Milionis, Ciamac C. Moallemi, Tim Roughgarden
- **Published**: 2023-05-24
- **arXiv**: [2305.14604](https://arxiv.org/abs/2305.14604)
- **Categories**: q-fin.MF, math.OC, q-fin.PM, q-fin.PR, q-fin.TR
- **Note**: PDF-only, not downloaded via arxiv MCP

Extends [2] to include trading fees and discrete Poisson block times. Key insight: **fees scale down arbitrage profits by the fraction of blocks with profitable trading opportunities**. Faster blockchains reduce LP losses. Introduces gas fees (fixed costs) showing lower gas -> smaller LP losses.

Relevance: Establishes that the fee tier choice (0.05%, 0.30%, 1.00%) directly modulates how much of LVR is recovered by LPs -- and therefore how much streaming premium accrues in Panoptic.

---

### [4] Modeling Loss-Versus-Rebalancing in AMMs via Continuous-Installment Options
- **Authors**: Srisht Fateh Singh, Reina Ke Xin Li, Samuel Gaskin, Yuntao Wu, Jeffrey Klinck, Panagiotis Michalopoulos, Zissis Poulos, Andreas Veneris
- **Published**: 2025-08-05
- **arXiv**: [2508.02971](https://arxiv.org/abs/2508.02971)
- **Categories**: q-fin.MF, q-fin.PR, q-fin.TR

**Key results:**

Models a CFAMM position as a portfolio of **perpetual American continuous-installment (CI) options**. Two results:

1. **LVR = theta of the at-the-money CI option** embedded in the replicating portfolio. This is the rigorous proof that the streaming premium model converges to option pricing.

2. Derives AMM liquidity position boundaries that suffer approximately **constant LVR** over arbitrarily long forward windows. Provides a calibration method from the IV term structure.

Relevance: This is the formal proof of the Panoptic intuition -- LP positions are options, LVR is theta, and streaming premium is the natural pricing mechanism.

---

### [5] Liquidity Provision Payoff on Automated Market Makers
- **Authors**: Jin Hong Kuan
- **Published**: 2022-09-04
- **arXiv**: [2209.01653](https://arxiv.org/abs/2209.01653)
- **Categories**: q-fin.MF, q-fin.PR, q-fin.TR
- **Note**: PDF-only, not downloaded via arxiv MCP

Derives the LP fee payoff formula under GBM + zero arbitrage:

```
Fee payoff ~ near-linear function of sigma (realized volatility)
```

Trading volume becomes endogenous (function of volatility and available liquidity). Proposes securitizing LP fee cash flows as a **volatility product** -- exactly what Panoptic does.

Relevance: Independent derivation showing LP fees are a volatility instrument. Supports the convergence argument from the other direction: if fee = f(sigma), then the fee accumulator is an implied vol oracle.

---

## The Convergence Chain

The five papers together form a complete argument:

```
[5] Kuan: LP fee payoff ~ sigma (volatility product)
        |
[2] Milionis: LVR_rate = sigma^2 * S^2 / (2*L) = theta_BS
        |
[3] Milionis+fees: fees recover fraction of LVR -> streaming premium = fees
        |
[1] Lambert: integral of streaming theta over paths -> E[premium] = BS price
        |
[4] Singh: Formal proof: AMM position = CI option portfolio, LVR = theta(CI)
```

**In one sentence**: LP fees are a volatility product [5] whose instantaneous rate equals Black-Scholes theta [2], partially recovered through trading fees [3], accumulated as Panoptic's streaming premium [1], and formally equivalent to the theta of a perpetual continuous-installment option [4].

---

## Genesis Blog Series (Guillaume Lambert, Medium)

These blog posts predate the whitepaper and contain the original derivations:

- **(2021a)** "Uniswap v3 LP Tokens as Perpetual Put and Call Options" -- Original observation that LP = short option
- **(2021b)** "Understanding the Value of Uniswap v3 Liquidity Positions" -- Payoff analysis
- **(2021c)** "Synthetic Options and Short Calls in Uniswap v3" -- Put-call parity for LP positions
- **(2021d)** "On-chain Volatility and Uniswap v3" -- IV derivation from fee/volume/liquidity (matches whitepaper Eq. for sigma)

Blog series index: https://lambert-guillaume.medium.com/

---

## Additional References

### Panoptic Documentation
- **Whitepaper**: https://paper.panoptic.xyz/ (JS-rendered, same content as arXiv 2204.14232)
- **Litepaper**: https://intro.panoptic.xyz/
- **Docs**: https://docs.panoptic.xyz/
- **Premia spread equations (interactive)**: https://www.desmos.com/calculator/mdeqob2m04

### Audit Reports
- **Obsidian Audits** (Oct 2025): `lib/2025-12-panoptic/audits/` (via Code4rena repo)
- **Nethermind**: `lib/2025-12-panoptic/audits/NM_0701_Panoptic_DRAFT.pdf`
- **Code4rena contest** (Dec 19, 2025 - Jan 7, 2026): $56k pool, `lib/2025-12-panoptic/`
- **V12 (Zellic AI) findings**: `lib/2025-12-panoptic/2025_12_panoptic_v12_findings.md`

### Uniswap v3 Foundation
- **Adams et al. (2021)**: "Uniswap v3 Core" -- concentrated liquidity whitepaper
- **Uniswap v3 Development Book**: https://uniswapv3book.com/

### Code References (this repo)
- `lib/2025-12-panoptic/contracts/SemiFungiblePositionManager.sol:1262` -- `_getPremiaDeltas` (streaming premium computation)
- `lib/2025-12-panoptic/contracts/PanopticPool.sol:197` -- `s_grossPremiumLast` accumulator
- `lib/2025-12-panoptic/contracts/RiskEngine.sol` -- collateral requirements for spreads/strangles/condors
- `lib/voltaire/src/BlackScholes.sol` -- explicit BS implementation for comparison
- `lib/voltaire/src/OptionHookV2.sol:274` -- upfront BS pricing at mint
- `lib/2025-12-panoptic/out.txt` -- full trace of `test_Success_mintOptions_ITMShortPutShortCall_Swap`
- `notes/panoptic/PRICING.md` -- side-by-side analysis of Voltaire vs Panoptic pricing
