# COPM / Minteo Deep Dive: Colombian Peso Stablecoin as Behavioral Reference for Income Flow Calibration

**Date:** 2026-04-02
**Status:** Research Complete
**Relevance:** Critical -- COPM with 100K+ users may be the behavioral reference that makes the Colombia interpolation strategy viable

---

## Executive Summary

COPM is a fiat-backed Colombian Peso stablecoin issued by Minteo, a Bogota-based fintech founded in 2021 by the team behind Wompi (acquired by Bancolombia). Launched in April 2024, COPM has achieved remarkable traction: 100,000+ retail users (primarily via the Littio neobank integration), 50+ B2B corporate clients, and over USD $200 million in monthly transaction volume. It is deployed on Polygon (primary), Celo, and Solana. Reserves are held 1:1 in Colombian banks supervised by the Superintendencia Financiera, with monthly attestation by BDO. COPM was listed on Kraken in December 2025.

The critical finding for our hedging instrument: COPM flow is primarily **income-conversion and B2B-settlement driven**, not speculative. Users convert salary/freelance income to COP-denominated stablecoin for savings (via Littio), or businesses use it for operational payments, treasury automation, and cross-border settlement. This makes COPM flow a meaningful proxy for Colombian household/business income activity -- precisely the behavioral signal needed for a variance swap on Colombian income flows.

---

## 1. Minteo -- The Company

### 1.1 Founding and Leadership

Minteo was founded in **2021** and is headquartered in **Bogota, Colombia**. The founding team has deep Colombian fintech pedigree:

- **Santiago Rodriguez** -- CEO and Co-Founder. Previously co-founded Vlipco, the company behind **Wompi**, a leading Colombian payment processor acquired by **Bancolombia** in 2021. [1]
- **William Duran** -- Co-Founder and Co-CEO, also CMO. Same Wompi/Vlipco background. [2]
- **Javier Lozano** -- CTO and Co-Founder. Also part of the Wompi founding team. [3]
- **Sebastian Salazar** -- Chief Operating Officer. [3]

The Wompi connection is significant: Wompi became one of Colombia's largest payment gateways before its acquisition by Bancolombia (Colombia's largest bank). This team knows Colombian payment infrastructure intimately.

Additional notable background: team members were also involved in **Easy Taxi**, one of Latin America's largest cab-hailing apps (acquired by Cabify). [3]

### 1.2 Funding

- **September 2022:** $4.3 million seed round. Investors include **G20 Ventures** and other institutional investors. [4]
- The company originally launched as an NFT marketplace for LATAM, then pivoted to stablecoin infrastructure -- a significant and pragmatic pivot. [4]

### 1.3 How is COPM Backed?

COPM is a **fully fiat-reserved stablecoin**. Not algorithmic. Not over-collateralized with crypto. Pure fiat backing:

- **1:1 cash deposits** in Colombian banks supervised by the **Superintendencia Financiera de Colombia (SFC)**. [5]
- For every COPM in circulation, one Colombian Peso is held in a regulated bank account. [5]
- Monthly attestation reports published by **BDO** (one of the world's top 5 auditing firms). [6]
- Transparency portal: https://transparency.minteo.com/ [7]
- Reserve management details: https://transparency.minteo.com/reserves [8]

### 1.4 Regulatory Status

Important nuance: Colombia does not yet have comprehensive crypto regulation. Cryptoassets are classified as digital assets, not financial instruments, under Colombian law. However:

- COPM reserves are held in banks **supervised by the SFC** -- so the reserves themselves are under regulatory oversight even if the token is not directly regulated as a security. [9]
- Colombia's financial supervisor ran a "La Arenera" regulatory sandbox testing bank-exchange interactions; lessons are expected to inform future on/off-ramp frameworks. [10]
- Minteo is positioning itself as compliant with existing financial regulations through BDO auditing and SFC-supervised bank custody. [5]

### 1.5 How Did They Acquire 100K Users?

The 100K users came **primarily through Littio**, a Y Combinator-backed Colombian neobank:

- **Littio** offers Colombian users dollar and euro savings accounts powered by stablecoins (USDC, EURC). [11]
- Over 200,000 Colombians use Littio (as of 2025). [11]
- COPM is integrated into Littio, giving users the ability to hold COP-denominated value on-chain. [5]
- The 100K figure specifically refers to Colombians using COPM via the Littio platform. [5]

This is crucial: these are **not crypto-native users**. They are **fintech users** who happen to be using blockchain rails without necessarily knowing it.

### 1.6 Business Model

Minteo makes money through:

1. **Mint/redeem spreads** -- Fees on converting COP fiat to COPM and back. [5]
2. **B2B API settlement fees** -- Charging fintechs, banks, and exchanges for using their settlement infrastructure. [12]
3. **Float on reserves** -- Interest earned on COP deposits held in regulated banks (standard stablecoin issuer model). [5]
4. **Cross-border FX settlement** -- Fees on USD stablecoin to COPM swaps for international settlement. [12]

---

## 2. COPM -- The Token

### 2.1 Contract Addresses and Chain Deployment

COPM is deployed on **multiple chains**:

| Chain | Contract Address | Standard | Status |
|-------|-----------------|----------|--------|
| **Celo** | `0xc92e8fc2947e32f2b574cca9f2f12097a71d5606` | ERC-20 | Active |
| **Polygon** | (Primary deployment) | ERC-20 | Active -- primary chain for $200M/mo volume |
| **Solana** | (Deployed) | SPL | Active |
| **Ethereum** | (EVM compatible) | ERC-20 | Supported |

Per Minteo's transparency portal: "For Ethereum and other EVM compatible chains such as Polygon, Minteo implements the ERC20 token standard. Minteo also adheres to the SPL token standard for the Solana blockchain." [13]

**Polygon is the primary chain** for the high-volume B2B settlement activity ($200M/mo). Celo deployment is more recent (November 2024) and is part of Celo's broader on-chain FX campaign. [14]

### 2.2 How Do Users Get COPM?

Multiple pathways:

1. **Via Littio (primary retail channel):** Users deposit COP fiat via Colombian bank transfer (Bancolombia, Nequi, Daviplata) into Littio, which mints COPM on their behalf. [5]
2. **Via Minteo API (B2B channel):** Companies integrate Minteo's API to mint COPM from COP bank deposits for operational use. [12]
3. **DEX purchase:** Available on Uniswap V3 (Celo), Stabull Finance (Ethereum/Polygon). Liquidity is thin on DEX -- the COPM/USDT Celo pool had only ~$22K liquidity. [15]
4. **CEX purchase:** Listed on **Kraken** as of December 23, 2025. [16]

### 2.3 How Do Users Cash Out?

1. **Via Littio:** Convert COPM back to COP, withdraw to Colombian bank account. [5]
2. **Via Minteo redemption:** Burn COPM, receive COP to bank account. [12]
3. **Via DEX:** Swap COPM for USDT/USDC, then use P2P platforms (El Dorado, Bitso) for fiat off-ramp. [15]
4. **Via Kraken:** Sell COPM on exchange (with geographic restrictions -- not available in EEA or Australia). [16]

### 2.4 Total Supply / Circulating Supply

Exact figures are not publicly aggregated across chains on major trackers. CoinCarp lists COPM at a price of approximately $0.000273 (consistent with 1 COP peg at ~4,200 COP/USD). [17]

Given the $200M/mo volume claim and the 1:1 backing model, the circulating supply should be verifiable via Minteo's transparency portal at https://transparency.minteo.com/reserves. [8]

The thin DEX liquidity (~$22K on Celo Uniswap V3) suggests the vast majority of COPM volume flows through **Minteo's own mint/redeem infrastructure** and Littio, not through open market DEX trading. [15]

---

## 3. Use Cases -- What Do Users Actually Do?

### 3.1 Savings (Primary Retail Use Case)

Through Littio, the dominant pattern is:
- Colombian user deposits COP from salary/income
- Converts to COPM (COP-denominated on-chain value) or USDC (dollar savings)
- Earns yield on holdings
- Withdraws when needed

Littio saw 100%+ growth in new USDC yield accounts during the Feb 2025 Petro-Trump tariff crisis, indicating users flee to dollar-denominated savings during macro stress. [11]

### 3.2 B2B Operational Payments (Primary Enterprise Use Case)

Over **50 companies** in Colombia use COPM for:
- Operational payments
- Treasury automation and financial reconciliation
- Fund traceability on blockchain
- 24/7 settlement (weekends/holidays -- a major advantage over Colombian bank clearing) [18]

Minteo has **tripled its B2B client portfolio** in Colombia. [18]

### 3.3 Remittances

COPM is positioned for the remittance corridor but evidence of direct retail-to-retail remittance use is indirect:
- Colombia receives **$11.8 billion** in annual remittances (2024), nearly 3% of GDP. [19]
- COPM's low transaction costs and instant availability are marketed for remittance use. [5]
- The **VelaFi partnership** specifically targets the Colombia-Asia cross-border corridor. [20]
- MoneyGram separately launched stablecoin-powered "digital dollar" accounts in Colombia (using USDT, not COPM). [10]

### 3.4 Cross-Border Trade Settlement

The VelaFi-Minteo alliance enables:
- Companies and platforms to convert and move funds in COP without traditional banking friction
- Faster, safer transactions between LATAM and Asia
- COPM as the COP settlement leg of international trade flows [20]

### 3.5 E-commerce

COPM enables instant payouts for e-commerce platforms and instant swaps with other on-chain currencies. [5]

### 3.6 NOT Observed (Yet)

- **Salary payments in COPM directly:** Not confirmed. The flow is salary -> COP fiat -> Littio -> COPM, not employer -> COPM.
- **Bill payments in COPM:** Not confirmed.
- **Cashback programs:** cCOP (Mento) ran a cashback pilot in Medellin, not COPM. [21]
- **Merchant POS payments:** No evidence of direct merchant acceptance of COPM.

---

## 4. User Demographics

### 4.1 Who Are the 100K Users?

Based on Littio's user profile (the primary COPM distribution channel):

- **Urban, digitally-native fintech users.** Littio requires a smartphone and Colombian bank account. [11]
- **Not crypto-native.** Littio abstracts blockchain away -- users think they are using a neobank, not a crypto platform. [11]
- **Income bracket:** Littio targets the broad Colombian middle class. The minimum to open an account is as low as $1 equivalent. [11]
- **Age:** Likely skews 25-45 based on fintech adoption patterns in Colombia.
- **Geographic concentration:** Likely Bogota, Medellin, Cali, Barranquilla (Colombia's major urban centers).

### 4.2 The 50+ B2B Clients

- Companies using COPM for operational payments and treasury. [18]
- Likely includes fintechs, digital wallets, payment companies (per William Duran's statements). [18]
- Banks and exchanges integrating via Minteo's API. [12]

### 4.3 User Acquisition Channels

1. **Littio integration** -- Littio's own growth drives COPM adoption passively. [5]
2. **B2B sales** -- Direct enterprise sales to Colombian companies. [18]
3. **Celo ecosystem incentives** -- The Stabila Foundation distributed $730K+ in CELO rewards through Merkl to incentivize stablecoin pools, including COPM/USDT with 100%+ APY. [14]
4. **Kraken listing** -- Exposure to global exchange users (Dec 2025). [16]

---

## 5. El Dorado Integration

### 5.1 Current Status

Based on research, **there is no confirmed direct COPM integration with El Dorado P2P**. El Dorado's primary stablecoin is **USDT**, with support for USDM (MountainUSD). El Dorado connects to 80+ Colombian finance apps (Nequi, Daviplata, Bancolombia) for COP on/off-ramp. [22]

### 5.2 Potential Path

El Dorado could theoretically list COPM as a tradeable stablecoin on its P2P marketplace, but currently the COP<->crypto bridge on El Dorado goes through USDT, not COPM. [22]

### 5.3 Implications

The lack of El Dorado integration means COPM's retail distribution is largely captive within the Littio ecosystem. If El Dorado were to integrate COPM, it would significantly expand the user base beyond Littio users and provide a new P2P price discovery mechanism.

---

## 6. Relationship to cCOP (Mento)

### 6.1 Key Differences

| Dimension | COPM (Minteo) | cCOP (Mento) |
|-----------|--------------|--------------|
| **Issuer** | Minteo (centralized company) | Mento Protocol (DAO-governed) |
| **Backing** | 1:1 fiat reserves in Colombian banks | Diversified on-chain collateral (crypto) |
| **Regulatory approach** | BDO-audited, SFC-supervised banks | Decentralized, no banking relationship |
| **Chain** | Polygon (primary), Celo, Solana | Celo only |
| **Users** | 100K+ via Littio + 50 B2B clients | Small (cCOP ~0.25% of Mento total reserves) |
| **Volume** | $200M/mo | Minimal |
| **Governance** | Corporate (Santiago/William/Javier) | Mento community governance |
| **Audit** | BDO monthly attestation | On-chain reserve transparency |

### 6.2 Competition or Coexistence?

Per Celo Colombia's forum post, "COPM (issued by Minteo) is a completely different asset from cCOP, and they do not create conflicts with each other." [23]

In practice, **COPM dominates** in real-world usage. cCOP is a governance experiment with minimal traction. The Celo Colombia team ran a cashback pilot in Medellin using cCOP but reported "a lack of consistent merchant commitment." [21]

### 6.3 For Hedging Instrument Purposes

COPM is the clear winner as a behavioral signal source. cCOP lacks the user volume and real-world transaction data needed for calibration.

---

## 7. Competitive Landscape

### 7.1 COP-Pegged Stablecoins

| Token | Issuer | Chain | Backing | Status |
|-------|--------|-------|---------|--------|
| **COPM** | Minteo | Polygon/Celo/Solana | 1:1 fiat | Active, $200M/mo volume |
| **cCOP** | Mento | Celo | On-chain collateral | Active, minimal volume |
| **nCOP** | Num Finance (Argentina) | Polygon | Over-collateralized reserves | Active, smaller scale |

nCOP (Num Finance) launched in August 2023 on Polygon, targeting the $10B Colombia remittance market. It offers 8% yield to attract corporate remittance senders. [24] However, nCOP has not achieved COPM's scale.

### 7.2 USDT/USDC + P2P Exchange Path

The dominant pattern in Colombia remains:
- Receive USD income (freelance, remittance)
- Convert to USDT on exchange
- Sell USDT for COP on P2P platform (El Dorado, Bitso, Binance P2P)
- Receive COP to Nequi/Daviplata/bank account

This path has **far higher volume** than COPM overall (4 out of 10 Colombian crypto purchases are stablecoins). [10] But it requires the user to actively manage crypto -- COPM via Littio abstracts this away.

### 7.3 Bitso

Bitso operates in Colombia as a regulated LATAM exchange with free COP deposits/withdrawals. It offers COP trading pairs for major assets and has published a "Stablecoin Landscape in Latin America" report covering H1 2025. [25] Bitso's volume likely exceeds COPM's, but Bitso is a general exchange, not a COP-specific stablecoin.

### 7.4 MoneyGram

MoneyGram launched its "digital dollar" app in Colombia (2025) with USDT-backed balances, providing a regulated bridge from on-chain value to cash pickup. [10] This competes with COPM for the remittance use case but uses USD-denomination, not COP.

---

## 8. Implications for Hedging Instrument

### 8.1 Is COPM Usage Income-Driven or Payment-Driven?

**Primarily income-driven.** The evidence:

1. **Littio channel (100K users):** Users deposit salary/freelance income as COP, convert to COPM or USDC for savings. This is income conversion behavior. [11]
2. **B2B channel (50+ companies):** Companies use COPM for operational payments -- this is business income/treasury management. [18]
3. **Remittance channel:** Incoming remittances represent diaspora income flowing into Colombian households. [19]
4. **NOT payment-driven (yet):** No merchant acceptance, no POS integration, no bill payment capability confirmed.

**Conclusion:** COPM flow is a proxy for **income deposited into the formal digital economy by Colombian households and businesses**. It captures the act of a Colombian person or company taking COP income and placing it on-chain.

### 8.2 Does COPM Flow Carry Information About Colombian Household Income?

**Yes, with caveats:**

**Signal strength:**
- Mint volume (COP -> COPM) reflects **income flowing into the stablecoin system** -- mostly via Littio savings deposits and B2B operational payments.
- Redeem volume (COPM -> COP) reflects **spending needs or capital withdrawal** -- when users need COP fiat for expenses.
- The mint/redeem ratio carries information about whether Colombian users are net saving (income > spending) or net withdrawing (spending > income).

**Caveats:**
- 100K users is significant for Colombia but is still a self-selected sample (urban, digitally-literate, fintech-friendly).
- $200M/month volume likely includes B2B flows that reflect business activity, not household income directly.
- The data is concentrated in one distribution channel (Littio) -- a single point of failure.

### 8.3 Could a Variance Swap on COPM Flows Be Meaningful?

**Yes, under specific construction:**

The observable we care about is the **realized variance of COPM net flow** (minting minus redemption volume, measured daily or weekly).

**Why this works:**
1. During normal times, COPM net flow should be relatively stable -- steady salary deposits, steady spending withdrawals.
2. During **income shocks** (recession, mass layoffs, informal sector collapse), mint volume drops (less income to deposit) while redeem volume may spike (households need cash).
3. During **COP depreciation shocks**, users may accelerate COPM->USDC conversion (flight from COP), creating measurable flow variance.
4. During **inflation shocks**, the purchasing power of COP-denominated COPM erodes, potentially driving behavioral shifts.

**Variance swap construction:**
- **Underlying:** Realized variance of daily COPM net mint/redeem flow (in COP terms)
- **Strike:** Implied variance based on historical Colombian macro stability
- **Settlement:** On-chain, using COPM or USDC
- **Tenor:** Monthly or quarterly, aligned with Colombian salary cycles (monthly) or GDP reporting (quarterly)

### 8.4 What Shocks Would Affect COPM Flows?

| Shock Type | Expected COPM Flow Impact | Direction |
|-----------|--------------------------|-----------|
| **COP depreciation** | Flight to USDC via Littio; reduced COPM minting, increased COPM->USDC swaps | Variance increase |
| **Inflation spike** | Mixed -- more nominal COP flowing in (wages adjust), but real value eroding | Moderate variance increase |
| **Recession / unemployment** | Sharp drop in mint volume (less income); spike in redemptions (cash needs) | Strong variance increase |
| **Remittance corridor disruption** | Reduced inflows from diaspora; affects COPM mint from remittance conversion | Variance increase |
| **Petro/political crisis** | Capital flight behavior (see Feb 2025 tariff crisis -- Littio saw 100%+ new USDC accounts) | Strong variance increase |
| **Minteo operational risk** | If Minteo or Littio has downtime, flows stop -- this is platform risk, not macro signal | Noise, not signal |
| **Regulatory action** | SFC crackdown on stablecoins would collapse all COPM activity | Regime break |

### 8.5 Critical Risk: Single Distribution Channel

The 100K users flow through **Littio**. If Littio changes strategy, is acquired, or fails, COPM retail volume collapses overnight. This is not macro risk -- it is idiosyncratic platform risk. A hedging instrument calibrated on COPM flows must somehow distinguish between:

- **Macro-driven flow variance** (the signal we want)
- **Platform-driven flow variance** (noise from Littio/Minteo operational decisions)

Possible mitigation: Monitor Littio's user growth separately. If COPM flow drops but Littio user count is stable, the flow change is more likely macro-driven. If both drop, it could be platform issues.

---

## 9. Key Data Sources for On-Chain Analysis

| Data Need | Source | Method |
|-----------|--------|--------|
| COPM mint/burn events on Celo | CeloScan / Celo Explorer | Monitor `Transfer` events from/to zero address at `0xc92e8fc2947e32f2b574cca9f2f12097a71d5606` |
| COPM mint/burn events on Polygon | PolygonScan | Same approach, need Polygon contract address |
| Reserve attestation | https://transparency.minteo.com/reserves | Monthly BDO reports |
| COPM/USDT DEX activity on Celo | GeckoTerminal pool `0x4495f525c4ecacf9713a51ec3e8d1e81d7dff870` | Uniswap V3 swap events |
| Littio user metrics | Littio public statements, YC profile | Indirect -- no public API |
| Colombian macro data | Banco de la Republica, DANE, IMF | COP/USD rate, inflation, remittance inflows, GDP |

---

## 10. Summary Assessment

### Strengths as Behavioral Reference

1. **Real users, real income flows.** 100K+ users depositing salary/income through Littio is genuine economic behavior, not DeFi farming.
2. **Fiat-backed, audited.** The 1:1 backing means COPM supply directly reflects COP deposited -- no algorithmic distortion.
3. **$200M/mo volume.** Sufficient scale for statistical significance.
4. **B2B adoption.** 50+ companies provide business income signal in addition to household income.
5. **Credible team.** Wompi/Bancolombia pedigree means this is not a fly-by-night operation.
6. **Multi-chain.** Celo deployment gives us direct on-chain observability.
7. **Kraken listing.** Increases legitimacy and potentially diversifies distribution beyond Littio.

### Weaknesses as Behavioral Reference

1. **Single distribution channel (Littio).** Platform risk is inseparable from macro signal without additional data.
2. **Thin DEX liquidity.** Most volume flows off-chain through Minteo's API, limiting on-chain observability.
3. **No direct merchant adoption.** Cannot observe spending patterns, only savings/treasury patterns.
4. **Urban bias.** Rural Colombia (where income volatility is highest) is likely underrepresented.
5. **Regulatory uncertainty.** Colombian crypto regulation is evolving; a crackdown could eliminate the signal entirely.
6. **Young token.** Launched April 2024 -- less than 2 years of data. Insufficient history for robust variance estimation.

### Recommendation

COPM is the **single best on-chain proxy** for Colombian income conversion activity available today. No other COP-denominated instrument has comparable real-world adoption. However, a hedging instrument should:

1. **Use COPM flow as one input in a composite index**, not the sole signal. Combine with COP/USD exchange rate, Colombian remittance inflow data (Banco de la Republica), and broader Celo stablecoin activity.
2. **Monitor mint/burn events on both Celo and Polygon** to capture the full picture.
3. **Build in circuit breakers** for platform-specific events (Littio downtime, Minteo operational issues).
4. **Start with longer tenor instruments** (quarterly) given the limited history -- monthly variance estimation on <2 years of data is noisy.
5. **Track the Minteo B2B expansion** -- if more companies adopt COPM, the signal becomes more representative and less Littio-dependent.

---

## Citations

[1] Minteo founding team: https://finance.yahoo.com/news/minteo-launches-stablecoin-based-settlement-130000239.html
[2] William Duran co-CEO: https://www.enter.co/startups/copm-la-stablecoin-colombiana-que-ya-mueve-mas-de-us200-millones-mensuales/
[3] Wompi/Easy Taxi backgrounds: https://www.newswire.com/news/minteo-launches-stablecoin-based-settlement-layer-for-latin-america-22295376
[4] $4.3M seed round: https://www.businesswire.com/news/home/20220929005294/en/Latin-American-NFT-startup-Minteo-raises-4.3-million-to-Introduce-Region-to-Web3
[5] COPM launch and backing: https://www.portafolio.co/economia/finanzas/lanzan-copm-la-primera-stablecoin-del-peso-colombiano-minteo-601440
[6] BDO attestation: https://newsroom.seaprwire.com/technologies/minteo-unveils-copm-stablecoin-transforming-latin-americas-financial-landscape/
[7] Minteo transparency portal: https://transparency.minteo.com/
[8] Reserve management: https://transparency.minteo.com/reserves
[9] Colombian crypto regulation: https://cms.law/en/int/expert-guides/cms-expert-guide-to-crypto-regulation/colombia
[10] Stablecoins in Colombia 2025: https://bitwage.com/en-us/blog/state-of-stablecoins-in-colombia---september-2025
[11] Littio neobank: https://www.circle.com/blog/littio-x-usdc-creating-stable-and-secure-banking-in-latam
[12] Minteo settlement layer API: https://minteo.com/
[13] COPM multichain deployment: https://transparency.minteo.com/blockchain
[14] Stabila Foundation / Celo FX campaign: https://x.com/StabilaFnd/status/1859612856750309595
[15] COPM/USDT Celo pool: https://www.geckoterminal.com/celo/pools/0x4495f525c4ecacf9713a51ec3e8d1e81d7dff870
[16] Kraken listing: https://blog.kraken.com/product/asset-listings/copm-is-available-for-trading
[17] CoinCarp COPM: https://www.coincarp.com/currencies/cop-minteo/
[18] COPM B2B adoption: https://www.larepublica.co/finanzas/como-hacer-transacciones-con-stablecoins-4221338
[19] Colombia remittances: https://www.chainalysis.com/blog/latin-america-crypto-adoption-2025/
[20] VelaFi-Minteo partnership: https://blog.velafi.com/en/home/velafi-and-minteo-strengthen-the-financial-bridge-between-colombia-and-asia
[21] Celo Colombia H1 2025 report: https://forum.celo.org/t/celo-colombia-report-2025-h1/11456
[22] El Dorado P2P: https://eldorado.io/en
[23] COPM vs cCOP coexistence: https://forum.celo.org/t/mento-stablecoin-rebranding-and-strategic-evolution/12639/6
[24] nCOP (Num Finance): https://www.coindesk.com/business/2023/08/24/colombian-peso-stablecoin-goes-live-on-polygon-aiming-for-10b-remittances-market
[25] Bitso stablecoin landscape: https://business.bitso.com/ebook/stablecoin-landscape-in-latin-america-first-half-2025
[26] Stabull Finance COPM: https://stabull.finance/supported-stablecoins/copm/
[27] G20 Ventures on Minteo: https://medium.com/g20-ventures/minteo-why-we-invested-43f607e7785a
[28] Colombia macroeconomic data: https://www.focus-economics.com/countries/colombia/
[29] COP depreciation 2024: https://www.ebc.com/forex/why-is-the-colombian-peso-so-weak-in-2025-key-drivers
[30] Celo Colombia cCOP proposal: https://forum.celo.org/t/launch-of-ccop-colombia-s-first-decentralized-stablecoin/9211
