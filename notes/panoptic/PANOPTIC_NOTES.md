```
V(p) = L · (√p - √pₗ)     [token1 terms, for pₗ ≤ p ≤ pᵤ]
(effective strike)
K = √(pₗ · pᵤ) = √(p*)    [geometric mean in √price space]


tickSpacing -> 0
payoff_LP(p) ≈ -|√p - √(p*)|     [short straddle on √price]
payoff_LONG(p) ≈ +|√p - √(p*)|    [long straddle on √price]

  value
    ∧
   / \                  --> addLiqudity --> SellOption --> isLong =0 
  /   \
 /     \
─────────── price
   pₗ p* pᵤ                       _createLegInAMM::SFPM:955-1020
 
	                       isLong == 0 (SHORT / selling option):
                             updatedLiquidity = startingLiquidity + chunkLiquidity   // ADD to AMM
                             → _mintLiquidity(chunk, pool)                           
                             → moved = LeftRightSigned{token0 moved, token1 moved}   


    |
	| panoptic(`isLong=1`)
	|
	v

  value
 \     /
  \   /               --> removeLiqudity --> BuyOption --> isLong =1
   \ /
─────────── price
   pₗ p* pᵤ

                                 _createLegInAMM::SFPM:955-1020
X 
	                         isLong == 1 (LONG / buying option):
							 updatedLiquidity = startingLiquidity - chunkLiquidity   // REMOVE from AMM
							 removedLiquidity += chunkLiquidity                       // track R
						      → _burnLiquidity(chunk, pool)                         
                              → moved = LeftRightSigned{token0 moved, token1 moved}   

`PanopticPool.sol:2062`:

```solidity
// for longs, negate: short premium becomes long premium
if (isLong == 1) {
    premiaByLeg[leg] = LeftRightSigned.wrap(0).sub(premiaByLeg[leg]);
}
```

           FeeRevenue (liquidityPosition)  ---> premiaShortEarns --> LeftRightUnsigned
                                                       |                      | 
 					   |                               v                      |  
					   v                        `s_accountLiquidity`          |
   `(netLiquidity (in AMM) + removedLiquidity(bought by longs) )`             |
                                                                              |
                                                                              |
                                                                            /   \ 
                                                                           /     \

                                                                RIGHT (token0)    LEFT (token1)
                                                                       ( premium)
																	   
																	   /       \
																	  /         \
                                                 s_accountPremiumOwed		s_accountPremiumGross															    (by longs)                 (by shorts)
																	  


A TokenId with multiple active legs composes option strategies:

| Strategy | Leg 0 | Leg 1 | riskPartner |
|---|---|---|---|
| **Naked put** | short, tokenType=0 | — | self |
| **Covered call** | short, tokenType=1 | — | self |
| **Bull call spread** | short call (isLong=0) | long call (isLong=1) | mutual (0↔1) |
| **Iron condor** | 4 legs, alternating long/short | | paired |

### 2. TokenId: The Multi-Leg Option Position

User: "I want to sell a put at strike 2000 USDC/ETH, width 10"

```
								 
								 |
							`TokenId` (uint256)` 
							     |
                         `TokenId.sol:17-46`:

       /              /         |        \            \                 \        \

  asset(1)  optionRatio(7)  isLong(1)  tokenType(1)  riskPartner(2)  strike(24)  width(12)

   |                |               |              |              |           |             |
   |				|			    |              |              |           |             |
 	            (CONTRACT                         LEGS
			      SIZE)           (SHORT/LONG) (CALL/PUT)       (MARGIN)      (STRIKE)     (EXPIRY)
   |
   |
   
  (UNDERLYING) 


    --> isLong=0, tokenType=0 (put→token0), strike=2000, width=10, optionRatio=1 <--

  (*) riskPartner × tokenType × isLong → Collateral Strategy

  (*) width x strike <->  [tickLower, tickUpper]



```

### Step-by-step call chain:

```

1. PanopticPool.mintOptions(tokenId, positionSize, ...)
   │
   ├─ 2. tokenId.validate()          ← TokenId.sol: checks legs valid, no gaps, no duplicate chunks
   │
   ├─ 3. SFPM.mintTokenizedPosition(tokenId, positionSize, ...)
   │     │                            ← SemiFungiblePositionManager.sol:586
   │     │
   │     └─ 4. _createPositionInAMM(univ3pool, tokenId, positionSize, isBurn=false)
   │           │                      ← SFPM:795
   │           │
   │           │  For each leg (up to 4):
   │           │
   │           ├─ 5. PanopticMath.getAmountsMoved(tokenId, positionSize, leg)
   │           │     └─ Converts positionSize → LiquidityChunk(tickLower, tickUpper, liquidity)
   │           │
   │           ├─ 6. _createLegInAMM(pool, tokenId, leg, liquidityChunk, isBurn=false)
   │           │     │                ← SFPM:921
   │           │     │
   │           │     ├─ isLong = tokenId.isLong(leg)  →  returns 0 (SHORT)
   │           │     │
   │           │     ├─ 7. updatedLiquidity = startingLiquidity + chunkLiquidity
   │           │     │     └─ s_accountLiquidity[positionKey].rightSlot += chunk  (net grows)
   │           │     │
   │           │     ├─ 8. _mintLiquidity(liquidityChunk, univ3pool)
   │           │     │     │              ← SFPM:1018-1019 (isLong==0 branch)
   │           │     │     │
   │           │     │     └─ univ3pool.mint(address(this), tickLower, tickUpper, liquidity, "")
   │           │     │        └─ Uniswap callback → transfers token0+token1 FROM user TO pool
   │           │     │
   │           │     │  Returns: moved = LeftRightSigned{token0 deposited, token1 deposited}
   │           │     │
   │           │     ├─ 9. _collectAndWritePositionData(...)  [if prior liquidity existed]
   │           │     │     ├─ pool.collect() → collects accumulated fees
   │           │     │     └─ _getPremiaDeltas(currentLiquidity, collected, vegoid)
   │           │     │           ├─ deltaPremiumOwed  → LeftRightUnsigned (longs will owe this)
   │           │     │           └─ deltaPremiumGross → LeftRightUnsigned (shorts earn this)
   │           │     │
   │           │     └─ 10. s_accountFeesBase[positionKey] = _getFeesBase(...)
   │           │           └─ Snapshots current feeGrowthInsideLastX128 * liquidity
   │           │
   │           └─ totalMoved += movedLeg  (LeftRightSigned, accumulates across legs)
   │
   ├─ 11. _validateAndForceExercise(...)  ← PanopticPool checks collateral
   │       ├─ CollateralTracker.takeCommissionAddData(...)  → deducts commission
   │       └─ CollateralTracker.checkCollateral(...)        → ensures sufficient margin
   │
   └─ 12. Mint ERC1155 token: SFPM mints tokenId to user as position receipt

`PanopticPool.t.sol:4036-4227`.

When you mint a 2-leg ITM short strangle (short put + short call, both ITM), the protocol correctly executes an internal swap to rebalance the token surplus, deducts commission, and tracks all amounts through the `LeftRightSigned` pipeline.

```

| Layer | What | Type |
|---|---|---|
| **Uniswap** | Liquidity added to `[tickLower, tickUpper]` | `pool.mint()` |


| **SFPM storage** | `s_accountLiquidity[key].rightSlot` increased | `LeftRightUnsigned` |
| **SFPM storage** | `s_accountFeesBase[key]` snapshotted | `LeftRightSigned` |
| **SFPM storage** | `s_accountPremiumGross[key]` starts accumulating | `LeftRightUnsigned` |

| **PanopticPool** | `s_options[user][tokenId][leg]` = premium snapshot | `LeftRightUnsigned` |

| **CollateralTracker** | Margin locked, commission taken | |

| **ERC1155** | User holds `tokenId` representing the position | |


Question: 
 How we can leverage bunni-v2 code to build custom adapters (bridges) betwee ALgebra AND  Panoptic
for bootstrapping liquidty by borrowing


# EXERCISES

## STRADDLE -> LPing


```
Helpers {
     lib/2025-12-panoptic/test/foundry/coreV3/RiskEngine/helpers/PositionFactory.sol,
     lib/2025-12-panoptic/test/foundry/core/Misc.t.sol::L1777    
}

Flow {
    PanopticPool.ITMShortPutShortCall == UniswapV4.addLiquidity
               |
               v
         --> liquidityPosition --> IL(position)

}
```

### Questions:

(1)  What is the formal definition of a straddle ?

[](../){
	Straddle(isLong){
		strike::Strike
		ratioSpread::optionRatio[2]
	}
}
(2) How it relates or maps to a vanilla CLAMM liquidity position ?

CLAMM{ 
        amountXOnL = L ( (\sqrt(p_u) - \sqrt(p_l) )/ \sqrt(p_l*p_u))
                      --- ----------(amountYOnL)-----------------

	    SOLVENCY:: \sqrt(p_l*p_u))* amountXOnL = L ( (\sqrt(p_u) - \sqrt(p_l) )
}

CoveredCall(isLong) {
	not(isLong) => p - max(p - k, 0) ==(clamm)=> p - max(p - \sqrt(p_l*p_u), 0)
}

CashSecuredPut(isLong){
   not(isLong) => k - max(k-p, 0) == (clamm) => \sqrt(p_l*p_u) - max(\sqrt(p_l*p_u) - p ,0)
}


CLAMM(\sqrt(p_l*p_u), p) - CoveredCall(\sqrt(p_l*p_u), p, expiration*) = RangePayoff([p_l, p_u], p,expiration*)
                                                                            
                                                                                        |
																			[MORE_ON](~/apps/liq-soldk-dev/src/libraries/TickRangeExpirationLib.sol)			
                                                                       \sqrt(p_u/p_l) --   
                                                                              |
																		      |
												expiration(\sqrt(p_u/p_l))<---			 
                                                            |
															|
							   						-------		
                   (2\pi/vol^2)(\sqrt(\sqrt(p_u/p_l)) -1 /\sqrt(\sqrt(p_u/p_l)) +1 )^2
				   
				                                   |
												   |
					sqrt(p_u/p_l) 
					    (expiration*,expiration) = (1 + vol\sqrt(expiration* - expiration/2\pi )
					                             (                                               )^2
												   /(1- vol \sqrt(expiration* - expiration)/2\pi)							   
                                    
//--> TEST INVARIANT

---> CALL^{ATM} (\sqrt(p_u*p_l), expiration* - expiration) = PUT^{ATM} (\sqrt(p_u*p_l)) < ----

OPEN QUESTIONS:

(R2Q1)  How `RangePayoff([p_l, p_u], p)` maps to [RANGE_ACCRUAL_NOTES](~/learning/cfmm-theory/lp-derivatives/pap-pricing_range_accrual-msc_thesis.pdf) ?


RangePayoff([p_l, p_u], p, optionExpiration*)
                              
				|			   |
				|			   |
				 \              \ 
 				   ------[conversion](~/apps/liq-soldk-dev/src/libraries/TickRangeExpirationLib.sol)
				                
                                |
								-------- > lpExpiration
                                              
											  |
											   \
	            RangeAccrualNote(coupon ,observationPeriods)		  
                                   |
								   | (from the feeRevnue ~ stremia for shorting the straddle)
								      the LP can decide to sell a range accrual note subject 
									  to the collateral his premia entails, this can be a primitive
									  for a standarized [income settle deriuvative on LPs](./INCOME_SETTLEMENT.md))
								   |
								   |
								   
								   
								  

(1) -> (3) What is the approach following [this approach](~/learning/cfmm-theory/refs/MLFiPaper.pdf)to define an [`straddleBuilder`](~/apps/liq-soldk-dev/src/interfaces/IStraddleBuilder.sol) interface ?


(2) ^ (3) -> How to bridge (3) to other protocols (e.g Panoptic, Algebra (CLAMM), etc) 
