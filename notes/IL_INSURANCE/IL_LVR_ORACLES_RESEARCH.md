# IL & LVR Oracles Research

> Solidity oracles and hooks for impermanent loss / loss-versus-rebalancing — scored on composability for building hedging instruments on Panoptic + CFMMs.
>
> **Date**: 2026-03-26

## Scoring

| Dimension | Weight | 5 | 3 | 1 |
|-----------|--------|---|---|---|
| **Composability** | 0.40 | Hook-based, modular interfaces, plug-and-play | Usable but needs adaptation | Monolithic, tightly coupled |
| **IL/LVR Relevance** | 0.30 | Directly computes IL or LVR on-chain | Related metrics (vol, fees, TWAP) | General oracle, tangential |
| **Code Quality** | 0.15 | Tested, audited, production-grade | Functional, limited tests | PoC / hackathon |
| **Activity** | 0.15 | Active development | Maintained but slow | Abandoned |

**Overall = Composability×0.4 + Relevance×0.3 + Quality×0.15 + Activity×0.15**

---

## Tier 1: Direct IL/LVR Oracles & Hooks

### 1.1 Panoptic V2 — OraclePack & RiskEngine
- **Repo**: [code-423n4/2025-12-panoptic](https://github.com/code-423n4/2025-12-panoptic) (audit repo) / [panoptic-labs/panoptic-v2-core](https://github.com/panoptic-labs/panoptic-v2-core)
- **Description**: Panoptic V2 rewrote its oracle engine from scratch — no external dependencies. Uses an 8-slot internal observation queue (`s_oraclePack`), multi-period EMA smoothing, and median-based safety checks. The `RiskEngine` manages internal pricing with volatility safeguards to prevent manipulation. This is the canonical oracle for pricing perpetual options on concentrated LP positions.
- **Architecture**: Library + internal oracle (not a hook — Panoptic is its own protocol layer on top of Uniswap V3/V4)
- **Key contracts**: `contracts/RiskEngine.sol`, `contracts/types/OraclePack.sol`, `contracts/PanopticPool.sol`
- **Scores**: Composability: 3 | Relevance: 5 | Quality: 5 | Activity: 5
- **Overall**: **4.2**
- **Notes**: The oracle is purpose-built for options pricing on LP positions — exactly what you'd compose with for IL/LVR hedging. The `OraclePack` type is a custom packed struct, so integration requires understanding Panoptic's type system. Not a standalone plug-in, but the most production-ready IL-adjacent oracle that exists. The V2 audit (Code4rena Dec 2025) is public.

### 1.2 Najnomics/LVR-Auction-Hook
- **Repo**: [Najnomics/LVR-Auction-Hook](https://github.com/Najnomics/LVR-Auction-Hook)
- **Description**: Uniswap V4 hook that integrates with an EigenLayer AVS to auction the right to be first-in-block for trades. Redistributes MEV/arbitrage proceeds directly to LPs as LVR compensation. Implements the Diamond paper's (McMenamin et al.) auction mechanism on-chain.
- **Architecture**: V4 Hook (`beforeSwap`) + EigenLayer AVS integration
- **Key contracts**: `src/hooks/LVRAuctionHook.sol`
- **Scores**: Composability: 5 | Relevance: 5 | Quality: 2 | Activity: 2
- **Overall**: **3.85**
- **Notes**: The most directly relevant LVR hook. Hook-based = maximally composable with V4 pools. However, code quality is hackathon-level — the EigenLayer AVS integration is a PoC. The architecture (auction LVR → redistribute to LP) is exactly the "other side" of what a hedge instrument would need to price against. Worth studying for the interface design even if the implementation needs work.

### 1.3 Najnomics/EigenLVR
- **Repo**: [Najnomics/EigenLVR](https://github.com/Najnomics/EigenLVR)
- **Description**: Earlier iteration of the LVR auction concept. Uses EigenLayer for decentralized validation of LVR claims. The hook computes per-block LVR and routes compensation.
- **Architecture**: V4 Hook + EigenLayer operator contracts
- **Key contracts**: `contracts/src/EigenLVRHook.sol`
- **Scores**: Composability: 4 | Relevance: 5 | Quality: 2 | Activity: 1
- **Overall**: **3.35**
- **Notes**: Predecessor to LVR-Auction-Hook. Less polished but shows the evolution of the design. The LVR computation logic in the hook is worth reading.

### 1.4 Tehlikeli107/il-protection-hook
- **Repo**: [Tehlikeli107/il-protection-hook](https://github.com/Tehlikeli107/il-protection-hook)
- **Description**: Claims to be the "first-ever Uniswap V4 Hook for Automated Impermanent Loss Protection. Live on Arbitrum." The hook monitors LP positions and automatically triggers protection mechanisms when IL exceeds thresholds.
- **Architecture**: V4 Hook
- **Key contracts**: `contracts/ILProtectionHookV4.sol`
- **Scores**: Composability: 5 | Relevance: 5 | Quality: 2 | Activity: 2
- **Overall**: **3.85**
- **Notes**: Hook-based IL protection directly on V4 — the exact pattern you'd want. Claims Arbitrum deployment (needs verification). The IL threshold + auto-protection pattern is a good template for a hedging instrument trigger. Code quality likely hackathon-grade given the ambitious claims.

### 1.5 artistic709/ImpermanentGain
- **Repo**: [artistic709/ImpermanentGain](https://github.com/artistic709/ImpermanentGain)
- **Description**: "The antiparticle of impermanent loss" — a contract that takes the other side of IL, allowing users to profit from IL that LPs suffer. This is literally an IL hedging instrument in Solidity.
- **Architecture**: Standalone contract (pre-V4, no hooks)
- **Key contracts**: `v1/ImpermanentGain.sol`
- **Scores**: Composability: 2 | Relevance: 5 | Quality: 3 | Activity: 1
- **Overall**: **3.10**
- **Notes**: Conceptually the most important find — someone already built the "long IL" instrument. Pre-V4 and standalone (not modular), but the payoff structure and replication logic are directly what you'd want to port to a hook-based architecture on Panoptic. Study the math in the contract.

### 1.6 LVR Shielded LP (ETHGlobal)
- **Showcase**: [ethglobal.com/showcase/lvr-shielded-lp-fyssi](https://ethglobal.com/showcase/lvr-shielded-lp-fyssi)
- **Description**: V4 Hook + Vault that reacts to market conditions to protect LPs against LVR. Implements freshness guards, hysteresis (lower exit than entry threshold), dwell window with confirmations.
- **Architecture**: V4 Hook + Vault pattern
- **Key contracts**: Check ETHGlobal showcase for repo link
- **Scores**: Composability: 4 | Relevance: 5 | Quality: 2 | Activity: 1
- **Overall**: **3.35**
- **Notes**: The hook+vault pattern is interesting — the vault could hold hedging collateral while the hook monitors LVR. Hysteresis and dwell-window are good UX patterns for avoiding unnecessary rebalancing costs. Hackathon project.

### 1.7 sameshl/uniswap-v4-hooks-exploration
- **Repo**: [sameshl/uniswap-v4-hooks-exploration](https://github.com/sameshl/uniswap-v4-hooks-exploration)
- **Description**: Research repo focused specifically on LP profitability and loss-vs-rebalancing on Uniswap V4. Contains analysis and hook prototypes for LVR measurement.
- **Architecture**: Research + V4 Hook prototypes
- **Scores**: Composability: 3 | Relevance: 5 | Quality: 2 | Activity: 2
- **Overall**: **3.25**
- **Notes**: More research than production code, but directly focused on the LVR problem in V4 hooks context. Good for understanding the design space.

---

## Tier 2: Volatility & Fee Oracles (Feed into IL/LVR Computation)

### 2.1 Valorem Labs — Greeks & Vol Oracles
- **Repo**: [valorem-labs-inc/oracles](https://github.com/valorem-labs-inc/oracles)
- **Description**: On-chain oracles for greeks, realized volatility, implied volatility, risk-free rate, and Black-Scholes pricing using on-chain data. Purpose-built for pricing options and derivatives in on-chain AMMs.
- **Architecture**: Library of standalone oracle contracts
- **Key contracts**: Check `src/` for individual oracle implementations
- **Scores**: Composability: 4 | Relevance: 4 | Quality: 3 | Activity: 2
- **Overall**: **3.55**
- **Notes**: This is a goldmine for the pricing layer. Realized vol oracle + BS pricing on-chain = you can compute LVR = σ²/2 × liquidity directly. The greeks oracles could feed Panoptic's collateral/margin calculations. Last pushed Oct 2022 but the math doesn't change.

### 2.2 scab24/univ4-risk-neutral-hook
- **Repo**: [scab24/univ4-risk-neutral-hook](https://github.com/scab24/univ4-risk-neutral-hook)
- **Description**: V4 hook that computes risk-neutral pricing with a volatility oracle. Uses on-chain vol estimation to adjust pool behavior dynamically.
- **Architecture**: V4 Hook with embedded volatility oracle
- **Key contracts**: `src/Hook/univ4-risk-neutral-hook.sol`
- **Scores**: Composability: 5 | Relevance: 4 | Quality: 2 | Activity: 2
- **Overall**: **3.70**
- **Notes**: Hook-based vol oracle → dynamic fee adjustment is the pattern from the Campbell/Bergault/Milionis optimal fees paper. The risk-neutral pricing in a hook is exactly what you'd need for pricing IL/LVR protection claims on-chain.

### 2.3 Hijanhv/VolatilityFeeHook (VolatilityShieldHook)
- **Repo**: [Hijanhv/VolatilityFeeHook](https://github.com/Hijanhv/VolatilityFeeHook)
- **Description**: V4 hook that adjusts fees dynamically based on realized volatility. The "VolatilityShieldHook" name suggests LP protection via fee scaling during high-vol periods.
- **Architecture**: V4 Hook
- **Key contracts**: `src/VolatilityShieldHook.sol`
- **Scores**: Composability: 5 | Relevance: 3 | Quality: 2 | Activity: 2
- **Overall**: **3.35**
- **Notes**: Dynamic fees based on vol is a partial LVR mitigation strategy (from the Milionis fees paper). The vol computation logic in the hook is reusable for an LVR oracle.

### 2.4 CJ42/ethsingapore-hackathon-2024 — ChainLink Volatility Oracle
- **Repo**: [CJ42/ethsingapore-hackathon-2024](https://github.com/CJ42/ethsingapore-hackathon-2024)
- **Description**: V4 hook that reads realized volatility from Chainlink's volatility data feeds and uses it for dynamic fee adjustment.
- **Architecture**: V4 Hook + Chainlink oracle integration
- **Key contracts**: `src/ChainLinkVolatilityOracle.sol`
- **Scores**: Composability: 4 | Relevance: 3 | Quality: 2 | Activity: 1
- **Overall**: **2.85**
- **Notes**: Shows the Chainlink realized vol feed integration pattern. Chainlink now offers 24h/7d/30d realized vol feeds — useful as an input for LVR computation. Hackathon code but the integration pattern is clean.

### 2.5 Aloe II — BalanceSheet with IV Estimation
- **Repo**: [aloelabs/aloe-ii](https://github.com/aloelabs/aloe-ii)
- **Description**: Money markets plugged into Uniswap V3. The `BalanceSheet` library computes IL-aware liquidation thresholds using on-chain implied volatility estimated from Uniswap V3 oracle data.
- **Architecture**: Protocol with library-based oracle
- **Key contracts**: `core/src/libraries/BalanceSheet.sol`, `core/src/libraries/Volatility.sol`
- **Scores**: Composability: 3 | Relevance: 4 | Quality: 4 | Activity: 3
- **Overall**: **3.45**
- **Notes**: Production-grade IV estimation from Uniswap V3 tick data. The `Volatility.sol` library is one of the few audited on-chain vol estimators. Could be adapted as the vol input for an LVR oracle. More monolithic than hooks but higher quality code.

---

## Tier 3: General Infrastructure (TWAP, Liquidity, Fee Oracles)

### 3.1 OpenZeppelin/uniswap-hooks
- **Repo**: [OpenZeppelin/uniswap-hooks](https://github.com/OpenZeppelin/uniswap-hooks)
- **Description**: Official OpenZeppelin library for secure, modular Uniswap V4 hooks. Includes a Panoptic oracle adapter mock (`OracleHookWithV3AdaptersMock`), suggesting OZ is building composable oracle hooks that bridge V3/V4 oracle data.
- **Architecture**: Library of composable V4 hook building blocks
- **Key contracts**: `src/general/ReHypothecationHook.sol`, `src/mocks/oracles/panoptic/OracleHookWithV3AdaptersMock.sol`
- **Scores**: Composability: 5 | Relevance: 2 | Quality: 5 | Activity: 5
- **Overall**: **3.90**
- **Notes**: The infrastructure layer. Any IL/LVR hook you build should extend OZ's hook base contracts for security. The Panoptic oracle adapter mock is a direct signal that OZ considers Panoptic integration a first-class use case. This is the framework, not the oracle itself.

### 3.2 Uniswap V4 Built-in Oracle (TWAP)
- **Repo**: [Uniswap/v4-core](https://github.com/Uniswap/v4-core)
- **Description**: V4's native oracle provides TWAP via the `Oracle.sol` library. In V4, oracle functionality is implemented as a hook rather than being built into every pool (unlike V3).
- **Architecture**: V4 Hook (official)
- **Key contracts**: See Uniswap v4-periphery oracle hook
- **Scores**: Composability: 5 | Relevance: 2 | Quality: 5 | Activity: 5
- **Overall**: **3.90**
- **Notes**: The base layer. TWAP alone doesn't give you LVR, but LVR = f(σ², liquidity) and σ² can be estimated from TWAP tick deviations (this is what Aloe II does). Any LVR oracle will likely read from V4's TWAP as a primitive.

### 3.3 Uniswap V4 Dynamic Fee Hook (Official Example)
- **Repo**: [uniswapfoundation/v4-doc-drafts](https://github.com/uniswapfoundation/v4-doc-drafts)
- **Description**: Official Uniswap Foundation example of a volatility-based dynamic fee hook. Reference implementation for adjusting LP fees based on market conditions.
- **Architecture**: V4 Hook (reference implementation)
- **Key contracts**: `hook-examples/Volatility-Based Dynamic Fee Hook`
- **Scores**: Composability: 5 | Relevance: 2 | Quality: 4 | Activity: 4
- **Overall**: **3.60**
- **Notes**: The official reference for dynamic fees. Clean starting point for building a vol-aware hook that could be extended to compute LVR.

### 3.4 Chainlink Volatility Data Feeds
- **Description**: Chainlink offers realized volatility feeds (24h, 7d, 30d lookback) for major crypto assets. Not a Solidity repo per se, but a key external oracle input.
- **Architecture**: External oracle (Chainlink data feed)
- **Scores**: Composability: 4 | Relevance: 3 | Quality: 5 | Activity: 5
- **Overall**: **3.90**
- **Notes**: If you want LVR = σ²/2 × L without computing vol on-chain, Chainlink's realized vol feeds are the fastest path. The tradeoff is external dependency vs. Panoptic V2's fully internal oracle. For a hedging instrument, you might use both: Chainlink for fast pricing, internal oracle for settlement.

---

## Tier 4: Monolithic / Low Composability (Still Worth Studying)

### 4.1 elkfinance/faas — StakingRewardsWithILP
- **Repo**: [elkfinance/faas](https://github.com/elkfinance/faas)
- **Description**: Elk Finance's "Farming as a Service" with built-in IL protection. The `StakingRewardsWithILP` contract computes IL for staked LP positions and compensates LPs from a coverage reserve.
- **Architecture**: Monolithic staking contract with embedded IL calculation
- **Key contracts**: `contracts/StakingRewardsWithILP.sol`
- **Scores**: Composability: 1 | Relevance: 5 | Quality: 3 | Activity: 1
- **Overall**: **2.60**
- **Notes**: The IL computation logic is production-tested (Elk was live). The problem is it's welded into a staking contract — not reusable. Study the IL calculation math, ignore the staking wrapper.

### 4.2 WGlynn/vibeswap — ILProtectionVault
- **Repo**: [WGlynn/vibeswap-private](https://github.com/WGlynn/vibeswap-private)
- **Description**: IL Protection Vault that provides insurance-style coverage for LP positions. Separate vault holds coverage funds and pays out based on IL calculations.
- **Architecture**: Vault (standalone, not hook-based)
- **Key contracts**: `contracts/incentives/ILProtectionVault.sol`
- **Scores**: Composability: 2 | Relevance: 4 | Quality: 2 | Activity: 1
- **Overall**: **2.50**
- **Notes**: The vault-based IL insurance pattern is relevant — a hedging instrument needs somewhere to hold collateral. But the implementation is tightly coupled to VibeSwap's specific pool design.

### 4.3 LayintonDev/Confidential-IL-Insurance-for-LPs
- **Repo**: [LayintonDev/Confidential-iImpermanent-Loss-Insurance-for-Lps](https://github.com/LayintonDev/Confidential-iImpermanent-Loss-Insurance-for-Lps)
- **Description**: V4 Hook providing confidential IL insurance using encrypted computations. Novel approach combining FHE/privacy with IL protection.
- **Architecture**: V4 Hook
- **Key contracts**: `contracts/hooks/ConfidentialILHook.sol`
- **Scores**: Composability: 4 | Relevance: 4 | Quality: 1 | Activity: 1
- **Overall**: **2.90**
- **Notes**: Interesting for the privacy angle — if IL insurance claims are public, sophisticated actors can front-run protection purchases. The confidential approach is novel but the implementation is likely very early stage.

### 4.4 yam-finance/synths-sdk — IL Leveraged Reserve
- **Repo**: [yam-finance/synths-sdk](https://github.com/yam-finance/synths-sdk)
- **Description**: YAM's UMA Synths SDK with an IL leveraged reserve contract. Uses UMA's optimistic oracle for IL dispute resolution.
- **Architecture**: UMA synth (standalone, oracle-dependent)
- **Key contracts**: `contracts/ImpermanentLossLeveragedReserveLSPL.sol`
- **Scores**: Composability: 2 | Relevance: 4 | Quality: 3 | Activity: 1
- **Overall**: **2.60**
- **Notes**: Historical interest — one of the earliest attempts at on-chain IL instruments. UMA's optimistic oracle pattern (claim → dispute → resolve) is an alternative to computing IL on-chain. The leveraged reserve concept is useful for understanding capital efficiency tradeoffs in IL protection.

---

## Summary: What to Build With

### For the Oracle Layer (computing IL/LVR on-chain):
1. **Panoptic V2 OraclePack** — most production-ready, options-native
2. **Valorem oracles** — standalone greeks/vol/BS, good for pricing
3. **Aloe II Volatility.sol** — audited on-chain IV estimation from Uniswap ticks
4. **Chainlink vol feeds** — external but highest quality realized vol

### For the Hook Architecture (composable V4 integration):
1. **OpenZeppelin/uniswap-hooks** — base framework, already has Panoptic adapter mock
2. **Najnomics/LVR-Auction-Hook** — best LVR-specific hook design
3. **Tehlikeli107/il-protection-hook** — best IL-specific hook design
4. **scab24/univ4-risk-neutral-hook** — best vol oracle → dynamic pricing hook

### For Instrument Design (payoff structures):
1. **artistic709/ImpermanentGain** — the "long IL" instrument, study the payoff math
2. **LVR Shielded LP** — hook + vault pattern for collateralized protection
3. **Elk Finance ILP** — production IL calculation logic (extract from monolith)

### Composability Stack (bottom → top):
```
V4 TWAP Oracle → Vol Estimation (Aloe/Chainlink/Panoptic) → LVR Computation (σ²/2 × L)
       ↓                                                              ↓
  OZ Hook Framework → IL/LVR Oracle Hook → Protection Claim Pricing → Panoptic Integration
       ↓                                                              ↓
  Dynamic Fee Hook ←←←←←←←←←←← feedback ←←←←←←←←←←←←←←←←←←← Hedge Settlement
```

---

## Missing / Gaps

1. **No production LVR oracle exists as a standalone composable contract.** Everything is either monolithic or hackathon-grade. This is the main build opportunity.
2. **No on-chain fee-implied-vol oracle** (the Bichuch & Feinstein paper). This would be novel — extracting implied vol from AMM fee streams entirely on-chain.
3. **No CI-option replicating portfolio on-chain** (the Fateh Singh paper). LVR = theta of continuous-installment option is proven in theory but not implemented.
4. **Panoptic V2 is the closest to production** but it's a full protocol, not a composable oracle primitive. Extracting its oracle into a standalone hook would unlock the ecosystem.
