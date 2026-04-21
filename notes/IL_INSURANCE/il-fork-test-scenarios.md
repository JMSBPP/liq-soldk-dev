# Impermanent Loss: Fork-Testable Scenarios from Papers

Extracted from 6 papers in the `cfmm-theory` repo. Every scenario below is either a direct numerical example from the paper or trivially derivable from its formulas with concrete numbers.

---

## 1. Uniswap v2 Full-Range IL (Classic)

**Source**: Hookathon Primer, Section 2.1.1 & 4.1

### Scenario 1A: Alice's ETH/DAI Position (Price Doubles)
 - **Setup**: Pool has 10 ETH + 1000 DAI. Alice owns 10% (1 ETH + 100 DAI). `k = 10000`, `P0 = 100 DAI/ETH`.
- **Price move**: ETH price rises to `P1 = 200 DAI/ETH` (alpha = 2.0).
- **Pool state**: `x1 = sqrt(10000/200) = 7.07 ETH`, `y1 = sqrt(10000*200) = 1414.21 DAI`.
- **Alice's share**: `0.707 ETH * 200 + 141.421 DAI = 282.82 DAI`.
- **HODL value**: `1 ETH * 200 + 100 DAI = 300 DAI`.
- **IL**: `-17.18 DAI` or **-5.72%**.
- **Formula**: `IL(alpha) = 2*sqrt(alpha)/(1+alpha) - 1`, where `alpha = P_T / P_0`.
- **Solidity check**: `IL(2.0) = 2*sqrt(2)/3 - 1 ~ -0.0572`

### Scenario 1B: ETH/USDC Full Range (1m USDT notional)
- **Source**: Lipton et al., Section 3.1, Figure 1
- **Setup**: Uniswap v2, `p0 = 2000 ETH/USDT`, notional = `1m USDT`.
- **Initial LP units**: `(250 ETH, 500000 USDT)`.
- **V_LP = 2L*sqrt(p)`, so `V0 = 2L*sqrt(2000)`.
- **At `p = 1500`**: LP units become `(289, 433013)`. Funded P&L = `2L*sqrt(1500) - 2L*sqrt(2000)` (negative).
- **At `p = 2500`**: LP units become `(224, 559017)`. Funded P&L likewise negative vs HODL.
- **Borrowed P&L formula**: `P&L_borrowed = -L*sqrt(p0) * (sqrt(p_t/p0) - 1)^2` (Eq 23, always <= 0)
- **Nominal borrowed IL**: `-0.5 * (sqrt(p_t/p0) - 1)^2` (Eq 24)

### Key Formulas for v2 Fork Tests:
```
// Funded IL (nominal, in USDT units)
Nom_IL_funded(p_t) = sqrt(p_t / p_0) - 1

// Borrowed IL (nominal)  
Nom_IL_borrowed(p_t) = -0.5 * (sqrt(p_t / p_0) - 1)^2

// IL protection payoffs (Lipton Corollary 3.1)
Payoff_funded(p_T) = 1 - sqrt(p_t / p_0)
Payoff_borrowed(p_T) = 0.5 * (sqrt(p_t / p_0) - 1)^2
```

---

## 2. Uniswap v3 Concentrated Liquidity IL

**Source**: Lipton et al., Section 3.2; Hookathon Primer Section 3.1.2 & 4.1.2

### Scenario 2A: ETH/USDT v3 (1m notional, range [1500, 2500])
- **Source**: Lipton et al., Section 3.2, Figure 2
- **Setup**: `p0 = 2000`, `p_a = 1500`, `p_b = 2500`, notional `N^y = 1m USDT`.
- **Initial LP units**: `(220 ETH, 559282 USDT)`.
- **Liquidity**: `L = N^y / (2*sqrt(p0) - p0/sqrt(p_b) - sqrt(p_a))` (Eq 40)
- **At `p = p_a = 1500`**: LP fully in ETH → `(543 ETH, 0 USDT)`. Max downside IL.
- **At `p = p_b = 2500`**: LP fully in USDT → `(0 ETH, 1052020 USDT)`. Max upside IL.

### Funded P&L (Lipton Proposition 3.3, Eq 41):
```
// Three regimes for P&L_funded:
if p_a < p_t < p_b:
  P&L = L * [2*(sqrt(p_t) - sqrt(p0)) + (p0 - p_t)/sqrt(p_b)]
if p_t <= p_a:
  P&L = L * [p_t*(1/sqrt(p_a) - 1/sqrt(p_b)) + p0/sqrt(p_b) - 2*sqrt(p0) + sqrt(p_a)]
if p_t >= p_b:
  P&L = L * [sqrt(p_b) + p0/sqrt(p_b) - 2*sqrt(p0)]
```

### Scenario 2B: Range Width vs IL Severity (Lipton Figure 3)
- **Setup**: `p0 = 2000`, notional `1m USDT`.
- Compare v3 ranges `[pa=90%*p0, pb=110%*p0]`, `[80%, 120%]`, `[50%, 150%]` vs v2 full range.
- **Key finding**: Narrower ranges → higher IL at same price levels.
- For borrowed LP at 20% price drop: v3 [90%,110%] → ~-30% P&L vs v2 → ~-5% P&L.

### Scenario 2C: Concentrated IL as Function of alpha (Hookathon Eq 20-21)
```
// V_LP for concentrated position:
V_LP = 2L*sqrt(P*alpha) - L*(sqrt(p_a) + P*alpha/sqrt(p_b))

// V_HODL:
V_HODL = L*sqrt(P)*(1 + alpha) - L*(sqrt(p_a) + P*alpha/sqrt(p_b))

// IL_{a,b}(alpha) = IL(alpha) * C  where C is the concentration leverage factor
```

---

## 3. IL as Option Replication (Static Hedge)

### Scenario 3A: Clark CPM Replication (Appendix A)
- **Source**: Clark 2020, Appendix A
- **Setup**: CPM with `(t, R_beta, R_alpha) = (1, 10, 200)`, `k = R_alpha * R_beta = 2000`.
- **Price**: `m_p = R_beta/R_alpha = 0.05`.
- **Pool value**: `P_V = 2*sqrt(k*m_p) = 2*sqrt(2000*0.05) = 20`.
- **Replicating portfolio**:
  - Bond: face value `W(m0) = 2*sqrt(k*m0) = 20`
  - Futures: notional `W'(m0) = sqrt(k/m0) = sqrt(2000/0.05) = 200`
  - Options at strike K: notional `W''(K) = -0.5*sqrt(k/K^3) dK`
- **Discrete strikes** `K = (0.0125, 0.025, ..., 0.1)`:

| Strike K | Call notional | Put notional |
|----------|-------------|-------------|
| 0.0125   | 0           | -200        |
| 0.025    | 0           | -70.7       |
| 0.0375   | 0           | -38.5       |
| 0.05     | 0           | -25         |
| 0.0625   | -17.8       | 0           |
| 0.075    | -13.6       | 0           |
| 0.0875   | -10.8       | 0           |
| 0.1      | -8.3        | 0           |

- **Solidity test**: Verify `2*sqrt(k*m_T)` matches replicated value across m_T values.

### Scenario 3B: Deng et al. Static Replication of v3 IL
- **Source**: Deng/Zong/Wang, Section 4.1, Table 1
- **Setup**: `P0 = 10`, `sigma = 0.7`, upper range `[P_l, P_u] = [11, 14]`, lower range `[S_l, S_u] = [6, 9]`, maturity `t = 7 days`.
- **Expected IL (right side)**: UIL^R varies from -0.424 to -0.502 depending on Heston params.
- **Static replication error**: ~1e-5 (0.01 basis points) with 10 strikes.
- **Key formula** (Proposition 3.5, Eq 9):
  ```
  E[UIL^R] = -0.5 * integral_{P_l}^{P_u} K^{-3/2} * C(K) dK
  ```
  where `C(K)` is European call price at strike K.

### Scenario 3C: Deng et al. Deribit BTC Options (Table 2)
- **Setup**: LP enters BTC-USDC daily, provides liquidity `[P0, u*P0]` and `[d*P0, P0]` for 1 or 2 weeks.
- **Concrete numbers**: `u = {1.1, 1.2, 1.3}`, `d = {0.9, 0.8, 0.7}`.
- T=1 week, u=1.1: E[UIL^R] = -1.588, Static = -0.991, with 3 strikes.
- T=1 week, u=1.3: E[UIL^R] = -3.597, Static = -3.253, with 10 strikes.
- **Solidity test**: Given a set of option strikes/prices, verify the static replication formula approximates the actual IL.

---

## 4. LVR (Loss-Versus-Rebalancing)

**Source**: Milionis/Moallemi/Roughgarden/Zhang, Section 4 (Theorem 1)

### Core LVR Formula (Theorem 1, Eq 7-8):
```
LVR_t = integral_0^t ell(sigma_s, P_s) ds

where instantaneous LVR:
ell(sigma, P) = (sigma^2 * P^2 / 2) * |x*'(P)|
```

### Scenario 4A: Constant Product (xy=L^2)
- **Source**: Section 5, Example 2
- `V(P) = 2L*sqrt(P)`, `x*(P) = L/sqrt(P)`, `x*'(P) = -L/(2*P^(3/2))`
- **Instantaneous LVR**: `ell = sigma^2 * L * sqrt(P) / 4`
- **For constant sigma**: `E[LVR_T] = sigma^2/8 * V_0 * T` (from footnote 3 / Evans formula)
- **Concrete**: V0 = 2M USDC, sigma = 50% annual, T = 1 year → E[LVR] = 0.25/8 * 2M = 62,500 USDC.

### Scenario 4B: Uniswap v3 Concentrated Liquidity
- **Source**: Example 4-5
- For price range `[p_a, p_b]`: `x*(P) = L*(1/sqrt(P) - 1/sqrt(p_b))` when `P in (p_a, p_b)`.
- `|x*'(P)| = L/(2*P^(3/2))` (same as v2 while in range, 0 out of range).
- **LVR is identical to v2 per unit of L while in range, but L is larger per dollar of capital.**
- This means LVR per dollar invested is amplified by the concentration factor.

### Scenario 4C: LVR = Arbitrageur Profits
- LVR_t = cumulative profits of rebalancing arbitrageurs = R_t - V_t.
- **Solidity test**: Simulate price path, compute arbitrageur profits from each swap, verify it matches the LVR integral.
- LP P&L decomposition: `V_t - V_0 = (R_t - V_0) - LVR_t`, where `R_t - V_0 = integral x*(P_s) dP_s`.

---

## 5. IL Decomposition into Exotic + Vanilla Payoffs (v3)

**Source**: Lipton et al., Section 3.3

### Funded LP IL Decomposition (Proposition 3.5, Eq 48-49):
```
IL_funded(p_t) = u_0(p_t) + u_{1/2}(p_t) + u_1(p_t)

where:
u_0(p_t) = -p_t/sqrt(p_b) + (p0/sqrt(p_b) - 2*sqrt(p0))          // linear
u_{1/2}(p_t) = sqrt(p_t) * 1{p_a < p_t < p_b}                      // exotic sqrt
u_1(p_t) = -(1/sqrt(p_a))*max(p_a - p_t, 0)                        // puts
           + (1/sqrt(p_b))*max(p_t - p_b, 0)                        // calls
           + 2*sqrt(p_a)*1{p_t <= p_a} + 2*sqrt(p_b)*1{p_t >= p_b}  // digitals
```

### Scenario 5A: Replication with Deribit Options (Lipton Figure 4)
- **Setup**: Borrowed v3 LP, `p0 = 2000`, `p_a = 1500`, `p_b = 2500`, notional `1m USDT`, strike width = 50 USDT.
- **Result**: Max residual between IL and option replication is 0.025% (2.5 basis points).
- Put and call portfolios use ~20-40 contracts each across strikes [1500, 2500].

### Scenario 5B: BSM Valuation (Proposition 5.2, Figure 5)
- **Setup**: Borrowed LP, `p0 = 2000`, `p_a = e^{-m} * p0`, `p_b = e^m * p0`, T = 14/365 years.
- **Range multiples** `m = {5%, 10%, 15%, ..., 40%}`:
  - At vol=25%, m=10%: BSM premium ~50% APR
  - At vol=50%, m=10%: BSM premium ~100% APR  
  - At vol=100%, m=10%: BSM premium ~175% APR
- **Formula** (Eq 81): involves Black-Scholes vanillas + digitals + sqrt payoff term.

---

## 6. Leveraged CL and Liquidation

**Source**: Elsts & Klas 2024

### Scenario 6A: Margin Level Dynamics
- **Setup**: Position `(L, p_a, p_b)` with borrowed capital `(x_D, y_D)`.
- **Value function** (Eq 1):
  ```
  V_pos(P) = L*(2*sqrt(P) - sqrt(p_a) - P/sqrt(p_b))  if p_a < P < p_b
  V_pos(P) = L*(sqrt(p_a_or_p_b)*...*P)                if out of range
  ```
- **Margin level**: `M(P) = (V_pos(P) + x_C*P + y_C) / (x_D*P + y_D)` (Eq 15)
- **Key property**: No local minima in M(P) → in-interval safety (check endpoints only).

### Scenario 6B: Divergence Loss = High-Leverage IL (Section 3.9)
- `DL_relative(P) = V_pos(P)/V_hold(P) - 1` (Eq 42)
- As `V_user → 0` (max leverage): `M(P) → DL(P) + 1`
- **Solidity test**: Create leveraged CL position, verify margin level tracks `DL + 1` as leverage increases.

### Scenario 6C: Price Manipulation Safety (Section 3.8, Eq 35-41)
- Swap changes position value by `DeltaV = L*(sqrt(P) - sqrt(P'))^2 / sqrt(P') > 0`.
- **Key invariant**: Price manipulation *always increases* position value.
- **Solidity test**: Execute arbitrary swaps against a CL pool, verify `V'_pos >= V_pos` always holds.

---

## 7. IL Sensitivity to Volatility and Time (Heston Model)

**Source**: Deng/Zong/Wang, Section 4.1

### Scenario 7A: Heston Model Parameters for Monte Carlo
- `P0 = 10`, `nu_0 = 0.3`, `mu = 0.1`, `rho = -0.3`
- Mean-reversion: `kappa = 0.4`, vol level `theta = 0.4`, vol-of-vol `xi = 0.15`
- Upper range `[11, 14]`, lower range `[6, 9]`, maturity `t = 7 days`.
- **Results** (Table 1):
  - kappa=0.3: E[UIL^R] = -0.424, replication = -0.424, error = 1.03e-5
  - kappa=0.5: E[UIL^R] = -0.439, replication = -0.439, error = 1.02e-5
  - theta=0.3: E[UIL^R] = -0.411, replication = -0.411, error = 1.08e-5
  - theta=0.5: E[UIL^R] = -0.502, replication = -0.502, error = 9.68e-7

### Scenario 7B: IL Increases with Volatility and Time (Figure 1)
- Both E[UIL^R] and E[UIL^L] decline (more negative) as sigma increases from 0.1 to 0.9.
- Both decline as time t increases from 0.02 to 0.16 (years).
- Right-side IL is more sensitive to sigma than left-side IL.

---

## 8. LP Greeks

**Source**: Hookathon Primer, Section 3.2

### Scenario 8A: Full-Range Greeks
```
V_LP  = V_0 * sqrt(alpha)
Delta = V_0 / (2*sqrt(alpha))
Gamma = -V_0 / (4*alpha*sqrt(alpha))
```
- **At alpha=1**: Delta = V0/2 (half exposure), Gamma = -V0/4 (always negative).
- **Solidity test**: Verify `V_LP(P+dP) - V_LP(P) ~ Delta*dP + 0.5*Gamma*dP^2`.

### Scenario 8B: HODL vs LP Greeks
- 50:50 HODL: `V = L*sqrt(P)*(1+alpha)`, Delta = V0/2 = const, Gamma = 0.
- 100% asset: `V = V0*alpha`, Delta = V0 = const, Gamma = 0.
- **LP**: Delta < HODL_delta when price increases, Delta > HODL_delta when price decreases.
- **Gamma always negative** = the LP is always short convexity = IL is always non-positive.

---

## Summary: Concrete Fork Test Matrix

| # | Scenario | Protocol | Key Params | What to Assert |
|---|----------|----------|-----------|----------------|
| 1 | v2 IL at alpha=2 | Uni v2 | P0=1000, 1 ETH + 1000 USDC | IL = -5.72% |
| 2 | v2 IL at alpha=0.5 | Uni v2 | P0=1000 | IL = -5.72% (symmetric) |
| 3 | v3 IL in-range | Uni v3 | p0=2000, [1500,2500], 1M USDT | Units match Eq 33 |
| 4 | v3 IL below range | Uni v3 | p drops to 1500 | All ETH (543,0), funded P&L < 0 |
| 5 | v3 IL above range | Uni v3 | p rises to 2500 | All USDT (0,1052020), funded P&L < 0 |
| 6 | LVR = arb profits | Uni v2 | sigma=50%, simulate path | LVR_T ~ sigma^2/8 * V0 * T |
| 7 | Borrowed IL is quadratic | Uni v2 | p0=2000, test p at 1500,2500,3000 | P&L = -L*sqrt(p0)*(sqrt(p/p0)-1)^2 |
| 8 | Static replication | Uni v2 | k=2000, 8 strikes | Replicated payoff matches 2*sqrt(k*m_T) |
| 9 | Concentrated leverage | Uni v3 | Narrow vs wide range | Narrower → higher IL per dollar |
| 10 | Price manipulation safety | CL + leverage | Arbitrary swaps | V'_pos >= V_pos always |
| 11 | IL with fees breakeven | Uni v2 | mu=5% fee return | LP beats HODL for alpha in ~[0.6, 1.5] |
| 12 | IL protection payoff | Uni v3 | BSM params | PV matches Eq 81 within tolerance |
