/* // SPDX-License-Identifier: UNLICENSED */
/* pragma solidity >=0.8.20; */


// harness


// test
/* Example 3.15. Assume that the yearly ETH/DAI volatility is */
/* σ = 100% and that we should create a Uniswap v3 position to */
/* mimic a covered call that expires t = 10 days before expiration */
/* and k = 3300. We start by finding rt : The daily volatility is */
/* σ = √100 */
/* = 5.23%, so that rt = 1.303. That means, one should */
/* 365 */
/* deploy a Uniswap V3 position within the range [2533, 4299]. */

// [From](~/learning/cfmm-theory/lp-derivatives/kristensen-perpetual_options_uniswap_v3-2024.pdf::PG81)
 
