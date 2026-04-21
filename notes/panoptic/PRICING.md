
| Dimension | Voltaire | Panoptic |
|---|---|---|
| **Premium timing** | Upfront (BS at mint) | Streaming (fee accumulation) |
| **Vol assumption** | Implied vol input to BS | No vol input -- realized vol *is* the premium |
| **Vol oracle needed** | Yes (Algebra TWAP or fallback) | No |
| **Risk-free rate** | Hardcoded 5% in BlackScholes.sol | None -- no discounting needed |
| **Writer risk** | Fixed premium received, bears exercise risk | Earns fees continuously, bears "removed liquidity" risk |
| **Expiry** | Fixed (European) | Perpetual (no expiry) |
| **Settlement** | Reactive Network cron at expiry | Continuous via premium accumulators |
| **Convergence to BS** | Exact by construction | Converges when sigma_realized ~ sigma_implied |
| **Spread control** | protocolFeeBps | VEGOID parameter |


# BLACK-SCHOLES

`lib/voltaire/src/OptionHookV2.sol:274` computes premium upfront:

```solidity

========BLACK-SCHOLES-PRICING =============== 
|    `lib/voltaire/src/OptionHookV2.sol:274` |
|                                            |
|			   |                             |
|			   V                             |
|   unitPremium = BlackScholes.price(        |
|                                    spot,   |
|                                    strike, |
|                                    tte,    |
|									 vol,    |
|									 isCall  |
|   );                                       |
|   totalPremium = unitPremium * quantity    |
|                                            | 
|    -> lock (writerCollateral)              |
 ============================================
            
```
                 |
                 |
   C (P,K, T, vol)


# FEE_ACCUMULATION_STREAM

```
lockCollateral (strike) ----> addLiquidity(tick)                 -------> buyOption(strike, size)
                                      |                          
                                      v                         | 
								  -----------    L (tick)	    |
								 |    l_1     |                 | 
								 |  ------    |                 |
								 |	  l_2     |                 |
								 |  ------    |  ---------(burnLiquidity(tick))-----
                                 |    ...     |                                    / |
 					    ---->	 |  ------    |                                   /  |
                       |          --------------                                 /   | 
        V(tick)        |              (tick)                           ----------   
		               |                                              |              v  
					   |                                              |  
    -----------        |                                              |            
--- (swap x fee) -------      fee: swap -> liquidity            premiumBase      
     -----------                                                    =
	                                                            collected       
	                                                            * totalLiquidity 
																/ netLiquidity^2    (size)             
    -----------																     ----------
    |    s_1    |                                                               | ------- | 
    | --------- |                                                               |   ...   |
    |    s_2    |                                                               |  ------ |
    |  -------  |                                                               |   l_k   |
    |    ...    |                                                                ---------
    |   -----   |
   ---------------                                                     \          /
        (tick)

          |
    Uniswap swap crosses tick range
    -> feeGrowthGlobal increments
        -> SFPM._updateStoredPremia() called on next touch                
                                                                          (premiumOwed)
						                                   premium_base * (net + removed/VEGOID) / total		    												
						|                                                                  |
						v                                                                  |
		                                                                /                  | 
																	   /
                                                                    <- 
                getPremiaDeltas` (`SemiFungiblePositionManager.sol:1262`) 																	   
                                    |
									v
                -> s_accountPremiumOwed[positionKey] += deltaOwed
                -> s_accountPremiumGross[positionKey] += deltaGross
				
				                     |
									 v
                    -> PanopticPool reads delta via s_grossPremiumLast
                        -> CollateralTracker settles premium transfers

                                                                                           |
																						   |
					VEGA MULTIPLIER	                                 																   
             -----------------------------------------																				 
---> premium spread between what longs pay and shorts earn		<--------------------						

Higher VEGOID compresses the spread (longs pay less relative to what shorts earn). Lower VEGOID widens it
This replaces the bid-ask spread that a traditional options market maker would charge.



vol_implied = sqrt(2 * fee_rate * range_width / (S^2 * L))
```


# BLACK-SCHOLES  == FEE_ACCUMULATION_STREAM


For a concentrated LP position in range `[K-d, K+d]`, the instantaneous fee income per unit time equals:


```                                 
    ---------------------------------LOCAL  ----------------------------------------- 
                 
 |                          FEE_ACCUMULATION_STREAM                                  |
							 
    d Fee/dt ([strike - d, strike + d ])  = (vol * price^2 * L) / (2 * range_width)
                                          |
										  |
										  
                                THETA(BLACK_SCHOLES)
								
      Theta_BS = -(price * vol * N'(d1)) / (2*sqrt(T)) - r * K * e^(-rT) * N(d2)
								
 |                                                                                   |
  -----------------------------------------------------------------------------------
                                     | |
									 | |
									 | |
									  v
	----------------------------- GLOBAL---------------------------------------------
  |								
  
  
  
               integral_0^T fee_rate(t) dt  --
			                                  |
											  |
											  v
	                             
								 
	      premium(  BlackScholes,     vol_implied = sqrt(2 * fee_rate * range_width / (S^2 * L)))
		                                    
											| |
											 
                                integral_0^T [ vol_realized^2 * S(t)^2 * L ] / (2 * width) dt 
  
  
  |
       premium(BlackScholes) - premium(FeeAccumulationStram) -> vol risk premia
	                                                                  |
																	  v
															vol_realized != vol_implied.		  
   ------------------------------------------------------------------------------


```


## Convergence Conditions

The convergence holds under:
- **Realized vol ~ implied vol** -- if the pool trades at the volatility the BS model assumes, cumulative fees = BS price
- **Continuous trading** -- fees accrue per swap; the more swaps crossing the range, the better the approximation
- **Narrow tick range** -- a single-tick LP position replicates a near-ATM option; wider ranges replicate a spread



1. **Define strike** = tick range center
2. **Define notional** = liquidity amount deployed
3. **Premium accrued** = `s_accountPremiumOwed` delta between two timestamps
4. **Implied vol extraction** = invert the fee-rate formula:

- The Uniswap pool where USDC/DAI/AMPL trade is simultaneously the **settlement venue** and the **pricing oracle** for any option-like instrument
- No need for an external vol surface or BS computation
- The premium a hedger pays is exactly what the market reveals through trading activity
- VEGOID-style parameters let us tune the spread for different risk profiles (e.g., tighter for liquid pairs, wider for exotic macro hedges)


## Source References

- `lib/voltaire/src/BlackScholes.sol` -- Full BS implementation
- `lib/voltaire/src/OptionHookV2.sol:274` -- BS pricing at mint
- `lib/2025-12-panoptic/contracts/SemiFungiblePositionManager.sol:1262` -- `_getPremiaDeltas`
- `lib/2025-12-panoptic/contracts/PanopticPool.sol:197` -- `s_grossPremiumLast` accumulator
- `lib/2025-12-panoptic/out.txt` -- Full trace of ITMShortPutShortCall_Swap test
- Panoptic whitepaper: https://paper.panoptic.xyz/
- Desmos visualization of premia spread equations: https://www.desmos.com/calculator/mdeqob2m04
