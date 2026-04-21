// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.20;

import {FixedPointMathLib} from "solmate/src/utils/FixedPointMathLib.sol";
import {SqrtPriceLibrary} from "@uniswap/v4-utils/libraries/SqrtPriceLibrary.sol";


uint256 internal constant SECONDS_PER_YEAR = 31_536_000;
uint256 internal constant LN_1_0001_WAD = 99_995_000_333_308;
uint256 internal constant LN_PRECISION = 1e14;
uint32 internal constant SECONDS_PER_HOUR= 3600;

function from0x88ToAnnualizedd0x256WADVolatility(uint88 vol0x88) pure returns(uint256) {
    uint256 tickStdDev = FixedPointMathLib.sqrt(uint256(vol0x88) * SECONDS_PER_YEAR);
    return FixedPointMathLib.mulDivDown(tickStdDev, LN_1_0001_WAD, LN_PRECISION);
}

function from0x88ToAnnualized0x256RAYVolatility(uint88 vol0x88) pure returns(uint256){


}
    
