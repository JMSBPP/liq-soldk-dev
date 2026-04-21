
### SIGNAL-> INDEX


```
Phase 1: SIGNAL PROCESSING (information theory)
┌─────────────────────────────────────────────┐
│                                             │
│  Raw Observable     →  Filter  →  Signal    │
│                                             │
│  funding_rate(raw)  →  TWAP    →  funding   │
│                        EMA        signal    │
│                        Kalman               │
│                        outlier              │
│                        removal              │
│                                             │
│  spot_price(raw)    →  TWAP    →  price     │
│                        median     signal    │
│                                             │
│  volume(raw)        →  normalize→ flow      │
│                        deseason   signal    │
│                                             │
│  Theory: Shannon, Wiener, Kalman            │
│  Question: what is the TRUE state?          │
│  Error: noise, distortion, latency          │
└─────────────────────────────────────────────┘
                      │
                      ▼
Phase 2: INDEX CONSTRUCTION (measurement theory)
┌─────────────────────────────────────────────┐
│                                             │
│  Signals     →  Methodology  →  Index       │
│                                             │
│  funding_signal ─┐                          │
│  price_signal   ─┼→  aggregate  →  macro    │
│  flow_signal    ─┘    weight       stress   │
│                       normalize    index    │
│                                             │
│  Theory: Laspeyres, Paasche, Fisher         │
│  Question: what REPRESENTS the concept?     │
│  Error: methodology bias, proxy distance    │
└─────────────────────────────────────────────┘
                      │
                      ▼
Phase 3: SETTLEMENT (contract theory)
┌─────────────────────────────────────────────┐
│                                             │
│  Index  →  payoff function  →  settlement   │
│                                             │
│  macro_stress_index(t)                      │
│    vs. strike_value                         │
│    = cash_payout                            │
│                                             │
│  Theory: derivatives pricing, Shiller       │
│  Question: what do we PAY?                  │
│  Error: basis risk (index ≠ actual income)  │
└─────────────────────────────────────────────┘
```
