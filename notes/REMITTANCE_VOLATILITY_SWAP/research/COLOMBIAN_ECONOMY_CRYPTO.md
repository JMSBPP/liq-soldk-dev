# Colombian Economy, Crypto Adoption, and Remittance Structure

## Foundational Research for a Variance Swap on Net USD-to-COP Flows

**Date**: 2026-04-02
**Purpose**: Understand the structural features of the Colombian economy that determine WHO converts USD to COP on-chain and WHY, so that on-chain flow data can be correctly interpreted as a proxy for USD-denominated income conversion.

**Why Colombia**: Dune data (query #6939820) showed cCOP with 4,913 unique senders, the flattest transaction size distribution among Mento stablecoins (68.3% remittance-sized, only 66 whale-sized), and Colombia timezone activity patterns. This suggests a broad, retail-driven population rather than bot-dominated activity.

---

## Executive Summary

Colombia received a record USD 11.85 billion in remittances in 2024 (2.8% of GDP), with the US corridor accounting for 53% and Spain ~20%. Remittances have risen from 1.1% of GDP a decade ago to their current all-time high share, making them the country's second-largest foreign exchange inflow after oil. The Colombian peso has experienced extreme volatility -- from ~3,500/USD in early 2020 to a peak of 5,133/USD in November 2022 after President Petro's election, recovering to ~3,700-4,400 range in 2024-2025. This currency instability, combined with 56% informal employment, 49% of workers earning below minimum wage, and a fiscal crisis (6.8% deficit in 2024), creates strong structural demand for USD-denominated savings and hedging instruments.

Colombia's crypto ecosystem is maturing rapidly: over 2.5 million crypto owners (4.8% of population), $44.2 billion in crypto transaction volume (2024), and a financial sandbox that has graduated into permanent bank-exchange integrations (Bancolombia/Wenia, Banco de Bogota/Bitso). The MoneyGram USDC app launched in Colombia as its first market (September 2025), Littio has 200,000+ users holding yield-bearing USDC accounts, and Nequi (21 million users) now integrates crypto purchases via Wenia. The MiniPay/El Dorado integration (November 2025) provides a direct Celo stablecoin-to-COP offramp.

**Key structural insight for the variance swap**: Net USD-to-COP flows on-chain are driven by at least four distinct populations with different economic motivations and shock sensitivities:

1. **Remittance receivers** (dominant by volume) -- US and Spain corridors; sensitive to US/Spanish labor markets, immigration policy, COP depreciation
2. **Freelancers/remote workers** (fast-growing) -- tech, BPO, creative sectors; sensitive to US tech spending, platform economics, COP/USD spread incentives
3. **Venezuelan diaspora** (~2.9M in Colombia) -- bidirectional flows; sensitive to Venezuelan crisis dynamics, documentation status, informal channel usage
4. **Crypto-native savers/hedgers** -- Littio users, DeFi participants; sensitive to COP volatility events, Petro policy shocks, yield differentials

A variance swap on net COP flows must either isolate one signal or model their mixture. The flatness of the cCOP transaction size distribution suggests a genuine retail population, not institutional or bot-driven activity.

---

## 1. Remittance Structure

### 1.1 Market Size and GDP Share

| Year | Remittances (USD B) | % of GDP | YoY Growth |
|------|---------------------|----------|------------|
| 2019 | 6.77 | ~2.0% | -- |
| 2020 | 6.85 | ~2.3% | +1.2% |
| 2021 | 8.60 | ~2.5% | +25.5% |
| 2022 | 9.49 | ~2.5% | +10.3% |
| 2023 | 10.09 | ~2.5% | +6.3% |
| 2024 | 11.85 | 2.8% | +17.4% |
| 2025 H1 | 7.57 (annualized ~15B) | est. ~3.0% | +14.1% YoY |

Sources: [BanRep: Recent Evolution of Remittance Inflows](https://www.banrep.gov.co/en/blog/recent-evolution-remittance-inflows-colombia); [BBVA Research: Remittances Matter](https://www.bbvaresearch.com/en/publicaciones/colombia-remittances-matter-and-more-than-ever/); [BanRep: Macroeconomic Results 2024](https://www.banrep.gov.co/en/blog/macroeconomic-results-2024-outlook-2025); [TradingEconomics: Colombia Remittances](https://tradingeconomics.com/colombia/remittances)

**Critical context**: Remittances crossed the USD 1 billion/month threshold for the first time in June 2024 and have maintained that level. The 2.8% GDP share is an ALL-TIME HIGH, up from just 1.1% a decade ago. Remittances now represent:
- 79% of oil export value
- 3x coffee export value
- 3.6% of disposable household income
- 3.9% of household consumption

This is NOT a declining flow -- it is accelerating and becoming more structurally important.

### 1.2 Top Corridors

| Rank | Corridor | Share of Total | Estimated USD B (2024) |
|------|----------|---------------|------------------------|
| 1 | United States | 53% | ~6.28 |
| 2 | Spain | ~20% | ~2.37 |
| 3 | Chile | ~5% | ~0.59 |
| 4 | Ecuador | ~3% | ~0.36 |
| 5 | Venezuela (reverse) | significant | (see section 1.5) |
| 6 | Other LATAM + Europe | ~19% | ~2.25 |

Sources: [BanRep: Box 3 - October 2024 Monetary Policy Report](https://www.banrep.gov.co/en/publications-research/monetary-policy-report/box-3-october-2024); [BBVA Research: Remittances Matter](https://www.bbvaresearch.com/en/publicaciones/colombia-remittances-matter-and-more-than-ever/)

**Structural implications for the variance swap**:
- The US corridor (53%) is overwhelmingly dominant. US-based Colombians have the easiest access to USDC on-ramps (Coinbase, MoneyGram app, etc.), making this the corridor most likely to shift to stablecoin rails.
- Spain (~20%) is notable because the Spain-Colombia corridor already has ~15% digital remittance penetration (end-to-end digital), the highest digital share of any Colombian corridor. Source: [Inter-American Dialogue](https://thedialogue.org/blogs/2025/04/the-state-of-the-remittance-industry-and-an-outlook-for-2025/)
- Unlike the Philippines (where Gulf corridors are significant), Colombia's remittance sources are concentrated in countries with mature crypto infrastructure (US, Spain, Chile).

### 1.3 Geographic Distribution Within Colombia

| Department | Share of Remittances Received |
|------------|------------------------------|
| Valle del Cauca | 26% |
| Cundinamarca (Bogota) | 16% |
| Antioquia (Medellin) | 16% |
| Risaralda (Coffee region) | 5% |
| Other | 37% |

Source: [BBVA Research: Remittances, the extra income](https://www.bbvaresearch.com/en/publicaciones/colombia-remittances-the-extra-income-that-balances-the-pockets-of-families/); [AmericaEconomia: Colombia Q1 2024](https://www.americaeconomia.com/en/negocios-e-industrias/colombia-reached-highest-receipt-remittances-its-history-during-first-quarter)

Valle del Cauca (Cali metropolitan area) alone receives over a quarter of all remittances. These three departments account for 58.1% of total flows. This geographic concentration matters for on-chain analysis because wallet clustering by timezone/activity patterns could help identify remittance-driven vs. other populations.

### 1.4 Crypto vs. Traditional Remittance Rails

**Traditional channels still dominate**: Western Union, MoneyGram (traditional), bank wires, and increasingly Nequi/Payoneer partnerships handle the vast majority. The average remittance cost for the US-Colombia corridor is approximately 4-6%.

**Stablecoin remittance is emerging with institutional backing**:

- **MoneyGram USDC App** (September 2025): Colombia was chosen as the FIRST market for MoneyGram's stablecoin-powered app. Users receive money into a USDC balance (powered by Circle/Stellar) and can store, spend, or cash out at 6,000+ MoneyGram locations in Colombia. Source: [Blockworks: MoneyGram stablecoin app Colombia](https://blockworks.com/news/moneygram-stablecoin-app-colombia)
- **Crypto remittance share**: No authoritative Colombia-specific figure exists. The Inter-American Dialogue estimates crypto remittances at 3-6% of global volume. For Colombia specifically, Chainalysis estimated 9% of Venezuelan remittance volume ($461M in 2023) was crypto-mediated. Source: [Inter-American Dialogue: Assessing Cryptocurrency in Remittances to LAC](https://thedialogue.org/blogs/2024/09/assessing-cryptocurrency-in-remittances-to-latin-america-and-the-caribbean)
- **Fee advantage**: Traditional rails charge 4-6%, while crypto rails typically cost <1.5% including on/off ramp fees. This creates persistent economic incentive for adoption.

**Implication for on-chain data**: If total remittances are ~$12B/year and crypto remittances are 3-6%, that suggests $360M-$720M/year in stablecoin-mediated conversion flows. Monthly: ~$30M-$60M. As MoneyGram's app scales, this could grow rapidly.

### 1.5 Venezuelan Diaspora Flows

Colombia hosts approximately 2.9 million Venezuelan refugees and migrants (as of November 2025), making it the largest host country globally. Source: [ReliefWeb: Venezuelan Refugees and Migrants - November 2025](https://reliefweb.int/report/colombia/venezuelan-refugees-and-migrants-region-november-2025)

Key dynamics:
- Very few Venezuelan migrants have Colombian bank accounts -- they exist outside formal financial systems and lack documentation
- **Valiu** (Mercy Corps-backed): Digital remittance platform allowing Colombia-to-Venezuela transfers with 8% fixed fee, arriving in hours. Uses crypto rails internally. Source: [Mercy Corps: Valiu](https://www.mercycorps.org/what-we-do/ventures/valiu)
- Venezuela receives ~$3.7 billion in remittances (5% of GDP), up over 10,000% since 2014. Chainalysis estimated 9% ($461M in 2023) was via crypto. Source: [Diaspora for Development: Venezuela](https://diasporafordevelopment.eu/wp-content/uploads/2024/05/CF_Venezuela-v.2.pdf)
- **Bidirectional flow**: Venezuelans in Colombia SEND money to Venezuela AND receive from Venezuelan diaspora elsewhere. This creates complex flow patterns in on-chain data.
- Several Venezuelan retail chains that previously accepted crypto no longer do (as of 2024), but P2P and remittance usage continues.

**Variance swap implication**: Venezuelan-related flows add noise to the COP conversion signal because they may involve COP-to-VES conversion chains (COP -> USDT -> VES), not pure USD-to-COP income conversion. These flows are likely identifiable by smaller transaction sizes and higher frequency.

### 1.6 BanRep Data Availability

Banco de la Republica publishes:
- **Quarterly**: Balance of Payments data including remittance aggregates
- **Monthly**: Family remittance totals (crossed $1B/month threshold June 2024)
- **Corridor breakdown**: Available in Monetary Policy Reports and special blog posts, but NOT as a downloadable monthly time series by country of origin
- **Department-level**: Published quarterly (Valle del Cauca, Cundinamarca, Antioquia breakdowns)

Source: [BanRep Data and Statistics](https://www.banrep.gov.co/en/taxonomy/term/5847); [BanRep Economic Statistics Site](https://www.banrep.gov.co/estad/dsbb/imfcolom.htm)

The monthly aggregate is useful for calibrating on-chain flow estimates against official totals. Department-level data could potentially be cross-referenced with on-chain wallet clustering.

---

## 2. Freelancer / Remote Worker Economy

### 2.1 Market Size

Colombia has a large and growing remote work sector, though precise figures are difficult to pin down:

- **Upwork**: Colombia is one of the top freelancer countries in Latin America, with significant presence in software development, design, writing, and virtual assistance
- **Indeed**: Over 179,000 remote job listings for Colombia-based workers
- **Arc.dev**: Colombia is highlighted as a top-2% freelancer market in Latin America
- Remote work grew substantially post-COVID and has been sustained by COP weakness (making Colombian labor extremely price-competitive internationally)

Source: [Workana: Colombia Jobs](https://www.workana.com/en/jobs?country=CO); [Arc.dev: Colombia Freelancers](https://arc.dev/en-co)

### 2.2 Payment Platforms and Crypto Usage

Colombian freelancers use a layered payment stack:

| Platform | Function | COP Conversion | Crypto Option |
|----------|----------|---------------|---------------|
| **Payoneer** | USD receiving account from Upwork/Fiverr | 1% fee (min $12) | No native crypto |
| **Deel** | Employer-of-record payroll | Bank transfer | USDC/USDT withdrawal option |
| **Wise** | Multi-currency account | Competitive FX | No crypto |
| **Nequi + Payoneer** | Direct USD-to-COP via partnership (March 2025) | Minutes, in COP | Via Wenia integration |
| **Parallax/Grey** | USD receiving + stablecoin conversion | Via USDC/USDT | Native crypto |
| **Direct crypto** | USDC/USDT salary payment | Self-managed | Native |

Source: [TransFi: Colombian Remote Workers Upwork](https://www.transfi.com/blog/how-colombian-remote-workers-on-upwork-can-easily-get-paid-in-usd); [Parallax: Deel Withdrawal Methods](https://www.withparallax.com/en/blog/7-best-withdrawal-methods-on-deel); [Fintech Global: Nequi-Payoneer Partnership](https://fintech.global/2025/03/07/nequi-and-payoneer-partner-to-simplify-cross-border-payments-for-colombian-entrepreneurs/)

**Key insight**: The Nequi-Payoneer partnership (March 2025) is particularly significant because it allows Colombian freelancers to receive USD from Payoneer directly into their Nequi wallet (converted to COP in minutes). This competes with crypto rails but also normalizes the USD-to-COP conversion pattern.

### 2.3 Income Levels

- **Average Colombian salary**: COP 2,200,000/month (~$533 USD)
- **Median Colombian income**: COP 1,100,000-1,400,000/month (~$280-$340 USD)
- **Bogota average**: COP 5,420,000/month (~$1,225 USD)
- **49% of employed Colombians**: Earn below minimum wage (COP 1,300,000 in 2024)
- **Remote worker premium**: Colombian remote workers for US companies typically earn $1,000-$4,000/month, representing 3-12x median local income

Sources: [RemotePeople: Average Salary Colombia](https://remotepeople.com/countries/colombia/average-salary/); [TimeCamp: Average Salary Colombia 2024](https://statistics.timecamp.com/average-salary/colombia/)

**Variance swap implication**: The 3-12x income premium for remote workers creates strong incentive to maintain USD-denominated earnings and convert only as needed. This population likely converts in regular, moderate-sized transactions ($200-$2,000 range) -- exactly matching the "remittance-sized" category in the Dune data.

### 2.4 Tax Treatment of Crypto Income

- Colombia does NOT have a specific crypto tax law. Crypto is treated as property/intangible assets.
- **Law 2277 of 2022** (Petro's tax reform): Broadened VAT application and hiked personal income tax rates and capital gains, but did not create crypto-specific provisions.
- **Resolution 000240** (December 24, 2025): DIAN (Colombia's tax authority) mandated that crypto exchanges, brokers, and platforms report detailed user and transaction data starting from the 2026 tax year. First full report due May 2027.
- Reported data includes: identity details, tax IDs, volumes, units transferred, market values, net balances -- covering BTC, ETH, stablecoins, and all other digital assets.
- Non-compliance penalties: fines up to 1% of unreported transaction values.

Sources: [CMS Expert Guide: Crypto Regulation Colombia](https://cms.law/en/int/expert-guides/cms-expert-guide-to-crypto-regulation/colombia); [CoinLaw: Colombia Crypto Tax Reporting 2026](https://coinlaw.io/colombia-crypto-tax-reporting-2026/); [BeinCrypto: Colombia France Crypto Tax Changes](https://beincrypto.com/colombia-france-crypto-tax-reporting-2026/)

**Important**: The December 2025 reporting mandate signals that Colombia is moving toward full crypto transaction visibility. This may push some users away from centralized exchanges toward DeFi/P2P rails, potentially increasing on-chain Celo/Mento activity.

---

## 3. Crypto Adoption in Colombia

### 3.1 Adoption Metrics

| Metric | Value | Source |
|--------|-------|--------|
| Crypto owners | 2.5+ million | Triple-A |
| % of population | 4.8% | Triple-A |
| Crypto transaction volume (2024) | $44.2 billion | Chainalysis 2025 |
| LATAM ranking by volume | 5th (after Brazil, Argentina, Mexico, Venezuela) | Chainalysis 2025 |
| Chainalysis Global Adoption Index (2022) | 15th (P2P sub-index) | Chainalysis 2022 |
| Stablecoin share of exchange purchases | >50% (Jul 2024-Jun 2025) | Chainalysis 2025 |

Sources: [Triple-A: Cryptocurrency Data Colombia](https://www.triple-a.io/cryptocurrency-data/colombia); [Chainalysis: 2025 LATAM Crypto Adoption](https://www.chainalysis.com/blog/latin-america-crypto-adoption-2025/)

**Stablecoin dominance**: More than half of all exchange purchases in the COP market are stablecoin purchases. This is critical -- it means the primary use case for Colombian crypto users is obtaining dollar-denominated stable value, not speculation on volatile assets.

### 3.2 Major Exchanges and Platforms

#### Bitso Colombia
- Over 6 million users across LATAM (Mexico, Argentina, Colombia, Brazil)
- COP on/off ramps via direct bank integration
- Processed $43 billion in US-Mexico remittances in 2024 (demonstrates remittance infrastructure capability)
- Partnered with Banco de Bogota in SFC sandbox

Source: [Bitso: Panorama Cripto LATAM 2024](https://blog.bitso.com/wp-content/uploads/2025/03/100325_FINAL-INFORME_BITSO-ESPANOL.pdf)

#### Binance Colombia
- Largest global exchange with extensive COP P2P market
- COP deposits via bank transfers, P2P, credit/debit cards
- P2P supports all major Colombian banks: Bancolombia, Banco de Bogota, Daviplata, Nequi
- Partnered with Davivienda in SFC sandbox (via Powwi)
- Specific COP P2P volume data not publicly available

Source: [Binance P2P: COP Trading](https://p2p.binance.com/en/trade/BancolombiaSA/USDT?fiat=COP)

#### Buda.com
- Chilean-headquartered LATAM exchange operating in Colombia
- COP deposits/withdrawals via PSE bank transfers
- Partnered with Banco de Bogota in SFC sandbox
- Smaller but regulated, trusted by institutional users

Source: [Buda.com Colombia](https://www.buda.com/colombia)

#### Bancolombia / Wenia (May 2024)
- Colombia's largest bank launched Wenia crypto platform
- Anyone with Bancolombia savings/checking account can trade crypto
- Integrated with Nequi (21M users) for crypto purchases
- 69% monthly transaction growth after Nequi integration

Source: [Finacle: Nequi Drives Crypto Adoption](https://www.finacle.com/client-stories/case-studies/nequi-drives-crypto-adoption/)

### 3.3 Minteo / COPM Stablecoin

**Launched**: April 10, 2024
**What it is**: First fully-reserved stablecoin pegged 1:1 to the Colombian peso (COP). Each COPM is backed by one peso held in a regulated Colombian bank, audited monthly by BDO.
**Distribution**: Primarily through Littio; 100,000+ Colombian users at launch.
**Use cases**: Fintech settlement, e-commerce payouts, remittance conversion.
**Funding**: $4.3M from institutional investors (2022).
**Expansion**: Plans for Mexico, Chile, Peru.

Sources: [Yahoo Finance: Minteo Launches Settlement Layer](https://finance.yahoo.com/news/minteo-launches-stablecoin-based-settlement-130000239.html); [Valora Analitik: Minteo lanza COPM](https://www.valoraanalitik.com/2024/04/13/minteo-lanza-copm-la-primera-stablecoin-del-peso-colombiano/); [Minteo Transparency](https://transparency.minteo.com/)

**Variance swap relevance**: COPM represents the COP side of on-chain COP/USD conversion. Swaps between USDC and COPM (or cCOP) are direct proxies for the income conversion behavior we want to measure.

### 3.4 MiniPay / El Dorado Integration (November 2025)

- **MiniPay** (Opera/Celo): Non-custodial stablecoin wallet on Celo, 10M+ users globally
- **El Dorado**: P2P on/offramp marketplace operating in 6 LATAM countries (Colombia, Brazil, Argentina, Bolivia, Paraguay, Peru)
- **Integration announced at Devconnect Argentina** (November 19, 2025): El Dorado integrated into MiniPay for COP-to-stablecoin and stablecoin-to-COP conversion
- Also supports PIX (Brazil) and Mercado Pago payments from stablecoin balances
- Supports USDT, cUSD, and USDC on Celo

Sources: [Opera: MiniPay connects stablecoins to real-time payment in LatAm](https://press.opera.com/2025/11/19/minipay-pay-like-a-local-mercadopago-pix/); [CoinDesk: USDT Spending Mainstream with MiniPay](https://www.coindesk.com/business/2025/11/19/stablecoin-spending-goes-mainstream-with-opera-minipay-s-latam-integration/)

**This is directly relevant to the variance swap**: The MiniPay/El Dorado integration creates a direct path from Celo stablecoins (cUSD, USDC) to COP via P2P market. Activity on this rail would show up in the cCOP/COPm transfer data we already have from Dune.

### 3.5 Littio

**What it is**: YC and Circle-backed Colombian neobank that allows users to save in USD (USDC) and earn yield on deposits.
**Users**: 200,000+ Colombians (as of early 2025, up from 80,000 in late 2024).
**Key product**: "Yield Pot" -- users deposit COP, which is converted to USDC and invested in tokenized T-bills via OpenTrade on Avalanche. Up to 12% E.A. on digital dollars.
**Volume**: Over $100M USDC yield subscription volume through OpenTrade.
**Yield paid**: $250,000 in user earnings in first 4 months.
**Shock response**: During the January 2025 Trump-Petro tariff confrontation, Littio saw >100% growth in new USDC yield accounts in 48 hours.

Sources: [OpenTrade: Littio Case Study](https://www.opentrade.io/case-studies/littio); [CryptoTimes: Stablecoins Support Colombia's Economy](https://www.cryptotimes.io/2025/02/24/stablecoins-support-colombias-economy-amid-trump-tariff-threats/); [Circle: Littio x USDC](https://www.circle.com/blog/littio-x-usdc-creating-stable-and-secure-banking-in-latam); [CoinDesk: Littio Ditches Ethereum for Avalanche](https://www.coindesk.com/business/2024/10/09/latam-bank-littio-ditches-ethereum-for-avalanche-as-demand-for-rwa-vaults-grows)

**Variance swap relevance**: Littio users represent the "crypto-native saver/hedger" population. Their behavior is driven by COP depreciation fear and yield-seeking. Flows related to Littio (COP -> USDC for savings) would create OUTFLOW pressure on COP on-chain markets, which is the OPPOSITE direction from remittance/freelancer income conversion (USD -> COP). This bidirectional flow creates the variance we want to trade.

---

## 4. COP/USD Exchange Rate History

### 4.1 Exchange Rate Timeline

| Date | COP/USD | Event |
|------|---------|-------|
| Jan 2020 | ~3,450 | Pre-COVID baseline |
| Mar 2020 | ~4,200 | COVID panic; flight to USD |
| Dec 2020 | ~3,450 | Recovery |
| Dec 2021 | ~3,950 | Global inflation + EM pressure |
| Jun 2022 | ~3,900 | Petro election (June 19) |
| Jul 2022 | ~4,600 | Post-election uncertainty |
| Nov 2022 | **5,133** | **All-time peak depreciation** |
| Dec 2023 | 3,822 | Recovery (Petro policy moderation + high BanRep rates) |
| Dec 2024 | 4,409 | Renewed depreciation; fiscal crisis |
| Q1 2025 | 3,700-4,460 | Volatile; tariff shock spike then recovery |
| Apr 2026 | ~4,050 | Current (average YTD 2025: 4,052) |

Sources: [EBC Financial Group: Dollar vs Colombian Peso](https://www.ebc.com/forex/dollar-vs-colombian-peso-historical-and-future-outlook); [FocusEconomics: Colombia Exchange Rate](https://www.focus-economics.com/country-indicator/colombia/exchange-rate/); [Medellin Advisors: USD vs COP](https://www.medellinadvisors.com/what-is-happening-usd-vs-cop-exchange-rate-and-inflation-in-colombia/); [Wise: USD to COP Rate History](https://wise.com/us/currency-converter/usd-to-cop-rate/history)

### 4.2 Major Depreciation Events and Causes

1. **COVID-19 (March 2020)**: ~3,450 to ~4,200. Capital flight, oil price collapse (Colombia is an oil exporter). Recovered by year-end.

2. **Petro Election Shock (June-November 2022)**: ~3,900 to 5,133. Political uncertainty over reform agenda (energy transition, pension reform, land reform, tax reform). The peso lost over 30% in 5 months. This was the WORST depreciation event in recent Colombian history.

3. **Fiscal Crisis (2024)**: Deficit hit 6.8% of GDP (above 5.6% target). Petro suspended the fiscal rule. FDI plummeted 45.6% from 2022 levels. COP weakened from 3,822 to 4,409.

4. **Trump Tariff Confrontation (January 2025)**: Brief tariff escalation between Trump and Petro. COP spiked to 4,459 before recovering. Littio saw 100%+ growth in USDC account openings during this 48-hour event.

5. **Economic Emergency Declaration (December 2025)**: Petro declared state of economic and social emergency, authorizing emergency fiscal measures. Signaled deep structural fiscal problems.

### 4.3 Inflation History

| Year | Annual CPI Inflation |
|------|---------------------|
| 2020 | 1.6% (COVID deflationary) |
| 2021 | 3.5% |
| 2022 | 10.2% |
| 2023 | 11.7% |
| 2024 | 6.6% |
| 2025 | 5.1% (Dec), trending down |
| 2026 Jan | 5.35% |

Source: [TradingEconomics: Colombia Inflation CPI](https://tradingeconomics.com/colombia/inflation-cpi); [Macrotrends: Colombia Inflation Rate](https://www.macrotrends.net/global-metrics/countries/col/colombia/inflation-rate-cpi)

BanRep's target is 3%. Inflation has been ABOVE target since 2022, with double-digit peaks in 2022-2023 driven by COP depreciation, global commodity prices, and supply chain disruption. Still elevated at 5.1-5.4% in early 2026.

### 4.4 Capital Controls

Colombia does NOT have formal capital controls in the traditional sense. The peso is freely floating. However:
- Cross-border transactions above certain thresholds require DIAN reporting
- The new Resolution 000240 (December 2025) mandates crypto transaction reporting from 2026
- No restrictions on holding USD accounts or USD-denominated assets
- Littio/USDC savings accounts are legal and operating openly
- The SFC has explicitly stated it does NOT supervise crypto, creating a permissive-by-omission environment

Source: [US State Department: 2025 Investment Climate Statement - Colombia](https://www.state.gov/reports/2025-investment-climate-statements/colombia)

---

## 5. Economic Vulnerability / Income Structure

### 5.1 Income Distribution

| Metric | Value |
|--------|-------|
| Median monthly income | COP 1,100,000-1,400,000 (~$280-$340) |
| Average gross monthly salary | COP 2,200,000 (~$533) |
| Bogota average | COP 5,420,000 (~$1,225) |
| Minimum wage (2024) | COP 1,300,000 (~$315) |
| Workers earning below minimum | 49% (~11.4 million people) |
| Gini coefficient | 0.50 (high inequality) |
| Median household annual income | COP 24,000,000 (~$5,800) |

Sources: [DANE: Gran Encuesta Integrada de Hogares 2024](https://www.dane.gov.co); [DevsData: Average Salary Colombia 2024](https://devsdata.com/average-salary-in-colombia-comprehensive-report/); [BanRep: Distribution, Inequality and Poverty](https://repositorio.banrep.gov.co/bitstream/handle/20.500.12134/10934/be_1279.pdf)

### 5.2 Informal Economy

| Metric | Value |
|--------|-------|
| Informal employment (national, 2024) | 55.4-56% |
| Informal employment (urban, 2024) | 43.6% |
| Historical baseline (2010) | 67.9% |
| Workers without formal contracts | ~12.5 million |

Source: [OECD Cogito: Can Colombia Turn the Corner on Informal Work](https://oecdcogito.blog/2025/05/14/can-colombia-turn-the-corner-on-informal-work/); [Statista: Informal Employment Share Colombia 2023](https://www.statista.com/statistics/1039930/informal-employment-share-colombia/)

The 56% informality rate is crucial. Informal workers:
- Cannot easily access traditional banking remittance channels
- Are more likely to use P2P/cash-based conversion methods
- Have stronger incentive to use crypto rails that don't require formal documentation
- Are the population MOST vulnerable to COP depreciation (no hedging access)

### 5.3 Remittance Dependence

| Metric | Value |
|--------|-------|
| Remittances as % of GDP | 2.8% (2024, all-time high) |
| Remittances as % of disposable income | 3.6% (2023) |
| Remittances as % of household consumption | 3.9% (2023) |
| Remittances vs. oil exports | 79% of oil value |
| Remittances vs. coffee exports | 3x coffee value |
| Estimated households dependent on remittances | Millions (Valle del Cauca, Antioquia, Cundinamarca concentrated) |

Source: [BBVA Research: Remittances Matter](https://www.bbvaresearch.com/en/publicaciones/colombia-remittances-matter-and-more-than-ever/); [Rio Times: Colombia Remittances Surge](https://www.riotimesonline.com/colombias-remittances-surge-a-lifeline-for-families-and-the-economy/)

### 5.4 Key Economic Shocks Affecting Households

1. **COVID-19 (2020)**: GDP contraction, informal workers devastated
2. **Petro election + reform agenda (2022-present)**: Peso crash, inflation spike, uncertainty
3. **Global commodity price shock (2022-2023)**: Food/energy inflation hit hardest on lowest-income households
4. **Fiscal crisis (2024-2025)**: Deficit at 6.8%, FDI collapse (-45.6%), economic emergency declared
5. **Trump tariff confrontation (January 2025)**: Brief but intense COP spike; demonstrated vulnerability
6. **Oil production decline**: Petro's anti-extraction policies threaten Colombia's primary export earner

---

## 6. Competing/Complementary Services

### 6.1 Nequi (Dominant Mobile Wallet)

- **Users**: 21 million (claimed), 13+ million active (H1 2025)
- **Owner**: Bancolombia Group
- **Crypto integration**: Via Wenia platform (May 2024); users can buy/sell BTC, ETH, stablecoins directly from Nequi
- **Cross-border**: Nequi-Payoneer partnership (March 2025) enables USD-to-COP deposits for freelancers
- **USDC payments**: Via Zypto App/PayAbroad integration -- scan Nequi QR code to pay with USDC (Stellar)
- **Record**: 66 million transactions in a single day (June 28, 2024)

Sources: [Finacle: Nequi Drives Crypto Adoption](https://www.finacle.com/client-stories/case-studies/nequi-drives-crypto-adoption/); [Zypto: Pay with USDC in Colombia via Nequi](https://zypto.com/blog/zypto-app/pay-with-usdc-colombia-nequi/); [EBANX: Nequi Digital Wallet Colombia](https://insights.ebanx.com/en/resources/nequi-digital-wallet-in-colombia/)

### 6.2 Daviplata

- **Owner**: Davivienda bank
- **Users**: Millions of accounts (one of top 3 Colombian neobanks alongside Nequi and MOVii)
- **Crypto**: No direct crypto trading, but Daviplata is accepted as a payment method on Binance P2P and other P2P markets for buying USDT/BTC
- **Role**: Primarily used for government subsidy payments, basic transfers; lower-income user base than Nequi

### 6.3 MOVii

- **Crypto sandbox participant**: Partnered with Panda and Bitpoint in SFC sandbox
- **Cash-in/cash-out operations**: Enables fiat on/off ramps for crypto exchanges
- **Role**: Digital wallet serving unbanked/underbanked populations

Source: [CMS Expert Guide: Crypto Regulation Colombia](https://cms.law/en/int/expert-guides/cms-expert-guide-to-crypto-regulation/colombia)

### 6.4 RappiPay

- **Parent**: Rappi (Colombia's first unicorn, super-app for delivery/fintech)
- **Financial products**: Credit cards (200,000+), savings accounts (300,000+, at 14% interest rate)
- **Assets**: COP 442.9 billion in total assets (September 2025)
- **Users**: ~750,000
- **Crypto**: No direct crypto integration currently; focused on traditional financial products
- **IPO**: Evaluating late 2026 IPO; profitable for 4+ consecutive quarters

Source: [Americas Quarterly: Colombia's First Unicorn Keeps Delivering](https://www.americasquarterly.org/article/colombias-first-unicorn-keeps-delivering/); [ColombiaOne: Rappi](https://colombiaone.com/2025/01/06/rappi-colombia/)

### 6.5 El Dorado P2P

- **Function**: P2P marketplace for buying/selling USDT at market rates in COP (and 5 other LATAM currencies)
- **How it works**: Users post buy/sell orders; counterparties settle via bank transfer, Nequi, Daviplata, or cash; USDT held in escrow during transaction
- **Spread**: Transparent pricing with visible buy/sell spreads
- **Countries**: Colombia, Brazil, Argentina, Bolivia, Paraguay, Peru
- **Now integrated into MiniPay** (November 2025): Direct on/offramp for Celo stablecoins

Source: [El Dorado](https://eldorado.io/en); [El Dorado Blog: Celo Stablecoin Rise](https://eldorado.io/en/blog/celo-stablecoin-rise/)

---

## 7. Regulatory Environment

### 7.1 Current Framework

Colombia has NO specific crypto legislation. The regulatory landscape is defined by:

1. **SFC (Superintendencia Financiera)**: Explicitly states it does NOT regulate, supervise, or approve crypto operations. Crypto is not legal tender, not securities, not under financial supervision. Source: [SFC: Statement on Cryptocurrencies](https://www.superfinanciera.gov.co/publicaciones/10115249/)

2. **SFC Sandbox (2021-2023)**: One-year pilot program that allowed 9 crypto firms to test bank-exchange integrations under supervision. Participants included:
   - Bancolombia + Gemini
   - Davivienda + Binance (via Powwi)
   - Banco de Bogota + Bitso + Buda.com
   - Coltefinanciera + Obsidiam
   - Coink + Banexcoin
   - MOVii + Panda + Bitpoint
   
   The sandbox concluded December 2023. Its success led to permanent integrations (Bancolombia/Wenia launched May 2024).

Source: [Bitcoin Magazine: Colombia Sandbox](https://bitcoinmagazine.com/business/with-bitcoin-to-bank-sandbox-colombia-will-become-btc-haven); [CoinDesk: Colombia Crypto Use Soars](https://www.coindesk.com/policy/2021/04/30/colombias-crypto-use-soars-and-local-regulators-step-in/)

3. **AML/KYC obligations**: VASPs must comply with anti-money laundering regulations under UIAF (Financial Intelligence Unit). No specific VASP licensing regime yet.

4. **Pending legislation**: Colombian senators have introduced multiple crypto regulation bills (most recently in 2024-2025), but none have passed. The legislative approach has been slow, with the government focused on fiscal emergencies.

Source: [Digital Watch: Colombian Lawmakers Push for Crypto Regulations](https://dig.watch/updates/colombian-lawmakers-push-for-crypto-regulations); [CryptoNews: Colombia Senators Fresh Bid](https://cryptonews.com/news/colombia-senators-launch-fresh-bid-to-regulate-crypto/)

### 7.2 Tax Treatment

- Crypto is treated as intangible assets for tax purposes
- Capital gains from crypto sales are taxable under general income tax rules
- No crypto-specific tax rates or exemptions
- **Law 2277 of 2022**: Petro's tax reform raised personal income tax rates and capital gains taxes broadly; did not single out crypto but increased the overall tax burden on asset gains
- **Resolution 000240 (December 2025)**: Mandates comprehensive crypto transaction reporting by exchanges/platforms starting 2026 tax year. Aligns with OECD CARF (Crypto-Asset Reporting Framework).

Source: [Lightspark: Is Crypto Legal in Colombia](https://www.lightspark.com/knowledge/is-crypto-legal-in-colombia); [Scorechain: Strengthening Cryptocurrency Regulations Colombia](https://www.scorechain.com/blog/strengthening-cryptocurrency-regulations-in-colombia-is-your-business-ready/)

### 7.3 Stablecoin-Specific Regulation

**None**. There is no stablecoin-specific regulation in Colombia. COPM (Minteo) and cCOP (Mento/Celo) operate without specific regulatory approval or prohibition. The SFC's position of non-supervision creates a permissive-by-omission environment. This could change if pending legislation passes, but there is no immediate regulatory threat to stablecoin operations.

### 7.4 Regulatory Risk Assessment

| Factor | Risk Level | Notes |
|--------|-----------|-------|
| Outright ban | Very Low | No political appetite; too much adoption |
| Exchange restrictions | Low-Medium | SFC sandbox graduated to permanent integrations |
| Tax reporting burden | Medium | Resolution 000240 adds compliance costs; may push to DeFi |
| Stablecoin regulation | Low (near-term) | No legislation pending; permissive by omission |
| Capital controls | Very Low | Free-floating peso; no restrictions on USD holdings |
| AML enforcement | Medium | UIAF active; may increase pressure on P2P markets |

---

## 8. Synthesis: Who Converts USD to COP On-Chain and Why?

### 8.1 Population Decomposition

Based on the structural analysis above, the on-chain USD-to-COP conversion population likely decomposes as:

| Population | Estimated Share | Transaction Pattern | Shock Sensitivity |
|------------|----------------|--------------------|--------------------|
| **Remittance receivers** | 40-50% | Regular, moderate-sized ($100-$500), monthly/biweekly | US employment, immigration policy, COP/USD spread |
| **Freelancer income conversion** | 20-30% | Regular, larger ($500-$2,000), monthly | US tech spending, platform economics, tax events |
| **Venezuelan diaspora** | 5-10% | Small, frequent, P2P-heavy | Venezuelan crisis, documentation status |
| **Crypto-native savers (reverse: COP->USD)** | 10-20% | Event-driven, clustered during COP crisis events | Petro policies, fiscal shocks, yield differentials |
| **Speculative/trading** | 5-10% | Erratic, correlated with crypto market cycles | BTC/ETH price, Celo ecosystem events |

### 8.2 Evidence Supporting Colombia as Variance Swap Target

1. **Flat transaction distribution** (68.3% remittance-sized, only 66 whale transactions): Strongly suggests genuine retail usage, not institutional or bot activity.

2. **4,913 unique senders**: More sender diversity than any other Mento stablecoin except cREAL (which has fewer unique senders per swap but more bot-like patterns).

3. **Structural USD demand**: 56% informal employment + 49% below minimum wage + remittances at 2.8% GDP = large population that NEEDS USD-to-COP conversion and cannot access traditional hedging.

4. **Bidirectional flow**: Remittance/freelancer income creates USD-to-COP pressure; Littio/savings creates COP-to-USD pressure. This bidirectional flow is exactly what creates VARIANCE in net flows.

5. **Macro sensitivity**: COP has exhibited extreme event-driven volatility (5,133 peak in 2022, tariff spike in 2025, economic emergency December 2025). Each event creates measurable spikes in on-chain conversion activity (demonstrated by Littio's 100%+ growth during tariff confrontation).

6. **Growing infrastructure**: MoneyGram USDC (September 2025), MiniPay/El Dorado (November 2025), Nequi/Wenia (May 2024), Nequi/Payoneer (March 2025) -- the rails are being built NOW. On-chain COP activity should accelerate significantly through 2026-2027.

### 8.3 Key Differences from Philippines

| Dimension | Philippines | Colombia |
|-----------|-------------|----------|
| Remittance/GDP | 7.3% | 2.8% |
| Absolute remittance volume | $39.6B | $11.85B |
| Primary corridor | US (40.6%) | US (53%) |
| Crypto adoption | ~4th-9th globally | ~15th-20th globally |
| Key stablecoin infrastructure | Coins.ph, GCash | Littio, Nequi/Wenia, MoneyGram USDC |
| Informal employment | ~40% | ~56% |
| Currency volatility (2020-2025) | Moderate (PHP relatively stable) | Extreme (COP: 3,450-5,133 range) |
| Stablecoin savings demand | Lower (PHP relatively stable) | Very high (COP depreciation fear) |
| Bidirectional flow evidence | Weaker (mostly USD->PHP) | Strong (remittance vs. savings hedging) |
| Regulatory environment | BSP regulates (licensed exchanges) | SFC does NOT supervise (permissive by omission) |

**Critical difference**: Colombia's COP volatility creates BOTH inflow (remittance/income) AND outflow (savings/hedging) pressure on-chain, generating higher variance in net flows. The Philippines has less currency risk, so the bidirectional flow is weaker. This makes Colombia potentially a BETTER target for a variance swap despite lower absolute remittance volume.

### 8.4 Risks and Limitations

1. **cCOP/COPm data gap**: cCOP had ZERO Mento broker swaps in the analyzed period. All activity is in ERC-20 transfers, not swap-venue transactions. Need to verify whether COPm (post-migration) has more swap activity.

2. **Regulatory uncertainty**: Resolution 000240 reporting requirements (starting 2026) could push users to DeFi or back to traditional channels.

3. **Venezuelan noise**: Venezuelan diaspora flows create measurement noise that is hard to separate from income conversion.

4. **Petro government instability**: Economic emergency + potential policy reversals create unpredictable regime changes in capital flows.

5. **Competing rails**: Nequi/Payoneer and MoneyGram USDC may capture remittance flows on NON-Celo rails, reducing the signal available on-chain via Mento.

---

## 9. Data Sources for Ongoing Monitoring

| Source | Data Available | Frequency | Access |
|--------|---------------|-----------|--------|
| BanRep | Aggregate remittances, BOP, exchange rate | Monthly/Quarterly | Free API |
| DANE | Employment, inflation, household income | Monthly/Quarterly | Free |
| Dune Analytics | cCOP, COPm, COPM on-chain transfers/swaps | Real-time | Query #6939814, #6939820 |
| Chainalysis | Colombia crypto volume, adoption metrics | Annual report | Paid/Report |
| El Dorado | P2P COP/USDT spreads and activity | Real-time | API may be available |
| Minteo Transparency | COPM reserves, issuance | Monthly | Free (transparency.minteo.com) |
| DIAN | Tax reporting data (from 2027) | Annual | Not yet available |

---

## 10. Conclusion: Is Colombia Viable for a Variance Swap on Net COP Flows?

**YES, with qualifications.**

Colombia presents a compelling case for a variance swap target:

**Strengths**:
- Large, growing remittance corridor ($12B+ and accelerating)
- US corridor dominance (53%) aligns with USDC on-ramp availability
- Extreme COP volatility creates bidirectional on-chain flows (the SOURCE of variance)
- Broad retail population on-chain (4,913 senders, flat distribution)
- Institutional stablecoin infrastructure building rapidly (MoneyGram, Nequi, Littio, MiniPay/El Dorado)
- 56% informal employment = large unserved population needing hedging

**Challenges**:
- Lower absolute crypto remittance volume than Philippines
- cCOP swap venue activity is thin (transfers yes, swaps no)
- Need to separate remittance signal from Venezuelan noise and savings hedging
- Regulatory reporting (2026+) could shift behavior

**Recommendation**: Proceed with Colombia as a primary target currency alongside Philippines. The extreme COP volatility and bidirectional flow dynamics may actually produce HIGHER variance in net flows than PHP, despite lower absolute volume. The key next step is to analyze post-migration COPm swap and transfer data (post January 2026) to verify that the retail population is still active and growing.
