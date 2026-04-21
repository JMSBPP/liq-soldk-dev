# PUSO Intermediary Analysis: Why Uniswap Has 99K Trades but Only 242 Takers

*Date: 2026-04-02*
*Dune queries: #6939848 (venue breakdown), #6939852 (top traders), #6939854 (address overlap)*

---

## 1. The Observation

| Venue | Trades (1yr) | Unique Takers | Trades/Taker |
|---|---|---|---|
| Uniswap | 98,990 | 242 | 409 |
| Carbon DeFi | 43,054 | 22 | 1,957 |
| Mento Broker | 17,097 | 2,788 | 6.1 |

Mento has 11x more unique addresses than Uniswap despite 6x fewer trades. Uniswap and Carbon are dominated by a small number of addresses executing many trades each.

---

## 2. Address Overlap Analysis

| Metric | Count |
|---|---|
| Mento unique traders | 2,788 |
| Uniswap unique takers | 242 |
| Uniswap unique tx_from | 558 |
| Carbon unique takers | 22 |
| Overlap: Mento AND Uniswap taker | 35 |
| Overlap: Mento AND Uniswap tx_from | 67 |
| Overlap: Mento AND Carbon | 16 |
| Uniswap takers NOT in Mento | 207 |
| Mento traders NOT in Uniswap | 2,753 |

### Key Finding

**98.7% of Mento traders (2,753 / 2,788) never appear as Uniswap takers.** 
**85.5% of Uniswap takers (207 / 242) never appear as Mento traders.**

These are almost completely disjoint populations. The 35 addresses that overlap are likely aggregator/router contracts that appear on both venues.

The Uniswap `tx_from` count (558) is higher than `taker` count (242), meaning many transactions are initiated by EOAs (558 unique signers) but routed through a smaller set of contract intermediaries (242 taker addresses).

---

## 3. Carbon DeFi: Bot-Dominated

| Rank | Address | Trades | % of All Carbon | Avg Size | Active Days |
|---|---|---|---|---|---|
| 1 | `0x2021...1271` | 31,157 | **72.4%** | $37 | 259 |
| 2 | `0xb961...4a40` | 2,063 | 4.8% | $32 | 14 |
| 3 | `0x7527...730c` | 1,511 | 3.5% | $0* | 8 |
| 4 | `0x019b...542d` | 1,345 | 3.1% | $0* | 30 |
| 5 | `0x8c05...e636` | 1,268 | 2.9% | $14 | 48 |

*$0 avg = amount_usd not priced (token not in price feeds during that period)

**One address accounts for 72.4% of all Carbon DeFi PUSO trades.** This is almost certainly an automated market-making bot executing the Carbon DeFi strategy (Carbon DeFi uses on-chain limit orders / recurring strategies, not a CFMM). The $37 average trade size and 259 active days confirm this is an automated strategy, not human trading.

**Hypothesis: Carbon DeFi is a bot-to-bot venue.** The 22 unique takers are automated strategies managing Carbon DeFi positions. They are NOT end-user remittance activity. Carbon DeFi should be excluded from the remittance signal.

---

## 4. Uniswap: Aggregator-Mediated

The 242 unique takers on Uniswap making 99K trades (409 trades/taker average) suggests:

### Hypothesis A: DEX Aggregator Routing
Retail users interact with a frontend (e.g., Mento app, Valora wallet, a Philippines-focused fintech). The frontend routes through a DEX aggregator contract. The aggregator contract appears as the `taker` on Uniswap. Result: many trades, few taker addresses, but 558 unique `tx_from` (the actual humans signing transactions).

### Hypothesis B: Arbitrage Bots
Professional arbitrageurs monitor Mento oracle price vs. Uniswap pool price. When they diverge, bots trade on Uniswap to capture the spread. These bots would be high-frequency, small number of addresses, large trade counts.

### Hypothesis C: Mento Internal Routing
Mento's own broker contract may route some swaps through Uniswap internally when the internal reserve price is less favorable. The Mento broker would appear as a taker on Uniswap.

### Evidence from the data:

**Address `0x2021...1271` appears on BOTH Carbon (31K trades, 72%) and Mento (895 trades).** This is likely the primary arbitrage/routing bot for the PUSO ecosystem. It:
- Manages Carbon DeFi strategies (automated limit orders)
- Also trades on Mento broker
- Likely arbitrages between venues

**Address `0xb7ec...24f8` on Mento: 1,307 trades, avg $907, 181 active days.** This looks like a large-volume intermediary — possibly a fintech or payment processor handling aggregated user flows. $907 average is above remittance size, suggesting batched transactions.

**Address `0xbe72...2f67` on Mento: 1,642 trades, avg $62, 173 active days.** $62 average is within remittance range. 173 active days suggests a real user or small business, not a bot.

---

## 5. The Layered Market Structure

```
Layer 3: END USERS (2,700+ unique on Mento)
         Filipino diaspora, remittance senders, small businesses
         Interact via: Valora, Mento app, fintech frontends
         Average trade: $60-$370
         ↓ submit tx to

Layer 2: AGGREGATOR/ROUTER CONTRACTS (242 on Uniswap, ~35 overlap)
         DEX aggregators, Mento internal routing, fintech backends
         Route to best execution across venues
         ↓ execute on

Layer 1: LIQUIDITY VENUES
         Uniswap v3 (CFMM) ← primary price discovery
         Carbon DeFi (limit orders) ← bot strategies
         Mento Broker (reserve) ← retail entry + oracle-anchored
         ↓ arbitraged by

Layer 0: ARBITRAGE BOTS (1-3 dominant addresses)
         Keep prices aligned across all three venues
         `0x2021...1271` is the primary arb bot (72% of Carbon, present on Mento)
```

---

## 6. Implications for Remittance Signal

### What this means for measuring net(USDT → PHP) flows:

1. **Mento broker `trader` addresses are the closest to end users.** The 2,788 unique traders with avg 6 trades each look like real humans or small businesses. This is where the remittance signal lives.

2. **Uniswap `taker` addresses are intermediaries, not end users.** The 242 takers are aggregator contracts. Counting them as "traders" would massively undercount the actual user base. Use `tx_from` (558) for a better estimate if analyzing Uniswap.

3. **Carbon DeFi is noise for remittance analysis.** 72% dominated by one bot. Exclude entirely from remittance flow estimation.

4. **The true user count is ~2,788 (Mento) + ~207 (Uniswap-only takers not on Mento) ≈ ~3,000 unique addresses** interacting with PUSO in the last year.

5. **For the REMITTANCE_VOLATILITY_SWAP observable, use Mento broker data as the primary signal source.** Filter: `mento_celo.broker_evt_swap` where tokenIn/tokenOut is PUSO. The `trader` field gives the closest proxy to end-user activity.

6. **Uniswap v3 pool data remains essential for CFMM observables** (price, fees, liquidity, ticks) needed for option construction and settlement. But volume/trade count on Uniswap is not a remittance signal — it's an aggregator/routing signal.

---

## 7. Open Questions

1. **Can we identify the aggregator contracts?** If we know which contracts are routers (e.g., 1inch, Odos, Mento's own router), we can trace through them to find the actual `tx_from` addresses.

2. **Is `0xb7ec...24f8` (avg $907, 1,307 trades on Mento) a fintech payment processor?** If so, its individual trades represent batched user flows and should be decomposed.

3. **Does Mento's own broker route through Uniswap?** If the 35-address overlap includes Mento infrastructure contracts, some Mento broker swaps may be double-counted in Uniswap volume.

4. **Transaction size distribution on Mento vs Uniswap** — do Mento trades cluster in the $10-$2000 remittance range while Uniswap trades show larger batched amounts?

---

## Dune Queries (permanent, verifiable)

| Query | ID | URL |
|---|---|---|
| PUSO venue breakdown | #6939848 | https://dune.com/queries/6939848 |
| PUSO top traders by venue | #6939852 | https://dune.com/queries/6939852 |
| PUSO address overlap analysis | #6939854 | https://dune.com/queries/6939854 |
| EM stablecoin broker swaps | #6939814 | https://dune.com/queries/6939814 |
| EM stablecoin multichain transfers | #6939820 | https://dune.com/queries/6939820 |
