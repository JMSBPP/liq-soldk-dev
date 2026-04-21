# Philippine Economy, Crypto Adoption, and Remittance Structure

## Foundational Research for a Variance Swap on Net USDC-to-PHP Flows

**Date**: 2026-04-02
**Purpose**: Understand the structural features of the Filipino economy that determine WHO converts USDC to PHP and WHY, so that on-chain flow data can be correctly interpreted as a proxy for USD-denominated income conversion.

---

## Executive Summary

The Philippines is one of the world's largest remittance-receiving economies, with personal remittances reaching USD 39.62 billion in 2025 (7.3% of GDP). The country ranks 4th-9th globally in crypto adoption depending on the index used, and a growing stablecoin infrastructure is emerging to serve both the OFW remittance corridor and the BPO/freelancer payment corridor. These two corridors -- remittances and freelancer income -- are the primary structural drivers of USDC-to-PHP conversion. Understanding their relative magnitudes, seasonality, and sensitivity to external shocks is essential for interpreting on-chain USDC flows as a macro observable.

**Key structural insight for the variance swap**: Net USDC-to-PHP flows are driven by at least three distinct populations with different economic motivations and shock sensitivities:

1. **OFW remitters** (dominant by volume) -- sensitive to US labor market, Gulf oil prices, and exchange rate spread incentives
2. **BPO/freelancer contractors** (fast-growing) -- sensitive to US tech spending and remote work demand
3. **Crypto-native traders/speculators** -- sensitive to crypto market cycles, less correlated with macro fundamentals

A well-designed variance swap must either isolate one of these signals or explicitly model their mixture.

---

## 1. Remittance Structure

### 1.1 Market Size and GDP Share

| Year | Personal Remittances (USD B) | Cash Remittances via Banks (USD B) | % of GDP | % of GNI |
|------|-----------------------------|------------------------------------|----------|----------|
| 2023 | 37.21 | 33.49 | ~8.5% | ~7.6% |
| 2024 | 38.34 | 34.49 | 8.3% | 7.4% |
| 2025 | 39.62 | est. ~36B | 7.3% | 6.4% |

Sources: [BSP Press Release on 2024 Remittances](https://www.bsp.gov.ph/SitePages/MediaAndResearch/MediaDisp.aspx?ItemId=7426); [FintechNews PH: OFW Remittances Record](https://fintechnews.ph/65862/remittance/philippines-ofw-remittances-hit-record-usd-38-34-billion/); [PNA: Remittances All-Time High](https://www.pna.gov.ph/articles/1244195); [World Bank Personal Remittances Data](https://data.worldbank.org/indicator/BX.TRF.PWKR.DT.GD.ZS?locations=PH)

**Note**: The slight decline in remittances-to-GDP ratio (from ~8.5% to 7.3%) despite rising absolute volumes reflects GDP growth outpacing remittance growth -- an important structural shift. The economy is slowly diversifying away from pure remittance dependence, but the absolute flow remains enormous.

### 1.2 Top Corridors (2024 Cash Remittances)

| Rank | Country | Share of Total | Estimated USD B (of $34.49B cash) |
|------|---------|---------------|-----------------------------------|
| 1 | United States | 40.6% | ~14.0 |
| 2 | Singapore | 7.2% | ~2.5 |
| 3 | Saudi Arabia | 6.4% | ~2.2 |
| 4 | Japan | 4.9% | ~1.7 |
| 5 | United Kingdom | 4.7% | ~1.6 |
| 6 | UAE | 4.4% | ~1.5 |
| 7 | Canada | 3.6% | ~1.2 |
| 8 | Qatar | 2.8% | ~1.0 |
| 9 | Taiwan | 2.7% | ~0.9 |
| 10 | South Korea | 2.5% | ~0.9 |

Source: [Gulf News: Top Sources of Remittances](https://gulfnews.com/world/asia/philippines/philippines-us-singapore-saudi-arabia-japan-uk-uae-among-top-sources-of-remittances-1.1707990905002); [Statista: OFW Remittance by Country](https://www.statista.com/statistics/1242763/remittance-overseas-filipino-workers-by-country/)

**Structural implications for the variance swap**:

- The US corridor alone accounts for 40.6% of flows. This means USDC-to-PHP conversion is disproportionately a US-to-PH phenomenon, since US-based OFWs have the easiest access to USDC on-ramps.
- Gulf corridors (Saudi + UAE + Qatar = 13.6%) are significant but these workers are more likely to use traditional hawala/bank channels and less likely to use stablecoin rails (lower crypto infrastructure in Gulf states).
- Singapore (7.2%) is interesting because Singapore has a mature crypto ecosystem, so this corridor may have higher-than-average stablecoin penetration.
- The top 10 corridors account for approximately 80% of total remittances.

### 1.3 Crypto vs. Traditional Remittance Rails

**Traditional channels still dominate**: Western Union, MoneyGram, bank wires, and most critically GCash international remittance remain the primary rails. The BSP tracks "cash remittances coursed through banks" separately, and the $34.49B figure for 2024 represents only bank-intermediated flows.

**Stablecoin remittance is growing rapidly but from a small base**:

- Coins.ph partnered with BCRemit in November 2025 to create a stablecoin corridor (USDC/USDT) for OFWs in the UK, EU, US, and Canada. The service claims 80% fee reduction vs. traditional channels (from 5-10% fees down to ~1%).
- Coins.ph reported trading volumes of $500 million/month in November 2025, a 327% increase year-over-year. However, this includes all trading activity, not just remittance-related USDC-to-PHP conversion.
- No authoritative estimate exists for the exact percentage of total remittances flowing through crypto rails. Industry observers suggest it is likely in the low single digits (2-5%) as of 2025, but growing rapidly.

Sources: [FintechNews PH: Coins.ph BCRemit Partnership](https://fintechnews.ph/68837/remittance/coins-ph-bcremit-partnership-stablecoin-remittance-philippines/); [Coins.ph 327% Growth](https://fintechnews.ph/70100/crypto/coins-ph-stablecoin-remittance-trading-growth-2025/); [BitPinas: Coins.ph BCRemit](https://bitpinas.com/business/coins-bcremit-remittance/)

**Implication for on-chain data interpretation**: If total remittances are ~$40B/year and crypto remittances are ~2-5%, that suggests $0.8B-$2B/year in stablecoin remittance flows. Monthly, this would be roughly $65M-$165M in stablecoin-mediated remittance conversion to PHP. This is the "signal" our variance swap would be tracking, mixed with freelancer income conversion and speculative flows.

### 1.4 Seasonality

OFW remittances exhibit strong seasonality:
- **December**: Peak month consistently (Christmas spending, "13th month pay" tradition). December 2024 hit a record $3.73B.
- **Q4 generally elevated**: October-December consistently above-average.
- **Q1 dip**: January-February typically the lowest months.

This seasonality directly affects USDC-to-PHP flow variance and must be accounted for in the swap's reference period.

---

## 2. BPO and Remote Contractor Economy

### 2.1 Industry Scale

| Metric | 2024 Value |
|--------|-----------|
| BPO Revenue | ~$38 billion |
| BPO Employment | 1.82 million formal jobs |
| Filipino Freelancers (digital platforms) | ~1.5 million |
| Growth Rate (2024) | 7% (vs. 3.5% global average) |
| Projected 2025 Revenue | >$40 billion |

Sources: [Unity Connect: BPO Guide 2025](https://unity-connect.com/our-resources/blog/bpo-outsourcing-philippines/); [GigaBPO: Philippine BPO Industry](https://gigabpo.com/philippine-bpo-industry/); [Magellan Solutions: BPO Employment Statistics](https://www.magellan-solutions.com/blog/bpo-employment-statistics-philippines/)

**Critical observation**: BPO revenue ($38B) is roughly equal to OFW remittances ($38.3B) in 2024. These are the two pillars of Philippine USD inflows. However, BPO revenue is mostly corporate-to-corporate (multinational BPO firms receiving USD from clients, paying Filipino employees in PHP), so it does NOT directly generate USDC-to-PHP on-chain flows. The freelancer segment is different.

### 2.2 Freelancer/Contractor Segment

- The Philippines is the 6th fastest-growing freelancing market globally.
- ~1.5 million Filipino freelancers operate on digital platforms.
- Common platforms: Upwork, OnlineJobs.ph, Fiverr, Freelancer.com
- Roles: virtual assistants, customer support, content creation, software development, data annotation, AI training

**Income ranges (2025 estimates)**:
- Entry-level VA: $3-6/hour (~$360-$600/month full-time)
- Mid-level specialists: $8-15/hour (~$960-$1,800/month)
- Senior developers/specialists: $15-40/hour (~$1,800-$4,800/month)

**Crypto payment adoption among freelancers**:

Filipino freelancers are increasingly receiving payments in USDC/USDT for several reasons:
1. **Fee savings**: Traditional Upwork-to-Philippine-bank transfers incur 3-6% in platform fees + conversion costs. Stablecoin transfers drop this to ~1%.
2. **Speed**: Bank wire transfers take 3-5 days; on-chain transfers settle in minutes.
3. **Platform support**: Services like Hurupay, TransFi, and Parallax enable USD-to-USDC-to-PHP conversion pipelines for freelancers.
4. **BIR treats crypto income the same as fiat income** -- no additional tax burden for choosing crypto rails.

Sources: [TransFi: How Freelancers Accept Crypto](https://www.transfi.com/blog/how-freelancers-in-the-philippines-accept-payment-in-crypto); [TransFi: Philippines Remote Workers Cash Out](https://www.transfi.com/blog/how-philippines-remote-workers-can-get-usd-payments-and-cash-out-in-crypto-and-philippine-peso); [Hurupay: Virtual USD Account for Filipino Remote Workers](https://hurupay.com/blog/best-virtual-usd-account-for-filipino-remote-workers)

**Structural implication**: If 1.5M freelancers earn an average of $800/month, the total freelancer income flow is ~$1.2B/month or ~$14.4B/year. Even if only 10-20% of this flows through crypto rails, that is $1.4B-$2.9B/year in stablecoin-mediated conversion -- potentially comparable to or larger than the OFW crypto remittance channel. This population's USDC-to-PHP conversion is more steady-state (monthly payroll) and less seasonal than OFW remittances.

---

## 3. Crypto Adoption in the Philippines

### 3.1 Adoption Rankings

| Index | Year | Philippines Rank | Notes |
|-------|------|-----------------|-------|
| Chainalysis Global Crypto Adoption | 2022 | 2nd | Peak, driven by Axie Infinity |
| Chainalysis Global Crypto Adoption | 2024 | 8th | Post-Axie decline |
| Chainalysis Global Crypto Adoption | 2025 | 9th | Continued slight decline |
| TRM Labs Country Crypto Adoption | 2024 | 8th | |
| TRM Labs Country Crypto Adoption | 2025 | 4th | Strong retail use |

Sources: [Chainalysis 2025 Global Adoption Index](https://www.chainalysis.com/blog/2025-global-crypto-adoption-index/); [BitPinas: PH Ranked 9th in Chainalysis 2025](https://bitpinas.com/feature/ph-chainalysis-2025/); [BitPinas: TRM Labs 2025 Ranking](https://bitpinas.com/feature/trm-labs-2025-country-crypto-adoption-index/)

**Key stat**: Approximately 10% of Filipinos (>12 million people) engage with cryptocurrency in some form.

### 3.2 Axie Infinity Legacy

The Axie Infinity play-to-earn boom (2020-2022) was transformative for Philippine crypto infrastructure:

- At peak, Filipinos constituted ~40% of Axie's player base.
- Players earned PHP 15,000/month ($300) playing -- slightly above minimum wage -- during the pandemic lockdowns.
- The crash (SLP dropped from $0.34 to <$0.01) left many players in debt, especially "scholars" who had invested entry fees.
- **Lasting infrastructure effects**:
  - Millions of Filipinos created crypto wallets (Ronin, MetaMask) for the first time
  - GCash integrated with Axie/Ronin in 2024 as an on/off-ramp via GCrypto
  - Local "guilds" and "scholarship" systems created a grassroots crypto education layer
  - The experience normalized crypto-to-PHP conversion as an income activity

Sources: [Business Inquirer: Filipinos Outgrow Axie](https://business.inquirer.net/523660/filipinos-outgrow-axie-infinity-as-crypto-wealth-surges); [Time: Axie Infinity Philippines Debt](https://time.com/6199385/axie-infinity-crypto-game-philippines-debt/); [CNBC: Filipinos Earn Playing Axie](https://www.cnbc.com/2021/05/14/people-in-philippines-earn-cryptocurrency-playing-nft-video-game-axie-infinity.html)

### 3.3 Celo/Mento/PUSO in the Philippines

**PUSO (Philippine Peso Stablecoin on Celo/Mento)**:
- Launched by Celo Philippines DAO in partnership with Mento Labs in late 2024
- Name means "heart" in Filipino -- community-driven branding
- PUSO is the 6th stablecoin on the Mento Platform (alongside cUSD, cEUR, cREAL, cKES, eXOF)
- Accessible via Valora wallet, MetaMask, and the Mento dApp
- Aims to target remittance use cases and unbanked populations
- **Current adoption is nascent** -- PUSO was only launched in late 2024 and does not yet have significant volume or integration with GCash/Maya

Sources: [Mento Blog: Introducing PUSO](https://www.mento.org/blog/introducing-puso-the-first-decentralized-philippine-peso-stablecoin); [BitPinas: PUSO Launched on Celo](https://bitpinas.com/cryptocurrency/philippine-peso-stablecoin-puso-celo-blockchain/); [Mento: Local Currency Stablecoins Philippines](https://www.mento.org/blog/mento-local-currency-stablecoins-insights-from-the-philippines-puso-stablecoin)

**PHPC (Coins.ph Peso Stablecoin)**:
- BSP-approved pilot in May 2024 under Regulatory Sandbox Framework
- 1:1 PHP-pegged, 100% backed by cash and short-term instruments in Philippine banks
- Deployed on Polygon and Ronin chains
- Exited BSP sandbox in July 2025 with increased minting capacity
- More commercially viable than PUSO due to Coins.ph's existing user base and regulatory approval

Sources: [Coins.ph Blog: BSP PHPC Approval](https://coins.ph/blog/bsp-grants-coins-ph-approval-to-pilot-phpc-stablecoin/); [CoinDesk: BSP Approves Coins.ph Stablecoin](https://www.coindesk.com/policy/2024/05/14/philippines-central-bank-gives-approval-to-coinsph-to-pilot-stablecoin-in-key-remittance-market); [FintechNews PH: PHPC Exits Sandbox](https://fintechnews.ph/67165/crypto/coins-ph-phpc-progresses-beyond-bsp-sandbox/)

### 3.4 GCash and Maya Crypto Integration

**GCash (by Mynt, Globe Telecom subsidiary)**:
- ~93 million registered users (as of 2025) -- the dominant e-wallet in the Philippines
- Offers GCrypto feature powered by PDAX (licensed VASP)
- **Added USDC support in September 2025** -- a critical development for our analysis
- Also supports PayPal's PYUSD stablecoin
- Supports 39 crypto assets for trading
- Integrated with Axie Infinity/Ronin as on/off-ramp

**Maya (formerly PayMaya)**:
- Licensed VASP since 2021 under BSP oversight
- Offers crypto trading within the Maya app
- Also operates Maya Bank (digital banking license)

Sources: [CoinDesk: GCash Adds USDC](https://www.coindesk.com/markets/2025/03/24/philippines-gcash-digital-wallet-adds-usdc-support); [FintechNews PH: GCash Adds USDC to GCrypto](https://fintechnews.ph/66319/crypto/g-cash-adds-usdc-to-crypto-platform-gcrypto/); [BeInCrypto: GCash USDC](https://beincrypto.com/gcash-integrates-usdc-stablecoin-philippines/)

**Critical implication for variance swap design**: GCash adding USDC support in September 2025 is a structural regime change. Before this date, USDC-to-PHP conversion required using crypto exchanges (Coins.ph, PDAX) or P2P markets. After this date, 93 million GCash users can theoretically interact with USDC directly. This means on-chain USDC flow patterns pre- and post-September 2025 are NOT directly comparable without adjustment.

---

## 4. Economic Vulnerability and Income Structure

### 4.1 Household Income

**2023 Family Income and Expenditure Survey (PSA)**:
- National average annual family income: approximately PHP 313,000 (~$5,500 at 2023 rates)
- NCR (Metro Manila) highest: PHP 513,520/year (~$9,170)
- BARMM (Bangsamoro) lowest: PHP 206,880/year (~$3,700)
- National average annual family expenditure: PHP 258,050 (~$4,600)

Source: [PSA FIES Data](https://psa.gov.ph/statistics/income-expenditure/fies); [CPBRD: Updates on Family Income and Expenditure](https://cpbrd.congress.gov.ph/wp-content/uploads/2025/03/FF2025-20-UPDATES-ON-FAMILY-INCOME-AND-EXPENDITURE-IN-THE-PHILIPPINES.pdf)

### 4.2 Remittance Dependency

- Approximately 10% of Filipino households receive international remittances.
- Among recipient households, 64% also receive domestic remittances, indicating multi-source income dependency.
- ADB research warns of "remittance dependency syndrome" -- households that reduce local income generation due to overseas support, which increases vulnerability to remittance disruption.
- Remittance-receiving households spend more on consumption, education, and housing, but financial constraints remain binding for the poorest recipients.

Source: [ADB Economics Working Paper No. 714 (Feb 2024)](https://www.adb.org/sites/default/files/publication/942041/ewp-714-remittances-household-expenditures-philippines.pdf); [World Bank: BSP Overview of Remittance Flows](https://thedocs.worldbank.org/en/doc/e522b834eaf0c4f81970f80a8c8ccb6e-0070012024/original/5-BSP-Overview-of-OF-Remittance-Flows-in-the-Philippines.pdf)

### 4.3 PHP/USD Exchange Rate History

| Year | Avg USD/PHP | Key Event |
|------|-------------|-----------|
| 2020 | ~49.6 | COVID-19 pandemic, PHP relatively stable |
| 2021 | ~49.2 | PHP strengthens slightly, low of ~47.7 in June |
| 2022 | ~54.5 | Sharp depreciation, peaked at 59.21 in September |
| 2023 | ~55.6 | Stabilization at elevated levels |
| 2024 | ~57.3 | Continued gradual depreciation, range 55.3-59.4 |
| 2025 | ~57-58 | Relative stability |

**Major depreciation drivers**:
1. **2022 spike (47 to 59)**: US Federal Reserve aggressive rate hikes (0% to 5.25%) widened interest rate differential. Philippines dependent on imported food and energy, so rising commodity prices simultaneously widened trade deficit to record levels. The 20%+ depreciation in 18 months was the most severe in decades.
2. **Structural weakness**: The Philippines runs a persistent trade deficit (imports > exports), meaning the peso faces chronic depreciation pressure that is partially offset by remittance inflows.
3. **BSP response**: BSP raised rates aggressively in 2022-2023 to defend the peso and combat imported inflation.

Sources: [Exchange-rates.org: USD-PHP History](https://www.exchange-rates.org/exchange-rate-history/usd-php); [BSP: Monthly Average Exchange Rates](https://www.bsp.gov.ph/statistics/external/Table%2012.pdf); [RCBC: Historical USD/PHP](https://www.rcbc.com/how-much-is-the-exchange-rate-of-peso-to-dollar)

**Implication for variance swap**: A depreciating peso creates incentive for OFWs and freelancers to HOLD USDC rather than convert immediately, since waiting means more pesos per dollar. This means exchange rate trends directly affect the TIMING of USDC-to-PHP conversion -- and therefore the variance of flows -- even if the total volume doesn't change. A rapidly depreciating peso paradoxically reduces flow variance (everyone delays conversion together), while a stable or appreciating peso increases conversion frequency and may increase variance.

### 4.4 Inflation History

| Year | Annual Inflation (CPI) |
|------|----------------------|
| 2020 | ~2.6% |
| 2021 | 3.93% |
| 2022 | 5.82% |
| 2023 | 5.98% |
| 2024 | 3.21% |
| 2025 | 1.7% |
| 2026 (Feb) | 2.4% |

Source: [Trading Economics: Philippines Inflation](https://tradingeconomics.com/philippines/inflation-cpi); [Macrotrends: Philippines Inflation](https://www.macrotrends.net/global-metrics/countries/phl/philippines/inflation-rate-cpi)

The 2022-2023 inflation spike (nearly 6%) eroded purchasing power significantly and was driven by:
- Global food price shocks (Russia-Ukraine war)
- Rising energy costs
- Peso depreciation making imports more expensive (imported inflation)

BSP's target range is 2-4%. The 2024-2025 disinflation suggests the tightening cycle worked, though at the cost of growth.

### 4.5 External Shock Sensitivity

The following shocks affect remittance flows and therefore USDC-to-PHP conversion:

| Shock | Mechanism | Corridor Affected | Expected Effect on Flows |
|-------|-----------|-------------------|--------------------------|
| US recession | OFW job losses, reduced overtime | US (40.6%) | Sharp decline in flows |
| Gulf oil price crash | Budget cuts, construction slowdown | Saudi+UAE+Qatar (13.6%) | Moderate decline |
| PHP rapid depreciation | Incentive to delay conversion | All corridors | Reduced flow frequency, increased lumpiness |
| US Fed rate hikes | Strengthens USD, weakens PHP | All (via FX channel) | Ambiguous: more pesos per send but FX uncertainty |
| Global tech recession | BPO/freelancer demand reduction | Freelancer segment | Decline in contractor USDC inflows |
| Typhoon/natural disaster | Spike in emergency remittances | All corridors | Temporary surge in flows |

---

## 5. Regulatory Environment

### 5.1 BSP VASP Framework

The BSP regulates Virtual Asset Service Providers under **Circular No. 1108** (2021), which covers:
- AML/CFT compliance requirements
- Capital adequacy standards
- Governance and operational risk management
- Cybersecurity frameworks
- Consumer protection requirements

The BSP has maintained an **indefinite moratorium on new VASP licenses** since 2025 (extended via August 2025 memorandum), citing consumer protection and cybercrime concerns. This means the current 9 active VASPs are the only players for the foreseeable future.

Source: [BSP Circular 1108](https://lpr.adb.org/resource/guidelines-virtual-asset-providers-bangko-sentral-ng-pilipinas-circular-no-1108); [BSP: Moratorium Extension](https://www.bsp.gov.ph/SitePages/MediaAndResearch/MediaDisp.aspx?ItemId=7647&MType=MediaReleases)

### 5.2 Active Licensed VASPs (as of October 2025)

1. **Betur Inc. (Coins.ph)** -- Licensed September 2017; largest consumer crypto platform
2. **Bloomsolutions, Inc.** -- Blockchain-based remittance infrastructure
3. **Direct Agent 5 (SurgePay)** -- Mobile payments
4. **Maya Philippines, Inc.** -- Major e-wallet with crypto features
5. **Moneybees Forex Corp.** -- Crypto-to-fiat exchange kiosks
6. **Philippine Digital Asset Exchange (PDAX)** -- Powers GCash's GCrypto
7. **TopJuan Technologies** -- Crypto services
8. **XenRemit, Inc.** -- Crypto remittance
9. **Union Bank of the Philippines** -- First bank with VASP license, in-app crypto trading
10. **GoTyme Bank** -- Newly licensed (October 2024), digital bank

Source: [BSP VASP List](https://www.bsp.gov.ph/Lists/Directories/Attachments/19/VASP.pdf); [FintechNews PH: Licensed Crypto Exchanges 2026](https://fintechnews.ph/61554/crypto/here-are-the-licensed-cryptocurrency-exchanges-in-the-philippines/); [BitPinas: Licensed VASPs](https://bitpinas.com/feature/list-licensed-virtual-currency-exchanges-philippines/)

### 5.3 Dual Regulatory Oversight

- **BSP**: Supervises custody, on/off-ramps, payment system roles, AML/CFT
- **SEC (Securities and Exchange Commission)**: Governs marketing, issuance, and trading of crypto-assets under the CASP (Crypto-Asset Service Provider) framework

This dual structure means stablecoin issuance falls under BSP oversight (PHPC sandbox), while token sales/offerings fall under SEC jurisdiction.

Source: [Lightspark: Is Crypto Legal in Philippines](https://www.lightspark.com/knowledge/is-crypto-legal-in-philippines); [GLI: Fintech Laws Philippines 2025](https://www.globallegalinsights.com/practice-areas/fintech-laws-and-regulations/philippines/)

### 5.4 Tax Treatment of Crypto Income

- The BIR (Bureau of Internal Revenue) treats cryptocurrency income identically to conventional income.
- Freelancers earning in crypto must register with BIR and pay applicable taxes.
- **8% flat tax option**: Available for individual non-VAT taxpayers earning less than PHP 3 million/year (~$52,000), applied to gross sales/receipts. This is the preferred option for most freelancers.
- **Regular system**: 3% percentage tax (non-VAT) or graduated income tax rates.
- **No specific crypto tax legislation** exists as of 2026. The Department of Finance proposed crypto-specific taxation in 2024, but no legislation has been enacted.
- Capital gains from crypto trading are technically taxable, but enforcement is minimal.

Source: [Taxumo: Taxes for Freelancers 2025](https://www.taxumo.com/blog/taxes-for-freelancers-in-the-philippines-2025-complete-guide/); [BitPinas: Dept. of Finance Crypto Tax Proposal](https://bitpinas.com/regulation/dept-of-finance-crypto-tax-by-2024-philippines/); [TransFi: Managing Freelance Income and Taxes PH](https://www.transfi.com/blog/how-to-manage-freelance-income-and-taxes-in-the-philippines)

### 5.5 Stablecoin-Specific Regulation

- No blanket restrictions on stablecoin use for remittance. The BSP has been supportive of stablecoin innovation within its sandbox framework.
- PHPC (Coins.ph) is the only BSP-approved PHP stablecoin. PUSO (Celo/Mento) operates outside BSP sandbox -- regulatory status unclear.
- Foreign stablecoins (USDC, USDT, PYUSD) are treated as virtual assets under Circular 1108 and can be freely traded by licensed VASPs.
- The BSP's wholesale CBDC pilot concluded testing in December 2024, suggesting the central bank is actively studying digital peso instruments but has not committed to a retail CBDC.

Source: [Bitwage: State of Stablecoins in Philippines Sept 2025](https://bitwage.com/en-us/blog/state-of-stablecoins-in-philippines-september-2025); [TransFi: BSP Crypto Regulations and Stablecoins](https://www.transfi.com/blog/bsps-crypto-regulations-what-stablecoin-users-should-know)

---

## 6. Competing and Complementary Services

### 6.1 Coins.ph (Betur Inc.)

- **Founded**: 2014; VASP license since 2017
- **Users**: Millions (exact figure not disclosed post-acquisition)
- **Key features**: Buy/sell crypto, bill payments, remittance, load top-up
- **Acquisition**: Acquired by a consortium including GoTyme Group stakeholders (not GoTyme Bank itself directly; some confusion in reporting). Previously acquired by Betur from original founders.
- **PHPC stablecoin**: The only BSP-sanctioned PHP stablecoin, live on Polygon and Ronin
- **BCRemit partnership (Nov 2025)**: Stablecoin remittance corridor for UK, EU, US, Canada
- **327% trading volume growth**: $117M/month (Nov 2024) to $500M/month (Nov 2025)

Source: [Coins.ph 327% Growth](https://fintechnews.ph/70100/crypto/coins-ph-stablecoin-remittance-trading-growth-2025/)

### 6.2 PDAX (Philippine Digital Asset Exchange)

- Licensed VASP, powers GCash's GCrypto feature
- This is the primary bridge between GCash's 93M users and the crypto ecosystem
- Launched PDAX Prime in 2022 for advanced trading
- UnionBank partnership via developer API

Source: [PDAX](https://pdax.ph/); [UnionBank-PDAX Developer API](https://developer.unionbankph.com/product/docs/partner-pdax)

### 6.3 UnionBank of the Philippines

- First Philippine universal bank with a VASP license
- Launched "Buy/Sell Crypto" feature in mobile app (2025)
- Partnership with PDAX for backend crypto infrastructure
- Positioned as the "crypto-friendly bank" for institutional and retail clients

Source: [Disruption Banking: How Philippines Became Asia's Crypto Giant](https://www.disruptionbanking.com/2025/11/11/how-the-philippines-became-asias-crypto-giant/)

### 6.4 Stablecoin Landscape Summary

| Stablecoin | Peg | Chain(s) | Issuer | BSP Status | Relevance |
|-----------|-----|----------|--------|------------|-----------|
| USDC | USD | Multi-chain | Circle | Traded by VASPs | Primary USD stablecoin; GCash integration |
| USDT | USD | Multi-chain | Tether | Traded by VASPs | Largest by volume globally |
| PHPC | PHP | Polygon, Ronin | Coins.ph | BSP sandbox graduate | Only BSP-approved PHP stablecoin |
| PUSO | PHP | Celo | Celo PH DAO / Mento | Not in BSP sandbox | Community-driven, nascent adoption |
| PYUSD | USD | Ethereum, Solana | PayPal | Traded via GCrypto | Available on GCash |
| cUSD | USD | Celo | Mento | Not regulated by BSP | Part of Celo ecosystem |

**None of the major Philippine platforms (GCash, Maya, Coins.ph) currently use Celo/Mento/PUSO as a primary rail.** PUSO remains a niche community project. The dominant stablecoins in Philippine crypto flows are USDC and USDT, with PHPC emerging as the local-currency alternative.

---

## 7. Synthesis: Structural Model of USDC-to-PHP Flows

### 7.1 Flow Population Decomposition

Based on the research, net USDC-to-PHP flows can be decomposed into:

```
Total USDC->PHP = OFW_Remittance_Via_Crypto + Freelancer_Income_Conversion + Speculative_Trading + Merchant_Settlement
```

**Estimated annual magnitudes (2025, rough)**:

| Component | Estimated Annual Volume | Variance Profile | Primary Driver |
|-----------|------------------------|-------------------|----------------|
| OFW Crypto Remittance | $0.8B - $2.0B | Seasonal (Q4 peak), shock-sensitive | US labor market, Gulf oil |
| Freelancer Conversion | $1.4B - $2.9B | Relatively steady, monthly cadence | US tech spending |
| Speculative/Trading | $3B - $5B+ | High variance, crypto-cycle-driven | BTC/ETH price, market sentiment |
| Merchant/Commercial | <$0.5B | Low variance, growing | E-commerce, B2B |

### 7.2 Key Structural Features for Swap Design

1. **Regime change in September 2025**: GCash USDC integration fundamentally changed the on-chain flow landscape. Any historical analysis must treat pre- and post-September 2025 as different regimes.

2. **Seasonality is NOT noise**: December-January swing in OFW remittances is a structural feature, not random variance. The swap's reference period should either normalize for this or explicitly include it as a tradeable feature.

3. **Exchange rate creates strategic delay**: A depreciating peso incentivizes USDC HODLing. This means flow variance may be inversely correlated with PHP depreciation rate -- counterintuitive but structurally grounded.

4. **The US corridor dominates**: 40.6% of all remittances originate from the US, and the US has the best USDC on-ramp infrastructure. This means US economic conditions (employment, interest rates) are the single most important external factor for USDC-to-PHP flows.

5. **Speculative flows contaminate the signal**: Without on-chain heuristics to separate remittance/income conversion from speculative trading, the raw USDC-to-PHP flow data will have a large noise component from trading activity. Coins.ph's $500M/month trading volume dwarfs estimated remittance flows.

6. **PHPC may eventually reduce USDC-to-PHP flows**: If PHPC gains adoption, the conversion may shift from USDC-to-PHP on exchanges to USDC-to-PHPC on-chain, which would change the observable data structure.

### 7.3 Risks and Limitations

- **Data availability**: On-chain USDC flows to Philippine VASPs can be partially tracked, but the conversion to PHP happens off-chain (on exchange order books or OTC desks). True USDC-to-PHP conversion volume is not fully observable on-chain.
- **Regulatory risk**: BSP's VASP moratorium and potential future stablecoin regulations could change the flow structure at any time.
- **Platform concentration**: A large share of flows goes through a small number of VASPs (Coins.ph, PDAX/GCash). Platform-specific policy changes can create discontinuities.
- **Informal channels**: A significant portion of crypto remittances may occur P2P (via Binance P2P, local Telegram groups) and never touch licensed VASP infrastructure, making it invisible to both on-chain and BSP data.

---

## 8. Research Gaps and Next Steps

1. **Quantify the speculative vs. fundamental flow mix**: Need on-chain analysis of USDC flows to Philippine VASP addresses, segmented by transfer size, frequency, and source patterns. Small regular transfers (~$200-$1000, monthly) are likely freelancer income; larger irregular transfers are more likely speculative.

2. **PHPC on-chain data**: Track PHPC minting/burning as a direct observable for PHP stablecoin demand. This is a cleaner signal than USDC flows because PHPC exists solely for PHP conversion.

3. **Coins.ph address identification**: Identify Coins.ph's on-chain USDC receiving addresses to measure inflow volume directly. The $500M/month trading figure suggests substantial on-chain footprint.

4. **Seasonality quantification**: Build a monthly time series of USDC inflows to Philippine VASPs and decompose the seasonal component (using BSP remittance seasonality as prior) from the cyclical component.

5. **Correlation analysis**: Test the hypothesis that USDC-to-PHP flow variance is inversely correlated with PHP depreciation rate. If true, this is the key structural relationship the variance swap would exploit.

---

## Sources Index

### BSP and Government Sources
- [BSP Press Release on 2024 Remittances](https://www.bsp.gov.ph/SitePages/MediaAndResearch/MediaDisp.aspx?ItemId=7426)
- [BSP Monthly Average Exchange Rates](https://www.bsp.gov.ph/statistics/external/Table%2012.pdf)
- [BSP VASP List (PDF)](https://www.bsp.gov.ph/Lists/Directories/Attachments/19/VASP.pdf)
- [BSP Moratorium Extension](https://www.bsp.gov.ph/SitePages/MediaAndResearch/MediaDisp.aspx?ItemId=7647&MType=MediaReleases)
- [BSP Circular 1108 (ADB)](https://lpr.adb.org/resource/guidelines-virtual-asset-providers-bangko-sentral-ng-pilipinas-circular-no-1108)
- [PSA Family Income and Expenditure Survey](https://psa.gov.ph/statistics/income-expenditure/fies)
- [CPBRD: Updates on Family Income](https://cpbrd.congress.gov.ph/wp-content/uploads/2025/03/FF2025-20-UPDATES-ON-FAMILY-INCOME-AND-EXPENDITURE-IN-THE-PHILIPPINES.pdf)
- [World Bank: Remittances % GDP](https://data.worldbank.org/indicator/BX.TRF.PWKR.DT.GD.ZS?locations=PH)
- [World Bank: BSP Overview of OF Remittance Flows](https://thedocs.worldbank.org/en/doc/e522b834eaf0c4f81970f80a8c8ccb6e-0070012024/original/5-BSP-Overview-of-OF-Remittance-Flows-in-the-Philippines.pdf)

### Industry and Adoption Reports
- [Chainalysis 2025 Global Adoption Index](https://www.chainalysis.com/blog/2025-global-crypto-adoption-index/)
- [TRM Labs 2025 Crypto Adoption Report](https://www.trmlabs.com/reports-and-whitepapers/2025-crypto-adoption-and-stablecoin-usage-report)
- [Bitwage: State of Stablecoins in Philippines](https://bitwage.com/en-us/blog/state-of-stablecoins-in-philippines-september-2025)
- [Disruption Banking: How Philippines Became Asia's Crypto Giant](https://www.disruptionbanking.com/2025/11/11/how-the-philippines-became-asias-crypto-giant/)
- [ADB Working Paper No. 714: Remittances and Household Expenditures](https://www.adb.org/sites/default/files/publication/942041/ewp-714-remittances-household-expenditures-philippines.pdf)

### News and Platform Sources
- [FintechNews PH: OFW Remittances Record $38.34B](https://fintechnews.ph/65862/remittance/philippines-ofw-remittances-hit-record-usd-38-34-billion/)
- [FintechNews PH: Coins.ph BCRemit Partnership](https://fintechnews.ph/68837/remittance/coins-ph-bcremit-partnership-stablecoin-remittance-philippines/)
- [FintechNews PH: Coins.ph 327% Growth](https://fintechnews.ph/70100/crypto/coins-ph-stablecoin-remittance-trading-growth-2025/)
- [FintechNews PH: PHPC Exits Sandbox](https://fintechnews.ph/67165/crypto/coins-ph-phpc-progresses-beyond-bsp-sandbox/)
- [FintechNews PH: GCash Adds USDC](https://fintechnews.ph/66319/crypto/g-cash-adds-usdc-to-crypto-platform-gcrypto/)
- [FintechNews PH: Licensed Crypto Exchanges 2026](https://fintechnews.ph/61554/crypto/here-are-the-licensed-cryptocurrency-exchanges-in-the-philippines/)
- [CoinDesk: BSP Approves Coins.ph Stablecoin Pilot](https://www.coindesk.com/policy/2024/05/14/philippines-central-bank-gives-approval-to-coinsph-to-pilot-stablecoin-in-key-remittance-market)
- [CoinDesk: GCash Adds USDC](https://www.coindesk.com/markets/2025/03/24/philippines-gcash-digital-wallet-adds-usdc-support)
- [BitPinas: PH Ranked 9th Chainalysis 2025](https://bitpinas.com/feature/ph-chainalysis-2025/)
- [BitPinas: TRM Labs 2025 Ranking](https://bitpinas.com/feature/trm-labs-2025-country-crypto-adoption-index/)
- [BitPinas: PUSO Launched on Celo](https://bitpinas.com/cryptocurrency/philippine-peso-stablecoin-puso-celo-blockchain/)
- [BitPinas: PHPC Exits Sandbox](https://bitpinas.com/regulation/phpc-exits-sandbox/)
- [BitPinas: Coins.ph BCRemit](https://bitpinas.com/business/coins-bcremit-remittance/)
- [BitPinas: Licensed VASPs](https://bitpinas.com/feature/list-licensed-virtual-currency-exchanges-philippines/)
- [Mento Blog: Introducing PUSO](https://www.mento.org/blog/introducing-puso-the-first-decentralized-philippine-peso-stablecoin)
- [Coins.ph Blog: BSP PHPC Approval](https://coins.ph/blog/bsp-grants-coins-ph-approval-to-pilot-phpc-stablecoin/)
- [Gulf News: OFW Remittances Record](https://gulfnews.com/your-money/ofw-remittances-hit-record-high-3834-billion-in-2024-1.500038796)
- [Gulf News: Top Sources of Remittances](https://gulfnews.com/world/asia/philippines/philippines-us-singapore-saudi-arabia-japan-uk-uae-among-top-sources-of-remittances-1.1707990905002)
- [PNA: Remittances All-Time High](https://www.pna.gov.ph/articles/1244195)
- [Business Inquirer: Filipinos Outgrow Axie](https://business.inquirer.net/523660/filipinos-outgrow-axie-infinity-as-crypto-wealth-surges)
- [Time: Axie Infinity Philippines](https://time.com/6199385/axie-infinity-crypto-game-philippines-debt/)
- [CNBC: Filipinos Earn Playing Axie](https://www.cnbc.com/2021/05/14/people-in-philippines-earn-cryptocurrency-playing-nft-video-game-axie-infinity.html)

### Freelancer/BPO Sources
- [Unity Connect: BPO Guide 2025](https://unity-connect.com/our-resources/blog/bpo-outsourcing-philippines/)
- [GigaBPO: Philippine BPO Industry](https://gigabpo.com/philippine-bpo-industry/)
- [Magellan Solutions: BPO Employment Statistics](https://www.magellan-solutions.com/blog/bpo-employment-statistics-philippines/)
- [TransFi: Freelancers Accept Crypto](https://www.transfi.com/blog/how-freelancers-in-the-philippines-accept-payment-in-crypto)
- [TransFi: Philippines Remote Workers Cash Out](https://www.transfi.com/blog/how-philippines-remote-workers-can-get-usd-payments-and-cash-out-in-crypto-and-philippine-peso)
- [TransFi: Stablecoin Payments Philippines](https://www.transfi.com/blog/stablecoin-payments-in-the-philippines-redefining-remittances-and-online-work-payments)
- [TransFi: BSP Crypto Regulations Stablecoins](https://www.transfi.com/blog/bsps-crypto-regulations-what-stablecoin-users-should-know)
- [Hurupay: Virtual USD Account Filipino Remote Workers](https://hurupay.com/blog/best-virtual-usd-account-for-filipino-remote-workers)

### Tax and Regulatory Sources
- [Taxumo: Taxes for Freelancers 2025](https://www.taxumo.com/blog/taxes-for-freelancers-in-the-philippines-2025-complete-guide/)
- [BitPinas: Dept. of Finance Crypto Tax Proposal](https://bitpinas.com/regulation/dept-of-finance-crypto-tax-by-2024-philippines/)
- [Lightspark: Is Crypto Legal in Philippines](https://www.lightspark.com/knowledge/is-crypto-legal-in-philippines)
- [GLI: Fintech Laws Philippines 2025](https://www.globallegalinsights.com/practice-areas/fintech-laws-and-regulations/philippines/)
- [Notabene: Travel Rule Crypto Philippines](https://notabene.id/world/the-philippines)

### Exchange Rate and Macro Sources
- [Trading Economics: Philippines Inflation](https://tradingeconomics.com/philippines/inflation-cpi)
- [Macrotrends: Philippines Inflation](https://www.macrotrends.net/global-metrics/countries/phl/philippines/inflation-rate-cpi)
- [Exchange-rates.org: USD-PHP History](https://www.exchange-rates.org/exchange-rate-history/usd-php)
- [Trading Economics: Philippines Remittances](https://tradingeconomics.com/philippines/remittances)
- [Statista: OFW Remittance by Country](https://www.statista.com/statistics/1242763/remittance-overseas-filipino-workers-by-country/)
