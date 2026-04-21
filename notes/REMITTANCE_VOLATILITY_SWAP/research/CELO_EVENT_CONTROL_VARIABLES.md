# Celo Ecosystem Event Control Variables for Time-Series Analysis

*Date: 2026-04-02*
*Purpose: Track ALL known scheduled/structural events that must be controlled for when estimating variance from Mento stablecoin flows*

---

## RECURRING EVENTS (must be dummied out in any time-series regression)

### Weekly
| Event | Day | Time (UTC) | Source | Impact |
|---|---|---|---|---|
| ImpactMarket UBI claim windows | Community-dependent (Thursday locked for some) | Varies | Smart contract initialization date | ~$12/claim, creates Thursday spike in cKES/PUSO |
| Celo Developer Office Hours | Thursday | 14:00 UTC (10am ET) | Celo governance repo | May trigger developer test transactions |

### Biweekly (Colombian Quincena — INCOME CYCLE)
| Event | Day | Source | Impact |
|---|---|---|---|
| Colombian salary payment (quincena) | 15th and last day of each month | Colombian Labor Code Art. 134 | Structural spike in USD→COP conversion as workers receive salary and convert. NOT noise — this IS the income signal. Must be controlled with dummy variable in weekly regressions. |
| Prima de servicios (mid-year bonus) | June 30 and December 20 | Colombian Labor Code Art. 306 | Mandated bonus = 1 month extra salary per year, paid in two installments. Creates predictable volume spikes. |

### Biweekly
| Event | Day | Time (UTC) | Source | Impact |
|---|---|---|---|---|
| Celo Governance Calls | Every 2nd Thursday | 14:00 UTC | github.com/celo-org/governance | Governance activity spike, possible parameter changes |

### Monthly
| Event | Cadence | Source | Impact |
|---|---|---|---|
| Proof of Ship distributions | Monthly, $5K in cUSD only | celopg.eco | Small; cUSD only, not local stablecoins |
| MiniPay reward campaigns | Irregular | Opera press releases | User acquisition spikes |

---

## ONE-TIME EVENTS (must be flagged as structural breaks or dummied)

### Protocol Events
| Date | Event | Impact on Stablecoin Data |
|---|---|---|
| 2025-03-26 | Celo L2 migration complete | Contract address continuity but gas parameter changes |
| **2025-07-09** | **Isthmus Hardfork (block 40172442)** | **Cross-currency repricing spike — explains July 2025 anomaly across PUSO, cKES, cGHS, cCOP** |
| 2025-07-02 | Eclair Testnet launch | Minor developer activity |
| 2026-01-25 | Mento token migration (cKES→KESm, cGHS→GHSm, cCOP→COPm, PUSO→PHPm) | **Structural break in token addresses** |

### Colombia-Specific Events
| Date | Event | Impact |
|---|---|---|
| 2024-04-10 | COPM launch (Minteo, 100K users) | New token enters ecosystem |
| 2024-10-09 | cCOP governance proposal posted | Community awareness |
| 2024-10-31 | cCOP deployment on Mento | New Mento stablecoin live |
| **2025-11-19** | **MiniPay + El Dorado integration** | **Colombian fiat on/off-ramp via Bancolombia/Nequi** |
| 2025-08-28 to 2025-12-10 | Celo Peach Round (grants) | Possible Colombian project funding |

### Philippines-Specific Events
| Date | Event | Impact |
|---|---|---|
| 2024-09-09 | PUSO launch on Celo | Token inception |
| 2025-07-30 to 2025-07-31 | PUSO mass onboarding campaign | 1,387 new addresses in 1 day, median $27 |
| 2025-08-13 to 2025-08-14 | PUSO second wave | 800 new addresses |
| 2025-09-XX | GCash adds USDC support | **Regime change — users migrate away from PUSO** |

### Kenya-Specific Events
| Date | Event | Impact |
|---|---|---|
| 2025-07-XX | cKES mass onboarding (same as PUSO) | 1,585 new traders, same campaign |
| 2026-01-25 | cKES→KESm migration | Token symbol change |

---

## HOW TO USE IN ECONOMETRIC SPECIFICATIONS

### For reduced-form regressions:
```
Y_t = α + β X_t + γ₁ D_thursday + γ₂ D_hardfork + γ₃ D_migration + γ₄ D_campaign + ... + u_t
```

### For variance estimation:
- Exclude hardfork window (July 7-12, 2025) from variance calculation
- Exclude campaign days (PUSO: July 30-31, Aug 13-14, 2025) 
- Exclude migration transition (Jan 24-26, 2026)
- Use Thursday dummy to absorb governance/UBI scheduling effect

### For population decomposition:
- Addresses active ONLY on Thursdays → likely UBI/governance
- Addresses active across multiple weekdays → more likely organic
- Addresses appearing during campaign dates only → campaign participants, exclude

---

## TO BE ADDED (as research completes)
- [ ] Exact ImpactMarket community initialization dates for Colombia, Kenya, Philippines
- [ ] MiniPay campaign dates with Colombia/Philippines specifics
- [ ] Minteo/COPM product launch dates and feature updates
- [ ] El Dorado integration milestones post November 2025
- [ ] Celo Colombia DAO event calendar (Medellín meetups, onboarding events)
