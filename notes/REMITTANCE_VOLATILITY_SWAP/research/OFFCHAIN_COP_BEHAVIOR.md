# Off-Chain USD/COP Conversion Behavior in Colombia
## Research for Structural Econometric Model

**Purpose**: Inform structural assumptions about off-chain latent conversion behavior, where on-chain cCOP flows are observable but off-chain decisions are not.

---

## 1. Littio (~220K users, YC-backed)

**Deposit mechanics**: Users top up via PSE bank transfer, Nequi button, Bancolombia Button, debit/credit cards, or blockchain transfer. Nequi is the most frictionless method (instant, no 4x1000 tax). COP is converted to USDC at the point of deposit; Littio mints USDC/EUROC and custodies on Avalanche (migrated from Ethereum, Oct 2024).

**Deposit triggers**:
- Primary driver is structural: hedging COP devaluation (COP -54% vs USD over 10 years, -88% since 1990).
- Secondary driver: freelancer/remote worker salary receipt from US employers (Deel, Payoneer, PayPal bypass).
- Tertiary: yield-seeking via Yield Pots (launched Feb 2024, backed by OpenTrade T-bill vaults, ~$11-13M/month managed).

**Documented stress response**: The Jan/Feb 2025 Trump tariff shock caused COP to fall sharply (COP collapsed for two consecutive sessions per Colombia One). Littio reported 100%+ growth in 48 hours during this period. No other documented spike of comparable magnitude in available sources, but the pattern — sharp COP depreciation event triggers burst inflow — is confirmed as the primary behavioral trigger.

**Deposit size proxy**: Littio held $11-13M/month in OpenTrade vaults as of Oct 2024 across ~220K users, implying a mean managed balance of roughly $50-60 per active depositor, though distribution is almost certainly right-skewed (freelancers hold far more than casual savers).

**Structural implication**: Deposit flow is NOT smooth. It is a mix of slow structural accumulation (payroll receipt) with sharp, event-driven spikes correlated to COP depreciation velocity. The spike response is faster than bank FX desk response — reaction time measured in hours, not days.

---

## 2. Nequi / Wenia (Bancolombia Group)

**Scale**: Nequi has 21M users; Wenia (the crypto layer) launched May 2024 and had ~16,000 users by May 2025. The crypto penetration rate within Nequi is therefore roughly 0.08% — very early adoption.

**What users buy**: USDC is the primary asset via Wenia. Entry is from 1 USD minimum. Bancolombia announced zero-commission USDC buy/sell on Nequi and Bancolombia apps. EURC added March 2025. COPW (COP stablecoin) also available.

**Use case split**: Based on Wenia's stated positioning, primary use is savings/dollarization rather than payments. The global account feature (USD inbound from US bank accounts) suggests a remittance-receipt use case is growing. USDC-to-Nequi QR payment rails (via Zypto/PayAbroad on Stellar) enable merchant payments but adoption is nascent.

**Pricing**: Exchange rate set by Wenia (no additional commission). This means Wenia internalizes the TRM spread; users see a Bancolombia-group FX rate that likely tracks TRM closely with a small markup, making it competitive but not as tight as DEX or P2P.

**Structural implication**: Wenia/Nequi represents the "trust-based" channel — users who will not use P2P or pure crypto. The 16K active users vs 21M Nequi base means this channel's contribution to on-chain USDC flows is currently small but growing. The zero-commission offer is a deliberate market-share grab that may accelerate adoption.

---

## 3. MoneyGram USDC (Colombia, Sept 2025)

**Mechanism**: Recipient-first design — funds sent from the US arrive as USDC in a MoneyGram app wallet (Stellar, Crossmint infrastructure). Recipient can: hold in USD (savings), cash out at retail partner in COP, spend via linked Visa/Mastercard. Sender pays traditional MoneyGram fees; recipient holds stablecoin.

**Flow direction**: Strongly asymmetric — Colombia receives 22x more than it sends in remittances. MoneyGram explicitly chose Colombia on this basis. The dominant flow is therefore USD inbound, with COP cash-out on demand. This is the opposite of Littio (COP in, USDC held).

**Adoption stage**: App launched Sept 2025, first live payments ~Nov 2025. Waitlist-based onboarding. No public user count or transaction volume available as of this writing. Too early for behavioral data.

**Structural implication**: MoneyGram USDC creates a new population of passive USDC holders — remittance recipients who hold stablecoins as a dollar proxy, cashing out to COP based on consumption needs, not hedging decisions. This behavior is distinct from Littio users and will create a different withdrawal pattern (lumpy, needs-driven COP demand rather than appreciation-driven).

---

## 4. El Dorado P2P

**Mechanism**: Order-book P2P marketplace for USDT/USDC vs COP. Buyers and sellers post ads; El Dorado escrows crypto during trade. Payment via Nequi, Daviplata, Bancolombia transfer, or other local rails. 400K+ users across LATAM, 3M+ P2P operations processed.

**Spread structure**:
- Reference price: TRM (official BanRep/SFC daily rate).
- Competitive maker spread: 0.25%–0.75% over TRM depending on payment method and competition.
- Nequi orders command slightly higher margins (less supply, faster settlement, avoids 4x1000 bank tax).
- Traditional bank transfers carry 4x1000 tax (~0.4%), which makes the effective spread wider; Nequi/Daviplata avoid this.
- El Dorado charges 0.25% maker fee.

**Behavioral pattern**: P2P users are price-sensitive and sophisticated — they are actively seeking tighter spreads than CEX or bank FX desks offer. Volume spikes on COP depreciation events as sellers of USDC (who hold dollars) can widen spreads and still attract buyers. This creates a natural spread-widening mechanism during stress.

**Structural implication**: P2P spread over TRM is observable data. During normal conditions it is 0.25-0.75%. During stress events, spread likely widens as USDC demand spikes faster than supply adjusts. This spread is a direct proxy for the latent shadow premium on dollars in Colombia.

---

## 5. TRM vs On-Chain Rate

**TRM**: Official rate published daily by Superintendencia Financiera de Colombia (SFC). It is the volume-weighted average of all formal USD/COP transactions that day. Published end-of-day. It is backward-looking by construction.

**On-chain tracking**: No Colombian cCOP stablecoin has sufficient DEX liquidity to generate a reliable real-time TRM signal. The relevant on-chain comparison is USDT/USDC vs COP on P2P platforms (El Dorado) and CEX (Bitso, Binance Colombia). These converge toward TRM under normal conditions.

**Stablecoin dominance data**: Per Chainalysis/TRM Labs 2025, stablecoin purchases represent over 50% of all crypto exchange purchases in Colombia (Jul 2024 – Jun 2025). Per Bitso data, 4 in 10 retail crypto buys in Colombia are stablecoins. USDC share of stablecoin market rising toward 30% (USDT still dominant).

**Stress behavior**: The systematic dynamics are qualitatively consistent with what is documented in Argentina and Venezuela: during sharp depreciation events, the P2P premium over official rate widens, and on-chain demand spikes before the TRM adjusts. The TRM's backward-looking daily calculation means there is always a latency gap during fast-moving FX events. This gap is the window in which off-chain conversion demand runs ahead of the formal rate.

**Structural implication**: On-chain USDC demand is a leading indicator of TRM direction during stress events, not a lagging one. The spread between P2P rate and TRM is a measurable proxy for conversion pressure.

---

## 6. Channel Substitution Patterns

**Channel menu** (cost/speed/trust ordering):

| Channel | FX Cost | Speed | Trust | Typical User |
|---|---|---|---|---|
| Bank FX desk (Bancolombia, Davivienda) | TRM + 1-3% | T+1 | High | Large amounts, corporates |
| Wenia/Nequi USDC | TRM + small markup, 0 commission | Instant | High | Nequi-native mass market |
| Littio | TRM + Littio margin | Instant | Medium-High | Freelancers, savers |
| CEX (Binance, Bitso) | TRM + 0.5-1.5% | Minutes-Hours | Medium | Crypto-native |
| El Dorado P2P | TRM + 0.25-0.75% | Minutes | Low-Medium | Price-sensitive, sophisticated |
| MoneyGram USDC | TRM + MG fee (sender side) | Instant (receive) | High | Remittance recipients |

**Switching drivers**:
- **Amount size**: Large amounts (>$5,000) go to banks (compliance, limits). Small amounts (<$500) go to Nequi/P2P.
- **Speed**: During COP depreciation spikes, users migrate from bank FX to Littio/P2P because bank desks are slow and can suspend quoting.
- **Cost**: Freelancers migrate from PayPal/Payoneer to Littio because the embedded FX fee on traditional platforms is 2-5% vs Littio's lower margin.
- **Trust**: Mass-market Nequi users will use Wenia rather than P2P because Bancolombia brand trust is high. P2P requires escrow trust in El Dorado.

**Documented mass migration**: The Jan/Feb 2025 tariff crisis is the clearest documented case — Littio's 100% 48-hour growth implies that users who were sitting on COP balances accelerated conversion en masse. No documented case of reverse migration (USDC back to COP) during peso appreciation events, though MoneyGram recipients will exhibit this pattern mechanically.

**Bre-B (BanRep instant payments, Sept 2025)**: Colombia's national instant-payment rail now connects 227 entities. This reduces friction for COP-side settlement on all channels, which should accelerate future P2P and stablecoin off-ramp velocity.

---

## Summary: Structural Assumptions for the Model

1. **Conversion is event-driven, not smooth**: Off-chain COP→USDC flow has a baseline accumulation component (payroll, regular savings) plus sharp event-driven spikes. Spike intensity correlates with the speed and magnitude of COP depreciation, not its level.

2. **Reaction time is hours, not days**: The leading channel (Littio, P2P) reacts within hours of a depreciation event. TRM is backward-looking by one day. This creates a systematic lead-lag structure.

3. **Channel segmentation is stable under normal conditions, unstable under stress**: Users pick their habitual channel. Under stress, they switch to the fastest channel that can handle their transaction size.

4. **P2P spread over TRM is the observable proxy for latent conversion pressure**: Normal spread is 0.25-0.75%. Widening of this spread is a signal that off-chain demand is exceeding supply at the current TRM.

5. **Inbound remittance flow (MoneyGram, traditional) is counter-cyclical to hedging flow**: Remittance recipients cash out to COP when they need pesos; this is a source of COP supply that partially offsets conversion demand. The two populations are largely non-overlapping.

6. **Wenia/Nequi will grow but is currently a small contributor**: 16K Wenia users vs 220K Littio users means Bancolombia channel contributes ~7% of observable fintech USDC holding flow. Growing rapidly but not yet structurally dominant.

---

## Sources

- [Littio x USDC: Circle Case Study](https://www.circle.com/blog/littio-x-usdc-creating-stable-and-secure-banking-in-latam)
- [Littio on Avalanche / OpenTrade Case Study](https://www.opentrade.io/case-studies/littio)
- [Littio Avalanche Migration — CoinDesk](https://www.coindesk.com/business/2024/10/09/latam-bank-littio-ditches-ethereum-for-avalanche-as-demand-for-rwa-vaults-grows)
- [Colombian Peso Collapses After Trump Tariffs — Colombia One](https://colombiaone.com/2025/04/09/colombia-peso-dollar/)
- [Wenia First Year: 16,000 users — Technocio](https://technocio.com/wenia-celebra-su-primer-ano-con-mas-de-16-000-usuarios-conectados-al-mundo-cripto/)
- [Nequi USDC buy/sell via Wenia — Technocio](https://www.technocio.com/nequi-habilita-la-compra-y-venta-de-dolares-digitales-usdc-desde-su-app-a-traves-de-wenia/)
- [Bancolombia zero-commission USDC announcement](https://www.bancolombia.com/acerca-de/sala-prensa/noticias/productos-servicios/usdc-a-cop-sin-comision-wenia)
- [Wenia EURC expansion — Invezz](https://invezz.com/news/2025/03/11/colombias-wenia-platform-expands-crypto-portfolio-with-eurc-stablecoin-integration/)
- [MoneyGram USDC app Colombia launch — Blockworks](https://blockworks.com/news/moneygram-stablecoin-app-colombia)
- [MoneyGram CoinDesk coverage](https://www.coindesk.com/business/2025/09/17/moneygram-makes-stablecoins-the-backbone-of-its-next-generation-app)
- [MoneyGram PR Newswire release](https://www.prnewswire.com/news-releases/moneygram-reinvents-cross-border-finance-with-next-generation-app-302559343.html)
- [El Dorado P2P spread explainer](https://eldorado.io/blog/que-es-el-spread-en-el-dorado-p2p-y-como-te-hace-ganar-dinero/)
- [El Dorado pricing guide](https://eldorado.io/en/blog/setting-competitive-p2p-prices)
- [El Dorado Arbitrum/LATAM adoption — Arbitrum blog](https://blog.arbitrum.io/el-dorados-stablecoin-powered-superapp-is-driving-tether-adoption-on-arbitrum-in-latam/)
- [Top P2P exchanges Colombia — Mural](https://www.muralpay.com/blog/top-p2p-exchanges-for-stablecoins-in-colombia-usdt-usdc-and-dai)
- [State of Stablecoins Colombia Sept 2025 — Bitwage](https://bitwage.com/en-us/blog/state-of-stablecoins-in-colombia---september-2025)
- [LATAM Crypto Adoption 2025 — Chainalysis](https://www.chainalysis.com/blog/latin-america-crypto-adoption-2025/)
- [Bre-B instant payments launch — Colombia channel context](https://cryptoforinnovation.org/crypto-adoption-rises-in-colombia-despite-legislative-hurdles/)
- [Nequi Drives Crypto Adoption — Finacle](https://www.finacle.com/client-stories/case-studies/nequi-drives-crypto-adoption/)
- [Pay with USDC in Colombia using Nequi — Zypto](https://zypto.com/blog/zypto-app/pay-with-usdc-colombia-nequi/)
