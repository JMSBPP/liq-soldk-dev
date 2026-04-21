# Verification Report: USDC/DAI Dynamic vs Static Fee Mechanism Identification Strategy

**Reviewed document**: `2026-04-01-usdc-dai-fee-mechanism.md`
**Assertions reviewed**: `T1-vol-sensitivity-sign.md`, `T3-sufficiency-exclusion.md`
**Reviewer**: Model QA Specialist (adversarial audit)
**Date**: 2026-04-01
**Formal verification status**: NOT VERIFIED (Aristotle API key missing; all assertions remain unproven)

---

## Overall Assessment

The identification strategy document is a well-structured first draft with economically motivated candidate strategies. However, it contains several material flaws that would undermine a Reiss-Wolak structural specification if left unaddressed. The most serious issues are: (1) the specification conflates two distinct simultaneity problems without acknowledging the resulting bias direction, (2) the exclusion restrictions are either untestable or economically implausible under the conditions when identification matters most (stress regimes), and (3) the cross-chain confound is acknowledged but not resolved, leaving the "natural experiment" claim without a credible control group.

---

## Strategy 1: Volatility Sensitivity of LP Fee Revenue

### Specification Review

**Equation under review**:

//  note: what is this equation trying to capture ?
```
FeeRevenue_{it} = alpha + beta_1 * sigma_t + beta_2 * (sigma_t * D_i^{dynamic}) + gamma * X_{it} + epsilon_{it}
```

### Finding 1.1: Simultaneity Bias in Volume -- FAIL

**Observation**: The specification treats `FeeRevenue_{it}` as if it is a direct function of volatility, but fee revenue is the product of fee rate and volume: `R_{it} = phi_{it} * V_{it}`. Volume itself is endogenous to the fee rate (higher fees reduce volume through aggregator routing, lower fees attract volume). This creates a simultaneous equations problem that the reduced-form specification does not address.

**Evidence**: The brainstorm document (`brainstorm-usdc-dai-fee-revenue-claims.md`, Section 2) correctly identifies that `feeRevenue = integral[fee_rate(t) * |volume(t)|] dt`, and that volume is driven by arbitrage, which is itself affected by the fee level. The Algebra pool's higher adaptive fee during stress periods mechanically repels price-sensitive flow to the Uniswap pool. This means `V_A(t)` and `V_U(t)` do NOT respond symmetrically to `sigma_t` -- the volume response is asymmetric precisely because of the treatment variable.

// note: The feeRate is a function of volatilitt that needs to be references from the algebra dynamic fee docs. But the point that regressing against it seem to be redundant since is incorporated on the fee rate dynacmi foormulae by desin
g 


**Impact**: beta_2 captures a mixture of two effects: 

(a) the direct fee-rate sensitivity to vol (the mechanism of interest) and 

(b) the endogenous volume reallocation driven by the fee differential. These have opposite signs. 
The fee rate rises with vol (positive contribution to beta_2), but volume migrates away from the higher-fee pool (negative contribution). The net sign and magnitude of beta_2 are ambiguous without decomposing these channels.

**Severity**: HIGH

**Remediation**: Decompose the specification into a structural system:

```
phi_{it} = f(sigma_t, D_i)          [fee equation -- known/deterministic for Algebra]
V_{it} = h(phi_{it}, sigma_t, Z_t)  [volume equation -- behavioral, needs identification]
R_{it} = phi_{it} * V_{it}          [revenue identity]
```

Estimate the volume equation separately, using the fee mechanism as an instrument for fee level (since it is exogenously assigned). 


Then compute the revenue effect from the structural parameters. Alternatively, estimate beta_2 on the fee rate equation alone (which is deterministic for Algebra and trivially zero for Uniswap) and on the volume equation separately, then combine.

---

### Finding 1.2: Exclusion Restriction Is Plausible for Mechanism Assignment but Not for LP Selection -- NEEDS_REVISION


// note: I do not understand this observation what is LP self-selxction and how it relates to our exercise ?
**Observation**: The exclusion restriction `E[D_i^{dynamic} * epsilon_{it}] = 0` 
claims that mechanism assignment is exogenous to USDC/DAI fundamentals.
The document correctly notes this holds at the protocol governance level (Quickswap chose Algebra for all pools, not targeting USDC/DAI specifically). However, the document then lists LP self-selection as a "potential violation" without quantifying its severity or proposing a test.


// note: Why is the uniswap V3 a control goup ? what is a control group ?
**Evidence**: LP self-selection is not a minor nuisance -- it is a first-order threat. If sophisticated LPs who want vol exposure concentrate in the Algebra pool, then TVL_{it} (which appears in controls X_{it}) is endogenous. Worse, the LP composition affects the liquidity distribution across ticks, which affects the effective fee per unit of volume (through feeGrowthGlobal normalization by active liquidity). Controlling for TVL does not solve this because TVL is an equilibrium outcome of LP decisions that are themselves driven by vol expectations.

**Impact**: If LP self-selection is present, the "control" group (Uniswap) has systematically different LP sophistication from the "treatment" group (Algebra). The DID estimator is biased because the parallel trends assumption fails -- the two pools would have different revenue trajectories even absent the fee mechanism difference, because they have different LP compositions.

**Severity**: MEDIUM

**Remediation**: (a) Test for LP overlap: use on-chain address analysis to determine what fraction of LP addresses provide liquidity in both pools. High overlap supports parallel trends. (b) Implement a Heckman-style selection correction using LP characteristics (address age, historical LP activity, portfolio size) as selection equation instruments. (c) At minimum, report results with and without TVL controls and discuss the sensitivity.

---

### Finding 1.3: Instruments Are Weak or Invalid -- NEEDS_REVISION

**Observation**: Three candidate instruments are proposed for GMM estimation. All three have issues.

**Evidence**:

1. **Lagged volatility (sigma_{t-k})**: For a stablecoin pair with mean-reverting volatility (OU-process, as correctly identified in the brainstorm document), lagged volatility is a weak instrument when the autoregressive coefficient is small. During calm periods (most of the sample), sigma_t is near zero and sigma_{t-k} provides essentially no variation. The instrument is only strong during stress episodes, creating a weak-instruments-with-heterogeneous-strength problem that standard first-stage F-tests will miss if computed over the full sample.

2. **ETH/USD realized vol**: This is correlated with USDC/DAI vol through a common macro factor, but the exclusion restriction requires that ETH/USD vol affects USDC/DAI fee revenue ONLY through USDC/DAI vol. This fails when ETH/USD vol directly affects (a) gas prices on Polygon (L2 sequencer load during ETH crashes), which affect arb profitability and thus volume, and (b) DAI collateral value (DAI is partially backed by ETH), which affects DAI peg stability through a channel distinct from the USDC/DAI vol measure.

3. **MakerDAO DSR changes**: These are rare events (perhaps 10-15 changes per year). The sample size of the instrument is too small for reliable asymptotic inference. Additionally, DSR changes are anticipated by the market through governance votes, so the announcement effect is partially priced in before the on-chain execution, making the timing of the instrument imprecise.

**Severity**: MEDIUM

**Remediation**: (a) Report the Kleibergen-Paap rk Wald F-statistic for weak instruments, separately for calm and stress subsamples. (b) For the ETH/USD instrument, add gas price and DAI collateral ratio as additional controls to block the excluded channels. (c) For DSR changes, consider using the full MakerDAO governance vote timeline (MKR voting, poll results, executive spell queued) rather than the execution block to capture the information arrival time. (d) Consider a control-function approach as an alternative to IV/GMM, which may perform better with heterogeneous instrument strength.

---

### Finding 1.4: The Rank Condition Discussion Understates the Identification Challenge -- NEEDS_REVISION

**Observation**: The rank condition section states `Var(sigma_t) > 0` and lists historical stress events. This is necessary but far from sufficient.

**Evidence**: The rank condition for the DID interaction term beta_2 requires not just that volatility varies, but that the CROSS-POOL DIFFERENCE in revenue response varies with volatility. If both pools happen to respond similarly to vol (because volume routing equalizes the effective exposure), then beta_2 is identified in theory but estimated with enormous standard errors. The relevant rank condition is:

```
Var(sigma_t * [R_A(sigma_t)/sigma_t - R_U(sigma_t)/sigma_t]) > 0
```

which is the variance of the differential sensitivity, not just the variance of the common shock.

Furthermore, the listed stress events (SVB crisis, USDC depeg) are essentially 1-2 episodes in the sample. A structural parameter identified from 1-2 events is fragile -- this is effectively an event study, not a panel regression, and should be acknowledged as such.

**Severity**: LOW

**Remediation**: (a) Compute power calculations: given the expected number of stress episodes and the magnitude of the fee differential during those episodes, what is the minimum detectable effect size? (b) Consider supplementing with simulation-based identification diagnostics (Berry-Haile style) to assess whether the model parameters are identifiable from the data generating process.

---

## Strategy 2: Dynamic Fee as Sufficient Statistic

### Finding 2.2: The Conditional Independence Assumption Is Economically Implausible -- FAIL


// note: A caveat to this is that if we want non-toxic trading flow this assumpttion might bit be that unreaslsitic. CFMM's are good price engines on reatil flo. Does a fileter on volume unlocks new queestions ?

**Observation**: Assertion T3 requires `V(t) _||_ sigma(t) | phi(t)` -- volume is independent of volatility conditional on the adaptive fee.

**Evidence**: This assumption fails on economic grounds. Traders observe real-time volatility (e.g., from CEX feeds, other on-chain pools, news) and adjust their trading behavior independently of what the Algebra fee accumulator shows. The Algebra fee accumulator is a backward-looking moving average with specific lookback parameters. A sudden vol spike (e.g., USDC depeg news) will cause traders to increase volume IMMEDIATELY, but the Algebra fee will adjust with a lag (it uses `volatilityCumulative` which is a rolling average over the timepoints window). During this lag period, volume responds to sigma_t but phi_t has not yet updated. Therefore `V(t) _||_ sigma(t) | phi(t)` fails whenever vol shocks arrive faster than the Algebra accumulator's update frequency.

The document itself identifies this as a "potential violation" but does not recognize that it is a CERTAIN violation during the exact stress periods that are most economically interesting.

**Severity**: HIGH

**Remediation**: (a) Replace the sufficiency hypothesis with a weaker, testable claim: phi_t captures MOST of the vol information relevant for revenue, but not all. Quantify the residual information in sigma_t beyond phi_t using a partial R-squared decomposition. (b) Characterize the lag structure: how many blocks does it take for phi_t to fully incorporate a vol shock? This is measurable from the Algebra accumulator mechanics (the `volatilityOracle` uses a specific window, verifiable in `VolatilityOracle.sol`). (c) The sufficient statistic framing is too strong for the application. Reframe as an information decomposition: what fraction of revenue variance is explained by phi_t vs. sigma_t vs. their interaction?

---

### Finding 2.1: The Sufficiency Test Is Mechanically Biased Toward Acceptance -- FAIL

**Observation**: The test regresses Algebra fee revenue on phi_t and sigma_t, testing whether beta_sigma = 0. The document claims this tests whether phi_t is a sufficient statistic for sigma_t.

**Evidence**: This test is mechanically biased toward accepting sufficiency (failing to reject H0) for two reasons:

(a) **Multicollinearity**: phi_t is a deterministic monotone function of the Algebra volatility accumulator, which is itself a lagged moving average of tick-based volatility. If sigma_t is measured from the same tick data (which is the natural measurement), then phi_t and sigma_t are near-perfectly collinear by construction. The regression coefficient beta_sigma will be imprecisely estimated (large standard error) and the test will have no power to reject H0. This is not evidence of sufficiency -- it is evidence of collinearity.

(b) **Measurement mismatch**: If sigma_t is measured differently from the Algebra accumulator (e.g., using a different lookback window or a different volatility estimator), then rejection of H0 merely reflects the measurement discrepancy, not a genuine failure of sufficiency. The test conflates "phi_t does not capture all vol information relevant for revenue" with "phi_t uses a different vol measure than the researcher."

**Impact**: The test as specified has no discriminating power. It will accept sufficiency when sigma_t is measured the same way (collinearity) and reject it when sigma_t is measured differently (measurement artifact). Neither outcome tells you anything about the economic content.

**Severity**: HIGH

**Remediation**: (a) The proper test of sufficiency requires measuring sigma_t from an INDEPENDENT source -- not from the same pool's tick data. Use ETH/USD realized vol, o

// note:Whta does this "spread" mean financially/ economically CAN it reflect a macro variable itself ?

ff-chain USDC/DAI spread data (CEX), or cross-chain USDC/DAI pool data as the external vol measure. (b) Alternatively, test sufficiency by checking whether phi_t exhausts the predictive content for NEXT-PERIOD revenue (a forecasting test), not concurrent revenue. If phi_t is sufficient, then E[R_{t+1} | phi_t, sigma_t] = E[R_{t+1} | phi_t]. This has more discriminating power because the lagged accumulator in phi_t may miss information in current sigma_t that predicts future revenue. (c) Report the variance inflation factor (VIF) between phi_t and sigma_t. If VIF > 10, acknowledge that the test has no power.

---

## Strategy 3: Fee Revenue Spread as DeFi Monetary Stress Signal

### Finding 3.1: The Exclusion Restriction Is Circular -- FAIL

**Observation**: The exclusion restriction claims: `E[Spread_t * epsilon_t | sigma_t] = 0`, i.e., the fee revenue spread affects stress indicators only through the volatility channel.

**Evidence**: This is circular. The spread IS a function of volatility (by construction, it exists because the two fee mechanisms respond differently to vol). Conditioning on sigma_t and claiming the spread has no residual effect is tautological IF the spread is a deterministic function of sigma_t. If the spread is NOT a deterministic function of sigma_t (because of volume routing, TVL differences, etc.), then the exclusion restriction fails because those non-vol components of the spread may independently affect stress indicators.

More precisely: the spread is `R_A(t) - R_U(t) = phi_A(sigma_t) * V_A(t) - phi_bar * V_U(t)`. This depends on sigma_t through both the fee channel AND the volume channel. Conditioning on sigma_t does not zero out the spread because V_A and V_U are not deterministic functions of sigma_t. The residual variation in the spread (after conditioning on sigma_t) comes from volume differences, which are driven by LP liquidity, aggregator routing, and gas costs -- all of which may independently affect DeFi stress indicators.

**Severity**: HIGH

**Remediation**: (a) Abandon the spread-as-instrument approach. Instead, use the spread as a DEPENDENT VARIABLE and study what predicts it. (b) If the goal is to use the spread as a stress signal, frame it as a forecasting/predictive exercise, not a causal/structural one. Test Granger causality from the spread to stress indicators, with appropriate controls. Granger causality does not require an exclusion restriction -- it only requires that the spread contains incremental predictive information beyond the history of the stress indicator and other controls. (c) If a causal interpretation is desired, specify the DAG explicitly: what is the hypothesized causal chain from spread to stress, and what are the back-door paths that must be blocked?

---

### Finding 3.2: "DeFi Monetary Stress" Is Undefined -- NEEDS_REVISION

**Observation**: The dependent variable `StressIndicator_t` is not defined. The macro connections section lists several potential manifestations (CDP liquidations, USDC confidence, DeFi-wide monetary conditions) but does not commit to a measurable variable.

**Evidence**: Without a precise definition, the strategy cannot be evaluated for data feasibility or tested. Different stress indicators will have different relationships with the fee revenue spread, and cherry-picking the indicator that gives the best result is a form of specification search that invalidates inference.

**Severity**: MEDIUM

**Remediation**: Pre-commit to a specific, measurable stress indicator before looking at data. Candidates that are available on-chain: (a) MakerDAO vault liquidation volume (measurable from Maker events), (b) USDC/DAI price deviation from 1.0 exceeding a pre-specified threshold, (c) aggregate DeFi TVL drawdown exceeding a threshold (measurable from DeFi Llama or on-chain). Register the choice and the threshold in the specification document.

---

## Assertion T1 Review: Vol-Sensitivity Sign

### Finding T1.1: Proof Sketch Relies on Symmetric Volume Assumption That Contradicts the Economic Setting -- FAIL

**Observation**: The proof sketch assumes `V_A(t) ~ V_U(t)` and `dV_A/d(sigma) ~ dV_U/d(sigma)` (symmetric volume response).

**Evidence**: This is directly contradicted by the economic setting. The entire point of the dynamic fee is that it changes the fee level with vol, which changes the relative attractiveness of the two pools to volume routers. During high vol, the Algebra fee rises (e.g., from 1bp to 30bp or more, per the sigmoid parameters in `AdaptiveFee.sol`: alpha1=2900 hundredths of a bip above baseFee, alpha2=12000 additional). This makes the Algebra pool more expensive, causing aggregators to route more volume to the Uniswap pool. Therefore `dV_A/d(sigma) < dV_U/d(sigma)` -- the volume responses are asymmetric with the OPPOSITE sign from what would support the assertion.

The assertion document correctly identifies condition 3 as the escape hatch: `|g'(sigma) * V_A| > |(g(sigma) - phi_bar) * dV/d_sigma|`. But this is an empirical condition, not a theoretical guarantee. The assertion should be classified as CONDITIONAL on this empirical magnitude, not as a theoretical result.

**Severity**: MEDIUM

**Remediation**: (a) Drop the symmetric volume assumption. (b) Restate T1 as: "Under the empirical condition that the direct fee-rate effect dominates the volume-routing effect, beta_2 > 0." (c) Provide the testable implication: compute the fee-rate elasticity of volume routing from aggregator data (1inch, Paraswap APIs record routing decisions). If volume elasticity with respect to fee is small (inelastic routing), the assertion likely holds. If elastic, it may fail. (d) Note that during extreme stress (very high vol), the Algebra fee saturates at baseFee + alpha1 + alpha2 = 15000 hundredths of a bip = 1.5%, which is substantial. Volume routing away from a 1.5% fee pool could easily dominate.

---

## Assertion T3 Review: Sufficiency Exclusion

### Finding T3.1: The Proof Is Logically Valid but the Premise Is Empirically False -- NEEDS_REVISION

**Observation**: The proof that `(V _||_ sigma | phi) ==> E[R | phi, sigma] = E[R | phi]` is correct as a mathematical derivation. The issue is entirely with the premise.

**Evidence**: As established in Finding 2.2, the conditional independence premise `V(t) _||_ sigma(t) | phi(t)` fails during stress periods due to the lag between real-time vol and the Algebra accumulator update. The assertion document correctly identifies both violation channels (traders observing sigma directly; sigma measured differently from the accumulator) but does not assess their magnitude.

Additionally, the proof treats phi as a function of lagged sigma: `phi(t) = g(sigma(t-1), ..., sigma(t-k))`. This is more nuanced than the specification document suggests. The Algebra accumulator (`volatilityCumulative`) is updated per-swap, not per-block. In low-activity periods, the accumulator may not update for many blocks, creating stale fee levels. During these stale periods, sigma_t (measured from actual price movements on other venues) diverges from the information embedded in phi_t, violating conditional independence.

**Severity**: MEDIUM

**Remediation**: (a) Characterize the accumulator staleness problem: compute the distribution of inter-update intervals for `volatilityCumulative` on the actual Quickswap USDC/DAI pool. If the median inter-update interval is large (e.g., >100 blocks), the sufficiency claim is empirically weak. (b) Qualify the assertion: "T3 holds in the limit of continuous accumulator updates and in the absence of information arrival faster than the accumulator lookback window." (c) Consider testing a relaxed version: conditional on phi_t AND phi_{t-1} (two lags of the fee), is sigma_t still informative for revenue? This tests whether the lag structure of the accumulator is the primary source of failure.

---

## Cross-Cutting Issues

### Finding CC.1: Cross-Chain Confound Is Unresolved -- NEEDS_REVISION

**Observation**: The specification states Algebra pool is on Polygon (Quickswap V3). The `USDC_DAI.md` notes file shows Uniswap V3 location as "TBD." If the Uniswap pool is on Ethereum mainnet, the pools face different gas cost regimes, different MEV environments, different block times, and different sequencer/validator behavior. These are all confounds.

**Evidence**: The identification strategy document mentions "chain effects" as a potential violation (Finding 1.2, point 3) but does not resolve it. For a credible natural experiment, the two pools must face the SAME external conditions except for the fee mechanism. Cross-chain deployment violates this requirement along multiple dimensions that are difficult to control for.

**Severity**: HIGH (if cross-chain), LOW (if same-chain)

**Remediation**: (a) Verify whether a USDC/DAI pool with meaningful liquidity exists on Uniswap V3 on Polygon. If yes, use it as the control. (b) If only an Ethereum mainnet pool exists, the specification must explicitly model the chain-specific confounds: gas costs (L2 vs L1), block time (2s Polygon vs 12s Ethereum), MEV exposure (centralized Polygon sequencer vs decentralized Ethereum validators). These must be controlled for, not merely acknowledged. (c) Consider using Quickswap's own static-fee pools (if any exist for USDC/DAI before the Algebra migration) as a within-protocol control, eliminating the cross-chain confound entirely.

---

### Finding CC.2: Temporal Alignment of Observables Is Not Addressed -- NEEDS_REVISION

**Observation**: The data requirements table lists variables at "per-block" and "per-swap" granularity but does not discuss how to align observations across pools that may have different swap frequencies.

**Evidence**: The Algebra pool and Uniswap pool will have different swap arrival rates. On a panel regression with time-indexed observations, the researcher must choose a common time grid (e.g., hourly, daily). If one pool has 100 swaps per hour and the other has 5, the aggregation methodology matters: is fee revenue the cumulative feeGrowthGlobal delta over the hour? Is sigma_t the realized variance computed from swap prices within the hour? The choice of aggregation window affects the results, and no aggregation scheme is proposed.

**Severity**: MEDIUM

**Remediation**: (a) Specify the temporal aggregation scheme explicitly: fixed time windows (hourly/daily) with feeGrowthGlobal differenced over the window, and realized variance computed from all swap prices within the window. (b) Test sensitivity to the aggregation window (hourly vs. 4-hourly vs. daily). (c) For the Algebra pool, note that the fee accumulator uses a specific lookback window -- the aggregation scheme should be informed by this window to avoid aliasing artifacts.

---

### Finding CC.3: Missing Assertion T2 and Incomplete T4/T5 -- NEEDS_REVISION

**Observation**: The testable implications table lists T1-T5, but only T1 and T3 have formal assertion files. T2 (monotonicity of beta_2 in sigma), T4 (Granger causality), and T5 (spread widening during stress) are listed but have no corresponding assertion documents.

**Evidence**: T2 is critical because it tests the non-linear extension of Strategy 1. The double-sigmoid structure in AdaptiveFee.sol implies a specific non-linear shape: the fee sensitivity to vol is highest in the transition region of each sigmoid and flat in the saturation regions. T2 as stated (`d(beta_2)/d(sigma) >= 0`) is monotonicity, but the sigmoid structure actually predicts non-monotonicity -- the sensitivity should peak in the sigmoid transition zones and flatten at high vol (saturation). The testable implication as stated may be WRONG for the actual mechanism.

**Severity**: MEDIUM

**Remediation**: (a) Create assertion files for T2, T4, and T5. (b) For T2, revise the mathematical statement to match the actual sigmoid structure: the sensitivity should follow the derivative of the sigmoid (a bell-shaped curve), not a monotonically increasing function. The correct implication is that beta_2 is highest in the moderate-vol regime (sigmoid transition) and actually DECREASES at very high vol (sigmoid saturation). (c) If T2 is intended as a local monotonicity condition (valid only below the saturation point), state this explicitly with the domain restriction.

---

## Summary of Findings

| # | Finding | Severity | Verdict | Domain |
|---|---------|----------|---------|--------|
| 1.1 | Simultaneity bias in volume (fee endogenous to volume routing) | HIGH | FAIL | Strategy 1 |
| 1.2 | LP self-selection threatens parallel trends | MEDIUM | NEEDS_REVISION | Strategy 1 |
| 1.3 | All three candidate instruments are weak or invalid | MEDIUM | NEEDS_REVISION | Strategy 1 |
| 1.4 | Rank condition discussion insufficient | LOW | NEEDS_REVISION | Strategy 1 |
| 2.1 | Sufficiency test mechanically biased toward acceptance | HIGH | FAIL | Strategy 2 |
| 2.2 | Conditional independence assumption is economically implausible | HIGH | FAIL | Strategy 2 |
| 3.1 | Exclusion restriction is circular | HIGH | FAIL | Strategy 3 |
| 3.2 | Stress indicator undefined | MEDIUM | NEEDS_REVISION | Strategy 3 |
| T1.1 | Symmetric volume assumption contradicts economic setting | MEDIUM | FAIL | Assertion T1 |
| T3.1 | Proof valid but premise empirically false | MEDIUM | NEEDS_REVISION | Assertion T3 |
| CC.1 | Cross-chain confound unresolved | HIGH | NEEDS_REVISION | Cross-cutting |
| CC.2 | Temporal alignment not specified | MEDIUM | NEEDS_REVISION | Cross-cutting |
| CC.3 | Missing assertions T2/T4/T5; T2 may be incorrectly stated | MEDIUM | NEEDS_REVISION | Cross-cutting |

**HIGH severity findings**: 5
**MEDIUM severity findings**: 7
**LOW severity findings**: 1

---

## Recommended Priority Actions

### Immediate (before proceeding to estimation)

1. **Decompose the revenue equation into structural components** (Finding 1.1). The current reduced-form specification conflates fee-rate and volume channels. This is the most fundamental issue -- all downstream analysis inherits this bias.

2. **Resolve the cross-chain question** (Finding CC.1). Determine whether a same-chain control pool exists. If not, the entire natural experiment framing needs revision.

3. **Abandon the sufficiency test as specified** (Findings 2.1, 2.2). Replace with an information decomposition using independently measured volatility.

4. **Reframe Strategy 3 as predictive, not causal** (Finding 3.1). The spread is a useful observable but cannot serve as an instrument with the proposed exclusion restriction.

### Before formal specification

5. Specify temporal aggregation scheme (Finding CC.2).
6. Complete all five assertion files with formal statements (Finding CC.3).
7. Correct T2 to match the sigmoid saturation structure (Finding CC.3).
8. Pre-commit to a measurable stress indicator (Finding 3.2).

### During estimation

9. Report weak instrument diagnostics by subsample (Finding 1.3).
10. Test LP overlap across pools (Finding 1.2).
11. Characterize Algebra accumulator staleness (Finding T3.1).

---

## Note on Formal Verification

All assertions remain formally unverified due to the missing Aristotle API key. The mathematical proof in T3 is logically valid (the conditional independence implies the sufficiency conclusion), but this is a trivial implication -- the substantive question is whether the premise holds. The proof in T1 is a sketch with an unverified dominance condition. Neither assertion should be treated as established until (a) the proofs are mechanically checked by Aristotle, and (b) the empirical premises are validated against data.

---

*Verification performed adversarially. All findings are evidence-based. The identification strategy shows strong economic intuition but requires significant revision before it can support a formal Reiss-Wolak structural specification.*
