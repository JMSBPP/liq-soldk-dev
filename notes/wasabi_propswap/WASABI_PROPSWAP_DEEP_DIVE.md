# Wasabi PropSwap Deep Dive

**Date**: 2026-04-08
**Status**: Research complete
**Relevance to project**: Low-to-moderate (see Section 7)

---

## 1. Protocol Overview

### What is Wasabi?

Wasabi is a decentralized leverage trading protocol founded by Eren Derman. It enables
long/short positions on "long tail" assets (memecoins, NFTs, and standard tokens) with up
to 20x leverage. Positions are backed by the actual underlying token, not synthetic
contracts -- when you open a leveraged long on cbBTC, the protocol holds cbBTC as
collateral.

The protocol has three core components:

1. **Prop AMM** -- A proprietary automated market maker where professional operators
   actively quote both sides of the market on-chain (the swap layer).
2. **Margin Engine** -- Facilitates leverage by letting traders borrow from vaults.
3. **Multi-Asset Vaults** -- ERC-4626 tokenized vaults that generate yield from trader
   borrowing demand (single-sided deposits, no impermanent loss for LPs).

### What is PropSwap?

PropSwap is the swap routing layer built on top of the Prop AMM. The `PropSwapRouter`
contract routes token swaps through individual `PropPool` contracts, each of which pairs a
base token with USDC as the universal quote token. The name "PropSwap" appears in the
contract naming convention (`PropSwapRouter`, `PropPoolFactory`).

### How does "sample-based pricing" work?

**Critical finding**: "Sample-based pricing" is NOT a protocol-level mechanism. It is an
**aggregator integration pattern** invented by the VeloraDEX/paraswap-dex-lib PR author
to approximate Wasabi's opaque on-chain pricing without replicating the proprietary
pricing logic locally.

The actual Prop AMM pricing is a **black-box**: professional market makers update quotes
at every block inclusion (~200ms on Base). The on-chain `quoteExactInput()` function
returns the current price, but the formula inside is proprietary and not publicly
verifiable from source (contracts are not verified on Basescan as of research date).

The VeloraDEX integration samples this black-box by:

1. Calling `quoteExactInput()` at 15 exponentially-spaced input amounts (from ~10^(d-7)
   to ~10^(d+7) where d = token decimals)
2. Storing these as `[amountIn, amountOut]` tuples
3. Refreshing every 30 seconds via multicall
4. Interpolating between samples for arbitrary input amounts using piecewise linear
   interpolation
5. Applying a 1% downward buffer (config: `buffer: 9900` out of 10000 basis points) to
   avoid overquoting

This is an engineering pattern to treat any opaque AMM as a sampled function, not a novel
pricing mechanism.

### What problem does it solve vs. traditional AMMs?

The Prop AMM solves the **passive liquidity problem**: traditional AMMs (Uniswap,
Balancer) reprice via arbitrage, meaning LPs systematically lose to informed traders (LVR).
The Prop AMM has active market makers who:

- Update prices every ~200ms (every Base block), not waiting for arbs
- Hedge externally when flow becomes one-sided
- Provide tight spreads competitive with CEX venues
- Maintain deep quoted size near mid-market

### Team, Funding, Chains, Status

| Field | Detail |
|-------|--------|
| **Founder** | Eren Derman |
| **Funding** | $3M seed (closed Feb 2024), led by Electric Capital |
| **Other investors** | Alliance, Memeland, Spencer Ventures, Luca Netz (Pudgy Penguins CEO), Zhouxun Yin (Magic Eden co-founder), Santiago Santos, Cygaar, Zagabond, DCF God, Bob Loukas |
| **Chains** | Ethereum, Base, Blast, Berachain, Solana |
| **TVL** | ~$18M (as of early April 2026, down 9%) |
| **Volume** | $500M+ cumulative since Jan 2024 |
| **Traders** | 18,000+ |
| **LPs** | 66,000+ |
| **Auditors** | Zellic, Sherlock, Narya.ai, Foobar (0xfoobar) |
| **Audit count** | 3 (Options) + 5 (Perps) = 8 total |
| **Security record** | $1B+ in originations, zero security incidents claimed |

---

## 2. Technical Architecture

### PropSwapRouter Contract

The PropSwapRouter is the primary entry point for token exchanges. It:

1. Accepts `swapExactInput` or `swapExactOutput` calls
2. Resolves the routing path (direct for USDC pairs, two-hop via USDC otherwise)
3. Delegates to the appropriate PropPool contract(s)
4. Returns the output amount

**ABI (4 functions)**:

```solidity
function quoteExactInput(address tokenIn, address tokenOut, uint256 amountIn)
    external view returns (uint256 amountOut)

function quoteExactOutput(address tokenIn, address tokenOut, uint256 amountOut)
    external view returns (uint256 amountIn)

function swapExactInput(address tokenIn, address tokenOut, uint256 amountIn,
    uint256 minAmountOut, address recipient, uint256 deadline)
    external returns (uint256 amountOut)

function swapExactOutput(address tokenIn, address tokenOut, uint256 amountOut,
    uint256 maxAmountIn, address recipient, uint256 deadline)
    external returns (uint256 amountIn)
```

### PropPoolFactory Contract

Manages pool discovery and creation:

```solidity
function getListedTokens() external view returns (address[] memory)
function getPropPool(address token) external view returns (address)
```

### PropPool Contract

Each pool is a single base-token/USDC pair:

```solidity
function quoteExactInput(address tokenIn, uint256 amountIn)
    external view returns (uint256 amountOut)

function getReserves()
    external view returns (uint256 baseTokenReserves, uint256 quoteTokenReserves)

function getBaseToken() external view returns (address)
function getQuoteToken() external view returns (address)
```

### Contract Addresses

| Chain | Component | Address |
|-------|-----------|---------|
| Base (8453) | PropSwapRouter | `0xfc81dfde25083a286723b7c9dd7213f8723369fe` |
| Base (8453) | PropPoolFactory | `0x851fc799c9f1443a2c1e6b966605a80f8a1b1bf2` |
| Base Sepolia (84532) | PropSwapRouter | `0x6bd7186801a50c2158c0c9ac5fd8bebd419212fe` |
| Base Sepolia (84532) | PropPoolFactory | `0x877c68779d0fef5458515c98f13355ca3780a486` |

**Perps contracts (separate from PropSwap)**:

| Chain | Long Pool | Short Pool |
|-------|-----------|------------|
| Ethereum | `0x8e0edfd6d15f858adbb41677b82ab64797d5afc0` | `0x0fdc7b5ce282763d5372a44b01db65e14830d8ff` |
| Base | `0xbDaE5dF498A45C5f058E3A09afE9ba4da7b248aa` | `0xA456c77d358C9c89f4DFB294fA2a47470b7dA37c` |
| Blast | `0x046299143A880C4d01a318Bc6C9f2C0A5C1Ed355` | `0x0301079DaBdC9A2c70b856B2C51ACa02bAc10c3a` |
| Berachain | `0x0da575D3edd4E3ee1D904936F94Ec043c06Bb12B` | `0x3EE6C6CdAa0073DE6Da00091329dE4390B0DF1EE` |
| Solana | `spicyTHtbmarmUxwFSHYpA8G4uP2nRNq38RReMpoZ9c` | (same program) |

### Swap Execution Flow (End-to-End)

```
User calls PropSwapRouter.swapExactInput(tokenIn, tokenOut, amountIn, minOut, recipient, deadline)
  |
  v
Router validates: non-zero amount, valid recipient, deadline not expired
  |
  v
Router determines path:
  - If tokenIn or tokenOut is USDC: single-hop via one PropPool
  - If neither is USDC: two-hop (tokenA -> USDC -> tokenB) via two PropPools
  |
  v
For each hop: PropPool executes the swap against its reserves
  (internal pricing logic is proprietary / not publicly verified)
  |
  v
Router validates: amountOut >= minAmountOut (reverts with InsufficientOutput if not)
  |
  v
Tokens transferred to recipient, SwapExactInput event emitted
```

### Events

```solidity
event SwapExactInput(address indexed sender, address indexed recipient,
    address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOut)

event SwapExactOutput(address indexed sender, address indexed recipient,
    address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOut)
```

---

## 3. Pricing Mechanism (CRITICAL)

### The Prop AMM pricing is NOT a deterministic bonding curve

This is the most important finding. Unlike Uniswap (xy=k), Curve (StableSwap invariant),
or Trader Joe (Liquidity Book discrete bins), Wasabi's Prop AMM is a **managed market
maker** where human/algorithmic operators set prices.

**What we know**:

1. Professional operators quote both sides continuously
2. Prices update at every block (~200ms on Base)
3. The `quoteExactInput()` view function returns current pricing
4. When flow becomes one-sided, operators hedge externally and continue quoting
5. Reserves exist on-chain (`getReserves()` returns baseTokenReserves and
   quoteTokenReserves)

**What we do NOT know** (proprietary/unverified):

1. The exact pricing formula inside `quoteExactInput()`
2. Whether there is an oracle feed (likely yes, given the Prop AMM pattern from Solana)
3. How the operator updates pricing parameters
4. Whether pricing is purely on-chain or involves off-chain signed quotes
5. The fee structure embedded in swap pricing

### Comparison to known AMM mechanisms

| Mechanism | Wasabi Prop AMM | Uniswap v3 | Trader Joe LB | Algebra Dynamic |
|-----------|----------------|------------|----------------|-----------------|
| **Pricing** | Active operator quoting | Passive concentrated liquidity | Discrete price bins | Dynamic fee on xy=k |
| **Repricing** | Every block (~200ms) | Via arbitrage | Via arbitrage | Via arbitrage |
| **Formula** | Proprietary / opaque | sqrt-price tick math | Bin-based | Constant product + plugin |
| **LP risk** | Zero (operator bears all) | IL + LVR | IL + LVR | IL + LVR (reduced by fees) |
| **MEV vulnerability** | Low (operator adjusts faster) | High (sandwich, JIT) | Moderate | Moderate |
| **On-chain verifiability** | Low (black box) | Full | Full | Full |

### The "Sample-Based Pricing" Interpolation (VeloraDEX Integration)

As described in Section 1, this is an integration pattern, not a protocol feature. The
algorithm:

```
function interpolate(samples: Sample[], amountIn: bigint): bigint {
  // Binary search for bracket
  // Case 1: Below first sample -> linear scale from origin
  // Case 2: Between samples -> piecewise linear interpolation
  // Case 3: Above last sample -> clamp to last known output (conservative)
}
```

Parameters:
- `SAMPLE_SIZE = 15` (number of price points sampled per direction)
- `SAMPLE_REFRESH_INTERVAL_MS = 30_000` (refresh every 30s)
- `POOL_LIST_REFRESH_INTERVAL_MS = 600_000` (refresh pool list every 10min)
- `DEFAULT_GAS_COST = 200_000`
- `buffer = 9900` (1% discount to avoid overquoting)

### Slippage Behavior

Because the Prop AMM is actively managed:
- Small trades get tight spreads near mid-market
- Large trades may see worse prices (operator manages inventory risk)
- The exact slippage curve is opaque and time-varying
- The VeloraDEX integration conservatively clamps output above the last sampled amount

---

## 4. On-Chain State & Observables

### State Variables per Pool

From the exposed ABI:

| Variable | Type | Access |
|----------|------|--------|
| baseTokenReserves | uint256 | `getReserves()` |
| quoteTokenReserves | uint256 | `getReserves()` |
| baseToken | address | `getBaseToken()` |
| quoteToken | address | `getQuoteToken()` |
| Current quote at any amount | uint256 | `quoteExactInput(tokenIn, amountIn)` |

**Note**: The internal state (operator parameters, oracle feeds, fee accumulators) is NOT
exposed through public view functions in the known ABI.

### Events Emitted

Per swap:
- `SwapExactInput(sender, recipient, tokenIn, tokenOut, amountIn, amountOut)`
- `SwapExactOutput(sender, recipient, tokenIn, tokenOut, amountIn, amountOut)`

Per liquidity change: **Unknown** -- no liquidity addition/removal events are documented.

### Extractable Observables

| Observable | Extractable? | Method |
|------------|-------------|--------|
| Spot price | Yes | `quoteExactInput(token, 1e18)` or from swap events |
| Trade volume | Yes | Sum amountIn/amountOut from swap events |
| Fee revenue | No | Fees are embedded in pricing, not separately reported |
| Reserves | Yes | `getReserves()` |
| Bid-ask spread | Partially | Compare `quoteExactInput` in both directions |
| Price impact curve | Yes | Call `quoteExactInput` at multiple amounts |

### Do samples encode novel microstructure information?

**Partially yes, partially no.**

The VeloraDEX "samples" are snapshots of the operator's current pricing function at 15
points. Tracking these over time could reveal:

1. **Spread dynamics**: How the bid-ask widens/tightens over time
2. **Inventory skew**: Asymmetry between base-to-quote vs. quote-to-base pricing
3. **Price impact convexity**: The shape of the pricing function (linear, concave, convex)
   at different sizes
4. **Operator confidence**: Tighter quotes = higher confidence in hedging ability

However, these are NOT novel in the sense that any exchange's order book reveals similar
information. The novelty is that this data is on-chain and queryable via view functions,
making it composable -- you could build an on-chain volatility estimator by calling
`quoteExactInput` at multiple sizes and measuring the spread.

---

## 5. Pool Inventory

### Known Deployment

Currently deployed only on **Base** for the PropSwap layer. The VeloraDEX E2E tests
confirm WETH/USDC as a live pair. The factory pattern suggests multiple pools exist
(discovered via `getListedTokens()`).

### On-chain query needed

To get the full pool list, you would need to call:
```
PropPoolFactory(0x851fc799...).getListedTokens()
```
Then for each token, call `getPropPool(token)` and `getReserves()`.

**I was unable to execute this on-chain query during research** (sandbox restriction on
`cast` calls). This should be done as a follow-up.

### Likely Pairs

Based on Wasabi's product (memecoins + standard tokens with leverage):
- WETH/USDC (confirmed)
- cbBTC/USDC (mentioned in docs as example)
- Various memecoin/USDC pairs (protocol's core use case)
- Potentially wstETH, AERO, or other Base-native tokens

### Macro-Relevant Pairs

**Unlikely**. Wasabi's focus is long-tail assets and memecoins, not:
- Stablecoin pairs (cUSD/cCOP, DAI/USDC)
- Yield-bearing token pairs (wstETH/WETH)
- Gold tokenization
- EM stablecoins

---

## 6. Integration Surface

### Reading PropSwap State

Any protocol can read pricing by calling view functions on the PropPool contracts:

```solidity
// Get current quote
uint256 amountOut = PropPool.quoteExactInput(tokenIn, amountIn);

// Get reserves
(uint256 baseReserves, uint256 quoteReserves) = PropPool.getReserves();

// Discover pools
address[] memory tokens = PropPoolFactory.getListedTokens();
address pool = PropPoolFactory.getPropPool(tokenAddress);
```

### Can PropSwap be used as a price oracle?

**Technically yes, practically risky.**

Pros:
- `quoteExactInput()` returns real-time pricing updated every block
- Atomic composability (can be read in same transaction)
- No TWAP lag

Cons:
- Pricing is set by a single operator (not decentralized consensus)
- Operator could quote manipulated prices (single point of failure)
- No time-weighted average mechanism built in
- No manipulation-resistance guarantees (unlike Uniswap v3 TWAP)
- Contracts are not verified, so the pricing logic cannot be audited by integrators

**Verdict**: Do NOT use as a price oracle for any security-critical application.

---

## 7. Macro Hedging Relevance

### Assessment: LOW relevance to our project

| Capability | Wasabi PropSwap | Our Need |
|------------|----------------|----------|
| FX depreciation measurement | No -- USDC-denominated only, no EM stablecoin pairs | cCOP/cUSD observables |
| Volatility estimation | Partial -- spread dynamics could inform vol | Need CFMM-based realized vol (fee accumulator or tick path) |
| Capital flow detection | No -- operator-managed, not passive liquidity flows | Need LP deposit/withdrawal patterns |
| Multi-token pool observables | No -- single base/USDC pair per pool | Need USDC/DAI/AMPL multi-numeraire |
| Manipulation resistance | Low -- single operator sets prices | Need decentralized price formation |
| On-chain verifiability | Low -- proprietary pricing | Need transparent, forkable math |

### Comparison to Our Existing Protocols

| Protocol | Relevance | Why |
|----------|-----------|-----|
| **Panoptic V2 / SFPM** | High | Options on CFMM positions, borrow-don't-bootstrap |
| **Algebra Dynamic Fees** | High | Fee accumulator = volatility observable |
| **Balancer Multi-Token** | High | Multi-numeraire measurement instrument |
| **Ekubo MEV-capture** | Medium | MEV auction revenue as observable |
| **Wasabi Prop AMM** | Low | Opaque pricing, no macro-relevant pairs, single operator |

### Is the sample-based mechanism more/less manipulation-resistant?

**Less resistant** than standard CFMMs for oracle purposes:

1. A single operator controls pricing (centralization risk)
2. No atomic arbitrage constraint (operator can quote any price)
3. No on-chain invariant that creates a cost to manipulation
4. CFMMs require capital to move price; Prop AMM requires only operator intent

For swap execution quality, it may be **better** (tighter spreads, less MEV), but that is
a different question from oracle resistance.

---

## 8. Risks

### Protocol Maturity

- **Prop AMM (swap layer)**: Relatively new, deployed on Base only
- **Perps (core product)**: More mature, 8 audits across Options + Perps
- **PropSwap contracts are NOT source-verified on Basescan** (as of research date)
- No known audit specifically covering the PropSwap/PropPool contracts (audits cover
  Options and Perps, not the swap AMM)

### Novel Mechanism Risks

1. **Operator dependency**: If the operator goes offline, pricing stops (though reserves
   remain on-chain). This is unlike passive AMMs which continue functioning indefinitely.
2. **Opaque pricing**: Without verified source code, integrators cannot audit the pricing
   logic for bugs, backdoors, or manipulation vectors.
3. **Centralized quote control**: The operator can theoretically front-run their own users
   or provide adversarial quotes during volatile conditions.
4. **Oracle risk**: If the Prop AMM relies on an external oracle (likely, per the Solana
   Prop AMM pattern), oracle manipulation could cascade to swap pricing.

### TVL/Adoption

- TVL: ~$18M total across all chains (relatively small)
- PropSwap TVL specifically: unknown, likely a fraction of total
- Single chain deployment for PropSwap (Base only)
- VeloraDEX integration PR is still open (not merged), suggesting early integration stage

### Audit Gap

The 8 audits (Zellic, Sherlock, Narya, Foobar) all target Options and Perps contracts.
There is **no publicly documented audit of the PropSwap/PropPool contracts**.

---

## Appendix A: VeloraDEX Integration Source Analysis

### Files in PR #1160 (12 files, +1200 lines)

| File | Purpose |
|------|---------|
| `src/dex/wasabi/wasabi.ts` | Main integration class (~490 lines) |
| `src/dex/wasabi/types.ts` | Type definitions (Sample, PoolState, DexParams, etc.) |
| `src/dex/wasabi/config.ts` | Config (addresses, buffer, sample params) |
| `src/abi/wasabi/WasabiFactory.json` | Factory ABI (2 functions) |
| `src/abi/wasabi/WasabiPool.json` | Pool ABI (4 functions) |
| `src/abi/wasabi/WasabiRouter.json` | Router ABI (4 functions) |
| `src/dex/wasabi/wasabi.test.ts` | Unit tests for interpolation |
| `src/dex/wasabi/wasabi-integration.test.ts` | Integration tests with on-chain verification |
| `src/dex/wasabi/wasabi-e2e.test.ts` | E2E swap tests (WETH<>USDC on Base) |
| `src/dex/wasabi/wasabi-events.test.ts` | Placeholder (polling-based, no events) |
| `src/dex/index.ts` | Registry update |
| `CLAUDE.md` | Dev instructions |

### Key Design Decision: Polling, Not Events

The integration uses `isStatePollingDex = true` -- it does NOT subscribe to on-chain
events. Instead, it polls `quoteExactInput()` via multicall every 30 seconds. This is
because:

1. The Prop AMM updates every block, so event-based tracking would be noisy
2. The pricing is opaque, so events alone don't allow local price computation
3. Multicall sampling gives a complete pricing curve snapshot

### PR Author

`WEBthe3rd` -- opened 2026-03-19, still open as of 2026-04-08.

---

## Appendix B: Prop AMM Pattern (Solana Comparison)

Wasabi's Prop AMM on EVM follows a pattern established on Solana by SolFi, ZeroFi,
Tessera V, HumidiFi, and Obric. Key differences from the Solana pattern:

| Aspect | Solana Prop AMMs | Wasabi (EVM) |
|--------|-----------------|--------------|
| Quote generation | Off-chain, cryptographically signed | On-chain view function |
| Oracle updates | Dedicated CPI calls (~143 CU) | Likely within quoteExactInput |
| Aggregator dependency | Jupiter (99%+ of flow) | 0x, KyberSwap, Base App |
| Execution | Signed quote verified on-chain | Direct smart contract call |
| Composability | Limited (signed quote model) | Full atomic composability |

Wasabi's claim of "fully atomic, on-chain" pricing with "no off-chain dependencies" is a
genuine differentiator vs. Solana Prop AMMs, which typically require off-chain signed
quotes.

---

## Sources

- [Wasabi Official Docs](https://docs.wasabi.xyz/_)
- [PropSwapRouter Integration Guide](https://docs.wasabi.xyz/_/overview/technical-documentation/propswaprouter-integration-guide)
- [VeloraDEX PR #1160](https://github.com/VeloraDEX/paraswap-dex-lib/pull/1160) -- Full source code of sample-based integration
- [Wasabi Fees Documentation](https://docs.wasabi.xyz/perps-lite-paper/fees)
- [Helius: Solana's Proprietary AMM Revolution](https://www.helius.dev/blog/solanas-proprietary-amm-revolution)
- [LimeChain: Making Sense of Prop AMMs on Solana](https://limechain.tech/blog/making-sense-of-prop-amms-on-solana)
- [The Block: Wasabi raises $3M](https://www.theblock.co/post/300465/memecoin-leverage-trading-protocol-wasabi-funding)
- [DeFiLlama: Wasabi TVL](https://defillama.com/protocol/wasabi)
- [ChainBroker: Wasabi Protocol](https://chainbroker.io/projects/wasabi-protocol/)
