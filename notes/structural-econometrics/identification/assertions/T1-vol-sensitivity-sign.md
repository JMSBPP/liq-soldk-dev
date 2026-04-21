# Assertion T1: Dynamic Fee Creates Positive Vol-Sensitivity of LP Revenue

## Mathematical Statement

Let R_i(t) denote fee revenue for pool i at time t, and sigma(t) denote realized volatility.

Define:
- Pool A (Algebra): phi_A(t) = g(sigma(t)) where g is increasing (double-sigmoid with positive slope in relevant domain)
- Pool U (Uniswap): phi_U = phi-bar (constant)

Fee revenue is: R_i(t) = phi_i(t) * V_i(t) where V_i(t) is swap volume.

Claim: Under the assumption that V_A(t) and V_U(t) respond symmetrically to sigma(t) (common volume effect), and g is increasing in sigma:

dR_A/d(sigma) - dR_U/d(sigma) > 0

Proof sketch:
- dR_A/d(sigma) = g'(sigma) * V_A + g(sigma) * dV_A/d(sigma)
- dR_U/d(sigma) = phi-bar * dV_U/d(sigma)
- If V_A ~ V_U and dV_A/d(sigma) ~ dV_U/d(sigma) (symmetric volume response):
  dR_A/d(sigma) - dR_U/d(sigma) = g'(sigma) * V_A + (g(sigma) - phi-bar) * dV/d(sigma)
- The first term g'(sigma) * V_A > 0 since g is increasing and V > 0
- The second term sign depends on whether g(sigma) > phi-bar and the sign of dV/d(sigma)

## Conditions for the assertion to hold
1. g'(sigma) > 0 (Algebra's adaptive fee is increasing in volatility) -- verifiable from contract code
2. V_A > 0 (non-zero volume) -- empirical condition
3. Either (g(sigma) - phi-bar) * dV/d(sigma) >= 0, or |g'(sigma) * V_A| > |(g(sigma) - phi-bar) * dV/d(sigma)|

## Formalize
The core mathematical claim to verify: Given g: R+ -> R+ is increasing and differentiable, V > 0, and phi-bar > 0 is constant:

g'(sigma) * V + g(sigma) * (dV/d_sigma) - phi-bar * (dV/d_sigma) > 0

when g'(sigma) * V > |g(sigma) - phi-bar| * |dV/d_sigma|
