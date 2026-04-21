# Data Dictionary: cCOP Residual Daily Flow + BanRep TRM

*Date: 2026-04-02*
*Spec: INCOME_SETTLEMENT/2026-04-02-ccop-cop-usd-flow-response.md*

---

## On-Chain Variables (Dune Query #6941901)

**QA FIX (L1)**: All filters are applied to the SENDER side only (`"from"` address). A transfer is included if the SENDER is in the clean address set, regardless of receiver. This means: if a clean sender sends to a bot address, the transfer is included. If a bot sends to a clean address, the transfer is excluded.

**QA FIX (L2)**: Raw TRM data was fetched via:
```bash
curl -o trm_daily.json "https://www.datos.gov.co/resource/mcec-87by.json?\$where=vigenciadesde>='2024-10-01'&\$order=vigenciadesde&\$limit=50000"
```

### Identifiers

| Variable | Type | Definition | Units | Source |
|---|---|---|---|---|
| `day` | DATE | Calendar date of observation | YYYY-MM-DD | CAST(block_time AS DATE) |

### Volume Measures

| Variable | Type | Definition | Units | Cleaning |
|---|---|---|---|---|
| `gross_volume_usd` | DOUBLE | Total USD value of all cCOP/COPm residual transfers on this day | USD | SUM(amount_usd) after all 5 filters applied |
| `income_volume_usd` | DOUBLE | USD value of transfers in $200-$2,000 range | USD | SUM WHERE amount_usd BETWEEN 200 AND 2000 |
| `small_volume_usd` | DOUBLE | USD value of transfers in $1-$50 range | USD | SUM WHERE amount_usd BETWEEN 1 AND 50 |
| `whale_volume_usd` | DOUBLE | USD value of transfers above $2,000 | USD | SUM WHERE amount_usd > 2000 |

**Volume interpretation**:
- `income_volume_usd` = proxy for income conversion (remittances, freelancer payouts)
- `small_volume_usd` = proxy for spending/outflow or UBI residual
- `whale_volume_usd` = large transfers (treasury operations, arbitrage, liquidity provision)
- `gross_volume_usd` = income + small + mid-range ($50-200) + whale

### Count Measures

| Variable | Type | Definition | Units | Cleaning |
|---|---|---|---|---|
| `total_transfers` | INT | Count of all transfers on this day | count | COUNT(*) after filters |
| `income_count` | INT | Count of transfers in $200-$2,000 range | count | COUNT WHERE amount_usd BETWEEN 200 AND 2000 |
| `unique_senders` | INT | Distinct sender addresses on this day | count | COUNT(DISTINCT "from") |

### Calendar Dummies

| Variable | Type | Definition | Values | Source |
|---|---|---|---|---|
| `day_of_week` | INT | ISO day of week | 1=Mon, 2=Tue, ..., 7=Sun | day_of_week(day) in DuneSQL |
| `is_quincena` | INT | Colombian salary payment day | 1 if DAY=15 or DAY=last day of month, else 0 | Colombian Labor Code Art. 134 |
| `is_thursday` | INT | Thursday dummy | 1 if day_of_week=4, else 0 | Celo governance/UBI residual |
| `is_weekend` | INT | Weekend dummy | 1 if day_of_week IN (6,7), else 0 | Activity level control |

---

## Off-Chain Variables (BanRep TRM — datos.gov.co)

### Raw Fields (trm_daily.json)

| Field | Type | Definition | Units | Source |
|---|---|---|---|---|
| `vigenciadesde` | DATETIME | Effective date (start) of TRM rate | ISO 8601 | BanRep via datos.gov.co |
| `vigenciahasta` | DATETIME | Effective date (end) — spans weekends/holidays | ISO 8601 | BanRep via datos.gov.co |
| `valor` | STRING | TRM rate (COP per 1 USD) | COP/USD | BanRep interbank weighted average |
| `unidad` | STRING | Always "COP" | - | - |

### Processed Fields (trm_processed.csv)

| Variable | Type | Definition | Units | Cleaning |
|---|---|---|---|---|
| `date` | DATE | Calendar date | YYYY-MM-DD | Expanded from vigenciadesde/vigenciahasta |
| `trm` | FLOAT | TRM rate: COP per 1 USD | COP/USD | Forward-filled for weekends/holidays |
| `delta_trm` | FLOAT | TRM_t - TRM_{t-1} (daily change) | COP | Null for first observation |
| `delta_trm_lag1` | FLOAT | TRM_{t-1} - TRM_{t-2} (lagged daily change) | COP | Null for first two observations |
| `is_weekend` | INT | Saturday or Sunday | 0/1 | Python weekday() >= 5 |
| `is_forward_filled` | INT | TRM was carried forward from prior business day | 0/1 | 1 if date not in original vigenciadesde set |

### TRM Notes

- BanRep TRM is the "Tasa Representativa del Mercado" — the official COP/USD rate
- It reflects the PREVIOUS trading day's weighted average interbank rate
- Published daily for business days only; weekends/holidays carry forward
- Fully exogenous to Celo: cCOP market is ~0.001% of interbank volume
- Higher TRM = weaker COP (more COP needed per USD)
- Positive ΔTRM = COP depreciation; negative ΔTRM = COP appreciation

---

## Filter Definitions

### 1. Thursday-Only (UBI)
- **Rule**: >80% of sender's transactions fall on Thursdays AND sender has >= 3 total txns
- **Rationale**: ImpactMarket UBI claims are concentrated on Thursdays
- **Impact**: 588 addresses removed (11.8% of total)

### 2. Bot
- **Rule**: >1,000 total transactions AND <10 unique counterparties
- **Rationale**: High-frequency + low counterparty diversity = automated routing
- **Impact**: 26 addresses removed (0.5% of total)

### 3. Campaign Spike
- **Rule**: Sender first appeared on a day with >50 new senders
- **Rationale**: Mass onboarding events produce addresses that transact once or briefly
- **Impact**: 3,563 addresses removed (71.4% of total)
- **Campaign days**: 2025-02-19, 2025-05-23, 2025-07-30, 2025-07-31, 2025-08-13, 2025-08-14

### 4. Dust
- **Rule**: amount_usd < $1
- **Rationale**: Sub-dollar transfers are test transactions or rounding artifacts

### 5. Hardfork Window
- **Rule**: block_date BETWEEN 2025-07-07 AND 2025-07-12
- **Rationale**: Isthmus Hardfork caused cross-currency repricing artifacts

---

## Merged Dataset Variables

The Analytics Reporter should join on `date = day` and add:

| Variable | Definition | Transformation |
|---|---|---|
| `ln_gross_volume` | ln(gross_volume_usd) | Primary LHS variable. Handle zeros with ln(1 + V) |
| `ln_income_volume` | ln(income_volume_usd) | Robustness R3 LHS. Handle zeros with ln(1 + V) |
| `delta_trm` | TRM_t - TRM_{t-1} | Primary RHS variable (same-day FX change) |
| `delta_trm_lag1` | TRM_{t-1} - TRM_{t-2} | Lagged RHS variable |

---

## Data Provenance

| Dataset | Source | API | Auth Required | Last Fetched |
|---|---|---|---|---|
| On-chain flow | Dune Analytics | MCP (createDuneQuery/executeQueryById) | API key | 2026-04-02 |
| BanRep TRM | datos.gov.co | Socrata REST API | None | 2026-04-02 |
| Table: stablecoins_multichain.transfers | Dune Spellbook | - | - | Updated continuously |
