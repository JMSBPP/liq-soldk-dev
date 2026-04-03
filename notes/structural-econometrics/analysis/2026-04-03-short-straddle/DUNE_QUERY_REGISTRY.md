# Dune Query Registry: Bunni V2 Short Straddle Research (Arbitrum)

Created: 2026-04-03
Chain: Arbitrum (chain_id 42161)
BunniHub contract: `0x000000dceb71f3107909b1b748424349bfde5493`

## Decoded Tables Used

Dune has fully decoded Bunni V2 tables on Arbitrum. These queries use decoded event tables
(not raw logs), providing proper ABI-decoded columns with native types.

| Decoded Table | Description |
|---|---|
| `bunni_v2_arbitrum.bunnihub_evt_newbunni` | Pool creation events |
| `bunni_v2_arbitrum.bunnihub_evt_deposit` | Deposit events |
| `bunni_v2_arbitrum.bunnihub_evt_withdraw` | Withdrawal events |

Multichain equivalents also exist under `bunni_v2_multichain.*` with a `chain` column filter.

## Permanent Queries

### Query 1: Bunni V2 Pool Inventory (Arbitrum)
- **Query ID**: 6945876
- **URL**: https://dune.com/queries/6945876
- **Result**: 32 pools found
- **Date range**: 2025-02-01 to 2025-06-13
- **Description**: All Bunni V2 pools deployed on Arbitrum via NewBunni events

### Query 2: Bunni V2 Deposits (Arbitrum)
- **Query ID**: 6945877
- **URL**: https://dune.com/queries/6945877
- **Result**: 100+ deposit events (first 100 returned, more exist)
- **Date range**: 2025-02-01 onwards
- **Description**: All deposit events with decoded amounts (amount0, amount1, shares)

### Query 3: Bunni V2 Withdrawals (Arbitrum)
- **Query ID**: 6945878
- **URL**: https://dune.com/queries/6945878
- **Result**: 100+ withdrawal events (first 100 returned, more exist)
- **Date range**: 2025-02-02 onwards
- **Description**: All withdrawal events with decoded amounts (amount0, amount1, shares)

## Phase 0 Assessment

- **Pools found**: 32 (sufficient for analysis)
- **Active deposits**: Yes, 100+ events
- **Active withdrawals**: Yes, 100+ events
- **Data quality**: Decoded tables with proper uint256 types, no raw log parsing needed
- **Verdict**: Phase 0 CAN proceed. Arbitrum has meaningful Bunni V2 activity.

## Most Active Pool IDs (by deposit count in first 100 rows)

1. `0x52820f86...` - Appears most frequently in deposits (likely a stablecoin pair)
2. `0xc3011ab2...` - Second most active (high amount1 values suggest ETH-denominated)
3. `0x16e2612a...` - Third most active
4. `0xcf3e20a0...` - Fourth most active (WETH/WETH-derivative pair)
