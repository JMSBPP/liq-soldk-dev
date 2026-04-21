# Filipino Play-to-Earn Gaming Income Economy and Crypto-to-PHP Conversion

*Date: 2026-04-02*
*Status: Research complete -- findings integrated with PUSO behavioral fingerprint data*
*Purpose: Determine whether PUSO's $10-50 median transaction cohort represents a gaming-income population, and whether that population is useful for a variance swap on net USD-to-PHP flows*

---

## Executive Summary

The Filipino play-to-earn economy experienced a boom-bust cycle from 2021 to 2023 (Axie Infinity), partially recovered through Pixels on Ronin in 2024-2025, and now exists as a smaller but persistent income source for an estimated 1-3 million active Filipino players. Typical daily earnings in 2025-2026 range from $1-5/day (down from $10-30/day during the 2021 Axie peak), with cashout pathways running through Ronin to Coins.ph/GCash.

**Critical finding for the variance swap project**: The PUSO $10-50 median transaction pattern is MORE consistent with gaming-income cashouts than with OFW remittance or freelancer income conversion. However, the Celo-Ronin ecosystem gap means Filipino gamers are unlikely to be the actual PUSO users. The $10-50 cohort on PUSO is more likely Celo community campaign participants than gamers. The gaming-income population exists and is large, but it lives on Ronin, not Celo.

**Bottom line**: Gaming income is a real, volatile, PHP-conversion-dependent income flow affecting millions of Filipinos. But it is not what PUSO is capturing, and it would need to be targeted through Ronin/PHPC infrastructure, not Celo/PUSO.

---

## 1. Current State of Play-to-Earn in Philippines (2025-2026)

### 1.1 Active Games and Ecosystems

| Game | Chain | Token(s) | Status (2025-2026) | Filipino Share |
|------|-------|----------|---------------------|----------------|
| Axie Infinity | Ronin | AXS, SLP | Declined from 2.7M to ~250K DAU; Ragnarok collab announced Dec 2025 with "Atia's Legacy" playtest Q1 2026 | ~35-40% of remaining players |
| Pixels | Ronin | PIXEL | 1M+ DAU as of Mar 2026; Chapter 2 launched 2025 with improved tokenomics | ~30% (est. 300K+ Filipino DAU) |
| Various Ronin games | Ronin | RON | Ronin network is the dominant Filipino gaming chain | Majority SE Asian |
| Solana games (various) | Solana | Various | Smaller Filipino presence; Star Atlas, Aurory | Minimal Filipino-specific data |

Sources:
- [Axie Infinity Live Player Count (ActivePlayer.io)](https://activeplayer.io/axie-infinity/)
- [Pixels hits 1.1M players on Ronin (P2E.game)](https://www.p2e.game/dailyNews/4sj4qu7fhwn8)
- [Pixels Crypto Game Fuels Resurgent Ronin (CoinDesk)](https://www.coindesk.com/business/2024/03/21/pixels-crypto-game-fuels-resurgent-ronin-blockchain/)
- [Ronin Network on X: Pixels growth from 5K to 1.5M DAU](https://x.com/Ronin_Network/status/1872621252885848195)

### 1.2 Estimated Filipino Player Population

| Source | Estimate | Date | Notes |
|--------|----------|------|-------|
| Fintech Alliance PH survey | 2.8M active in P2E | 2025 | Likely includes casual participants |
| Pixels (30% of 1M DAU) | ~300K daily Filipino Pixels players | Mar 2026 | Active, daily engagement |
| Axie Infinity (~40% of 250K) | ~100K daily Filipino Axie players | 2025 | Down from ~1M at peak |
| Total gaming population | 67.7M Filipino gamers | 2024 | All games, not just P2E |

Sources:
- [BusinessDiary.com.ph: P2E Games in 2025](https://businessdiary.com.ph/35388/play-to-earn-games-in-2025-how-filipinos-are-earning-via-blockchain/)
- [BitPinas: Pixels Philippine players](https://bitpinas.com/feature/pixels-achieves-1-million-daily-users/)
- [Antom: Philippines Gaming & Payment Trends](https://knowledge.antom.com/philippines-gaming-payment-trends-report-active-value-driven-players-power-growth-as-digital-wallets-take-centre-stage)

### 1.3 Current Daily/Monthly Earnings (2025-2026)

Earnings have collapsed from the 2021 peak. Current estimates:

| Era | Typical Daily Earnings (USD) | Monthly (USD) | Context |
|-----|-----|------|---------|
| Axie peak (Jul-Nov 2021) | $15-30 | $300-$400 | SLP at $0.20-0.35; above PH minimum wage |
| Axie decline (2022-2023) | $1-3 | $30-$80 | SLP crashed to $0.003-0.01 |
| Pixels 2024 | $2-5 | $50-$150 | PIXEL token airdrop + farming |
| Pixels 2025-2026 | $1-3 (est.) | $20-$80 (est.) | PIXEL at ~$0.008; energy-gated earnings |
| Exceptional case | Higher | ~$500+ | University tuition paid via Pixels; requires months of grinding + event participation |

The PIXEL token price as of early 2026 is approximately $0.008. A player accumulating 6,000 PIXEL over several months (documented case) would earn roughly $48, consistent with the $10-50 per cashout transaction size observed in PUSO data.

Sources:
- [CoinGecko: Axie Infinity research on Filipino income](https://www.coingecko.com/research/publications/how-playing-axie-infinity-nft-game-helps-filipinos-earn-income)
- [Pixels pays university tuition (GAMES.GG)](https://games.gg/news/pixels-pays-university-tuition-with-game-earnings/)
- [CoinMarketCap: PIXEL price](https://coinmarketcap.com/currencies/pixels/)
- [TIME: Axie Infinity Philippines debt](https://time.com/6199385/axie-infinity-crypto-game-philippines-debt/)

### 1.4 Cashout Pathway

The standard Filipino gamer cashout pipeline in 2025-2026:

```
In-game tokens (PIXEL, SLP, AXS)
    --> Ronin Wallet
        --> Katana DEX (swap to RON or USDC on Ronin)
            --> Binance or Coins.ph (centralized exchange)
                --> GCash / Maya / bank transfer (PHP)
```

Key infrastructure:
- **Coins.ph** launched PHPC stablecoin on Ronin specifically to serve this population
- **PHPC on Ronin** enables direct: game token --> PHPC --> GCash PHP cashout
- **QRPH integration planned for 2026**: Would connect PHPC to 600K+ merchants

Sources:
- [Coins.ph launches PHPC on Ronin](https://coins.ph/blog/coins-ph-launches-phpc-stablecoin-on-ronin/)
- [Ronin Blog: PHPC is LIVE](https://roninchain.com/blog/posts/phpc-is-live-on-ronin)
- [CryptoNews: PHPC on Ronin](https://cryptonews.com/news/coins-ph-launches-first-philippine-peso-stablecoin-phpc-on-ronin-blockchain/)
- [BitPinas: How to cash out P2E earnings](https://bitpinas.com/feature/how-to-cash-out-earnings-from-play-to-earn-metaverse-games/)

---

## 2. Gaming Income as Livelihood

### 2.1 Primary vs. Supplementary Income

During the 2021 Axie peak, play-to-earn was treated as PRIMARY income by a significant cohort:
- Families told stories of students, parents, and even grandparents joining Axie scholarship programs
- Players in the Philippines were earning $300-$400/month, exceeding the minimum basic salary
- Some quit traditional jobs to play full-time

By 2025-2026, gaming is overwhelmingly SUPPLEMENTARY:
- Current daily earnings of $1-5/day are below Metro Manila minimum wage (PHP 695/day, approximately $12.50/day)
- Even in lower-cost provinces (minimum wage PHP 435-550/day), gaming earnings are insufficient as primary income
- Games are now "a source of income" alongside other work, not a replacement

Sources:
- [France24: "Life-changing" or scam? Axie Philippines](https://www.france24.com/en/live-news/20220215-life-changing-or-scam-axie-infinity-helps-philippines-poor-earn)
- [Playroll: Philippines Minimum Wage Rates](https://www.playroll.com/minimum-wage/the-philippines)
- [Sprout Solutions: Minimum Wage Manila 2026](https://sprout.ph/articles/how-much-is-the-minimum-wage-in-manila/)

### 2.2 Player Demographics

| Dimension | Profile |
|-----------|---------|
| Age | Primarily 18-35 (Gen Z and Millennials) |
| Location | Mix of Metro Manila and provinces; provincial players disproportionately represented (lower opportunity cost) |
| Education | Mixed; includes college students, some graduates, some without higher education |
| Income bracket | Lower-income households (PHP 9,000-18,200/month household income common among gaming populations) |
| Urban/Rural | Both; mobile gaming penetration is high in rural areas |
| Gender | Skews male but female participation significant (especially through scholarship programs) |
| Tech access | Smartphone with mobile data; gaming requires moderate bandwidth |

Sources:
- [Statista: Online gamers Philippines by age](https://www.statista.com/statistics/1117251/philippines-online-gamers-by-age/)
- [Kadence: Online gaming Philippines demographics](https://kadence.com/knowledge/how-online-gambling-is-changing-the-game-in-the-philippines-2/)
- [SAGE Journals: Gaming in Manila slum communities](https://journals.sagepub.com/doi/10.1177/1461444819838497)

### 2.3 Comparison to Minimum Wage

| Metric | Value | Source |
|--------|-------|--------|
| Metro Manila daily minimum (non-agri, 2025-2026) | PHP 695 (~$12.50) | DOLE Wage Order NCR-26 |
| Provincial daily minimum (lowest) | PHP 435 (~$7.80) | MIMAROPA region |
| Axie peak daily earnings (2021) | $15-30 (PHP 750-1,500) | Above Metro Manila minimum |
| Current P2E daily earnings (2025-2026) | $1-5 (PHP 56-280) | Well below any regional minimum |
| Average annual OFW remittance per worker | PHP 129,000 (~$2,300) | PSA Survey on Overseas Filipinos 2024 |

**The income comparison is stark**: In 2021, gaming rivaled or exceeded minimum wage. In 2025-2026, it provides roughly 10-40% of the minimum daily wage, making it supplementary income only.

### 2.4 Guilds and Scholarship Programs

| Organization | Status (2025-2026) | Notes |
|-------------|---------------------|-------|
| Yield Guild Games (YGG) | Pivoted to "Guild Protocol" (Sep 2024); launched yggplay.fun (Nov 2025); $YGG token on Abstract (May 2025) | No longer primarily a scholarship operator; now a protocol layer |
| Community guilds | Some still active but smaller scale | Many dissolved after Axie crash |
| Scholarship model generally | Largely defunct for Axie; limited revival for Pixels | The profit-sharing model collapsed when token values fell below subsistence |

YGG, the largest Philippine-origin guild, raised $30M+ and was founded by Gabby Dizon and Beryl Li. Its strategic pivot from monolithic guild to protocol infrastructure (Sep 2024 concept paper) signals the broader transition of the scholarship model from livelihood provision to platform-level tooling.

Sources:
- [Naavik: YGG Update and Outlook](https://naavik.co/digest/yield-guild-games-update/)
- [Messari: YGG Profile](https://messari.io/project/yield-guild-games/profile)
- [CoinGecko: Play-to-Earn Scholarship Viability Study](https://www.coingecko.com/research/publications/play-to-earn-a-study-on-scholarship-viability)

### 2.5 Academic Research

Three significant peer-reviewed papers on Filipino P2E income:

1. **"Playing for keeps: Digital labor and blockchain precarity in play-to-earn gaming"** (2024, Geoforum / ScienceDirect)
   - Examines P2E as digital labor; finds "blockchain-based precarity" through volatile earnings, insecure contractual employment, and onerous working conditions
   - Uses Axie Infinity as case study with Reddit discourse analysis
   - [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0016718524000708)

2. **"Web3 and deep play: Blockchain gaming in the Global South"** (2025, New Media & Society / SAGE)
   - Grounded Theory analysis of interviews with Filipino players
   - Key finding: players contextualize P2E through the cultural frame of cockfighting and the "side hustle" economy
   - Argues that players approached the game as entrepreneurial agents, developing scholarship programs
   - [SAGE Journals](https://journals.sagepub.com/doi/10.1177/14614448251336435)

3. **"Playing, earning, crashing, and grinding: Axie Infinity and growth crises in the Web3 economy"** (2025, Big Data & Society / SAGE)
   - Traces Axie's economic collapse; argues it was not merely crypto volatility but a tokenomics failure of reliance on infinite growth
   - Examines how players transitioned from earning to grinding to abandoning
   - [SAGE Journals](https://journals.sagepub.com/doi/10.1177/20539517251357296)

No World Bank working papers or arxiv papers were found specifically on Filipino P2E income.

---

## 3. Income Volatility in Gaming

### 3.1 Sources of Volatility

Gaming income has THREE layers of volatility, making it significantly more volatile than traditional income:

**Layer 1: Token Price Volatility**
- SLP (Axie) went from $0.03 to $0.32 (+900%) in one week (Apr-May 2021), then to $0.003 (-99%) by 2023
- PIXEL is currently at $0.008, down from ATH of ~$0.60 at launch (-98%)
- These are not normal asset price swings; they are existential for income-dependent players

**Layer 2: Game Economy Changes**
- Reward schedule updates (developers adjust token emission rates)
- Energy systems limit daily earning capacity
- New game mechanics can obsolete existing earning strategies
- Developer decisions to rebalance in-game economy

**Layer 3: Platform/Infrastructure Risk**
- Ronin bridge hack (Mar 2022): $625M stolen, bridge closed for months, all cashouts frozen
- Exchange delistings can remove cashout pathways
- Regulatory actions (BSP moratorium on new VASPs)

### 3.2 Comparison to Other Income Volatility

| Income Type | Annualized Volatility (est.) | Shock Frequency | Recovery Time |
|-------------|------------------------------|-----------------|---------------|
| Gaming P2E tokens | 200-500% | Weekly | Months-never |
| OFW remittance flow | 5-15% | Quarterly | 1-2 quarters |
| Freelancer USD income | 20-40% | Monthly | 1-3 months |
| PHP/USD exchange rate | 8-12% | Continuous | N/A (mean-reverting) |
| Philippine CPI | 3-6% | Monthly | Sticky |

**Gaming income is an order of magnitude more volatile than any other Filipino income source.** The variance is dominated by token-price risk rather than labor-market risk.

### 3.3 FX Risk Exposure

Filipino gamers face the SAME USD/PHP exchange rate risk as OFW remittance receivers, PLUS additional layers:

```
Total income risk = Token_price_risk * Game_economy_risk * USD_PHP_FX_risk * Platform_risk
```

For OFW remittance:
```
Total income risk = Employment_risk * USD_PHP_FX_risk
```

The multiplicative structure means gaming income variance is dramatically higher.

### 3.4 Demand for Hedging

**There is no observed demand for hedging gaming income volatility.** Players appear to:
- Accept volatility as inherent to the activity
- "Dollar-cost average out" by cashing out small amounts daily/weekly rather than holding
- Diversify across multiple games rather than hedging any single one
- Treat gaming as gambling/side-hustle with expected downside risk

This is consistent with the academic finding (Witteborn 2025) that Filipino players culturally frame P2E through cockfighting -- an activity where volatility IS the point, not something to hedge against.

Sources:
- [Cornell: What the crash of P2E reveals about Web3](https://infosci.cornell.edu/news-stories/what-crash-play-earn-game-reveals-about-future-web3)
- [Euronews: P2E legitimate income or house of cards](https://www.euronews.com/next/2022/02/18/are-play-to-earn-crypto-games-a-legitimate-revenue-stream-or-a-house-of-cards)

---

## 4. Behavioral Comparison: Gamers vs. OFW Remittance vs. Freelancers

### 4.1 Transaction Pattern Fingerprints

| Dimension | P2E Gamers | OFW Remittance | Freelancers |
|-----------|-----------|----------------|-------------|
| **Frequency** | Daily to weekly | Monthly (payday-aligned) | Biweekly to monthly |
| **Typical Size** | $5-50 per cashout | $200-$1,000 per transfer | $500-$2,000 per invoice |
| **Timing** | Afternoons/evenings PHT (post-gameplay) | 1st and 15th of month (US payday) | End of sprint/month |
| **Day pattern** | Slightly weekend-heavy (more play time) | Weekday (banking hours) | Weekday |
| **Regularity** | Irregular (depends on token price, gameplay) | Highly regular (monthly obligation) | Semi-regular (project-based) |
| **Seasonal** | Event-driven (game launches, airdrops) | December peak (Christmas + 13th month) | Q4 elevated (year-end projects) |
| **Chain** | Ronin (dominant), some Solana | Ethereum/Polygon/Celo (stablecoin rails) | Ethereum/Polygon (USDC) |
| **Token** | PIXEL, SLP, AXS, RON | USDC, USDT | USDC, USDT |
| **Cashout method** | DEX swap to RON/USDC then CEX to GCash | Stablecoin to Coins.ph/GCash | Payoneer/Wise to bank, or USDC to Coins.ph |

### 4.2 PUSO Data vs. These Fingerprints

Comparing to the PUSO behavioral fingerprint data from `PUSO_BEHAVIORAL_FINGERPRINTS.md`:

| PUSO Observable | Gamer Match? | OFW Match? | Freelancer Match? |
|----------------|-------------|-----------|-------------------|
| Median tx $20, modal $10-50 | **YES** | No ($200-1K expected) | No ($500-2K expected) |
| PHT business hours peak (9am-3pm) | Partial (gamers often play evenings) | No (US payday timing expected) | Partial |
| Thursday 56% of trades | No (no gaming reason for Thursday) | No | No |
| No December seasonality | **YES** (gaming not Christmas-aligned) | **No** (OFW December peak expected) | Partial |
| July 2025 explosive spike | **Maybe** (could be game event) | No | No |
| 83.7% occasional users | **YES** (try-and-leave consistent with campaigns) | No (remitters are regular) | No |
| Only 2 regular multi-month users | Problematic for any hypothesis | No | No |

**The $10-50 size and lack of December seasonality are consistent with gaming income.** But the Thursday spike and campaign-driven user pattern point to Celo ecosystem activity, not organic gaming cashouts.

### 4.3 Population Overlap

These populations are NOT cleanly separated:

- Some OFWs play P2E games as a side activity (especially during COVID)
- Some freelancers game on the side
- Some gamers graduate to freelancing as they develop tech skills
- Filipino crypto literacy built through gaming creates pathways to other crypto-income activities

However, the overlap is smaller than it might appear. The core gaming population (lower-income, provincial, younger) is demographically distinct from the freelancer population (higher-income, educated, English-fluent, urban) and the OFW population (diverse ages, geographically dispersed, less crypto-native).

### 4.4 Population Sizing for Weighting

| Population | Estimated Size (2025-2026) | Est. Monthly Crypto-to-PHP Conversion | Source Quality |
|-----------|---------------------------|---------------------------------------|----------------|
| OFW remittance (total) | ~10M OFWs, ~5M active remitters | ~$3B/month total; ~$60-165M via crypto rails (2-5%) | BSP data (high quality) |
| OFW crypto remittance | Unknown; est. 100K-500K using stablecoin rails | $60M-$165M/month | Industry estimates (low quality) |
| Freelancers (all) | ~1.5M | ~$750M/month total; crypto portion unknown | Industry reports (medium) |
| P2E gamers (active earners) | ~500K-1M earning regularly | $15M-$50M/month (est. $30-50/person/month avg) | Very rough estimate |
| P2E gamers (total registered) | 2.8M (Fintech Alliance PH) | Most earning near-zero | Survey data |

**Gaming income's share of total PHP conversion**: If total USD-to-PHP conversion (all channels) is roughly $5-6B/month, gaming represents approximately 0.3-1% of total flow. This is small but NOT negligible -- it is in the same order of magnitude as crypto-mediated OFW remittance.

Sources:
- [BSP: Personal remittances 2025](https://www.bsp.gov.ph/SitePages/MediaAndResearch/MediaDisp.aspx?ItemId=7554)
- [Mordor Intelligence: Philippines Remittances Market](https://www.mordorintelligence.com/industry-reports/philippines-remittances-market)
- [Disruption Banking: Philippines crypto giant](https://www.disruptionbanking.com/2025/11/11/how-the-philippines-became-asias-crypto-giant/)

---

## 5. Celo / Ronin Ecosystem Connection

### 5.1 The Ecosystem Gap

**This is the critical finding**: Filipino gamers live on Ronin. PUSO lives on Celo. There is no bridge between them.

| Feature | Celo (PUSO) | Ronin (PHPC) |
|---------|-------------|--------------|
| Filipino gaming presence | Minimal | Dominant |
| Filipino gamer wallet | Valora (limited adoption) | Ronin Wallet (millions) |
| Peso stablecoin | PUSO (decentralized, Mento) | PHPC (Coins.ph, BSP-regulated) |
| Cashout to GCash | Indirect (via BloomX, limited) | Direct (via Coins.ph) |
| Transaction volume | ~600-1000 trades/month (20 traders) | Orders of magnitude larger |
| Regulatory status | Community DAO, no BSP license | Coins.ph is BSP-licensed VASP |

**Filipino gamers are NOT using Celo.** The Celo Philippines DAO exists as a community initiative, and Valora had some early adoption (98% onboarding success in a Grameen Foundation COVID relief program), but the gamer cashout pipeline runs entirely through Ronin.

### 5.2 What Is PUSO Actually Capturing?

Based on the behavioral fingerprints:
- The July 2025 spike (1,617 unique traders) is almost certainly a Celo ecosystem campaign/airdrop, not gaming activity
- The Thursday concentration (56% of trades) suggests coordinated community activity
- The $10-50 median is consistent with campaign reward sizes, not organic economic activity
- Post-campaign, the market settled to ~20 active traders

**PUSO is capturing Celo community experiment participation, not gaming income conversion.**

### 5.3 Could the July 2025 PUSO Spike Be Gaming-Related?

Unlikely for several reasons:
1. No major Ronin game event in July 2025 that would drive Celo activity
2. No Celo-Ronin bridge exists for gamers to move funds
3. The spike pattern (massive one-month surge followed by collapse) matches airdrop/campaign behavior, not income conversion
4. Pixels Chapter 2 launched earlier in 2025, not in July

### 5.4 Valora Wallet in Philippines

Valora (Celo's mobile wallet) had early momentum in the Philippines through the Grameen Foundation partnership and COVID relief distributions. However:
- Recent adoption data (2025-2026) is unavailable
- The wallet is not listed among top Filipino crypto wallets in 2025 surveys
- GCash (with USDC support as of Sep 2025) and Coins.ph dominate mobile crypto in PH
- Valora's Philippine user base appears to have stagnated

Sources:
- [BitPinas: Valora Guide Philippines](https://bitpinas.com/cryptocurrency/send-money-valora-guide-celo/)
- [Valoraapp.com: Grameen Foundation Success Story](https://valoraapp.com/blog/the-grameen-foundation-and-valora-a-success-story)
- [Bitwage: State of Stablecoins Philippines Sep 2025](https://bitwage.com/en-us/blog/state-of-stablecoins-in-philippines-september-2025)

---

## 6. Population Sizing Summary

### 6.1 Filipino Crypto-Income Earners (All Sources)

| Category | Estimated Population | Monthly Income (USD, median) | Growth Trajectory |
|----------|---------------------|------------------------------|-------------------|
| P2E Gaming (active earners) | 500K-1M | $30-80 | Stable to slowly declining |
| Freelancing (crypto-paid) | 200K-400K (of ~1.5M total freelancers) | $800-2,000 | Growing |
| OFW crypto remittance senders | 100K-500K (of ~5M remitters) | $500-1,000 per transfer | Growing rapidly |
| DeFi/trading (income, not speculation) | 50K-100K | Highly variable | Cyclical |
| **Total** | **~1M-2M** | Varies | Mixed |

### 6.2 Share of Total PHP Conversion from Gaming Income

```
Total OFW remittances (2025):          $39.62B/year  = $3.3B/month
Estimated freelancer income (crypto):   $2B-$5B/year  = $170M-$420M/month (rough)
Estimated gaming income conversion:     $180M-$600M/year = $15M-$50M/month (rough)

Gaming share of total crypto-to-PHP:    ~5-15%
Gaming share of ALL USD-to-PHP:         ~0.3-1%
```

### 6.3 Trajectory

| Direction | Evidence |
|-----------|----------|
| **Gaming income is stable to declining** | Token prices at multi-year lows; no new Axie-scale breakout game; scholarship model defunct; current earnings below minimum wage |
| **Freelancer crypto income is growing** | BPO sector strong; remote work trend; crypto payment infrastructure improving |
| **OFW crypto remittance is growing fastest** | Coins.ph/BCRemit partnerships; GCash USDC; fee advantage (1% vs. 5-10%); BSP endorsement |

---

## 7. Assessment: Can Gaming Income Population Be Targeted?

### 7.1 (a) Direct targeting as hedging instrument users

**Verdict: Probably not, for three reasons.**

1. **Income too small for hedging to matter**: At $30-80/month, the cost of any hedging instrument (spread, gas, complexity) would eat a disproportionate share of income. These users need to maximize every dollar, not pay insurance premiums.

2. **Wrong volatility structure**: Gaming income volatility is dominated by token-price risk and game-economy risk, which are idiosyncratic and game-specific. A variance swap on aggregate USD-to-PHP flows would NOT hedge their primary risk. They need token-price hedges, not FX-flow hedges.

3. **Cultural mismatch**: Academic research (Witteborn 2025) shows Filipino gamers frame P2E through cockfighting culture -- they are risk-seeking, not risk-hedging. The population that treats volatile income as a feature rather than a bug is not the natural customer for a hedging instrument.

### 7.2 (b) Behavioral reference for interpolation to broader population

**Verdict: Limited but not zero utility.**

The gaming-income cashout pattern ($10-50, daily/weekly, irregular) represents the SMALLEST transaction size in the Filipino crypto-to-PHP conversion spectrum. This is useful because:

1. **It establishes a floor**: If we observe on-chain transactions at $10-50 on a peso stablecoin, we can flag this as "likely not remittance, likely not freelancer income" -- it is either gaming income, micro-savings, or experimental/campaign activity.

2. **Behavioral ratio**: If national surveys (PSA Survey of Overseas Filipinos, Fintech Alliance PH) provide population-level breakdowns, we can use the observed on-chain ratio of small ($10-50) to medium ($200-1K) to large ($1K+) transactions as a consistency check against the expected population mix.

3. **The ratio is informative for the variance swap**: If the variance in net flows is driven primarily by the $10-50 cohort (high-frequency, high-variance gaming cashouts), the swap payoff structure is different than if variance is driven by the $200-1K cohort (low-frequency, low-variance remittance flows). Knowing the population composition determines the variance decomposition.

However, the interpolation is limited because:
- Gaming income lives on Ronin, not Celo (where PUSO trades)
- The PUSO $10-50 cohort is likely campaign participants, not gamers
- We cannot directly observe Ronin-based gaming cashouts in PUSO data

---

## 8. Implications for the Variance Swap Project

### 8.1 PUSO Is NOT Capturing Gaming Income

The behavioral fingerprints in `PUSO_BEHAVIORAL_FINGERPRINTS.md` superficially resemble gaming income ($10-50 median), but the ecosystem gap (Celo vs. Ronin) and the campaign-driven spike patterns indicate PUSO is capturing Celo community experimentation, not organic income conversion of any type.

### 8.2 PHPC on Ronin IS the Gaming Income Observable

If the project wants to capture gaming income specifically, PHPC on Ronin is the correct instrument to monitor:
- Coins.ph launched PHPC on Ronin specifically to serve Filipino gamers
- The cashout pathway (game token --> PHPC --> GCash) is live
- QRPH integration (2026) would make PHPC directly spendable at merchants
- Ronin has millions of Filipino wallets

**However**: PHPC on Ronin is currently in early stages (launched 2025) and the existing `PUSO_BEHAVIORAL_FINGERPRINTS.md` notes that PHPC had only 87 transfers on Polygon and was "effectively dormant" as of the analysis date. Ronin-specific PHPC data needs separate investigation.

### 8.3 Revised Population Model

For the variance swap's population decomposition (from `PUSO_POPULATION_DECOMPOSITION.md`), gaming income should be added as a sixth category:

```
(F) P2E_GAMER {
    location: Philippines (local)
    income_source: blockchain gaming tokens (PIXEL, SLP, AXS)
    conversion_purpose: supplement daily expenses, mobile load, small purchases
    frequency: daily to weekly (when earning)
    size: $5-50 per cashout
    economic_meaning: volatile supplementary income
    chain: Ronin (not Celo)
    NOTE: Would NOT appear in PUSO data; appears in PHPC/Ronin data
}
```

### 8.4 What This Means for the "Underserved" Narrative

The gaming-income population IS genuinely underserved:
- Lower-income households
- Provincial locations
- Limited access to traditional financial products
- Facing extreme income volatility with no hedging tools

But they are underserved in a way that is DIFFERENT from the OFW remittance narrative:
- OFW families need FX-rate hedging on a predictable monthly flow
- Gamers need token-price hedging on an unpredictable daily flow
- These are fundamentally different products

---

## 9. Recommendations

1. **Do not assume PUSO's $10-50 cohort is gamers.** The ecosystem gap makes this unlikely. Treat PUSO behavioral fingerprints as Celo-community-specific, not gaming-specific.

2. **Monitor PHPC on Ronin for gaming income data.** As adoption grows through the Coins.ph pipeline and QRPH integration, Ronin-based PHPC flows will become the observable for Filipino gaming-income conversion.

3. **For the variance swap, prioritize the freelancer + OFW populations.** These have higher income per transaction, more regular patterns, and are more likely to value hedging. The gaming population's income is too small and too volatile (in the wrong dimension) to be the primary target.

4. **Use the gaming population as a LOWER BOUND benchmark.** If on-chain peso stablecoin transactions show a $10-50 median and no seasonality, that is a signal of gaming/experimental activity rather than the remittance/income-conversion signal the variance swap needs.

5. **The PHPC-Ronin-QRPH pipeline is the most promising development to watch.** If Coins.ph successfully integrates PHPC into QRPH (600K+ merchants), this creates a genuine high-volume peso stablecoin conversion observable that would capture gaming, freelancer, and potentially even OFW populations on a single rail.

---

## Appendix: Key Data Points for Quick Reference

| Metric | Value | Date | Source |
|--------|-------|------|--------|
| PH total gamers | 67.7M | 2024 | Antom/Statista |
| P2E active (Fintech Alliance PH) | 2.8M | 2025 | BusinessDiary.com.ph |
| Pixels DAU | 1M+ | Mar 2026 | Ronin/BitPinas |
| Filipino share of Pixels | ~30% | 2025 | BitPinas |
| PIXEL token price | ~$0.008 | Apr 2026 | CoinMarketCap |
| Metro Manila daily minimum wage | PHP 695 (~$12.50) | 2025-2026 | DOLE |
| Provincial daily minimum (lowest) | PHP 435 (~$7.80) | 2026 | DOLE MIMAROPA |
| Total OFW remittances | $39.62B/year | 2025 | BSP |
| Average OFW annual remittance | PHP 129,000 (~$2,300) | 2024 | PSA |
| PH crypto ownership | 6.1% (~7M) | 2025 | Disruption Banking |
| BSP-licensed VASPs | 13 | 2025 | BSP |
| Coins.ph trading volume | $500M/month | Nov 2025 | FintechNews PH |
| GCash USDC launch | Sep 2025 | 2025 | Bitwage |
| PHPC launched on Ronin | 2025 | 2025 | Coins.ph |
| PUSO median transaction | ~$20 | All-time | Dune #6939960 |
| PUSO modal bucket | $10-50 (50.8%) | All-time | Dune #6939960 |
