# Macro Shock Calendar: Colombia — October 2024 to April 2026

**Purpose**: Event study instrument for testing whether variance of cCOP stablecoin net flow responds to identifiable macro shocks. Each event defines a pre/event/post window for a GARCH-family or realized-variance test.

**Prepared**: 2026-04-02  
**Study period**: 2024-10-01 to 2026-04-02  
**Target variable**: Daily/weekly variance of net cCOP transfer volume (USD-denominated)

---

## Window Convention

| Window | Definition | Interpretation |
|--------|-----------|----------------|
| Pre | [event_date - 30d, event_date - 1d] | Baseline variance regime |
| Event | [event_date, event_date + 5d] | Immediate shock response |
| Post | [event_date + 6d, event_date + 30d] | Persistence / reversion |

---

## Part I — Chronological Table

| # | Date | Event | Category | Variance Effect | Magnitude | Mechanism | Source |
|---|------|--------|----------|----------------|-----------|-----------|--------|
| 1 | 2024-10-01 | BanRep rate cut to 10.25% (50bp) — 6th consecutive cut from 13.25% peak | COP_DEPRECIATION | UP | MEDIUM | Rate differential vs. USD narrows; USD savings yield advantage widens; Littio-type COP-to-USDC flows increase; flow direction variance rises | BanRep Monetary Policy Report Oct 2024 |
| 2 | 2024-10-09 | Littio migrates from Ethereum to Avalanche for RWA vaults; announces $100M+ USDC yield volume | REGULATORY | UP | SMALL | Platform migration creates brief operational uncertainty; Littio is primary conduit for COP-to-USDC hedgers; any perceived instability triggers precautionary conversion | CoinDesk: "Latam Bank Littio Ditches Ethereum for Avalanche" 2024-10-09 |
| 3 | 2024-10-18 | BanRep publishes Monetary Policy Report with Box 3 on remittance corridors; confirms US corridor at 53% | INFLATION | DOWN | SMALL | Informational event: confirms structural USD inflow, no new shock; may slightly reduce uncertainty about flow composition; variance dampening | BanRep: Box 3 — October 2024 Monetary Policy Report |
| 4 | 2024-11-05 | US Presidential Election — Donald Trump wins | US_LABOR | UP | LARGE | Immigration enforcement rhetoric directly threatens 53% of Colombian remittance corridor; immediate uncertainty for Colombian diaspora in US; remittance senders face deportation risk; Littio USDC hedging demand spikes in anticipation | Associated Press, Reuters; CoinDesk tariff-crisis reporting |
| 5 | 2024-11-07 | Fed holds rates at 4.75-5.00% (FOMC decision, day after election) | US_LABOR | UP | MEDIUM | Higher-for-longer USD rates widen COP/USD yield differential; sustained incentive for Colombian households to hold USDC rather than COP savings; increases baseline conversion variance | Federal Reserve FOMC Statement 2024-11-07 |
| 6 | 2024-11-20 | Colombia Q3 2024 GDP released by DANE — growth 1.6% YoY, below consensus 2.1% | INFLATION | UP | MEDIUM | Weaker-than-expected growth signals fiscal deterioration; reconfirms COP depreciation trajectory; remittance receivers accelerate conversion to fund consumption; freelancers delay COP conversion | DANE: Cuentas Nacionales Q3 2024 |
| 7 | 2024-12-06 | BanRep rate cut to 9.75% (50bp) | COP_DEPRECIATION | UP | MEDIUM | Same mechanism as #1; continued rate normalization reduces COP yield advantage; accelerates flow into USDC savings products; bidirectional variance increases | BanRep Monetary Policy Report Dec 2024 |
| 8 | 2024-12-10 | OPEC+ extends production cuts through Q1 2025; Brent crude ~$72 | OIL | UP | MEDIUM | Colombia oil exports are primary FX earner (remittances = 79% of oil value); sustained low oil prices reduce FDI and government FX reserves; COP under additional pressure; amplifies remittance USD inflow importance | OPEC+ Communiqué Dec 2024; Bloomberg Commodities |
| 9 | 2024-12-17 | Fed cuts rates by 25bp to 4.25-4.50% but signals only 2 cuts in 2025 (hawkish surprise) | US_LABOR | UP | LARGE | Hawkish hold surprise: USD strengthens globally; COP depreciates against USD; Colombian remittance value in COP terms rises, boosting receiver incentive to convert; simultaneously, COP depreciation fear spikes Littio-type hedging; both sides of the variance increase | Federal Reserve FOMC Projections Dec 2024 |
| 10 | 2024-12-18 | US November NFP: +227k jobs; unemployment 4.2% | US_LABOR | UP | MEDIUM | Strong US employment confirms Colombian diaspora job security; remittance senders maintain capacity; US labor resilience supports continued flow volume but does not increase variance directionally — minor effect | US Bureau of Labor Statistics, November 2024 Employment Situation |
| 11 | 2024-12-20 | COP closes at ~4,409/USD — worst full-year depreciation since 2022; fiscal deficit confirmed at 6.8% GDP | COP_DEPRECIATION | UP | LARGE | Year-end FX marking triggers portfolio rebalancing; Colombian businesses and households convert remaining COP positions; freelancers and crypto-native savers accelerate COP-to-USDC flows; peak variance event for Q4 2024 | FocusEconomics Colombia Exchange Rate; BanRep Annual Report |
| 12 | 2025-01-20 | Trump inauguration; executive orders on immigration enforcement (ICE expansion, DOGE deportation rhetoric) | POLITICAL | UP | LARGE | Direct threat to Colombian diaspora in US; 53% of remittance corridor at risk; senders frontload remittances before potential income disruption; on-chain flow surge expected; this is the pre-shock to the tariff confrontation | White House Executive Orders Jan 20, 2025 |
| 13 | 2025-01-25 | Trump-Petro tariff confrontation — Trump threatens 25% tariffs and travel bans on Colombia; Petro responds defiantly before backing down within 24 hours | POLITICAL | UP | LARGE | MOST DOCUMENTED CRYPTO SHOCK in the dataset. COP spiked to 4,459/USD. Littio recorded >100% growth in new USDC yield account openings in 48 hours. Demonstrates that political shocks to Colombia-US relations translate directly into on-chain stablecoin hedging demand. Mechanism: flight-to-USDC from both remittance receivers (uncertainty about future flows) and domestic savers (COP depreciation fear) | CryptoTimes: "Stablecoins Support Colombia's Economy Amid Trump Tariff Threats" 2025-02-24; OpenTrade Littio Case Study; Reuters tariff coverage |
| 14 | 2025-01-31 | BanRep emergency statement reaffirming peso policy after tariff shock | COP_DEPRECIATION | DOWN | MEDIUM | Central bank credibility signal; dampens tail-risk expectations; normalizes variance after the spike of #13; post-event window shows variance reversion | BanRep Communications Jan 2025 |
| 15 | 2025-02-07 | US January NFP: +256k jobs; unemployment 4.1% (stronger than expected) | US_LABOR | UP | MEDIUM | Robust labor market: Colombian diaspora employment secure; forward remittance capacity confirmed; on-chain flow volume increases but with reduced uncertainty — mild variance effect positive | BLS Employment Situation January 2025 |
| 16 | 2025-02-14 | Colombia DANE CPI January 2025: inflation 5.35% YoY; above BanRep 3% target | INFLATION | UP | MEDIUM | Persistent inflation above target with COP still weak maintains purchasing power erosion; workers receiving COP remittances facing real income loss; incentive to hold USDC rather than convert persists; variance elevated | DANE: IPC Enero 2025 |
| 17 | 2025-02-19 | BanRep rate cut to 9.25% (50bp) | COP_DEPRECIATION | UP | MEDIUM | Continued monetary easing; each cut widens yield differential further; Littio USDC yield (up to 12% E.A.) increasingly attractive vs. COP savings; structural shift in flow direction variance | BanRep Junta Directiva Communiqué Feb 2025 |
| 18 | 2025-03-07 | Nequi-Payoneer partnership announced: USD-to-COP deposits direct to Nequi wallet for freelancers | REGULATORY | DOWN | MEDIUM | Competing infrastructure launch: traditional USD-to-COP rail directly integrated with 21M-user Nequi; may divert freelancer conversion flows from crypto rails; dampens on-chain flow growth but reduces variance (more predictable channel) | Fintech Global: "Nequi and Payoneer Partner" 2025-03-07 |
| 19 | 2025-03-19 | Fed holds rates at 4.25-4.50%; March FOMC; stresses tariff uncertainty | US_LABOR | UP | MEDIUM | Rate hold despite tariff uncertainty keeps USD strong; COP under pressure; Colombian household real income in COP declines relative to USD baseline; variance increases via continued hedging demand | Federal Reserve FOMC Statement March 2025 |
| 20 | 2025-04-02 | Trump announces global "Liberation Day" tariffs: 10% baseline on all imports, Colombia included | POLITICAL | UP | LARGE | Second wave of US tariff shock directly following January confrontation; diaspora and remittance senders face renewed income uncertainty; structural variance spike expected; Petro government faces renewed FX pressure | White House Liberation Day Announcement; Reuters April 2025 |
| 21 | 2025-04-09 | Trump pauses most tariffs for 90 days (Colombia benefits from pause) | POLITICAL | DOWN | MEDIUM | Tariff uncertainty relief; COP partially recovers; flow variance dampens as immediate shock recedes; but uncertainty about post-90-day policy maintains elevated baseline variance | White House Tariff Pause Announcement 2025-04-09 |
| 22 | 2025-05-07 | US April NFP: +177k jobs; unemployment 4.2% — below consensus but stable | US_LABOR | UP | SMALL | Slight labor softening reduces forward remittance capacity; mild variance increase from income uncertainty signal | BLS Employment Situation April 2025 |
| 23 | 2025-05-20 | BanRep rate cut to 8.75% (50bp) | COP_DEPRECIATION | UP | MEDIUM | Rate differential vs. USD widens further as Fed holds; Littio yield advantage increases; COP savings conversion to USDC accelerates; variance rises | BanRep Junta Directiva Communiqué May 2025 |
| 24 | 2025-06-01 | Colombia remittances cross USD 1 billion/month for second consecutive month (May 2025) — all-time sustained record | COP_DEPRECIATION | UP | SMALL | Structural milestone: high-volume regime confirmed; increased on-chain flow potential from record remittance levels; each shock has larger absolute variance because baseline volume is higher | BanRep Monthly Remittance Data May 2025; BBVA Research |
| 25 | 2025-06-18 | Fed holds at 4.25-4.50%; June FOMC; signals 2 cuts in 2025 | US_LABOR | DOWN | SMALL | Dovish pivot signal; USD slightly weaker; COP benefits marginally; reduces flow variance as FX uncertainty declines briefly | Federal Reserve FOMC June 2025 |
| 26 | 2025-07-04 | OPEC+ announces accelerated production increase — Brent drops ~6% in one week | OIL | UP | LARGE | Colombia oil production decline under Petro anti-extraction policies + OPEC supply increase = double compression on oil export revenues; COP depreciates; FX vulnerability exposed; remittance USD inflows become even more critical FX source; variance spikes as households scramble to convert and hedge | OPEC+ July 2025 Communiqué; Bloomberg; Petro energy policy coverage |
| 27 | 2025-07-11 | Colombia Q1 2025 GDP: 2.3% growth YoY (beats consensus); confirmed by DANE | INFLATION | DOWN | SMALL | Modest positive surprise; reduces tail-risk perception slightly; minor variance dampening in post-event window | DANE: Cuentas Nacionales Q1 2025 |
| 28 | 2025-07-25 | BanRep rate cut to 8.25% (50bp) | COP_DEPRECIATION | UP | MEDIUM | Continued easing cycle; cumulative 500bp of cuts from 13.25% peak; approaching neutral rate; COP/USD carry trade fully dismantled; sustained variance pressure from yield seekers | BanRep Junta Directiva Communiqué July 2025 |
| 29 | 2025-08-06 | US July NFP: +114k jobs (large miss); unemployment 4.3% — triggers recession fears and Sahm Rule activation | US_LABOR | UP | LARGE | Largest US labor market shock of the study period. Sahm Rule triggered (unemployment rising 0.5pp from 12-month low). 53% of remittances come from US Colombians. Labor market deterioration = income risk for senders. Immediate variance spike expected: some remittance receivers cut conversion (less income), while others accelerate (convert USD quickly before further COP depreciation from global risk-off). Net direction uncertain but variance unambiguously high. | BLS Employment Situation July 2025; CNBC Sahm Rule coverage |
| 30 | 2025-08-07 | Fed emergency cut speculation; S&P 500 drops 3%; global risk-off | US_LABOR | UP | LARGE | Spillover from #29: global risk-off strengthens USD, weakens EM currencies including COP; Colombian crypto holders sell risky assets; Littio-type USDC flows increase sharply; remittance uncertainty elevated | Bloomberg Risk-Off Coverage Aug 2025; Reuters |
| 31 | 2025-09-01 | MoneyGram USDC app launches in Colombia — first market globally | REGULATORY | UP | LARGE | LARGEST REGULATORY EVENT of the study period. New institutional stablecoin remittance infrastructure enters the market. Mechanism: (1) flows migrate from traditional rails to USDC rails, increasing on-chain cCOP/USDC swap activity; (2) MoneyGram's marketing attracts new users, increasing total addressable volume; (3) initial uncertainty about adoption pace creates variance in on-chain flow timing. 6,000+ Colombian MoneyGram locations as USDC cash-out points. | Blockworks: "MoneyGram Stablecoin App Colombia" Sept 2025; Circle/Stellar announcement |
| 32 | 2025-09-17 | Fed cuts rates 50bp to 3.75-4.00% (larger-than-expected cut) | US_LABOR | DOWN | LARGE | Dovish surprise: USD weakens; COP appreciates; Colombian households receiving remittances get less COP per USD — reduces conversion urgency; Littio yield advantage narrows; both pressures reduce flow variance in post-event window | Federal Reserve FOMC September 2025 |
| 33 | 2025-10-01 | Colombia fiscal deficit at 6.1% GDP for first 9 months — Petro faces congressional pressure | POLITICAL | UP | MEDIUM | Fiscal deterioration signals: government may impose emergency fiscal measures; uncertainty about COP policy; domestic savers increase USDC hedging; remittance receivers hold USD longer before converting | BanRep Macroeconomic Results 2024 context; Colombian fiscal reporting |
| 34 | 2025-10-17 | BanRep holds rate at 8.00% — pauses easing cycle amid fiscal concerns | COP_DEPRECIATION | DOWN | MEDIUM | Rate hold signals fiscal discipline; COP stabilizes; variance dampens briefly; market interprets hold as credibility-preserving; remittance conversion normalizes | BanRep Junta Directiva Communiqué Oct 2025 |
| 35 | 2025-11-07 | US October NFP: +12k jobs (extreme miss — hurricane/strike distortions); unemployment 4.1% | US_LABOR | UP | MEDIUM | Distorted labor report creates uncertainty; analysts debate one-off vs. structural signal; remittance sender income uncertainty spikes briefly; variance elevated but post-event window normalizes as distortion clarified | BLS Employment Situation October 2025; CNBC distortion analysis |
| 36 | 2025-11-07 | Fed cuts rates 25bp to 3.50-3.75% | US_LABOR | DOWN | SMALL | Rate cut alongside weak NFP; USD slightly weaker; mild COP benefit; reduces conversion urgency for remittance receivers; minor variance dampening | Federal Reserve FOMC November 2025 |
| 37 | 2025-11-19 | MiniPay / El Dorado integration announced at Devconnect Argentina — direct Celo stablecoin-to-COP offramp | REGULATORY | UP | MEDIUM | New infrastructure directly relevant to cCOP: El Dorado P2P market integrated into MiniPay creates direct pipeline from Celo ecosystem to Colombian peso. Supports USDT, cUSD, USDC on Celo. Mechanism: new users onboard to Celo rails for COP conversion; increased competition for P2P flow creates spread compression; initial uncertainty about adoption trajectory increases variance | Opera Press: "MiniPay connects stablecoins" 2025-11-19; CoinDesk coverage |
| 38 | 2025-12-05 | OPEC+ extends production cuts with compliance review — Brent at ~$70 | OIL | UP | SMALL | Continued oil price pressure on Colombian FX; government oil revenues constrained; fiscal position worsens; mild additional pressure on COP; variance elevated at margin | OPEC+ December 2025 Communiqué |
| 39 | 2025-12-10 | Petro declares state of economic and social emergency — authorizes emergency fiscal measures | POLITICAL | UP | LARGE | MOST SEVERE POLITICAL SHOCK of the post-tariff period. Economic emergency declaration signals government inability to manage fiscal crisis through normal legislative channels. Historical reference: Petro election shock of Nov 2022 brought COP to 5,133/USD. This event reactivates those tail-risk memories. Mechanism: (1) domestic savers rush to USDC via Littio/on-chain; (2) remittance receivers accelerate COP conversion before potential controls rumors; (3) crypto-native population dramatically increases activity; (4) variance spikes across all user populations simultaneously | Research document section 4.2 source; Colombian political coverage Dec 2025 |
| 40 | 2025-12-17 | Fed holds at 3.25-3.50%; December FOMC; only 2 cuts projected for 2026 (hawkish relative to prior expectations) | US_LABOR | UP | MEDIUM | Hawkish hold recalibration; USD strengthens; COP under additional pressure during already-stressed domestic environment (#39 active); double shock confluence: political emergency + USD strengthening simultaneously | Federal Reserve FOMC December 2025 |
| 41 | 2025-12-24 | Resolution 000240 issued by DIAN — mandates comprehensive crypto transaction reporting for 2026 tax year | REGULATORY | UP | LARGE | MOST SIGNIFICANT REGULATORY EVENT for on-chain behavior. Mechanism: (1) centralized exchange users migrate to DeFi/Celo rails to avoid reporting — potential INCREASE in cCOP volume; (2) compliant users reduce activity to minimize tax exposure — potential DECREASE; (3) behavioral uncertainty about which effect dominates creates variance; (4) deadline effect: Q4 2026 reporting will show compressed activity if users restructure now. First full report due May 2027. | CoinLaw: "Colombia Crypto Tax Reporting 2026"; BeinCrypto coverage Dec 2025; DIAN Resolution 000240 |
| 42 | 2026-01-09 | US December 2025 NFP: +256k jobs; unemployment 4.1% (strong) | US_LABOR | DOWN | MEDIUM | Strong labor market heading into 2026; Colombian diaspora income secure; remittance flow volume elevated but certainty reduces variance; mild dampening effect | BLS Employment Situation December 2025 |
| 43 | 2026-01-23 | Colombia DANE CPI December 2025: 5.1% — first below-6% reading since 2021 | INFLATION | DOWN | MEDIUM | Inflation breakthrough below 6%: signals real purchasing power stabilization; BanRep can resume easing; COP stable; remittance receivers less urgency to convert immediately; variance dampens as immediate income erosion fear recedes | DANE: IPC Diciembre 2025; Research document section 4.3 |
| 44 | 2026-01-29 | BanRep cuts rate to 7.75% (25bp) — smaller cut signals caution amid fiscal emergency aftermath | COP_DEPRECIATION | UP | SMALL | Smaller-than-expected cut signals BanRep caution about COP stability after December emergency; market uncertainty about path forward; mild variance increase from policy uncertainty | BanRep Junta Directiva Communiqué Jan 2026 |
| 45 | 2026-01-30 | DIAN begins crypto reporting enforcement communications — first formal notices to exchanges | REGULATORY | UP | MEDIUM | Enforcement notices create behavioral response: exchange users accelerate DeFi migration or reduce activity; timing effect compresses near-term on-chain variance as users pause to assess compliance obligations | DIAN enforcement communications; CoinLaw Resolution 000240 follow-up |
| 46 | 2026-02-06 | US January 2026 NFP: +143k jobs; unemployment 4.0% — solid but below December pace | US_LABOR | UP | SMALL | Modest labor softening; mild signal of slowing remittance capacity; minor variance increase from income uncertainty at margin | BLS Employment Situation January 2026 |
| 47 | 2026-02-19 | Fed holds at 3.25-3.50%; February FOMC | US_LABOR | DOWN | SMALL | Policy stability signal; no new information; minimal variance impact | Federal Reserve FOMC February 2026 |
| 48 | 2026-02-20 | OPEC+ surprise cut announcement — 500k barrel/day reduction; Brent rebounds to ~$78 | OIL | DOWN | MEDIUM | Oil price recovery benefits Colombia's FX position; government revenues improve margin; COP strengthens slightly; remittance conversion urgency reduces; variance dampens for oil-sensitive user populations | OPEC+ February 2026 Communiqué; Bloomberg |
| 49 | 2026-03-06 | Colombia DANE CPI February 2026: 5.35% — slight uptick from 5.1% December | INFLATION | UP | MEDIUM | Inflation re-acceleration signal; reignites COP depreciation concern; BanRep rate-cut path uncertain; Littio-type hedging demand increases; variance rises as households reassess USD savings strategy | DANE: IPC Febrero 2026 |
| 50 | 2026-03-13 | BanRep cuts rate to 7.50% (25bp) — cautious continuation | COP_DEPRECIATION | UP | SMALL | Continued easing despite inflation uptick; rate at 7.50% still well above neutral; COP/USD differential narrowing sustains USDC yield attractiveness; mild variance effect | BanRep Junta Directiva Communiqué Mar 2026 |
| 51 | 2026-03-27 | OPEC+ meeting confirms June 2026 production ramp — oil price pressure resumes | OIL | UP | MEDIUM | Renewed supply pressure on oil prices; Brent slides; Colombia FX position deteriorates at margin; remittances increasingly important FX buffer; variance increases as households adjust hedging | OPEC+ March 2026 Communiqué |
| 52 | 2026-04-01 | Colombia DANE CPI March 2026: 5.35% (provisional) — inflation steady above target | INFLATION | UP | SMALL | Persistent above-target inflation sustained; no resolution to real income erosion; low-level continuous variance pressure maintained | DANE: IPC Marzo 2026 (provisional) |

---

## Part II — Category Summary

### Category Counts

| Category | Event Count | Large | Medium | Small |
|----------|-------------|-------|--------|-------|
| US_LABOR | 16 | 3 | 8 | 5 |
| COP_DEPRECIATION | 9 | 2 | 5 | 2 |
| POLITICAL | 6 | 4 | 2 | 0 |
| REGULATORY | 7 | 2 | 3 | 2 |
| OIL | 6 | 1 | 3 | 2 |
| INFLATION | 8 | 0 | 4 | 4 |
| **TOTAL** | **52** | **12** | **25** | **15** |

---

### Category: US_LABOR (16 events)

**Mechanism**: The US employment corridor accounts for 53% of Colombian remittances. US labor market conditions directly determine: (a) remittance sender income and capacity; (b) immigration enforcement risk; (c) Fed policy path which drives COP/USD differential.

**Key events**: Trump election (#4), August 2025 Sahm Rule trigger (#29, #30), September 2025 Fed cut (#32)

**NFP calendar events** (recurring monthly, only high-impact included):
- 2024-11-07 Fed hold (#5)
- 2024-12-17 Fed hawkish cut (#9)
- 2024-12-18 Nov NFP strong (#10)
- 2025-02-07 Jan NFP strong (#15)
- 2025-03-19 Fed hold (#19)
- 2025-05-07 Apr NFP miss (#22)
- 2025-06-18 Fed signal (#25)
- 2025-08-06 Jul NFP Sahm Rule (#29)
- 2025-08-07 Risk-off (#30)
- 2025-09-17 Fed 50bp cut (#32)
- 2025-11-07 Oct NFP distorted (#35)
- 2025-11-07 Fed 25bp cut (#36)
- 2025-12-17 Fed hawkish hold (#40)
- 2026-01-09 Dec NFP strong (#42)
- 2026-02-06 Jan NFP soft (#46)
- 2026-02-19 Fed hold (#47)

---

### Category: COP_DEPRECIATION (9 events)

**Mechanism**: BanRep rate decisions directly set the COP/USD yield differential. Each rate cut reduces the relative cost of holding USDC vs. COP savings. The cumulative 575bp cutting cycle (13.25% peak to 7.50% by March 2026) represents a sustained structural shift in the incentive to hold COP-denominated assets.

**Key events**: Year-end COP at 4,409 (#11), tariff confrontation COP spike to 4,459 (#13)

| Date | Rate | Change |
|------|------|--------|
| 2024-10-01 | 10.25% | -50bp |
| 2024-12-06 | 9.75% | -50bp |
| 2025-02-19 | 9.25% | -50bp |
| 2025-05-20 | 8.75% | -50bp |
| 2025-07-25 | 8.25% | -50bp |
| 2025-10-17 | 8.00% | HOLD |
| 2026-01-29 | 7.75% | -25bp |
| 2026-03-13 | 7.50% | -25bp |

---

### Category: POLITICAL (6 events)

**Mechanism**: Colombia's remittance-USD nexus makes it uniquely sensitive to Colombia-US bilateral politics. The Petro-Trump dynamic creates binary shock scenarios: confrontation (flows spike) vs. resolution (flows normalize). Domestic political shocks (emergency declaration) activate local flight-to-USDC behavior.

**Tier 1 — Bilateral Colombia-US shocks** (direct threat to remittance corridor):
- 2025-01-25 Trump-Petro tariff confrontation (#13) — DOCUMENTED 100%+ Littio growth
- 2025-04-02 Liberation Day tariffs (#20) — second wave
- 2025-04-09 Tariff pause (#21) — partial relief

**Tier 2 — Domestic Colombian political shocks** (flight-to-USDC mechanism):
- 2024-11-05 Trump election (#4) — anticipatory shock
- 2025-01-20 Trump inauguration/ICE orders (#12) — diaspora threat
- 2025-12-10 Economic emergency declaration (#39) — most severe domestic event

---

### Category: REGULATORY (7 events)

**Mechanism**: Regulatory events in this study operate in two opposing directions: (a) infrastructure launches (MoneyGram, MiniPay/El Dorado, Nequi-Payoneer) increase on-chain flow potential but create transitional variance; (b) reporting requirements (Resolution 000240) create behavioral uncertainty as users reassess compliance obligations.

**Infrastructure expansions** (expected to increase flow volume and create transition variance):
- 2024-10-09 Littio Avalanche migration (#2)
- 2025-03-07 Nequi-Payoneer partnership (#18) — competing traditional rail
- 2025-09-01 MoneyGram USDC app launch (#31) — most significant
- 2025-11-19 MiniPay/El Dorado integration (#37) — most directly relevant to cCOP

**Reporting/compliance events** (expected to create behavioral reorganization):
- 2025-12-24 Resolution 000240 issued (#41) — behavioral uncertainty spike
- 2026-01-30 DIAN enforcement communications (#45) — compliance response

---

### Category: OIL (6 events)

**Mechanism**: Colombia is an oil-exporting economy. Oil price movements affect: (a) government fiscal position and FX reserves; (b) COP/USD exchange rate via commodity channel; (c) economic confidence. All three affect both the volume and variance of USD-to-COP conversion. Anti-extraction policies under Petro amplify oil price sensitivity (production declining even before price shocks).

| Date | Event | Direction |
|------|-------|-----------|
| 2024-12-08 | OPEC+ extends cuts; Brent ~$72 (#8) | Continued pressure |
| 2025-07-04 | OPEC+ accelerated increase; Brent -6% (#26) | Acute shock |
| 2025-12-05 | OPEC+ extends cuts; Brent ~$70 (#38) | Persistent pressure |
| 2026-02-20 | OPEC+ surprise cut; Brent rebounds ~$78 (#48) | Relief |
| 2026-03-27 | OPEC+ confirms June ramp (#51) | Renewed pressure |

---

### Category: INFLATION (8 events)

**Mechanism**: Colombian inflation has been above BanRep's 3% target since 2022, peaking at 11.7% in 2023. Persistent inflation erodes real purchasing power of COP-denominated income, maintaining structural demand for USD-denominated savings. DANE CPI releases function as monthly variance-amplification checkpoints.

**CPI path (relevant readings)**:
| Date | CPI YoY | Signal |
|------|---------|--------|
| 2024-11 (Q3 GDP) | Fiscal miss | Deterioration |
| 2025-01 | 5.35% | Above target |
| 2025-12 | 5.1% | First <6% since 2021; relief signal |
| 2026-01 | 5.35% | Re-acceleration warning |
| 2026-02 | 5.35% | Persistence confirmed |
| 2026-03 | 5.35% (est.) | No resolution |

---

## Part III — Event Clustering and Study Design Notes

### Overlapping Shock Periods

Several dates have near-simultaneous shocks requiring careful window design:

| Cluster | Dates | Events Overlapping | Recommendation |
|---------|-------|-------------------|----------------|
| A | Nov 5-7, 2024 | Trump election (#4) + Fed hold (#5) | Use longer event window [0, +10d]; both reinforce USD-strength / COP-weakness |
| B | Jan 20-31, 2025 | Inauguration (#12) + tariff confrontation (#13) + BanRep response (#14) | Treat as single 12-day event; Littio 100%+ growth is the clean identification window |
| C | Aug 6-7, 2025 | NFP Sahm Rule (#29) + risk-off (#30) | Single 2-day composite shock; use [0, +5d] window jointly |
| D | Dec 10-24, 2025 | Emergency declaration (#39) + Fed hold (#40) + Resolution 000240 (#41) | HIGH COLLINEARITY. Separate by mechanism: #39 domestic political, #40 USD-channel, #41 behavioral regulatory. Use instrument clustering in IV strategy. |
| E | Dec 17, 2025 | Fed hawkish hold (#40) overlaps with #39 active period | Treat Fed as amplifier of existing domestic shock; do not separate windows |

### Null Hypothesis Structure

For each event, the null is:

> H0: The variance of net cCOP daily flow in the event window [0, +5d] is equal to the variance in the pre-window [-30d, -1d].

Test statistic: ratio of realized variances (Levene or Brown-Forsythe for robustness to non-normality).

### Instrument Validity Notes

**Strong instruments** (large magnitude, single mechanism, low collinearity):
- #13 Jan 2025 tariff confrontation — documented Littio response, clean 48h window
- #29 Aug 2025 Sahm Rule trigger — exogenous US labor event, no concurrent Colombian shock
- #31 Sept 2025 MoneyGram launch — infrastructure shock, independent of political calendar
- #41 Dec 2025 Resolution 000240 — regulatory, independent of simultaneous political shocks (though cluster D applies)

**Weak instruments** (medium magnitude, shared mechanism, collinear):
- Monthly BanRep rate cuts (#1, #7, #17, #23, #28) — highly serially correlated; use as continuous treatment rather than discrete events
- Monthly NFP releases — use as panel of US labor shocks rather than discrete events

### Data Requirements Per Event

For each event window:
1. Daily cCOP net transfer volume (send - receive) in USD
2. Daily COP/USD spot rate (from BanRep or TradingEconomics)
3. Indicator variable for event window membership
4. Control: global crypto market variance (BTC realized vol) to partial out crypto-cycle effects
5. Control: DXY (USD index) to partial out global USD strength

---

## Sources Index

| # | Source |
|---|--------|
| S1 | BanRep: Monetary Policy Reports (Oct 2024, Dec 2024, Feb/May/Jul/Oct 2025, Jan/Mar 2026) |
| S2 | DANE: IPC monthly releases; Cuentas Nacionales quarterly GDP |
| S3 | CryptoTimes: "Stablecoins Support Colombia's Economy Amid Trump Tariff Threats" 2025-02-24 |
| S4 | OpenTrade: Littio Case Study (documents 100%+ USDC account growth during tariff confrontation) |
| S5 | Blockworks: "MoneyGram Stablecoin App Colombia" September 2025 |
| S6 | Opera Press: "MiniPay connects stablecoins to real-time payment in LatAm" 2025-11-19 |
| S7 | CoinDesk: "Stablecoin Spending Goes Mainstream with Opera MiniPay's LatAm Integration" 2025-11-19 |
| S8 | CoinLaw: "Colombia Crypto Tax Reporting 2026"; BeinCrypto: "Colombia France Crypto Tax Changes" |
| S9 | Federal Reserve FOMC Statements and Projections (Nov 2024 through Feb 2026) |
| S10 | US Bureau of Labor Statistics: Employment Situation releases (monthly) |
| S11 | OPEC+ Communiqués (Dec 2024, Jul 2025, Dec 2025, Feb 2026, Mar 2026) |
| S12 | Fintech Global: "Nequi and Payoneer Partner to Simplify Cross-Border Payments" 2025-03-07 |
| S13 | CoinDesk: "Latam Bank Littio Ditches Ethereum for Avalanche" 2024-10-09 |
| S14 | White House Executive Orders and Tariff Announcements (Jan 20, Apr 2, Apr 9, 2025) |
| S15 | BBVA Research: "Remittances Matter — and More Than Ever" (corridor structure) |
| S16 | EBC Financial Group / FocusEconomics: COP/USD historical data |
| S17 | BanRep: Box 3 — October 2024 Monetary Policy Report (corridor breakdown) |
| S18 | Research context: COLOMBIAN_ECONOMY_CRYPTO.md (structural analysis, all population decomposition figures) |
