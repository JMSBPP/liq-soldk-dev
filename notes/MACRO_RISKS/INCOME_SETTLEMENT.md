
# Income Settlement

## Evidendce/ Methodology / Preliminaries

----> estimates(returns(TimeSeries(GDP))) == estimates(returns(TimeSeries(stockMarket))) < ----
                            
- estimates(returns(TimeSeries(stockMarket ~ S&P500)) -----> HAS HEDGING MARKET							
- estimates(returns(TimeSeries(GDP))) ------> HAS NOT HEDGING MARKET							


risk (TimeSeries(GDP)) := {
	'''
	fluctuations in market present values of long streams of aggregate income flows
	'''
}

===============================================
GDP = (corportateDividends)   +   (other)
          (~ 3%)                  (~ 97%) 
	    (hedgeable)            (non-hedgeable)
===============================================
                                 (other)
								 
								    |
	                           /        \ 
							  /          \ 
							 /      |      \
						(labor)	    |     (real-state)
                                    |
	                         (unincorporated
							  businesses)

### Requirements
- price(IncomeFlow) => {
  
  require(payoff(IncomeInstrument, to = LONG ) \propto measure(Income))
                              &&
  require(pay(from = SHORTS, payoff(IncomeInstrument, to = LONG)))
  {
  
	FUNDING_RATE:: > 0 => (LONGS PAY CAPITAL LOSS TO SHORTS)? < 0 => (SHORTS PAY CAPITAL GAINS TO LONGS)     '''
	in cfmm's LP's are both long are shorts LONG before the mid tick and SHORT after the mid tick
	
	'''
  }  
}

### SETTLEMENT

PerpetualFutures(IncomeFlow){
	incomeIndex ::TimeSeries<Index>
	settle( assetPrice:TimeSeries)::{
		'''
		Excess return from t-1 to t between an asset that pays dividend incomeIndex and
		an alternative asset that pays the return(assetPrice)
		
		'''
	   diff(price(timestamp),1) + 
	   diff(incomeIndex(timestamp), prod(return(assetPrice)),price(timestamp,1)
	
	
	}
}


### ECONOMETRIC_METHODS_QUESTIONS


#### **IncomeSettledFutures<IncomeClaims>**

(-) How much short-run variability would there be in income present values that would cause
price volatility in perpetual income futures markets

d (price(PerpetualFutures(IncomeFlow))) = d(incomeIndex)


Why? -> ( volatility(price(PerpetualFutures(IncomeFlow)))<-> interest(PerpetualFutures(IncomeFLow)) )
    
	-> If incomes were smooth -> extrapolation would good estimate future levels -> no perpetuals market
	                      -> incomes would not carry information -> they would not be valuable 
						                                                    -> not tradeable
	CaveatsOnCFMM{
		LP income is proportional to trading volume which is NOT smooth 
	}
	
	

// note: Why this question ?
To what is extent is the `incomeIndex` forecastable ? {

	incomeIndex =      E [futureIncome]          +                error
                      ----------------                            -----
				   (forecastable component)               (unforecastable shock)

                            |                                       |
	                (level -> pricingKernel)           (volatility -> tradability)
}

ln (incomeIndex) = lag(incomeIndex,1) - ln(price(asset))

if constant(discountFactor(incomeIndex)) {
	return(perpetualFutures)  = ln (incomeIndex) - lag(ln(incomeIndex),1) + diff(incomeIndex)
     => var(return(perpetualFutures)) = prod((1- discountFactor(incomeIndex)),var(diff(ln (incomeIndex), \delta*))
}

what is the term [\delta* -> PG18](~/apps/liq-soldk-dev/refs/macro-risk/shiller-aggregate-income-risks-hedging-1993.pdf) , 
 --> [CLAIM from PG18](~/apps/liq-soldk-dev/refs/macro-risk/shiller-aggregate-income-risks-hedging-1993.pdf) {
	'''
	It will be difficult to estimate how much of the variability of \delta* is forecastable becuase series is expected to be dominated by long-term or low-frequency movements, not enough degrees of freedom
	'''
 }

	CaveatsOnCFMM{
		LP income is observable
	}



```
On-Chain Income Observables {

    // Protocol-level income (accrues to LPs/stakers)
    LP_Fee_Revenue {
        source    :: pool.feeGrowthGlobal{0,1}    // Uniswap v3
        granularity :: per-tick, per-position, per-block
        queryable :: yes, fully on-chain
        example   :: "USDC fees earned by cNGN/USDC LPs in epoch t"
    }
	   ....
}

Span(IncomeInstrument) {

    // 1. INCOME FLOOR (put on income stream)
    // "Pay me if my LP fee revenue drops below X"
    IncomeFloor {
        underlying :: cumulative_fees(pool, epoch)
        strike     :: minimum_acceptable_income
        payoff     :: max(0, strike - realized_income)
        analog     :: interest rate floor
    }
    
    // 2. INCOME SWAP (exchange variable for fixed)
    // "I give you my variable LP fees, you give me fixed rate"
    IncomeSwap {
        leg_A :: realized_fees(pool, epoch)       // variable
        leg_B :: fixed_rate × notional             // fixed
        payoff :: leg_B - leg_A  (for fixed receiver)
        analog :: interest rate swap
    }
    
    // 3. INCOME CAP (call on income stream)
    // "Pay me the excess if fees exceed X" 
    // (useful for protocol treasuries capping LP rewards)
    IncomeCap {
        underlying :: cumulative_fees(pool, epoch)
        strike     :: cap_level
        payoff     :: max(0, realized_income - strike)
        analog     :: interest rate cap
    }
    
    // 4. RELATIVE INCOME (cross-protocol spread)
    // "Pay me if Aave USDC yield drops below Compound USDC yield"
    RelativeIncome {
        underlying :: income_A - income_B
        strike     :: spread_threshold
        payoff     :: f(spread vs. threshold)
        analog     :: basis swap
    }
    
    // 5. INCOME SWAPTION (option to enter income swap)
    // "Give me the right to lock in fixed income next epoch"
    IncomeSwaption {
        underlying :: IncomeSwap(future_epoch)
        strike     :: fixed_rate
        payoff     :: optionality on the swap
        analog     :: swaption
    }
    
    // 6. INCOME PERPETUAL (Shiller's construct, directly)
    // Perpetual claim on rolling income stream

	IncomePerpetual(cNGN_USDC_pool) {

	     index_value :: cumulative_fee_revenue(pool, trailing_30d)
    
          // Dividend: realized income distribution
        dividend(t) :: fee_revenue(t-1, t) / total_long_notional
        direction   :: always shorts → longs
        frequency   :: every epoch (could be every block on-chain)
    
        // Mark-to-market: expectation adjustment  
        mark_to_market(t) :: (market_price - fair_value) × rate
        direction         :: overpriced side → underpriced side
        frequency         :: continuous (via funding rate)
    
       // Fair value of the perpetual claim
       fair_value :: Σ(expected_future_dividends) / discount_rate
       // This IS the "cash market price" Shiller describes
	}
	
   // 7. CROSS-COUNTRY INCOME SPREAD
    // "Pay me if Nigerian LP income falls relative to 
    //  Philippine LP income" (macro relative value)
    CrossCountrySpread {
        underlying :: income(cNGN_pools) / income(PUSO_pools)
        strike     :: ratio_threshold
        payoff     :: f(ratio vs. threshold)
        analog     :: macro relative value trade
    }
}
```
