



## DESIRED MEANS ( TOOLING )

- Use Lean4 heavily 
- Express problems as convex optimization prblmes
- Numerical optimizatoipn, Apporximation
- Compariative statics
- Dynamic General Equilibria


forge test  --mt test_Success_mintOptions_ITMShortPutShortCall_Swap  
--fork-url 
                                                                                                         
export RCP="https://eth-mainnet.g.alchemy.com/v2/fd_m2oikp78msnnQGxO6H" && 
export DEFAULT_BLOCK_NUMBER=18963715 &&
source /home/jmsbpp/.bashrc && 

forge test --mt test_Success_mintOptions_ITMShortPutShortCall_Swap --fork-url "https://eth-mainnet.g.alchemy.com/v2/fd_m2oikp78msnnQGxO6H"  --fork-block-number 18963715 --json --summary --detailed --flamechart -vvvv > out.txt



The question we have is note that there is an out that TXT with the trace of a test and that test is actually the one that we are tracing on the panoptic roadmap that MD file but essentially what is important about this test is that it essentially has the whole workflow from someone minting and boarding an option and then swaps on between. Now, on volt here, note that on volt here, if you look, the process for pricing an option is directly using the black sholes, a black sholes library that does a complete computation directly and calculates a unit premium. However, the process of panoptic is more elegant in the sense that the premium is passed from lungs to shorts through the trading fee. How do this converge and how one can use the same idea of panoptic to price the option.
