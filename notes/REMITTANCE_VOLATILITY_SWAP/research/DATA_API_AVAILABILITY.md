# Philippine Crypto Data Source Availability
## API Access, On-Chain Queryability, and Cost Assessment

Date: 2026-04-02

---

## Source B: USDC Flows to Philippine VASPs

### B.1 Coins.ph

**Public API: YES — authenticated, rate-limited, Binance-compatible structure**

Coins.ph exposes a public REST API at `https://docs.coins.ph/rest-api/` with WebSocket streams and a user-data stream. The API follows a Binance-style design.

- Authentication: API key passed via `X-COINS-APIKEY` header; both key and secret are case-sensitive
- Rate limits: 1200 req/min (IP), 1800 req/min (UID), across `/openapi/*`; HTTP 429 on breach
- Endpoints cover: spot market data (order book, ticker, trades), account balances, withdrawal address whitelist (`/openapi/wallet/v1/withdraw/address-whitelist`), system status
- SDKs available: Python, Java (Dec 2025), JavaScript (Jan 2026)
- A legacy "Coins Access API" (readthedocs, April 2023) exists separately and covers older fiat/on-off-ramp flows

**Key limitation:** The API is designed for trading and account management, not for observing aggregate USDC inflow/outflow volumes. It does not expose institutional flow data.

**On-chain deposit addresses (Ethereum/Polygon): NOT publicly disclosed**

Coins.ph does not publish its custodial hot/cold wallet addresses. No official disclosure found.

**Dune `labels.addresses`: No confirmed labeling found**

No evidence of Coins.ph addresses in Dune's community label tables. Dune's `labels.addresses` covers major CEXs (Binance, Coinbase) but Philippine regional exchanges are not documented as labeled there.

**Chainalysis:** Chainalysis ranks the Philippines 9th in their 2025 Global Crypto Adoption Index and does maintain a VASP Data Flat File product that links on-chain addresses to off-chain VASP metadata (legal names, jurisdiction, licensing). However, this product is enterprise-tier and **not publicly queryable** — pricing is in the $100k–$500k/year range for institutional AML suites. Whether Coins.ph addresses are specifically labeled in that dataset cannot be verified without a paid subscription.

**Arkham Intelligence:** Arkham's ULTRA AI clusters related addresses under named entities. A search for Coins.ph-specific entity labeling on Arkham returned no public confirmation. Arkham's Intel Exchange allows bounty-based address attribution, but no community intelligence on Coins.ph is documented in open sources.

**Nansen:** No public evidence of Philippine VASP tagging in Nansen's smart money or exchange label sets.

**Etherscan labels:** No confirmed Coins.ph label on Etherscan's address tags.

---

### B.2 PDAX

**Public API: NOT FOUND**

No developer documentation, public API portal, or API reference was found for PDAX. Their website (`pdax.ph`) and all public-facing developer resources are silent on API access. PDAX appears to be a retail-only app platform without a public market data or trading API.

**GCash/GCrypto relationship:** Confirmed — PDAX powers GCrypto (GCash's crypto product) via an exclusive partnership. GCash added USDC support in March 2025, with Circle as the direct USDC partner. USDC on GCrypto is available on Ethereum Mainnet (ERC-20), Base, and Solana — not Polygon.

**On-chain deposit addresses: NOT publicly disclosed**

No known on-chain attribution for PDAX custodial wallets.

**Dune / Arkham / Nansen / Etherscan:** No confirmed labeling in any of these platforms.

---

### B.3 GCash / Mynt

**On-chain footprint: INDIRECT only, via PDAX**

GCash does not hold or custody crypto directly. PDAX is the licensed VASP and custodian. GCrypto is a white-label interface over PDAX infrastructure.

USDC on GCash (launched March 2025) uses Circle's infrastructure. Supported networks are ERC-20 (Ethereum mainnet), Base, and Solana. Polygon is not listed as a supported chain for GCash USDC.

**On-chain addresses: UNKNOWN**

The custodial wallets serving GCash USDC are operated by PDAX (or Circle's institutional custody layer) and are not publicly disclosed.

---

### B.4 General Philippine VASP Address Labeling Summary

| Platform | PH VASP Labels | Cost | Notes |
|---|---|---|---|
| Dune `labels.addresses` | None confirmed | Free (if existed) | No PH regional exchange labels documented |
| Etherscan | None confirmed | Free (if existed) | No Coins.ph, PDAX tags found |
| Arkham | Unconfirmed | Free tier / bounty | ULTRA may have partial clustering; not public |
| Chainalysis VASP Flat File | Probable (paid) | $100k–$500k/yr | Institutional only; includes VASP jurisdiction metadata |
| Nansen | None confirmed | Paid | No documented PH exchange coverage |

**Bottom line:** On-chain flow attribution for Philippine VASPs is effectively blocked for free/open-source querying. The only viable path is either (a) Chainalysis enterprise subscription, (b) submitting Arkham bounties, or (c) direct VASP cooperation.

---

## Source C: PHPC (Coins.ph PHP Stablecoin)

### C.1 Contract Addresses

| Network | Contract Address |
|---|---|
| Polygon | `0x87a25dc121Db52369F4a9971F664Ae5e372CF69A` |
| Ronin | `0x63c6e9f027947be84d390cfa7b2332d13b529353` |

Sources: PolygonScan token tracker, Ronin App token page.

### C.2 Dune Queryability (Polygon)

**Partially queryable — raw logs available, no decoded table confirmed**

The Polygon contract is on PolygonScan and emits standard ERC-20 events (Transfer, Approval). Since Dune supports Polygon, raw event logs for this contract are queryable via `polygon.logs` filtered on the contract address. However, no dedicated decoded Dune table (e.g., `coins_ph_polygon.PHPC_evt_Transfer`) was found in Dune's public spellbook or decoded dataset catalog.

Mint and burn events are queryable via:
```sql
SELECT *
FROM polygon.logs
WHERE contract_address = 0x87a25dc121db52369f4a9971f664ae5e372cf69a
  AND topic0 = 0xddf252ad...  -- Transfer event sig
  AND "from" = 0x0000...0000  -- mint: from zero address
```

Historical supply derivation is feasible from cumulative mint minus burn transfers.

### C.3 DEX Pools on Polygon

**No confirmed DEX pool found**

No evidence of PHPC trading on Uniswap v3, QuickSwap, or any other Polygon DEX was found. PHPC appears to be a closed-loop stablecoin used within Coins.ph's app, with no secondary market liquidity on public DEXs as of early 2026. The CoinGecko listing for PHPC does not show any DEX pool or price feed.

This is consistent with PHPC's design: it is redeemable only through the Coins.ph platform, not freely tradable on-chain.

### C.4 Supply Data

**Queryable on-chain; no third-party feed confirmed**

- Polygon total supply: readable directly from contract `totalSupply()` call, or derived from Transfer events
- Ronin supply: 331,234 PHPC total supply with 396 holders and 53,218 transfers as of last available data
- No CoinMarketCap or CoinGecko market cap/supply feed confirmed for PHPC (it is a small-cap, primarily in-app token)
- Historical mint rate is fully reconstructible from on-chain Transfer events on both Polygon and Ronin

---

## BSP Published Data

### Availability: YES — monthly, downloadable tables, no REST API

The BSP publishes Overseas Filipinos' Cash Remittances data at:
- **Primary statistics page:** `https://www.bsp.gov.ph/statistics/external/ofw2.aspx`
- **Direct table example:** `https://www.bsp.gov.ph/statistics/external/Table%2011.pdf` (PDF format)
- **Statistics metadata search:** `https://www.bsp.gov.ph/SitePages/Statistics/StatisticsMetadataList.aspx`

**Granularity:** Monthly, by source country (corridor-level). Covers cash remittances and personal remittances separately. 2025 data publishes with approximately 2-month lag.

**Format:** PDF and Excel tables are available for download. No JSON/REST API endpoint is documented. The BSP does not publish a machine-readable API in the World Bank sense.

**2025 coverage:** Monthly releases confirmed through December 2025. Full-year 2025 total: USD 35.63B cash remittances (record high, +3.3% YoY).

**Limitations:**
- No crypto/stablecoin breakdown
- Corridor data aggregates all channels (banks, remittance companies, informal)
- No sub-monthly granularity
- PDF format requires scraping for time-series construction

**Alternative access:** The Philippine Institute for Development Studies (PIDS) SEIS database (`seis.pids.gov.ph`) mirrors BSP remittance data in a structured table format, potentially easier to scrape.

---

## Other Potential Sources

### Chainalysis

- Has Philippines in its 2025 Global Crypto Adoption Index (ranked 9th globally)
- VASP Data Flat File product includes on-chain address-to-VASP mapping with jurisdiction metadata
- **Cost: enterprise only, not publicly queryable.** Pricing unavailable publicly; estimated $100k–$500k/yr for full platform access
- No public Philippines-specific dashboard

### Arkham Intelligence

- Platform: `intel.arkm.com`
- Has a public API (`intel.arkm.com/api`) with free-tier access for querying entity-tagged addresses
- Intel Exchange allows community bounty submissions for address attribution
- **No confirmed Coins.ph or PDAX entity page found in public sources**
- Viable path: submit a bounty on Arkham Exchange to label PDAX/Coins.ph wallets; cost is in ARKM tokens

### Nansen

- No documented Philippine VASP coverage
- Nansen's "Smart Money" and exchange labels focus on large global CEXs
- Paid platform; no public Philippines-specific content found

### Triple-A Crypto Payments

- Publishes Philippines-specific crypto adoption statistics (ownership rates, demographics)
- Has a public developer API (`developers.triple-a.io`) for payment processing integration
- **The statistics data (ownership %, user counts) is marketing/research content, not an API feed** — it is published as static web pages, not queryable endpoints
- Not a source for USDC flow data

### World Bank Remittance Prices Worldwide

- **Fully accessible, no API key required**
- REST/SDMX API base: `https://api.worldbank.org/v2/`
- DataBank portal: `https://databank.worldbank.org/source/remittance-prices-worldwide-(corridors)`
- Direct data download (Excel): `https://remittanceprices.worldbank.org/data-download`
- Python library: `wbgapi` (PyPI) provides clean programmatic access
- **Coverage:** 365 corridors, 48 sending countries to 105 receiving countries; Philippines corridors from US, UAE, Saudi Arabia, etc.
- **Granularity:** Quarterly, per-corridor, per-operator cost data (total cost as % of send amount)
- **Content:** RSP pricing data collected via mystery shopping; does NOT include volume or flow data
- **Free and open, CC-licensed with attribution**

---

## Summary Assessment

| Source | Accessible? | Cost | Best Access Method |
|---|---|---|---|
| Coins.ph REST API (trading) | Yes | Free | `docs.coins.ph` with API key |
| Coins.ph aggregate USDC flows | No | Blocked | Not exposed publicly |
| PDAX API | No | N/A | No public API exists |
| GCash on-chain addresses | No | Blocked | Custody via PDAX, undisclosed |
| Dune PH VASP labels | No | Free (if existed) | Not present in labels tables |
| Chainalysis PH VASP addresses | Probable (paid) | $100k–$500k/yr | Enterprise contract only |
| Arkham PH VASP entities | Unconfirmed | Free/ARKM bounty | Submit attribution bounty |
| PHPC Polygon contract | Yes | Free | `0x87a25dc121Db52369F4a9971F664Ae5e372CF69A` |
| PHPC Ronin contract | Yes | Free | `0x63c6e9f027947be84d390cfa7b2332d13b529353` |
| PHPC Dune decoded table | No (raw logs only) | Free | Query `polygon.logs` directly |
| PHPC DEX pools | None exist | N/A | Not traded on-chain |
| PHPC supply (on-chain) | Yes | Free | `totalSupply()` + Transfer events |
| BSP remittance data | Yes (PDF/Excel) | Free | `bsp.gov.ph/statistics/external/ofw2.aspx` |
| BSP REST API | No | N/A | Does not exist |
| World Bank RPW (cost data) | Yes | Free | `wbgapi` or DataBank SDMX API |
| World Bank RPW (volume data) | No | N/A | Not in this dataset |
| Triple-A stats API | No | N/A | Static web content only |

---

## Recommended Queryable Stack (Zero Cost)

1. **PHPC on-chain supply and mint flow:** Dune SQL on `polygon.logs` + `ronin.logs` using contract addresses above
2. **BSP monthly aggregate remittances:** Scrape or manually download Excel from `ofw2.aspx`; build time series
3. **World Bank corridor cost (proxy for remittance friction):** `wbgapi` Python library, quarterly, US-PH and UAE-PH corridors
4. **Coins.ph spot market data (PHP/USDC pair):** REST API with API key, for exchange rate and order book depth
5. **PHPC mint rate as remittance proxy:** Reconstruct from Transfer events (zero-address mints) on Polygon

The primary gap is custodial USDC flow data for Coins.ph and PDAX: that signal requires either Chainalysis enterprise access or a breakthrough in community address labeling (Arkham bounty).
