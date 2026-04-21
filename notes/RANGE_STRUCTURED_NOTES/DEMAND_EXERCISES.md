
Right on on documentation or summary of the data exercise we have done and what limitations we have come up with because I'm able we are unable and why we're unable to continue without the do an API key Also document the references that you use from external directories such as the LPs deraver the LPs deraver, the directories, the external LPs deraver, the directories for nodes and for pdf references and then the pdf and the sources for data and also the resources on the apps, link, sole SDK, dev directory.

# Demand Identification: Range Accrual Notes

## Exercise B: ThetaSwap Fee Concentration as Demand Signal

### Question
In pools where adverse competition (JIT) is high, do LPs exit faster or accept worse terms — and does that exit behavior price the theta component?

### Why B First
- ThetaSwap Phase 1 already validated: 600 ETH/USDC positions, 9% fee dispersion threshold, ~20% of positions better off hedged
- The oracle already measures fee concentration in real time
- The backtest infrastructure exists (`~/apps/ThetaSwap/thetaSwap-core-dev/backtest/`)
- This exercise extends Phase 1 rather than starting from scratch

### Identification Strategy
1. Partition historical LP positions into HIGH vs LOW fee-concentration regimes (using ThetaSwap's FCI oracle threshold at 9% dispersion)
2. Measure LP survival time (blocks from mint to burn) in each regime
3. Test: `H0: survival_HIGH = survival_LOW` vs `H1: survival_HIGH < survival_LOW`
4. If LPs exit faster under high concentration → they are implicitly expressing WTP for theta protection
5. The hazard rate difference × average fee income = implied price of the range accrual note

### Data Requirements
- ThetaSwap oracle output: fee concentration index per block per pool
- LP position lifecycle data: mint block, burn block, tick range, liquidity (Dune query #6941901 + extensions)
- Fee income realized per position over its lifetime

### What Success Looks Like
- Statistically significant difference in LP survival across regimes
- A monetizable spread: LPs in adverse regimes would pay X bps above hourly fees for a range accrual note that smooths their income
- Connects to ThetaSwap pitch: "20% of positions better off hedged" → now we have the instrument they'd hedge WITH

### Output
- Estimated WTP (bps) for theta protection conditional on fee concentration regime
- Feeds directly into coupon calibration for `RangeAccrualNote.VANILLA`

---

## Exercise A: Revealed Preference from LP Range Width Choices

### Question
Do LPs already implicitly pay for "time-in-range" insurance by choosing narrower ranges than fee-maximizing widths?

### Why A Second
- Requires Exercise B's regime classification to control for adverse competition
- Without B's fee concentration partition, the range width analysis conflates directional bets with theta bets
- B provides the counterfactual: what WOULD fee income be without adverse competition → then A measures the behavioral response

### Identification Strategy
1. For each pool, compute the fee-maximizing range width (given realized vol and fee tier)
2. Compare against actual range widths chosen by LPs
3. Decompose the gap:
   - Narrower than optimal → LP is accepting lower expected fees for higher time-in-range probability (revealed WTP for accrual certainty)
   - Wider than optimal → LP is hedging directional risk (Panoptic's domain, not ours)
4. Condition on B's fee concentration regimes: does the narrowing behavior intensify in HIGH concentration periods?

### Data Requirements
- Same LP lifecycle data as Exercise B
- Realized volatility per pool per epoch (for computing fee-optimal width)
- Pool fee tier

### What Success Looks Like
- Systematic range narrowing in HIGH concentration regimes = LPs are self-insuring by sacrificing fee income
- The "insurance cost" they're paying (fee income gap between actual and optimal width) = upper bound on range accrual note price
- Cross-validated with B's WTP estimate: if both exercises produce consistent pricing, the demand signal is robust

### Output
- Revealed WTP (bps) for time-in-range certainty, decomposed by regime
- Range accrual note coupon bounds: [Exercise B lower bound, Exercise A upper bound]

---

## Sequencing

```
Exercise B (extend ThetaSwap Phase 1)
    |
    ├── fee concentration regimes (HIGH/LOW)
    ├── LP survival hazard rates
    └── WTP estimate (lower bound on coupon)
            |
            v
Exercise A (revealed preference)
    |
    ├── fee-optimal vs actual range widths
    ├── narrowing behavior conditional on B's regimes
    └── WTP estimate (upper bound on coupon)
            |
            v
Coupon Calibration
    |
    └── RangeAccrualNote.VANILLA parameterization
            |
            v
Product hierarchy: RangeAccrualNote → FCI Index → DataSwap
```

## Design Decisions (resolved 2026-04-03)

### Pools: ETH/USDC + USDC/DAI + wstETH/WETH
Three pools give a 2x2 matrix (high/low vol × high/low fee concentration).
- ETH/USDC: baseline, reuses ThetaSwap Phase 1 infra
- USDC/DAI: stable pair, theta-dominant income — expected STRONGEST range accrual demand
- wstETH/WETH: correlated volatile pair, Algebra Camelot data already seeded (5 positions in git)

### Dataset: 600 as baseline → re-pull as robustness
- Run Exercise B on ThetaSwap's existing 600-position ETH/USDC dataset first for quick signal
- Then re-pull with 5-filter definition, longer time window, all 3 pools as robustness check
- If results agree → strong. If they disagree → the disagreement itself reveals selection bias
- Do NOT publish on 600 alone — the re-pull is the real result

### Granularity: Two-scale (block-level FCI, epoch-level survival)
- Block-level for FCI regime classification (HIGH/LOW) — must capture JIT dynamics (1-3 block positions)
- Epoch-level (hourly) for survival analysis — position lifetime in blocks is mostly noise for non-JIT LPs
- Mirrors product architecture: oracle detects regime at block granularity, note settles at epoch granularity
