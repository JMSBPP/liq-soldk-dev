
# DESCRIPTION
'''
A derivative paying the realized variance of net-remittance (-> filter for arbitrage volume) flows in a corridor which AIMS to provide exposure to (or hedge against) instability of household income driven by cross border transfers
'''

Payoff \propto Var (Net USDT -> FX)


======

Do you have memory updated? Since we are falling back from the open-baking, open-viking approach, since it's not working, do you have everything written on disk on MD files, such that if the conversation gets compacted, a new agent can carry out and get context easily?

======

Use **Mento broker data as the remittance signal** (real users) and **Uniswap v3 pool data for CFMM observables** (price, fees, settlement). These serve different roles in the instrument.

## EXERCISES
 
  Proving this is what open the door for estiumating the demand :
 
 (PRE_REQ)
 '''
 (Net USDT -> FX) ----(predicts/ explain ? (not sure)) > (d household income driven by cross border transfers)
 '''
 
## EXPECTED LONGS
 
 -  LOCAL FINTECHS LENDERS {
            technology: lend to users whose income depend on remittances 
			cost : credit default risk
			relation:  UP (Net USDT -> FX) =>  UP( default risk ) 
			use_case: HEDGING
}

- PAYMENT APPS {
        technology:{
		   - off-ramps into local currency
		   - handling USD inflows
		}
		
		cost: operational stress when flows spike unpredictably
		use_case: HEDGING

}

- LPs{
     cost: d LVR /d volatility of volume > 0
	 use_case: HEDGING
	 
}


## EXPECTED_SHORTS


iff (PRE_REQ) then payoff is EXPECTED to be valuable when 

## EXERCISES
-  (Net USDT -> FX) -> MIGRATION SHOCK: We need to prove that migration shocks predict/cause Var((Net USDT -> FX))

- (Net USDT -> FX) -> RECESSION_LOCAL_COUNTRY
- CAPITAL_CONTROLS/CORRUPTION
- INFLATION_SPIKES


