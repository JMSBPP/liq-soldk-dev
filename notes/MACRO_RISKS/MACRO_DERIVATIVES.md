

# MACRO_DERIVATIVES


CreditRisk
```
	                              -------------------------------
	         ----> BRANCH/INDEX  | CDS INSURANCE (SHORT)/ (LONG) |
           |                      -------------------------------
 CDS ------ 
  |
   ----------------- d risk(lender) ---(LONG)---> (MARKET_MAKER)---(SHORT)------> CDS( LONGS)   
                     /             \
					/               \
					                  -------------------->
	   \beta1 (systematic (d risk (lender)))	 +        \beta_2   (undersystematic(d risk (lender)))
             - not diversifiable                 |            - diversifiable
             - tradeable                         |
    
	             |
				 | (driven by)
				 |
			(macroeconomic
			  conditions)
			  
                 | ----->   (m1, m2, ..., mn)
				           (macro observables)
                                 |
								 
							Agg(M)= Agg((m1, m2, ..., mn))	 


==> d risk(lender) =  \beta1 (systematic (d risk (lender)))+\beta_2   (undersystematic(d risk (lender)))
                                                              ----------------------------------------
	                                   |                                        S
									   |
									   V
		  
		           =  \beta1         Agg(M)                     +               S


```


[BussinessCycleRisk](~/apps/liq-soldk-dev/refs/macro-risk/macroDerivatives002.pdf)::
  - variations in a firm’s performance measures that are associated with variations
	in the general level of economic activity
	 
```

Swap(BussinessCycleRisk){

    ---------------------------------------------------------------------------------------
    | payoff:: (  floatLeg LONG ~(pegged)~> d(GDP ~ Agg(M))) (-) --> (fixedLeg SHORT)      |
              	 ------               
				    
					^                                            |
					|                                         
					                                      firm/agent (SHORT)
				market maker
				    
					|                                            |
				(d revenue)	                                   (d cost)
					|                                            |
	          firm/agent LONG                                    |
			        |                                            v
					 
	   (product markets/revenue source)            (factor markets/cost source)
    |                                                                                     | 
     -------------------------------------------------------------------------------------
         d \pi (cash flow) = d (revenue) - d (cost)


}

```

## MACRO DEFAULT SWAP

MacroDefaultSwap{
	underlying:: Agg(M)
	 	
	payoff()  [(31)]((~/apps/liq-soldk-dev/refs/macro-risk/macroDerivatives001.pdf))

}

 
