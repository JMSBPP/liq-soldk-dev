# Uniswap V4 USDC/DAI Pool Hook Research

*Date: 2026-04-01*
*Pool Manager: 0x67366782805870060151383f4bbff9dab53e5cd6 (Polygon)*

---

## Key Findings

### 1. The Address Is the PoolManager Singleton, Not a Pool

The address `0x67366782805870060151383f4bbff9dab53e5cd6` is the **Uniswap V4 PoolManager singleton** on Polygon — confirmed by [PolygonScan](https://polygonscan.com/address/0x67366782805870060151383f4bbff9dab53e5cd6). It is the single entry point for ALL V4 pools on Polygon. In V4's singleton architecture, individual pools do not have their own contract addresses. They exist as entries in the PoolManager's internal `mapping(PoolId => Pool.State)`, identified by a `bytes32` PoolId (keccak256 of the PoolKey struct).

### 2. The $56.8M Volume Is Almost Certainly V3, Not V4

The only USDC/DAI pool on Uniswap V4 Polygon found via [GeckoTerminal](https://www.geckoterminal.com/polygon_pos/pools/0x250c8f3e57eee96da7377491fe103ef05e6e70e2fb0d65d80747f4ec8ff939e2) was created ~2 days ago (~2026-03-30), has ~$7,800 liquidity, a non-standard 0.009% fee, and only ~$20K/day volume. At that rate, 30-day volume would be ~$600K, not $56.8M.

The established USDC/DAI pools on Polygon are on **Uniswap V3**:
- `0x5645dcb64c059aa11212707fbf4e7f984440a8cf` — 0.01% fee, ~$181K TVL, 3+ years old
- `0x5f69C2ec01c22843f8273838d570243fd1963014` — 0.05% fee

The $56.8M volume against the PoolManager address in dex.trades is most likely a Dune data mapping issue where `project_contract_address` for V4 trades points to the singleton.

### 3. V4 USDC/DAI Pool Hook Status Cannot Be Determined Without On-Chain Event Data

The V4 pool's 0.009% fee is non-standard (V3 only had 0.01%, 0.05%, 0.3%, 1%). V4 allows arbitrary fee tiers without hooks, so 0.009% could be:
- A static non-standard fee on a vanilla pool (hooks = address(0))
- A dynamic fee at capture time (fee = 0x800000 in PoolKey, with hook attached)

To determine definitively: decode the `Initialize` event emitted by the PoolManager when this pool was created. The event contains the `hooks` address and `fee` fields from the PoolKey. See [BowTiedDevil on V4 Pool Data](https://www.degencode.com/p/uniswap-v4-part-v-pool-data).

### 4. V4 Dynamic Fees vs Algebra Dynamic Fees Are Fundamentally Different

| Dimension | Algebra | V4 Dynamic Fee Hook |
|-----------|---------|---------------------|
| Fee function | Known double-sigmoid of volatilityCumulative | Arbitrary — defined by hook developer |
| Identifiability | Can write phi_t = g(sigma_{t-1}, ...) for known g | Cannot write closed-form without hook source code |
| Sufficient statistic | volatilityCumulative fully determines fee | Depends on hook inputs |
| Scope | All Algebra pools use same mechanism | Each V4 pool can have different hook |

V4 provides no opinionated fee calculation ([docs](https://docs.uniswap.org/contracts/v4/concepts/dynamic-fees)). Comparing Algebra (known deterministic mechanism) against a V4 dynamic fee hook requires knowing the hook's source code.

### 5. Hook Permissions Are Address-Encoded

V4 hook permissions are encoded in the **least significant 14 bits** of the hook contract's deployed address ([Hooks.sol](https://github.com/Uniswap/v4-core/blob/main/src/libraries/Hooks.sol)). The dynamic fee flag is `DYNAMIC_FEE_FLAG = 0x800000` in the fee field of the PoolKey ([LPFeeLibrary](https://docs.uniswap.org/contracts/v4/reference/core/libraries/LPFeeLibrary)).

---

## Verification Query

Run this Dune query to resolve the volume attribution:

```sql
SELECT
    project,
    version,
    project_contract_address,
    SUM(amount_usd) as volume_30d,
    COUNT(*) as trade_count
FROM dex.trades
WHERE blockchain = 'polygon'
    AND (
        (token_bought_address = 0x3c499c542cef5e3811e1192ce70d8cc03d5c3359
         AND token_sold_address = 0x8f3cf7ad23cd3cadbd9735aff958023239c6a063)
        OR
        (token_sold_address = 0x3c499c542cef5e3811e1192ce70d8cc03d5c3359
         AND token_bought_address = 0x8f3cf7ad23cd3cadbd9735aff958023239c6a063)
    )
    AND block_time >= NOW() - INTERVAL '30' DAY
    AND project = 'uniswap'
GROUP BY 1, 2, 3
ORDER BY volume_30d DESC
```

This separates V3 and V4 volume definitively.

---

## Implications for the Structural Econometrics Comparison

1. **If the $56.8M is V3 (most likely)**: The Algebra vs Uniswap V3 comparison is viable with $54.5M vs $56.8M — well-matched volume. But the routing spillover finding (100% of Uni V3 USDC/DAI volume is Algebra spillover) still applies and needs to be verified for this higher-volume pool.

2. **If a V4 pool with dynamic fees exists**: Comparing two different dynamic fee mechanisms (Algebra sigmoid vs V4 hook) is a different question than dynamic vs static. Would need the hook source code to specify the model.

3. **If V4 is vanilla (no hooks)**: Same as comparing Algebra vs V3 — dynamic vs static fee on same architecture generation.

---

## Sources
- PolygonScan: https://polygonscan.com/address/0x67366782805870060151383f4bbff9dab53e5cd6
- GeckoTerminal V4 pool: https://www.geckoterminal.com/polygon_pos/pools/0x250c8f3e57eee96da7377491fe103ef05e6e70e2fb0d65d80747f4ec8ff939e2
- Uniswap V4 dynamic fees docs: https://docs.uniswap.org/contracts/v4/concepts/dynamic-fees
- V4 Hooks.sol: https://github.com/Uniswap/v4-core/blob/main/src/libraries/Hooks.sol
- BowTiedDevil V4 Pool Data: https://www.degencode.com/p/uniswap-v4-part-v-pool-data
