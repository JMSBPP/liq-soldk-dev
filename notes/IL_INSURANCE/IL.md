Report written to `cfmm-theory/lp-derivatives/notes/IL_LVR_ORACLES_RESEARCH.md`.


**Tier 1 — Direct IL/LVR (sorted by score):**
| Score | Project | Pattern |
|-------|---------|---------|
| 4.20 | Panoptic V2 OraclePack | Internal oracle, production, audited (C4 Dec 2025) |
| 3.85 | Najnomics/LVR-Auction-Hook | V4 hook + EigenLayer AVS — auctions LVR to compensate LPs |
| 3.85 | Tehlikeli107/il-protection-hook | V4 hook — auto IL protection, claims Arbitrum deployment |
| 3.35 | LVR Shielded LP (ETHGlobal) | V4 hook + vault — hysteresis, dwell windows |
| 3.10 | artistic709/ImpermanentGain | **"The antiparticle of IL"** — someone already built the long-IL instrument |

**Tier 2 — Vol/Fee Oracles:**
| Score | Project | What it gives you |
|-------|---------|-------------------|
| 3.70 | scab24/univ4-risk-neutral-hook | Risk-neutral pricing + vol oracle in a V4 hook |
| 3.55 | valorem-labs-inc/oracles | On-chain greeks, realized vol, IV, Black-Scholes |
| 3.45 | aloelabs/aloe-ii | Audited IV estimation from Uni V3 tick data |

**The 4 gaps nobody has built yet** (your opportunity):
1. Standalone composable LVR oracle (everything is monolithic or PoC)
2. On-chain fee-implied-vol oracle (Bichuch & Feinstein paper — novel)
3. CI-option replicating portfolio (Fateh Singh paper — LVR = theta)
4. Panoptic oracle extracted as a standalone hook primitive

=======================================================================================================

For path-dependant metrics Algebra has good oracle design patterns on their volatility oracle



| Canonical type | Crypto manifestations |
|---|---|
| **Interest** | Lending yield (Aave/Compound), liquid staking (stETH, rETH), vault shares (ERC-4626) |
| **Dividends** | Protocol fee distributions, staking rewards (discrete), **airdrops** (one-shot dividends) |
| **Convenience yield** | Governance voting rights, gas token utility, collateral eligibility, access/membership tokens |
| **Storage cost** (negative) | Gas costs for rebasing tokens, maintenance transactions, renewal fees (ENS) |


[il, i*] U [i*, iu] 
   
   |
    -----> (lx , ly, l = Agg(lx,ly) )

Assuming T_1 is unit of account since P_{T_1/T_0} by default:

for every price update (event-driven) A position tracks it's impermanent loss per unit of liquidity  as:

( IL/ D L ) : [unitOfAccount] / [liquidity]

Position{
	// Right-side provision [P0, Pu]: LP deposits only ((token0 ) the volatile asset)
	// replicated by a portfolio of CALLS with strikes in [Pl, Pu]
	
	// right slot (low 128 bits)  = token0 amounts  ←→  UIL^R (call-replicable)
	int256 RightIlPerLiq(priceRange) = 2 * sqrtP_t - FullMath.mulDiv(sqrtP_t, sqrtP_t, sqrtP_l) - sqrtP_l;
     // Left-side provision [Pl, P0]: LP deposits only token1 (the numeraire). 
	 // replicated by a portfolio of PUTS with strikes in [pl, pu].
     
	 // left slot  (high 128 bits) = token1 amounts  ←→  UIL^L (put-replicable)
     int256 LeftIlPerLiq(priceRange) = ...


=====> PANOPTIC CONNECTION LeftRight

 (1) RiskEngine.sol:1066-1067

--> shortPremia: right slot = token0 credit, left slot = token1 credit

--> longPremia:  right slot = token0 debit,  left slot = token1 debit

(2) FeesCalc.sol:65-66

--> .addToRightSlot(int128(int256(Math.mulDiv128(ammFeesPerLiqToken0X128, liquidity))))
--> .addToLeftSlot(int128(int256(Math.mulDiv128(ammFeesPerLiqToken1X128, liquidity))))
}
                                                                                                                                                                                       
==>   LeftRightSigned premia value <------------>  (RightIlPerLiq, LeftIlPerLiq)   <===
 
 
 (3) Risk Assymetry -> CollateralTrackers
 
 vega(RightIlPerLiq) > vega(LeftIlPerLiq)     
                                             
 theta(RightIlPerLiq) > theta(LeftIlPerLiq)              
     
A single collateral pool couldn't properly margin these asymmetric risks — you need independent margin for the call-replicable component (token0) vs. the put-replicable component
   (token1)                                                  
                                         
  ┌────────────────────────────────────────┬────────────────────────────────────────────────────────────┐                                                                               
  │             Paper Concept              │                       Panoptic Code                        │
  ├────────────────────────────────────────┼────────────────────────────────────────────────────────────┤                                                                               
  │ UIL^R (right-side IL, call-replicated) │ rightSlot() = token0 amounts                               │
  ├────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ UIL^L (left-side IL, put-replicated)   │ leftSlot() = token1 amounts                                │                                                                               
  ├────────────────────────────────────────┼────────────────────────────────────────────────────────────┤                                                                               
  │ Independent decomposition at P0        │ Bitmask overflow isolation in addToRightSlot/addToLeftSlot │                                                                               
  ├────────────────────────────────────────┼────────────────────────────────────────────────────────────┤                                                                               
  │ Same underlying price process          │ addCapped freezes both slots together                      │
  ├────────────────────────────────────────┼────────────────────────────────────────────────────────────┤                                                                               
  │ (·)+ option payoff floors              │ subRect rectifies to zero                                  │
  ├────────────────────────────────────────┼────────────────────────────────────────────────────────────┤                                                                               
  │ Asymmetric risk profiles (10-20x)      │ Two separate CollateralTracker contracts                   │
  └────────────────────────────────────────┴────────────────────────────────────────────────────────────┘                                                                               



gamma(lpPosition) = K^(-3/2) dK


gamma of the √price payoff 

how many vanilla options at each strike K you need in the replicating portfolio.                         

(RightIlPerLiq, LeftIlPerLiq) = il(lpPosition);

to hedge the IL of an LP position using vanilla options

for (tick in lpPosition){
	mint (amount: d tick * tick^(-3/2), strike: tick)
}
                                                                                                           
																										   lpPosition <--> optionLeg
                                                                                                          premium_base = collected_fees * totalLiquidity / netLiquidity²
                                           l^{4/2 - 2/2}                                                   This is raw fee revenue divided by liquidity², tracked per-token in LeftRight slots. 
                                                                                                           Uniswap's feeGrowthInsideX128 already embeds the √price structure.
  The fee accumulation is feeGrowthX128 * liquidity
  liquidity for token0 is defined as amount0 * √(upper) * √(lower) / (√(upper) - √(lower)) (line 369).
  The √price is baked into the liquidity calculation, not into the premia accounting.                                                      
  3. The asset parameter (lines 383-385) handles the numeraire choice: asset=0 means 1 unit of token0 moves at strike K, asset=1 means K units of token1 move. This is where Panoptic
  accounts for the price-dependent sizing that the K^(-3/2) handles in the continuous replication.                                                                                      
                                                                                                           Scenario 1: Computing the theoretical IL of a Panoptic position                                                                                                                       
  The raw LeftRight values give you (collected_token0, collected_token1). To convert these to the paper's UIL framework, you'd weight by the tick-to-price mapping: K = 1.0001^tick, so 
  K^(-3/2) = 1.0001^(-3tick/2).                                                                                                                                                                                                                                                                  
  Summary                                                    
                                                                                                                                                                                        
  ┌──────────────────┬────────────────────────────────────────────┬────────────────────────────────────┐                                                                                
  │                  │             Panoptic on-chain              │      Static replication paper      │
  ├──────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤                                                                                
  │ Primitive        │ Single LP position = one option            │ Portfolio of vanilla C(K), P(K)    │
  ├──────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤
  │ Weighting        │ Raw token amounts, no K^(-3/2)             │ K^(-3/2) dK per strike             │                                                                                
  ├──────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤                                                                                
  │ √price structure │ Embedded in Uniswap's liquidity formula    │ Explicit via Carr-Madan on f(x)=√x │                                                                                
  ├──────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤                                                                                
  │ Purpose          │ Track premia/fees between longs and shorts │ Hedge IL with external instruments │
  └──────────────────┴────────────────────────────────────────────┴────────────────────────────────────┘                                                                                
 
