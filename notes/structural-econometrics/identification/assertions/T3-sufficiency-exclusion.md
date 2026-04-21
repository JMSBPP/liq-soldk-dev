# Assertion T3: Dynamic Fee as Sufficient Statistic for Volatility

## Mathematical Statement

Let phi(t) = g(sigma(t-1), sigma(t-2), ..., sigma(t-k)) be the Algebra adaptive fee, where g is the known double-sigmoid function applied to the volatility accumulator.

Let R(t) = phi(t) * V(t) be fee revenue where V(t) is volume.

Claim: If V(t) is independent of sigma(t) conditional on phi(t), then phi(t) is a sufficient statistic for sigma(t) in the fee revenue equation.

Formally: If V(t) _||_ sigma(t) | phi(t), then:

E[R(t) | phi(t), sigma(t)] = E[R(t) | phi(t)]

Proof:
R(t) = phi(t) * V(t)
E[R(t) | phi(t), sigma(t)] = phi(t) * E[V(t) | phi(t), sigma(t)]
                            = phi(t) * E[V(t) | phi(t)]  (by conditional independence)
                            = E[R(t) | phi(t)]

## Conditions
1. g is a known deterministic function (verifiable from AdaptiveFee.sol)
2. V(t) _||_ sigma(t) | phi(t) -- this is the key economic assumption
   - Violation: if traders observe sigma(t) directly and adjust volume beyond what phi(t) captures
   - Violation: if sigma(t) measures something different from Algebra's internal volatility accumulator

## Formalize
The core claim: For a deterministic function g and random variables R, V, sigma, phi where R = phi * V and phi = g(sigma):

(V _||_ sigma | phi) ==> E[R | phi, sigma] = E[R | phi]
