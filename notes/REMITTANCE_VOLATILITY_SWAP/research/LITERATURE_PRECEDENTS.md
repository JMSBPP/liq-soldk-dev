# Literature Precedents: On-Chain Stablecoin Flows as Real-Economy Proxies

**Date**: 2026-04-02
**Purpose**: Systematic survey of academic papers, institutional reports, and data analysis projects that use on-chain stablecoin flow data to measure or proxy real-world economic variables (remittance, income, macro indicators) for emerging market countries.
**Relevance**: We are building a variance swap on net USD-to-COP stablecoin flows as a hedging instrument, using Dune Analytics to query Mento broker swaps and ERC-20 transfers on Celo for Colombian peso stablecoins (cCOP, COPM).

---

## Executive Summary

The literature on using on-chain stablecoin data as a proxy for real-economy variables is nascent but rapidly growing. The field is dominated by three institutional clusters: (1) IMF working papers developing geographic attribution methodologies for stablecoin flows, (2) BIS papers establishing causal links between stablecoin flows and FX markets using gravity models and instrumental variables, and (3) industry analytics from Chainalysis, TRM Labs, and Dune providing the raw data infrastructure. Academic work on behavioral fingerprinting of blockchain users exists but has not yet been applied to the specific problem of identifying remittance-type flows. No prior work has attempted to build a derivatives instrument (variance swap or otherwise) on stablecoin flow metrics, making our project genuinely novel. The closest methodological precedent is the IMF/BIS work on estimating bilateral stablecoin flows and measuring their FX spillover effects.

---

## 1. IMF Working Papers

### 1.1 "Decrypting Crypto: How to Estimate International Stablecoin Flows"

- **Authors**: Marco Reuter
- **Date**: July 2025
- **Reference**: IMF Working Paper WP/25/141
- **URL**: https://www.imf.org/en/Publications/WP/Issues/2025/07/11/Decrypting-Crypto-How-to-Estimate-International-Stablecoin-Flows-568260
- **PDF**: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025141-source-pdf.pdf

**Methodology**: Combines AI/ML with web traffic data to estimate geographic distribution of stablecoin flows. Since on-chain transactions do not reveal user locations, the paper uses web traffic to virtual asset service providers (VASPs) as a proxy for geographic attribution. The share of visits from each country is applied to that platform's incoming transaction volume to produce bilateral flow estimates.

**Key Findings**:
- Analyzed 2024 stablecoin transactions totaling $2 trillion
- Stablecoin flows highest in North America ($633bn) and Asia-Pacific ($519bn)
- Relative to GDP: most significant in Latin America and Caribbean (7.7%) and Africa/Middle East (6.7%)
- North America exhibits net outflows, meeting global dollar demand
- Flows increase during periods of dollar appreciation against other currencies
- 2023 banking crisis significantly impeded flows from North America
- Provides comparison to Chainalysis dataset

**Relevance to Our Project**: HIGH. This is the closest methodological precedent for what we are attempting. Their web-traffic-based geographic attribution is a reasonable but coarse approach. Our Celo-specific approach (analyzing cCOP/COPM transfers directly) provides much higher geographic precision because the very existence of a COP-pegged stablecoin implies Colombian involvement. We do not need their ML-based geographic attribution -- the token itself is the geographic signal. However, their panel regression framework for identifying drivers of net stablecoin flows (remittance costs, dollar demand, crisis events) is directly applicable to our identification strategy.

**Data Used**: On-chain USDT/USDC transaction data combined with SimilarWeb traffic data for VASPs.

---

### 1.2 "Stablecoin Inflows and Spillovers to FX Markets"

- **Authors**: Inagio Aldasoro, Daniel Beltran, and Federico Grinberg
- **Date**: March 2026
- **Reference**: IMF Working Paper WP/26/056 (also published as BIS Working Paper No. 1340)
- **URL**: https://www.imf.org/en/publications/wp/issues/2026/03/27/stablecoin-inflows-and-spillovers-to-fx-markets-575046
- **BIS PDF**: https://www.bis.org/publ/work1340.pdf

**Methodology**: Uses data on four USD-pegged stablecoins and 27 fiat currencies. Employs a granular instrumental variable (GIV) that exploits idiosyncratic shocks to stablecoin net inflows in other currencies. The instrument is constructed from idiosyncratic shocks in other currencies, purged of common factors, so it has no direct channel to affect the local FX market except via global stablecoin market equilibrium. Also uses a constrained arbitrage model providing structural foundations.

**Key Findings**:
- A 1% exogenous increase in net stablecoin inflows raises parity deviations by 40 basis points
- Stablecoin inflows depreciate the local currency
- Stablecoin inflows widen the dollar premium in synthetic funding markets (CIP deviations)
- Counterfactual: halving cross-market frictions would attenuate CIP spillovers by roughly one-half
- Spillovers grow disproportionately when intermediaries suffer losses (depleted capital reduces shock absorption)

**Relevance to Our Project**: VERY HIGH. This paper establishes that stablecoin flows have causal, measurable effects on traditional FX markets. Their IV strategy -- using idiosyncratic shocks in other currencies as instruments -- is a template for our own identification. The finding that stablecoin inflows depreciate local currencies and widen CIP deviations is exactly the channel our variance swap is designed to hedge. If COP stablecoin flows are volatile, the FX effects are real and hedgeable.

**Data Used**: Daily stablecoin transaction data (USDT, USDC, DAI, BUSD), FX spot rates for 27 currencies, CIP deviation measures.

---

### 1.3 "Stablecoin Shocks"

- **Authors**: Eugenio Cerutti et al.
- **Date**: March 2026
- **Reference**: IMF Working Paper WP/26/044
- **URL**: https://www.imf.org/en/publications/wp/issues/2026/03/06/stablecoin-shocks-574528

**Methodology**: Combines a daily narrative dataset of stablecoin-specific news with changes in combined USDC+USDT market capitalization. Implements heteroskedasticity-based identification within an event-study and SVAR-IV framework.

**Key Findings**: Measures high-frequency movements in stablecoin market cap and identifies their macrofinancial transmission channels.

**Relevance to Our Project**: MODERATE. The event-study and SVAR-IV methodology could be adapted for our cCOP/COPM flow data. Their narrative dataset approach (using news events as instruments) maps to our Colombia Event Timeline work.

---

### 1.4 "Understanding Stablecoins"

- **Date**: 2025
- **Reference**: IMF Monetary and Capital Markets Department Discussion Paper
- **URL**: https://www.imf.org/-/media/files/publications/dp/2025/english/usea.pdf

**Key Finding**: Stablecoin flows between emerging market and developing economies (EMDEs) account for the largest share by value. Flows from EMDEs to advanced economies and vice versa also represent a significant portion. Stablecoin cross-border flow was $1.4 trillion in 2024.

**Relevance to Our Project**: Contextual. Confirms that EMDE stablecoin flows are economically significant.

---

## 2. BIS Working Papers

### 2.1 "DeFiying Gravity? An Empirical Analysis of Cross-Border Bitcoin, Ether and Stablecoin Flows"

- **Authors**: Raphael Auer, Ulf Lewrick, and Jan Paulick
- **Date**: May 2025
- **Reference**: BIS Working Paper No. 1265
- **URL**: https://www.bis.org/publ/work1265.htm
- **PDF**: https://www.bis.org/publ/work1265.pdf

**Methodology**: Uses unique bilateral data on cross-border crypto flows between 184 countries from 2017 to 2024. Applies a gravity model framework (standard in international trade/finance) to stablecoin flows for the first time, distinguishing drivers across asset types (BTC, ETH, USDT, USDC).

**Key Findings**:
- Total cross-border crypto flows peaked at ~$2.6 trillion in 2021; stablecoins accounted for close to half
- Speculative motives and global funding conditions drive native crypto asset flows
- Transactional motives play a significant role for stablecoins and low-value BTC transactions
- Strong association between stablecoin flows and higher costs of traditional remittances
- Geographic barriers play a diminished role compared to traditional financial flows
- Capital flow management measures (capital controls) appear ineffective against stablecoin flows

**Relevance to Our Project**: HIGH. The gravity model finding that stablecoin flows are associated with high remittance costs is the economic rationale for why COP stablecoin flows proxy for remittance activity. The finding that capital controls are ineffective means our flow data captures activity that traditional statistics miss. Their bilateral flow dataset structure is a template for how to organize our Dune query results.

**Data Used**: Proprietary bilateral crypto flow data across 184 countries, traditional gravity model variables (GDP, distance, language, trade), remittance cost data from World Bank RPW.

---

### 2.2 BIS Bulletin No. 108: "Stablecoin Growth - Policy Challenges and Approaches"

- **URL**: https://www.bis.org/publ/bisbull108.pdf

**Relevance**: Background context on regulatory concerns about stablecoin growth in EMDEs.

---

## 3. NBER Working Papers

### 3.1 "Inflation Expectation and Cryptocurrency Investment"

- **Reference**: NBER Working Paper No. 32945 (2024)
- **URL**: https://www.nber.org/papers/w32945

**Methodology**: Combines detailed transaction data from cryptocurrency exchanges with household surveys. First paper to combine trading data with household surveys to analyze cryptocurrency investments in emerging economies.

**Key Findings**: Cryptocurrencies serve as an inflation hedge in emerging markets. Exchange-level trading data combined with household surveys provides evidence of inflation-hedging behavior.

**Relevance to Our Project**: MODERATE. The methodology of combining on-chain/exchange data with household survey data is relevant to our calibration problem. If we want to validate that our cCOP flow data actually reflects remittance behavior, household survey data (from DANE in Colombia) would be the natural validation dataset. Their approach of linking exchange-level data to household-level economic behavior is a template.

---

### 3.2 "Stablecoins" (NBER Working Paper No. 34475)

- **URL**: https://www.nber.org/papers/w34475

**Key Finding**: Stablecoins may bring efficiency gains to international payments and remittances, with potential to reduce cross-border intermediation fees and provide 24/7 payment system access.

---

### 3.3 "The Effects of Cryptocurrency Wealth on Household Consumption and Investment"

- **Reference**: NBER Working Paper No. 31445
- **URL**: https://www.nber.org/papers/w31445

**Relevance**: Establishes that crypto wealth has real effects on household economic behavior. Relevant to our thesis that stablecoin flows proxy for real economic activity.

---

## 4. Academic Journal Papers

### 4.1 "Cryptocurrencies in Emerging Markets: A Stablecoin Solution?"

- **Authors**: Ferriani (2025)
- **Journal**: Journal of International Money and Finance
- **URL**: https://www.sciencedirect.com/science/article/pii/S0261560625000798

**Methodology**: Calibrated macro model examining costs and benefits of digital dollarization. Uses CRRA coefficient of 2 for money and cryptocurrency. Models physical cash at 10% of GDP as baseline.

**Key Findings**: Cryptocurrency adoption responds to sovereign default risk (higher CDS spreads lead to increased app downloads). Provides a theoretical rationale for why stablecoins are adopted in EMDEs.

**Relevance to Our Project**: MODERATE. The finding that sovereign risk drives stablecoin adoption is an identification lever. If we observe cCOP/USDC flow spikes correlating with Colombian CDS spreads, we have evidence that flows respond to macro fundamentals -- exactly what we need for our variance swap to be a meaningful hedging instrument.

---

### 4.2 "Stablecoins and Emerging Market Currencies: A Time-Varying Analysis"

- **Journal**: Digital Transformation and Society (2025)
- **URL**: https://www.doi.org/10.1108/DTS-09-2024-0167

**Methodology**: Uses probabilistic principal component analysis (PPCA) to create stablecoin and EMDE currency returns/volatility indices. Employs time-varying correlation and TVP-VAR connectedness measures.

**Key Findings**: Documents time-dependent correlation and connectedness between EMDE currencies and stablecoin markets.

**Relevance to Our Project**: MODERATE. The TVP-VAR methodology is relevant for modeling the time-varying relationship between cCOP flow volatility and COP/USD FX volatility.

---

### 4.3 "Stablecoins and the Emerging Hybrid Monetary Ecosystems"

- **Authors**: Multiple
- **Date**: May 2025
- **Reference**: arXiv:2505.10997
- **URL**: https://arxiv.org/abs/2505.10997

**Methodology**: Econometric models analyzing dependencies between stablecoin prices and financial assets. Includes GARCH, copula, quantile-based models, VAR, and VECM methods.

**Key Findings**: Stablecoins maintain strong peg stability, but each type exhibits distinctive responses to market variables depending on stabilization mechanisms.

**Relevance to Our Project**: LOW-MODERATE. The econometric toolkit (GARCH, copula models) is relevant for modeling cCOP/COPM flow volatility and designing the variance swap payoff.

---

### 4.4 "Stablecoins: Fundamentals, Emerging Issues, and Open Challenges"

- **Date**: July 2025
- **Reference**: arXiv:2507.13883
- **URL**: https://arxiv.org/abs/2507.13883

**Relevance**: Comprehensive survey; useful reference for stablecoin econometric literature.

---

## 5. Behavioral Fingerprinting Literature

### 5.1 "Fingerprinting Bitcoin Entities Using Money Flow Representation Learning"

- **Journal**: Applied Network Science (2023)
- **URL**: https://appliednetsci.springeropen.com/articles/10.1007/s41109-023-00591-2

**Methodology**: Applies representation learning to assign fingerprint vectors summarizing transaction flows for entities. Uses these fingerprints to classify distinct entities and cluster those with similar patterns.

**Relevance to Our Project**: HIGH. This is the closest academic precedent for our behavioral fingerprinting work on cCOP/COPM addresses. Their representation learning approach could be applied to Celo addresses to classify remittance senders, traders, institutional users, etc.

---

### 5.2 "Bitcoin and Cybersecurity: Temporal Dissection of Blockchain Data to Unveil Changes in Entity Behavioral Patterns"

- **Journal**: Applied Sciences, 9(23), 5003 (2019)
- **URL**: https://www.mdpi.com/2076-3417/9/23/5003

**Methodology**: Temporal dissection of blockchain data to identify changes in entity behavior over time. Analyzes batch sizes and temporal stability of classification.

**Key Findings**: Behavioral patterns for some entity types (Exchange, Gambling, eWallet) are stable over time; others (Mining Pool) evolve. Models trained on recent data outperform those trained on older data.

**Relevance to Our Project**: MODERATE. The finding that behavioral patterns have variable temporal stability is important for our fingerprinting approach. If remittance-type patterns on Celo are stable, our classification will be robust. If they evolve (e.g., as Littio changes UX), we need rolling retraining.

---

### 5.3 "Behavioral Structure of Users in Cryptocurrency Market"

- **Journal**: PLOS ONE (2020)
- **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0242600

**Methodology**: Combines k-means clustering and Support Vector Machines to derive behavioral types of users in cryptocurrency markets.

**Relevance to Our Project**: MODERATE. K-means + SVM is a simple, interpretable pipeline we could apply to our Celo address features.

---

### 5.4 "Characterizing Key Agents in the Cryptocurrency Economy Through Blockchain Transaction Analysis"

- **Journal**: EPJ Data Science (2021)
- **URL**: https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00276-9

**Methodology**: Uses transactional patterns (volume features, temporal features, structural features) to characterize and differentiate agents in different roles within the crypto economy.

**Relevance to Our Project**: HIGH. Their feature engineering (volume, temporal, structural) maps directly to our behavioral fingerprinting queries for cCOP/COPM users. The distinction between "key agents" (intermediaries, exchanges) and retail users is exactly the decomposition we need.

---

## 6. Industry and Data Analysis Reports

### 6.1 Chainalysis: Geography of Cryptocurrency Reports (2024, 2025)

- **2024 Report**: https://go.chainalysis.com/2024-geography-of-cryptocurrency-report.html
- **2025 Report**: https://go.chainalysis.com/2025-geography-of-cryptocurrency-report.html
- **2025 LATAM Analysis**: https://www.chainalysis.com/blog/latin-america-crypto-adoption-2025/
- **2024 LATAM Analysis**: https://www.chainalysis.com/blog/2024-latin-america-crypto-adoption/

**Methodology**: Chainalysis Global Crypto Adoption Index normalizes countries on a 0-1 scale using blockchain transaction data adjusted for PPP and population. Uses proprietary on-chain attribution data to identify geographic origins of flows.

**Key Findings for Colombia/LATAM**:
- In Colombia, Argentina, and Brazil, stablecoin purchases make up over 50% of all exchange purchases (July 2024 - June 2025)
- Latin America's crypto adoption grew 63% year-over-year
- Regional volumes more than doubled, reaching $87.7 billion in December 2024
- Wenia (Bancolombia's crypto exchange) identified as a major Colombian platform
- Stablecoin dominance reflects persistent inflation, currency volatility, and capital controls

**Relevance to Our Project**: HIGH. Chainalysis provides the macro context for why COP stablecoin flows are economically meaningful. Their data on Colombian stablecoin purchase share (>50%) validates our thesis. However, their analysis does not drill into specific tokens like cCOP or COPM -- that is where our Dune-based approach provides granularity they lack.

---

### 6.2 TRM Labs: 2025 Crypto Adoption and Stablecoin Usage Report

- **URL**: https://www.trmlabs.com/reports-and-whitepapers/2025-crypto-adoption-and-stablecoin-usage-report

**Key Findings**:
- Stablecoins accounted for 30% of crypto transaction volume (Jan-Jul 2025)
- Annual stablecoin volume exceeded $4 trillion (83% increase YoY)
- USDT and USDC account for 93% of stablecoin market cap
- South Asia: 80% increase in adoption (Jan-Jul 2025 vs. prior year)
- Retail-driven growth dominates, with user acquisition on consumer platforms driving 70%+ of volume growth

**Relevance to Our Project**: MODERATE. Confirms the macro trend but lacks corridor-level or token-level granularity.

---

### 6.3 Dune Analytics: Stablecoin Datasets and Dashboards

- **Stablecoin Overview**: https://dune.com/collection/stablecoins/overview
- **Stablecoin Activity**: https://dune.com/collection/stablecoins/activity
- **Coverage**: https://dune.com/collection/stablecoins/coverage

**Capabilities** (as of February 2026):
- Trigger-aware logic classifies each transfer by economic action (DEX, bridge, CEX, lending, issuer flows)
- Enriched activity logs span 37 EVM networks and Solana
- Address labels distinguish exchanges, DeFi protocols, institutional custodians, retail users
- Can separate settlement usage (merchants, remittances, treasury transfers) from bot/arbitrage noise

**Relevance to Our Project**: VERY HIGH. Dune's enriched stablecoin dataset is our primary data infrastructure. Their ability to classify transfers by economic action and label addresses by role is exactly what we need for behavioral fingerprinting. Key question: does Dune's enriched dataset cover Celo and specifically cCOP/COPM? If not, we build equivalent queries using raw Celo ERC-20 transfer tables.

---

### 6.4 Wharton Stablecoin Toolkit (January 2026)

- **URL**: https://bdap.wharton.upenn.edu/wp-content/uploads/2026/01/Stablecoin-Toolkit.pdf

**Description**: Comprehensive taxonomy of stablecoin models developed with 20+ global experts. Identifies four stabilization mechanisms. Maps stablecoins within the broader universe of 10 categories of money-like instruments.

**Relevance to Our Project**: LOW. Provides definitional framework but not empirical methodology.

---

## 7. Colombia-Specific Sources

### 7.1 Banco de la Republica: CBDC Research

- **Paper**: "Relevance and Risks of Issuing a Central Bank Digital Currency in Colombia"
- **URL**: https://www.banrep.gov.co/sites/default/files/publicaciones/archivos/relevance-risks-issuing-central-bank-digital-currency-colombia.pdf

**Key Finding**: Introducing a retail CBDC would not entail substantial macroeconomic risks. BanRep has been experimenting with DLT since 2018, conducting PoCs with wholesale CBDC and digitized public securities.

**Relevance to Our Project**: LOW. BanRep is focused on CBDC, not stablecoin analytics. However, their macro modeling of digital currency effects in the Colombian economy could inform our identification strategy.

---

### 7.2 CEMLA: "Stablecoins in Latin America and the Caribbean"

- **URL**: https://www.cemla.org/fintech/docs/stablecoins-in-latin-america-and-the-caribbean.pdf

**Key Finding**: Survey shows stablecoin adoption across participating jurisdictions is considered low but growing. Notes that EME currencies may exhibit higher volatility, making stablecoin backing choices critical.

**Relevance to Our Project**: LOW-MODERATE. Regional context.

---

### 7.3 Bancolombia/Wenia and COPW Stablecoin

- **Source**: Cointelegraph (2024)
- **URL**: https://cointelegraph.com/news/bancolombia-group-wenia-crypto-exchange-copw-stablecoin

Colombia's largest bank launched a crypto exchange (Wenia) and a COP-pegged stablecoin (COPW). This is a centralized, bank-issued competitor to the decentralized cCOP (Mento) and the asset-backed COPM (Minteo).

**Relevance to Our Project**: MODERATE. COPW represents a third COP stablecoin ecosystem. If we want comprehensive COP stablecoin flow measurement, we may need to track COPW alongside cCOP and COPM. However, COPW likely operates on different rails (possibly not Celo).

---

### 7.4 Minteo / COPM

- **URL**: https://minteo.com/
- **Transparency**: https://transparency.minteo.com/

**Details**: Minteo raised $4.3M in 2022. COPM is fully-reserved via cash deposits in regulated Colombian banks, audited monthly by BDO. Deployed on Celo as the 13th native stablecoin via Stabila Foundation. Over 100,000 Colombians use COPM via Littio. COPM-USDT pair on Uniswap V3 via Merkl with >100% APY incentives.

**Relevance to Our Project**: VERY HIGH. COPM is our primary data source alongside cCOP. The Minteo/Littio connection means COPM flows have a direct link to real Colombian users (not just DeFi speculators). The Uniswap V3 pair gives us additional AMM-based price/flow data.

---

### 7.5 Littio

- **URL**: https://littio.co/en/
- **Circle Partnership**: https://www.circle.com/blog/littio-x-usdc-creating-stable-and-secure-banking-in-latam

**Details**: Y-Combinator and Circle-backed neobank for Colombia. 200,000+ Colombian users. Offers USDC/EUROC savings accounts with yield via OpenTrade. During the February 2025 Petro-Trump tariff episode, saw 100%+ growth in new USDC yield accounts. Uses COPM for COP-denominated functionality.

**Relevance to Our Project**: VERY HIGH. Littio is the primary user-facing application driving real Colombian adoption of on-chain stablecoins. Their user base (200K+) represents a significant fraction of Colombian stablecoin users. The tariff-episode spike is a natural experiment we should be able to observe in our Dune data. Littio's address(es) on Celo are likely among the top intermediaries in our behavioral fingerprinting analysis.

---

### 7.6 Mento / cCOP

- **Mento Blog**: https://www.mento.org/blog/announcing-the-launch-of-ccop---celo-colombia-peso-decentralized-stablecoin-on-the-mento-platform
- **Celo Governance Proposal**: https://forum.celo.org/t/launch-of-ccop-colombia-s-first-decentralized-stablecoin/9211
- **Reserve**: https://reserve.mento.org/

**Details**: cCOP is a decentralized stablecoin on Mento. Liquidity minted/burned during swaps (virtual AMM with Mento Reserve as LP). On-chain circuit breakers and trading limits configurable per pair. Reserve shows cCOP supply at ~$61,887.35 (very small).

**Relevance to Our Project**: HIGH but note the extremely small supply ($62K). cCOP is conceptually important but may lack sufficient volume for robust statistical analysis. COPM (via Minteo/Littio) likely has much more activity. Our Dune queries should quantify both, but COPM may end up being the primary signal.

---

## 8. Crypto Remittances Context

### 8.1 World Bank Remittance Prices Worldwide

- **URL**: https://remittanceprices.worldbank.org/
- **Corridor Data**: https://remittanceprices.worldbank.org/countrycorridors

Global average remittance cost: 6.49%. Digital remittances: 4.96%. Non-digital: 6.94%. Database covers 367 corridors from 48 sending to 105 receiving countries.

**Relevance to Our Project**: HIGH for calibration. The US-to-Colombia corridor cost is the benchmark our stablecoin flow data should be compared against. If stablecoin flows spike when corridor costs are high, we have identification.

---

### 8.2 Bitwage: "State of Stablecoins in Colombia" (September 2025)

- **URL**: https://bitwage.com/en-us/blog/state-of-stablecoins-in-colombia---september-2025

**Key Data Point**: Remittance inflows to Colombia hit $3.131 billion in Q1 2025.

**Relevance to Our Project**: HIGH. This is the real-economy benchmark. If our on-chain cCOP/COPM flows correlate with official remittance inflows (from BanRep Balance of Payments data), we have validation that stablecoin flows proxy for remittances.

---

## 9. Gap Analysis: What Has NOT Been Done

Based on this literature survey, the following are genuinely novel aspects of our project:

### 9.1 No Prior Derivatives on Stablecoin Flow Metrics
No paper or project has built a variance swap, futures contract, or any derivative instrument on stablecoin flow volume/velocity as an underlying. The closest is Feldmex (on-chain variance swaps on crypto price volatility), but that is on asset prices, not flow metrics.

### 9.2 No On-Chain Remittance Index
While IMF and BIS estimate bilateral stablecoin flows using geographic attribution, nobody has constructed a continuous "remittance index" from on-chain data that could serve as a settlement reference for derivatives. This is what our net USD-to-COP flow metric would become.

### 9.3 No Behavioral Fingerprinting for Remittance Identification on Stablecoins
The Bitcoin behavioral fingerprinting literature (Entity classification via representation learning, k-means + SVM clustering) has not been applied to stablecoin ecosystems to identify remittance-type flows specifically. Our work on cCOP/COPM behavioral fingerprinting is novel.

### 9.4 No Address Overlap Analysis Between Stablecoins for Population Calibration
No published work uses the overlap between addresses holding cCOP and COPM (or any pair of EM stablecoins) to estimate unique user populations or calibrate coverage ratios.

### 9.5 No Celo/Mento-Specific Academic Analysis
Despite Celo's focus on real-world payments and mobile-first design, there is zero academic analysis of Celo stablecoin flow patterns, Mento broker swap dynamics, or cCOP/COPM usage patterns.

---

## 10. Methodological Toolkit from the Literature

The following methods from the surveyed literature are directly applicable to our project:

| Method | Source | Application to Our Project |
|--------|--------|---------------------------|
| Web-traffic geographic attribution | IMF WP/25/141 (Reuter) | Not needed -- token is geographic signal |
| Gravity model for bilateral flows | BIS WP/1265 (Auer et al.) | Framework for modeling cCOP flow drivers |
| Granular instrumental variable (GIV) | IMF WP/26/056 (Aldasoro et al.) | Identification strategy for causal cCOP-to-FX link |
| SVAR-IV with heteroskedasticity | IMF WP/26/044 (Cerutti et al.) | Event-study for Colombia-specific shocks |
| TVP-VAR connectedness | DTS (2025) | Time-varying cCOP flow / COP-USD correlation |
| GARCH / copula models | arXiv:2505.10997 | Variance swap pricing from flow volatility |
| Representation learning fingerprinting | Applied Network Science (2023) | cCOP/COPM address classification |
| K-means + SVM clustering | PLOS ONE (2020) | User type decomposition |
| PPP-adjusted flow scaling | Chainalysis, IMF | Normalizing Colombian flow data |
| Exchange+survey data fusion | NBER WP/32945 | Validating on-chain data against DANE surveys |

---

## 11. Key Data Sources Identified

| Source | Type | Coverage | Access |
|--------|------|----------|--------|
| Dune Analytics (enriched stablecoin dataset) | On-chain | 37 EVM + Solana | Public queries |
| World Bank RPW | Remittance costs | 367 corridors | Public API |
| Chainalysis Geography of Crypto | Geographic attribution | Global | Report (gated) |
| BanRep Balance of Payments | Official remittances to Colombia | Colombia | Public |
| DANE household surveys | Colombian household income/consumption | Colombia | Public |
| Mento Reserve | cCOP supply/reserves | Celo | On-chain |
| Minteo Transparency | COPM supply/attestation | Celo | Public |
| CDS spreads (Colombian sovereign) | Sovereign risk | Colombia | Bloomberg/FRED |

---

## 12. Recommended Reading Priority

For immediate project needs, read in this order:

1. **IMF WP/26/056** (Aldasoro et al.) -- IV strategy for stablecoin-to-FX causal link
2. **BIS WP/1265** (Auer et al.) -- Gravity model + remittance cost association
3. **IMF WP/25/141** (Reuter) -- Geographic attribution methodology
4. **Applied Network Science (2023)** -- Fingerprinting entities via representation learning
5. **EPJ Data Science (2021)** -- Feature engineering for agent classification
6. **NBER WP/32945** -- Combining exchange data with household surveys
7. **Ferriani (2025)** -- CDS spread as adoption driver

---

## 13. Citation Notes

This literature review was compiled on 2026-04-02 through systematic web search. Several papers (especially IMF and BIS working papers) are available as open-access PDFs. The NBER papers may require institutional access. The Chainalysis Geography of Crypto reports are gated but summaries are publicly available through their blog posts. All URLs were verified at time of compilation.
