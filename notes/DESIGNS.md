[Channel A — Swap Fee/IL (Panoptic)](./panoptic/**){
   - Swaps flow through concentrated liquidity → fees = premium
   - IL = payout. Requires organic swap volume.
}

[Channel B — Rebalancing (Bunni V2)](./bunni/**){
	- LDF defines target portfolio composition at every price. 
	- Rebalancer trades via FloodPlain to maintain the distribution. 
	- The rebalancing pattern IS the option:{
		- Selling rallie
		- buying dips (around LDF center)
		-**constant-mix strategy** = **short straddle** (Perold & Sharpe 1988)
		
	}
	
	- Premium = rebalancing profit (mean-revert regime)
    - Payout = rebalancing loss (trending regime) 
} 

[Channel C — Dynamic Fee (Algebra)](./SIGMOID_VARIANCE_SWAP/**){
	- Standard concentrated liquidity with vol-adjusted premium
	- 
}

## The Bridge

**Concentrated liquidity IS a rebalancing rule, and rebalancing rules ARE options.**

Uniswap V3 automates the rebalancing through the AMM formula — each swap that crosses the range forces a trade. Bunni V2 separates the rebalancing into explicit FloodPlain orders governed by the LDF. Both produce the same payoff shape through different execution channels.

The key equation: for any LDF `f(tick)`, the position value is `V(S_T) = V₀ + ∫Δ(S,f)dS + friction`, where `Δ(S,f)` is the density-weighted delta. A GeometricDistribution LDF produces the delta profile of a short straddle.

## Design Implication

For pairs WITHOUT organic volume (like cCOP/cUSD), Channel B (Bunni V2's rebalancing) is the only viable path — the option payoff tracks an external oracle price without needing in-pool swap volume. This is actually better suited for your macro hedging use case.

The full analysis is at `results/architecture_discovery.md`. This is the Gate A finding — it reframes the entire research from "do positions look like straddles" to "these architectures write options through three distinct channels that converge on the same payoff shape."
