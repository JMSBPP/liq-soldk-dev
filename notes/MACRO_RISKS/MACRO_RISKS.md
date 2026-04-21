  The Reality Check                                                                                                                                                                     
  Macro Risk Proxies Beyond Pure FX                                                                                                                                                     
                                         
  For underserved countries, FX depreciation is often the dominant macro risk 
  ---> It proxies GDP decline, inflation, capital flight). But you can go further:                              
                                                                     
MacroRisk {
	LocalInflation       -->    AMP/other currrency , PAXG/ , WBTC , 
	InterestRateShock    -->    stETH yield vs. local stablecoin yield spread
	TermsOfTrade         -->    RWACommodityToken / local stable coin
	CapitalFlight        -->    LocalStableCoint/ cUSD implied vol
	RemittanceCorridorRisk -->  CrossStableCoin spreads
}


LocalInflation{
	Attemps: [
		{
			usa,
			1985,
			CPI index futures
		},
		
		{
			Brazil,
			1987
			CPI index futures
		}
	]

}

d Flow = deterministic + (random -> hedgeable)

   | 
    --> d _{lags}     ease of observable measurement
	   d_{inmediate} (e.g fire of a house) -> easier to observe -> easier to ensure

Macro(FinancialContract){
     settlement(MacroRisk, measure (input))
	                             |
                                  ----> exisiting difficulty
								              |
                                            (Theory of Index Numbers)
 }


TradingVolume (Agg (local / host (migrant country)){
      Corridor-weighted basket as HOST-country	---> labor demand 
	  d TVOLUME / DT --> host recession hitting local migrant workers
}

ExchangeRate (local /host ){
     Spread (onChain, centralBank (via chainlink)) --> capital controls, currency crisis, macro stress

      Perpetual claim on the cNGN/USDC implied depreciation rate

       Index = rolling 30d VWAP of cNGN/USDC across Mento + Uniswap
           vs. CBN official rate (via Chainlink or custom oracle)

        Premium = f(realized vol of the spread) 
        Index = rolling 30d VWAP of cNGN/USDC across Mento + Uniswap
           vs. CBN official rate (via Chainlink or custom oracle)
}



### Pension Funds

- Employer contributions to pension funds could be debited and credited representing the employee's gains or losses in macro markets

### Labor Unions
- use these markets to help protect their members against adverse labor market conditions 
  --> transference of risks that individual workers face to the financial markets, by loading the risk 
    d risk(W) ---> d price (firm) ---> Held in diversified portafolios


#### **Challenge**
	- not(perpetual (laborContracts)) ^ perpetual(worker hedging intertests) ->

#### **Solution**
	 - employer ----> hedge(random (d W / d I)) ---> employee
	                           
                               |
							   |
							   v
					          d W  --> not fixed salary		   


# Psychology --> Approaching the Public


risk management ----(attracteiveness) ----> insurance
x							                   |
                                               |
                                               v
											 losses market


frame:: income

-  no risk averse on gains market 
    -> (   [100%,- 3000]      ,    [80% , -4000])
                 |                      |
                 V                      v
         E [" "] = 3000     <        E[" "] = -3200  (X)

- risk averse on loss market 
   -> (    [100% , 3000]      ,      [80% , 4000 ])
                 
                 |                       |
 				 V                       v
		 E [" "] = 3000 [X]	             E[" "] = 3200
                  
frame :: wealth optimal is the reverse



- informational cascades
- gambling behavior{
	- risk-taking behavior
	- play a game that is attractive to them (mastery of the game dominate chance)
}


- adoption --> public education --> retail firms -------nexus (context)--->  social-psycological effects
                                                             |
                                                             |
		insurance best offered framed as/on part of contract negotioation rather than  offered by insurance salesman
		
- IMPORTANT (COMPOSABILITY): combination with other risk-management products that already won accpentance

frame risk as eliminatign rather than reducing, adn eliminating a "borader" trather than a specific



```
FinancialContract {

    // Layer 1: What we WANT to hedge
    Claim :: Flow(Forward(Income, futureTime))
    
    // Layer 2: What we CAN observe
    Settlement {
        
        // The market itself IS the oracle
        oracle :: CashMarket {
            // The cash market produces a price by aggregating
            // private information from participants with skin in the game
            mechanism :: Aggregator(Expectations, Information, Incentive)
            
            // What the market actually trades
            underlying :: PerpetualClaim(Index(Income))
        }
        
	   // note: Removes the noise from the signal/index such that it reflects the value
        // wnated to be tracked and it DOES reduce risk not introdouce it du to thje noise fo the signla
		
		/// 
		observable :: controlled(process(oracle(observables)))) :: Series<Signal>
		
		// build / construccted to reflect the Claim best observable proxy
		::Index 
  		// The actual payout computation
        payoff :: f(observable.price, strike, direction)
    }

    // Layer 3: The gap between claim and settlement
    BasisRisk :: Distance(Claim, Settlement.oracle.underlying)
    // i.e., how far is the traded index from actual income?
}

PerpetualFutures :: CashMarket {
    
    observables :: {
        mark_price    :: continuous, manipulation-resistant
        funding_rate  :: 8h signal encoding directional consensus
        open_interest :: total capital committed to views
        basis         :: spread(perp_price, spot_price)
        liquidations  :: forced unwinds = stress signal
    }
    
    // The funding rate IS Shiller's "incentivized information revelation"
    // Traders pay to hold their view → they only hold if they believe it
    funding_rate :: Transfer(longs, shorts) | Transfer(shorts, longs)
    // positive funding = market is net long = consensus expects price UP
    // negative funding = market is net short = consensus expects price DOWN
```


## Settlement


```
PRICE-SETTLED CLAIMS                 INCOME-SETTLED CLAIMS
─────────────────────                ─────────────────────
Observable: market price             Observable: accrued revenue
Updates: every trade                 Updates: every block
Source: exchange/pool                Source: protocol accounting
                                     
Measures: expectations               Measures: ACTUAL REALIZED VALUE
          (forward-looking)                    (backward-looking)

Manipulation: Flash loans,           Manipulation: Income accrues over time, not in a single tx
              wash trading, 
			  oracle attacks

Basis Risk : High — price may       Basis Risk : Low — income IS the fundamental
             diverge from 
			 fundamentals


Liquidity                            Liquidity 
requirement: Needs deep cash         requirement: Needs none — reads protocol state directly
             market

Latency:    Real-time (every trade)  Latency:  Real-time (every block) -> requires block accumultor/tracj                                                king ?

Hedging                              Hedging
utility:   Hedges against            utility:   Hedges agains income decline
           price movements 

Speculation:                        Speculation: Harder - short someone's yield
           Trade  underlying

Bootstrapping:                        Bootstrapping: None - income exists already
           need liquidity for prices


Composability:                       Composability: 
           Universal —                             Protocol-specific
		   any ERC-20 has a price                  must understand each income source
		   


Noise: speculation, manipulation,    Noise: MEV, protocol upgrades,
       liquidity artifacts                  reward schedule changes

Settlement: f(price_t - strike)      Settlement: f(income_t - strike)

===> INCOME > PRICE < ====
```

## [INCOME_SETTLEMENT](./INCOME_SETTLEMENT.md)
## **Claim Flows**

```
ClaimFlows{
	Flow 1: MARK-TO-MARKET (price convergence) --> correction
        Purpose: keep derivative price = fair value
		Direction: alternates (longs↔shorts based on mispricing) 
		
		PERP-FUTURES {
		
			 funding_rate (every 8h)
                    = (perp_price - index_price) × position_size
                    Direction: overpriced side pays underpriced side
		}
		
		CFMM {
			Arbitrageurs
                    When index price moves, arbs trade the pool 
                    to correct the price
                    LPs "pay" via impermanent loss
                    Arbs "receive" the profit
		
		}
        
	Flow 2: DIVIDEND (income distribution)  --> payment for bearing risk
        Purpose: transfer the actual income to claim holders
        Direction: always shorts → longs
        (shorts are "renting out" their side of the income stream)
		
		
		PERP-FUTURES {
		            NOT NATIVELY SUPPORTED
                    Standard perps have no dividend mechanism
                    
                    To add it, you modify the funding rate:
                    
                    total_funding = convergence_funding + dividend_funding
                    
                    convergence = (perp_price - spot) / 8h
                    dividend    = index_income_accrued / 8h
                    
                    Shorts always pay the dividend component
                    Convergence component alternates as usual

		}
		
		CFMM  {
			Dividend:           
			               Fee accrual
			               Every swap pays a fee to LPs
	                       This fee IS an income stream
		
		}

```
### **ClaimFlows<CFMM>**

```
Shiller's Construct          CFMM Realization
───────────────────          ────────────────────

LONG the income claim   ←→   LP position
(receives dividend)          (receives fee revenue)

SHORT the income claim  ←→   Swap traders / arbitrageurs  
(pays dividend)              (pay fees on every trade)

Mark-to-market          ←→   Arbitrage  
(price convergence)          (corrects pool price to oracle)

Dividend payment        ←→   Trading fees
(income transfer)            (flow from traders to LPs)

==============================================================
                     Mark-to-Market    Dividend
                     (who benefits     (who receives
                      from price       income)
                      convergence)

Shiller Long         ✓ benefits        ✓ receives
Shiller Short        ✗ pays            ✗ pays

CFMM LP              ✗ pays (IL)       ✓ receives (fees)
CFMM Trader          ✓ benefits (arb)  ✗ pays (fees)

Perp Long            ✓/✗ (alternates)  ✓ receives (if modified)
Perp Short           ✗/✓ (alternates)  ✗ pays (if modified)

================================================================
LP_Position = Income_Component + Price_Component

Income_Component (Shiller's dividend):
    = cumulative_fees_earned(t)
    Observable: feeGrowthGlobal, feeGrowthInside
    Always positive, always flows to LP
    THIS is what your income perpetual settles against

Price_Component (mark-to-market):
    = impermanent_loss(t)  
    Observable: position value vs. HODL value
    Can be positive or negative
    THIS is what Panoptic options already handle
```

[ARBS](https://github.com/sterlingcrispin/arb-hook/blob/master/contracts/ArbHook.sol)


## [PRICE_SETTLEMENT](./PRICE_SETTLEMENT.md)
### [SIGNAL-> INDEX](./SIGNAL_TO_INDEX.md)

```
Phase 1: SIGNAL PROCESSING (information theory)
┌─────────────────────────────────────────────┐
│                                             │
│  Raw Observable     →  Filter  →  Signal    │
│                                             │
│  funding_rate(raw)  →  TWAP    →  funding   │
│                        EMA        signal    │
│                        Kalman               │
│                        outlier              │
│                        removal              │
│                                             │
│  spot_price(raw)    →  TWAP    →  price     │
│                        median     signal    │
│                                             │
│  volume(raw)        →  normalize→ flow      │
│                        deseason   signal    │
│                                             │
│  Theory: Shannon, Wiener, Kalman            │
│  Question: what is the TRUE state?          │
│  Error: noise, distortion, latency          │
└─────────────────────────────────────────────┘
                      │
                      ▼
Phase 2: INDEX CONSTRUCTION (measurement theory)
┌─────────────────────────────────────────────┐
│                                             │
│  Signals     →  Methodology  →  Index       │
│                                             │
│  funding_signal ─┐                          │
│  price_signal   ─┼→  aggregate  →  macro    │
│  flow_signal    ─┘    weight       stress   │
│                       normalize    index    │
│                                             │
│  Theory: Laspeyres, Paasche, Fisher         │
│  Question: what REPRESENTS the concept?     │
│  Error: methodology bias, proxy distance    │
└─────────────────────────────────────────────┘
                      │
                      ▼
Phase 3: SETTLEMENT (contract theory)
┌─────────────────────────────────────────────┐
│                                             │
│  Index  →  payoff function  →  settlement   │
│                                             │
│  macro_stress_index(t)                      │
│    vs. strike_value                         │
│    = cash_payout                            │
│                                             │
│  Theory: derivatives pricing, Shiller       │
│  Question: what do we PAY?                  │
│  Error: basis risk (index ≠ actual income)  │
└─────────────────────────────────────────────┘
```







