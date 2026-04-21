// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.20;


import {TickRange, lowerTick, upperTick} from "@typed-v4/types/TickRangeV2Mod.sol";
import {Trigonometry} from "@trigonometry/Trigonometry.sol";
import {IVolatilityOracle} from "@cryptoalgebra/integral-base-plugin/contracts/interfaces/plugins/IVolatilityOracle.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {FixedPointMathLib} from "solady/src/utils/FixedPointMathLib.sol";

uint256 constant SECONDS_PER_YEAR = 31_536_000;
uint256 constant LN_1_0001_WAD = 99_995_000_333_308;
uint256 constant LN_PRECISION = 1e14;
uint256 constant WAD_PRECISION = 1e18;
uint32 constant SECONDS_PER_HOUR= 3600;


function fromLPingTickRangePositionToExpiration(
						IVolatilityOracle volatilityOracle,
						uint32 secondsAgo,
						TickRange tickRange
) view returns (uint32){
    (,uint88 vol0x88) = volatilityOracle.getSingleTimepoint(secondsAgo);
    uint256 vol0x256 = from0x88ToAnnualizedd0x256WADVolatility(vol0x88);
    uint160 quot2PiVolWAD0x96 = uint160(FixedPointMathLib.sqrt(
								FixedPointMathLib.mulDiv(
									Trigonometry.TWO_PI,
									WAD_PRECISION,
									vol0x256
								)
    ));

    uint256 quotSqrtPriceRange = FixedPointMathLib.mulDiv(
						 uint256(TickMath.getSqrtPriceAtTick(
										     upperTick(tickRange)
						 )),
						 uint256(1 << 96),
						 uint256(TickMath.getSqrtPriceAtTick(
										     lowerTick(tickRange)
						 ))
    );

    uint256 quot = FixedPointMathLib.mulDiv(
			     WAD_PRECISION,
			     quotSqrtPriceRange - (1 << 96),
			     quotSqrtPriceRange + (1 << 96)
    );

    // todo:
    return 0;


}

// @dev; takes deltaExpiration := expirationOption - expirationCLAMM position
function fromExpirationToLPingTickRange(
					IVolatilityOracle volatilityOracle,
					uint32 deltaExpiration
) view returns (TickRange){
    // todo:
    return TickRange.wrap(bytes6(0));
}

function from0x88ToAnnualizedd0x256WADVolatility(uint88 vol0x88) pure returns (uint256) {
    // todo: convert Algebra's tracking-error accumulator to annualized WAD vol
    return uint256(vol0x88);
}
