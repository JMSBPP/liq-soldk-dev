// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.8.26;

import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolId} from "v4-core/src/types/PoolId.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";
import {LeftRightSigned} from "@types/LeftRight.sol";
import {Math as PanopticMath} from "@libraries/Math.sol";
import {TickRange} from "@typed-v4/types/TickRangeV2Mod.sol";
import {fromTickRangeToSqrtPriceX96Range} from "@typed-v4/libraries/TickRangeSqrtPriceX96Lib.sol";
import {ILAccountingStorage, ILAccountingLib, ILSnapshot} from "../modules/ILAccounting.sol";
import {rightIlXLiq, leftIlXLiq} from "../libraries/LeftRightILX96.sol";

using StateLibrary for IPoolManager;

/// @notice Read-only periphery: computes LeftRight IL for any tracked position.
/// @dev Reads entry/exit prices from ILAccounting storage, current price from PoolManager.
///      Returns Panoptic-typed LeftRightSigned for direct composition with Panoptic risk engine.
contract ILView {
    IPoolManager internal immutable UNI_V4;

    constructor(IPoolManager uniV4) {
        UNI_V4 = uniV4;
    }

    /// @notice Compute current IL for a tracked position.
    /// @param id Pool identifier
    /// @param positionKey keccak256(owner, tickLower, tickUpper, salt)
    /// @param tickRange Packed (tickLower, tickUpper) from typed-uniswap-v4
    /// @return il LeftRightSigned — right slot = token0 IL (call-side), left slot = token1 IL (put-side)
    function computeIL(
        PoolId id,
        bytes32 positionKey,
        TickRange tickRange
    ) external view returns (LeftRightSigned il) {
        ILAccountingStorage storage accounting = ILAccountingLib.load();
        ILSnapshot storage snap = accounting.getSnapshot(id, positionKey);

        uint160 entrySqrtPriceX96 = snap.entrySqrtPriceX96;
        if (entrySqrtPriceX96 == 0) return LeftRightSigned.wrap(0);

        // If frozen (exited), use exit price. If live, use current pool price.
        uint160 refSqrtPriceX96;
        if (snap.exitSqrtPriceX96 != 0) {
            refSqrtPriceX96 = snap.exitSqrtPriceX96;
        } else {
            (refSqrtPriceX96,,,) = UNI_V4.getSlot0(id);
        }

        (uint160 sqrtPriceLowX96, uint160 sqrtPriceUpX96) = fromTickRangeToSqrtPriceX96Range(tickRange);

        // IL = IL(currentOrExit) - IL(entry)
        int256 rightIL = rightIlXLiq(refSqrtPriceX96, sqrtPriceLowX96, sqrtPriceUpX96)
            - rightIlXLiq(entrySqrtPriceX96, sqrtPriceLowX96, sqrtPriceUpX96);

        int256 leftIL = leftIlXLiq(refSqrtPriceX96, sqrtPriceLowX96, sqrtPriceUpX96)
            - leftIlXLiq(entrySqrtPriceX96, sqrtPriceLowX96, sqrtPriceUpX96);

        il = LeftRightSigned.wrap(0)
            .addToRightSlot(PanopticMath.toInt128(rightIL))
            .addToLeftSlot(PanopticMath.toInt128(leftIL));
    }
}
