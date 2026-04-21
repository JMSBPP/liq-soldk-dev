# Celo Ecosystem Users: Population Identification for Mento Stablecoin Micro-Payment Patterns

**Date:** 2026-04-02
**Context:** Investigating whether $10-50 median transaction sizes across PUSO (PHP), cKES (KES), cGHS (GHS), and cCOP (COP) reflect income-level behavior or Celo-app-specific behavior, following the hypothesis that uniform transaction sizes across economically dissimilar currencies point to a shared Celo ecosystem cause rather than underlying macro fundamentals.

---

## 1. Opera MiniPay

### What It Is

MiniPay is a non-custodial stablecoin wallet built on the Celo blockchain, launched by Opera in September 2023. It was designed for mobile-first users in markets with limited traditional banking infrastructure. The wallet initially launched inside the Opera Mini browser as a lightweight embedded feature (hence "Mini"), requiring no separate app download.

As of early 2026, MiniPay has spun off into a standalone iOS and Android app and has surpassed **14 million activated wallets across 60+ countries**. It processed over 300 million transactions in its first two years and reported 3.64 million estimated on-chain users on Celo.

Key metrics across its history:
- 1 million wallets: within 5 months of September 2023 launch
- 10 million wallets: mid-2025
- 14 million wallets: late 2025 / early 2026
- Q4 2025 alone saw 50% on-chain user growth

### Countries and Regions

MiniPay launched first in **Nigeria, Kenya, Ghana, and South Africa**. It has since expanded to 60+ countries including Tanzania, Cameroon, Brazil, Germany, Poland, the United States, France, and countries in Southeast Asia and Latin America.

The wallet reached 3 million wallet activations across Nigeria, Ghana, Kenya, and South Africa by mid-2024. Latin American integration (PIX for Brazil, Mercado Pago for Argentina) rolled out in November 2025.

**Philippines:** MiniPay added GCash as a crypto-fiat partner, indicating active presence in the Philippines. The wallet supports 40+ local currencies via fiat on/off-ramp partners (Yellow Card, Fonbnk, Partna, TransFi, Transak, Onramper).

**Colombia:** MiniPay integrated El Dorado as a P2P on/off-ramp partner, covering Colombia, Brazil, Argentina, Bolivia, Paraguay, and Peru. Colombian users can convert between local currency and stablecoins via Llaves, Bancolombia, and Nequi payment rails.

### Supported Stablecoins

MiniPay's primary stablecoin is **cUSD** (Celo Dollar). The July 2024 UI refresh introduced "Pockets," which added USDT and USDC alongside cUSD, with drag-and-drop swaps via the Mento Protocol. Local-currency Mento stablecoins (cKES, cGHS, PUSO, cCOP) are not directly displayed in MiniPay's interface but are accessible on Celo through the Mento dApp and other wallets such as Valora.

**Implication for the Thursday pattern and $10-50 transactions:** MiniPay is focused on cUSD/USDT/USDC rather than local Mento stablecoins. The uniform $10-50 micro-transaction sizes in PUSO, cKES, cGHS, and cCOP are not directly attributable to MiniPay activity since MiniPay's swap mechanism primarily routes through cUSD intermediaries. However, when users acquire local Mento stablecoins from cUSD via the Mento broker, those conversions would appear as Mento broker swaps — and would carry MiniPay-scale transaction sizes ($10-50 is consistent with typical MiniPay bill-pay and peer transfer amounts).

### Transaction Sizes

No published median figures were found for MiniPay transaction sizes. The platform is described as enabling micro-payments at under $0.01 fee per transaction. Given the $12/week UBI amounts disbursed via impactMarket on Celo, and MiniPay's design for low-income users, the $10-50 range is structurally plausible for this user population.

**Sources:**
- [Opera MiniPay launch announcement (Sep 2023)](https://press.opera.com/2023/09/13/opera-launches-minipay/)
- [Opera-Celo Foundation partnership extension (Dec 2025)](https://press.opera.com/2025/12/03/opera-and-celo-foundation-partnership/)
- [MiniPay Latin America integration (Nov 2025)](https://press.opera.com/2025/11/19/minipay-pay-like-a-local-mercadopago-pix/)
- [MiniPay lands in Ghana (Dec 2023)](https://blogs.opera.com/africa/2023/12/minipay-lands-in-ghana-to-simplify-peer-to-peer-financial-transactions/)
- [MiniPay Pockets feature launch](https://crypto.news/minipay-brings-one-click-stablecoin-swaps-to-users-via-new-feature-pockets/)
- [Tether and Opera emerging markets expansion (Feb 2026)](https://press.opera.com/2026/02/02/tether-and-opera-expand-financial-access-in-emerging-markets-through-minipay/)
- [MiniPay 2-year anniversary blog](https://blog.celo.org/celebrating-two-years-of-minipay-operas-noncustodial-stablecoin-wallet-built-on-celo-6ca80ff5c39a)

---

## 2. Celo Proof of Ship / Developer Programs

### What Is Proof of Ship

Proof of Ship (PoS) is a monthly developer incentive program run by CeloPG (Celo Public Goods). Builders submit their active projects, prove on-chain impact, and earn rewards from a monthly prize pool.

**Prize pool per round:** $5,000 cUSD, distributed by AI agents based on milestones, GitHub activity, on-chain activity, and project updates.

### Program Rounds and Timeline

- **Pre-Season (monthly rounds):** Running throughout 2024-early 2025. Labeled by number (Proof of Ship 1, 2, 3, ...). Celo Developers on X announced Proof of Ship 1 Winners in March 2025.
- **Season 1:** Kicked off August 8, 2025. Season 1 ran as part of Celo PG's broader "Celo Season 1" initiative (August-December 2025), which included Proof of Ship allocations, contributor rewards, and Support Streams.
- **Season 2:** Ran until March 28, 2025 (this refers to a Season 2 of an earlier format, as the program evolved).
- Proof of Ship rounds are numbered (at least up to #7 confirmed by mid-2025 beehiiv newsletter).

### Are Prizes in Mento Stablecoins?

Prizes are distributed in **cUSD** specifically. No evidence was found of prize distributions in cKES, PUSO, or cCOP. The $5,000/month prize pool at $5,000 cUSD is modest relative to the transaction volumes seen in PUSO and cKES.

### Could Proof of Ship Explain the July 2025 Spike?

**Unlikely as primary driver, but worth noting:**
- $5,000/month cUSD would need to be converted to local Mento stablecoins to explain spikes in cKES and PUSO.
- If developers in Kenya or the Philippines converted cUSD prize distributions into cKES/PUSO via the Mento broker, this would generate a burst of broker swap transactions — but at only $5,000/month total pool, the scale is too small to explain ecosystem-wide spikes.
- Celo PG Season 1 launched August 8, 2025 — not July 2025.

**Conclusion:** Proof of Ship prize distributions are in cUSD, not local stablecoins, and are too small in scale to explain the July 2025 cross-currency spike.

**Sources:**
- [Proof of Ship program page (CeloPG)](https://www.celopg.eco/programs/proof-of-ship)
- [Proof of Ship Season 1 page](https://www.celopg.eco/programs/proof-of-ship-s1)
- [Expanding Celo's Proof of Ship Program (Karma HQ)](https://paragraph.com/@karmahq/expanding-celos-proof-of-ship-program)
- [Proof of Ship GitHub repo](https://github.com/celo-org/Proof-of-Ship)
- [Celo 2025 Year in Review](https://blog.celo.org/2025-year-in-review-while-crypto-talked-celo-delivered-1f2472952abf)
- [Celo Season 1 Program Guide](https://www.celopg.eco/insights/celo-season-1-program-guide)

---

## 3. Celo Apps Using Mento Stablecoins

### Valora Wallet

Valora is the reference mobile wallet for Celo, originally developed by cLabs, spun out as an independent company with Series A funding (2021). It supports the full suite of Mento stablecoins (cUSD, cEUR, cREAL, cKES, PUSO, cCOP, cGHS, eXOF).

**Countries with Mobile Money withdrawal:**
- Kenya (M-Pesa integration)
- Nigeria
- Ghana (Mobile Money)
- Philippines (early adopter via Celo Philippines DAO)
- India (mentioned in live-country list)

Valora had 200K users with a balance and 53K monthly active users across 100+ countries as of mid-2021. Growth has continued, though MiniPay has since become the dominant consumer wallet.

**Role in Mento stablecoin flows:** Valora is the primary wallet used by impactMarket UBI recipients, Celo Philippines DAO users, and early PUSO/cKES community members. UBI distributions (cUSD) received via Valora are often converted into local Mento stablecoins for local use.

**Sources:**
- [Valora Series A and standalone company announcement (2021)](https://www.prnewswire.com/news-releases/celo-powered-valora-closes-series-a-funding-becomes-a-standalone-company-as-crypto-mobile-app-gains-traction-301341674.html)
- [Valora Philippines guide (BitPinas)](https://bitpinas.com/cryptocurrency/send-money-valora-guide-celo/)
- [Valora withdrawal to Mobile Money (support docs)](https://support.valoraapp.com/hc/en-us/articles/18451688731789-How-to-withdraw-to-Mobile-Money)

### ImpactMarket — UBI Distribution on Celo

ImpactMarket is a decentralized UBI protocol on Celo. It operates as a poverty alleviation program, distributing unconditional basic income in cUSD to beneficiaries in approximately 30 countries.

**Scale:**
- Over $4M distributed to 18,000+ beneficiaries (as of 2023 reports)
- 45,000+ people supported through UBI as of April 2024
- Countries include: Ghana, Philippines, Zimbabwe, Brazil, and others

**Philippines — Montalban Action Group:**
- 45 community members receive $12 (approx. PhP575) per week in cUSD via Valora
- This is a documented use case of regular, predictable, weekly cUSD disbursements to Filipino users
- Recipients are below or marginally above the national poverty threshold (~PhP2,680 or $55/week)

**Transaction size implication:** $12/week per member, received weekly, is directly within the $10-50 range observed in PUSO/cKES Mento broker swaps. If recipients convert their cUSD to PUSO via the Mento broker, each conversion would appear as a $10-15 broker swap.

**Weekly disbursement cadence:** ImpactMarket UBI claims are claimable on a weekly basis, with on-chain smart contracts enforcing the cycle. The specific day of the week is not documented in public sources, but the weekly cadence overlapping with any day-of-week pattern is structurally consistent.

**Sources:**
- [ImpactMarket joins Celo DeFi for the People](https://medium.com/celoorg/impactmarket-joins-celos-defi-for-the-people-initiative-f172b690ea24)
- [Montalban Action Group Philippines — impactMarket docs](https://docs.impactmarket.com/impactmarket-apps/2.-impactmarkets-products/unconditional-basic-income-ubi/how-communities-work/highlighted-stories/philippines-montalban-action-group)
- [Montalban Action Group — Celo Blog spotlight (July 2021)](https://medium.com/celoorg/the-multiplier-effect-of-communities-spotlight-on-the-montalban-action-group-29ec2c7983f3)
- [Crypto Altruism: Three Celo-based social impact projects](https://www.cryptoaltruism.org/blog/chain-highlight-three-celo-based-social-impact-projects)

### Kolektivo — Circular Economy on Celo

Kolektivo is a regenerative finance (ReFi) project building circular economy tools on Celo. It uses community currencies (Kolektivo Guilder) backed by natural assets. It is part of the Climate Collective on Celo.

**Geographic focus:** Netherlands and Caribbean (Curacao initial deployment). Less directly relevant to the KES/PUSO/GHS/COP populations under study, though it demonstrates Celo's non-speculative local currency use-case model.

**Sources:**
- [Crypto Altruism: Celo ReFi projects](https://www.cryptoaltruism.org/blog/chain-highlight-three-celo-based-social-impact-projects)

### Colombian Apps on Celo

**Celo Colombia DAO** is the primary organized entity driving cCOP adoption. Key activities in 2024-2025 H1:

- Launched a cashback pilot in Medellín offering cCOP rewards for fiat payments
- Organized onboarding events where attendees received first wallets, first POAPs, and made small cCOP payments
- Focused on education, promotion, engagement, and loyalty programs
- cCOP makes up approximately 0.25% of Mento's total reserve value as of June 2025 — indicating very low overall circulation (~$75,000 USD equivalent at $30M total Mento outstanding)

**MiniPay in Colombia:** MiniPay integrated El Dorado (P2P on/off-ramp) covering Colombia via Bancolombia, Nequi, and Llaves payment rails. This provides a fiat-crypto bridge but the stablecoin used is cUSD/USDT — not cCOP.

**Implication:** The cCOP user base is small and concentrated in Medellín-area early adopters. Transaction patterns likely reflect a small, organically-grown community rather than mass market adoption. The $10-50 range could reflect event-driven small cCOP transactions from community activities.

**Sources:**
- [Mento cCOP launch announcement](https://www.mento.org/blog/announcing-the-launch-of-ccop---celo-colombia-peso-decentralized-stablecoin-on-the-mento-platform)
- [Celo Colombia Report 2025 H1 (Celo Forum)](https://forum.celo.org/t/celo-colombia-report-2025-h1/11456)
- [Celo Colombia 2024 H2 Report (Celo Forum)](https://forum.celo.org/t/celo-colombia-2024-h2-report/10032)
- [MiniPay Latin America integration — El Dorado](https://minipay.to/blog/pay-like-a-local-with-minipay-latin-america)

---

## 4. The Thursday Pattern

### Finding: Celo Governance Calls Are Held on Thursdays

The most structurally significant finding for the Thursday pattern is that **Celo Governance Calls are scheduled on Thursdays at 7:00 PT / 10:00 ET / 14:00 UTC / 16:00 CET**.

Documented governance call dates include:
- Call #39: January 19, 2024 (Thursday)
- Call #42: February 15, 2024 (Thursday)
- Call #46: April 25, 2024 (Thursday)
- Call #48: June 27, 2024 (Thursday)
- Call #49: July 18, 2024 (Thursday)
- Call #52: September 12, 2024 (Thursday)
- Call #53: October 24, 2024 (Thursday)
- Call #55: December 19, 2024 (Thursday)

The calls are bi-weekly (approximately every 2-4 weeks). These are governance discussions, not on-chain transactions, so they would not directly explain a *weekly* Thursday swap pattern.

### Alternative Thursday Hypotheses

The 56% PUSO / 67% cKES Thursday concentration in Mento broker swaps likely reflects a combination of:

**1. ImpactMarket weekly UBI claim windows.** Smart contract-based UBI on Celo allows beneficiaries to claim cUSD on a weekly basis. If communities coordinate their claim day (which is rational to minimize gas competition and maximize the utility of coordinated spending), a day-of-week concentration would emerge. The Montalban Action Group (Philippines) receives $12/week; similar programs exist in Kenya. If any specific community set its weekly claim window to open on Thursdays, this would drive concentrated Mento broker swap activity as recipients convert cUSD to PUSO or cKES.

**2. Celo community event cadence.** Multiple Celo DAO communities (Celo Africa DAO, Celo Philippines DAO) hold weekly or bi-weekly coordination calls and events. If educational events or onboarding activities cluster on Thursdays (a common mid-week slot used in African and Philippine tech communities), first-time swaps and onboarding transactions would cluster on that day.

**3. Celo Africa DAO or Celo Philippines DAO internal disbursements.** Contributor payments and community grants within DAOs are often dispersed on a fixed weekly cadence. If either DAO pays contributors in cKES or PUSO on Thursdays, this would produce a concentrated weekly signal.

**4. Arbitrage or bot activity responding to Thursday governance signal.** Governance calls on Thursdays may trigger informed trading activity: participants who know about upcoming protocol changes may swap into/out of local stablecoins ahead of or during governance discussions.

**Assessment:** No public source documents a Thursday-specific Mento broker swap schedule. The most plausible explanation is ImpactMarket-style weekly claim cadence combined with Celo DAO contributor disbursements — but this requires on-chain data validation against specific smart contract addresses (ImpactMarket community contracts, DAO treasury contracts).

**Sources:**
- [Celo Governance Call #46 (April 25, 2024)](https://github.com/celo-org/governance/issues/424)
- [Celo Governance Call #49 (July 18, 2024)](https://forum.celo.org/t/celo-governance-call-49-jul-18th-2024/8270)
- [Celo Governance Call #55 (December 19, 2024)](https://github.com/celo-org/governance/issues/511)
- [Current Celo Governance Overview and Procedures](https://forum.celo.org/t/current-celo-governance-overview-procedures/7735)

---

## 5. Celo L2 Migration

### Migration Date and Details

Celo migrated from a Layer 1 blockchain to an Ethereum Layer 2 on **March 26, 2025 at 3:00 AM UTC** at block height 31,056,500. The migration used Optimism's OP Stack with EigenDA for data availability, executed as a hardfork.

**Timeline of migration preparation:**
- July 7, 2024: Dango Testnet launched
- September 26, 2024: Alfajores testnet migrated (block 26,384,000)
- October 9, 2024: Dango Testnet shut down
- February 20, 2025: Baklava testnet migrated (block 28,308,600)
- March 26, 2025: Mainnet migration (block 31,056,500)

The migration preserved nearly five years of transaction history and slashed security costs by 99.8%. It launched with 100+ ecosystem partners.

**Post-migration performance:**
- 600,000 daily active users immediately post-migration
- $1 billion+ monthly stablecoin volume
- 365% protocol revenue growth
- 840,000 daily active users one year after migration

### Were There Migration-Related Airdrops?

No documented airdrop of CELO tokens or Mento stablecoins was found in connection with the L2 migration. CGLD/CELO token balances migrated automatically — existing holders did not need to take any action and received no new tokens as a result of the migration.

**The CELO token now exists on both Celo L2 and Ethereum mainnet**, connected by a native bridge. Coinbase documented a CGLD migration event for exchange users, but this was a technical token migration (CGLD renamed to CELO), not an airdrop.

**Implication for July 2025 spike:** The L2 migration (March 2025) is too early to directly explain a July 2025 spike. However, the migration may have increased ecosystem activity and drawn new users into Mento stablecoins during Q2-Q3 2025 as the new L2 infrastructure matured and new dApps launched.

**Sources:**
- [Celo L2 migration documentation](https://docs.celo.org/cel2/notices/l2-migration)
- [Everything you need to know about Celo's migration to L2 (Stakely)](https://stakely.io/blog/everything-you-need-to-know-about-celos-migration-to-l2)
- [Returning Home to Ethereum: Launch of Celo L2 Mainnet (Celo Forum)](https://forum.celo.org/t/returning-home-to-ethereum-the-launch-of-celo-l2-mainnet/10466)
- [Celo hits 840K daily active users one year after L2 migration](https://bitcoinethereumnews.com/ethereum/celo-hits-840k-daily-active-users-one-year-after-ethereum-l2-migration/)
- [Celo CGLD migration — Coinbase Help](https://help.coinbase.com/en/exchange/crypto-transfers/celo-migration)

---

## 6. Celo in Colombia Specifically

### cCOP Launch

cCOP was launched by **Celo Colombia DAO** with support from Mento Labs. The governance proposal was posted October 9, 2024, and the stablecoin launched on the Mento Platform shortly thereafter in late 2024.

cCOP is pegged to the Colombian Peso (COP) and backed by the Mento Reserve (USDT, USDC, BTC, ETH).

### Who Uses It

The cCOP user base is currently a small community of Celo/Web3 early adopters in Colombia, primarily Medellín-based. Key activities:
- **Cashback pilots:** Medellín merchants offer cCOP rewards for fiat payments
- **Onboarding events:** Small-scale education events where attendees make first on-chain transactions in cCOP
- **Developer community:** Builders in the Proof of Ship and Celo PG ecosystem

As of June 2025, cCOP represents only ~0.25% of Mento's total reserve value — roughly $75,000 USD equivalent against ~$30M total outstanding Mento stablecoins.

### Is MiniPay Available in Colombia?

**Yes, but not with cCOP.** MiniPay is available in Colombia via El Dorado (P2P on/off-ramp) with support for Bancolombia, Nequi, and Llaves payment rails. However, MiniPay's interface offers cUSD, USDT, and USDC — not cCOP. Colombian MiniPay users transact in USD-denominated stablecoins and convert to COP fiat at withdrawal.

This creates a clear gap: the active cCOP user population is the small Celo Colombia DAO community, not the broader MiniPay user base in Colombia.

**Sources:**
- [Mento cCOP launch announcement](https://www.mento.org/blog/announcing-the-launch-of-ccop---celo-colombia-peso-decentralized-stablecoin-on-the-mento-platform)
- [cCOP governance proposal (Celo Forum)](https://forum.celo.org/t/launch-of-ccop-colombia-s-first-decentralized-stablecoin/9211)
- [Celo Colombia Report 2025 H1](https://forum.celo.org/t/celo-colombia-report-2025-h1/11456)
- [MiniPay "Pay like a local" Latin America blog](https://minipay.to/blog/pay-like-a-local-with-minipay-latin-america)
- [MiniPay DevConnect Latin America investor release](https://investor.opera.com/news-releases/news-release-details/minipay-connects-stablecoins-real-time-payment-latin-america)

---

## 7. Synthesis: What Explains the $10-50 Uniform Transaction Pattern

Based on all research, the most likely explanation for $10-50 median transaction sizes uniformly across PUSO, cKES, cGHS, and cCOP is **Celo ecosystem app-level behavior, not income-proportional remittance behavior**.

### Primary Candidate Populations

| Currency | Likely Primary User Population | Transaction Driver |
|---|---|---|
| PUSO (PHP) | Celo Philippines DAO, impactMarket UBI recipients (Montalban Group), Filipino crypto-remittance early adopters | Weekly UBI claims ($12/week), peer transfers, small purchases |
| cKES (KES) | Celo Africa DAO contributors, M-Pesa-to-cKES converters, micro-entrepreneur credit pilots | Community credit disbursements (1M+ cKES to 114 entrepreneurs documented), M-Pesa off-ramp conversions |
| cGHS (GHS) | MiniPay users in Ghana converting to cGHS, Ghanaian fintech early adopters | M-Pesa equivalent transfers, bill payments via cGHS |
| cCOP (COP) | Celo Colombia DAO community in Medellín, event-driven onboarding transactions | Cashback pilot redemptions, community event micro-payments |

### Why the Sizes Are Uniform Across Currencies

The uniformity is explained by:

1. **ImpactMarket UBI amount is fixed at ~$12/week.** This amount is set in USD terms, not in local currency. When a Filipino recipient converts $12 cUSD to PUSO, and a Kenyan recipient converts $12 cUSD to cKES, the Mento broker sees two transactions of the same USD value — even though the local purchasing power differs dramatically.

2. **Celo developer program rewards are denominated in cUSD.** Proof of Ship prizes, Celo PG contributor payments, and DAO disbursements are all in cUSD. When recipients in different countries convert to their local Mento stablecoin, the conversion size reflects USD-denominated prize amounts, not local income levels.

3. **MiniPay default transaction patterns.** MiniPay users interact primarily in cUSD. When they use the "Pockets" swap feature to convert to local Mento stablecoins, the swap sizes reflect typical MiniPay peer transfer sizes, which are anchored to USD micro-payment norms ($5-50), not local currency wage levels.

4. **Mento broker trading limits impose floor/ceiling.** Mento's exchange mechanics include protocol-level trading limits (bucket sizes, rate limits) that may create clustering at certain swap sizes. Small swaps cluster at minimum meaningful amounts.

### Thursday Hypothesis — Refined Assessment

The Thursday concentration (56% PUSO, 67% cKES) most likely reflects **weekly ImpactMarket UBI claim windows** combined with **Celo DAO contributor disbursement days**. The Celo Governance Call cadence (bi-weekly Thursdays) is a correlate but not a driver of on-chain swaps.

To confirm or reject this hypothesis, on-chain analysis should identify:
1. The `CommunityTreasury` smart contracts for impactMarket communities in the Philippines and Kenya, and whether their `claimInterval` and initialization timestamps produce a Thursday claim window.
2. Whether Celo Africa DAO or Celo Philippines DAO treasury disbursement transactions cluster on Thursdays.

---

## 8. Stablecoin Market Statistics (Reference)

| Stablecoin | Market Cap (approx. mid-2025) | Notes |
|---|---|---|
| cKES | ~$216,000 | Driven by remittance flows and M-Pesa integration |
| cGHS | ~$22,000 | Early-stage experimentation |
| Total African local stablecoins (cNGN, cKES, cZAR, ZARP, cGHS, eXOF) | 670M+ tokens in circulation | ~$7M+ volume mid-2025 |
| Total Mento stablecoins outstanding | ~$30M | cCOP = 0.25% (~$75K) |

Mento processed 550M+ transactions in 2024, serving 8M+ users. Total decentralized stablecoin trading volume via Mento exceeded $18.5B in 2025.

**Sources:**
- [Rise of Local Stablecoins in Africa (IntelliSages)](https://intellisages.substack.com/p/the-rise-of-local-stablecoins-in)
- [Mento Labs $10M fundraise announcement](https://www.mentolabs.xyz/blog/mento-labs-fundraise)
- [Mento Protocol on DefiLlama](https://defillama.com/protocol/mento)
- [Mento cKES Hackathon 2024 (Devpost)](https://mento-innovate-hackathon.devpost.com/)

---

## 9. Action Items for Further Investigation

1. **On-chain:** Query ImpactMarket community smart contracts (specifically Philippines and Kenya community addresses) for `claimPeriod` parameter and first-claim timestamps. Verify if weekly claim windows align with Thursdays.

2. **On-chain:** Identify Celo Africa DAO and Celo Philippines DAO treasury addresses. Check disbursement transaction timestamps for day-of-week pattern.

3. **On-chain:** Cross-reference PUSO and cKES Mento broker swap addresses against known Valora wallet addresses and impactMarket beneficiary addresses.

4. **Research:** Contact Celo Colombia DAO directly (active on Celo Forum as `CeloColombia`) to ask about their cCOP onboarding event schedule — specifically whether events consistently occur on Thursdays.

5. **Data:** Query Mento broker swap contracts filtering by transaction sizes $5-60 to isolate the micro-payment cluster, then check counterparty wallet age (new wallets suggest onboarding events; old wallets suggest recurring users like UBI recipients).
