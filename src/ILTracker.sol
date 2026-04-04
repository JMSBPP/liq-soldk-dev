// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.8.26;

import {UniConsumer} from "angstrom/contracts/src/modules/UniConsumer.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {Hooks, IHooks} from "v4-core/src/libraries/Hooks.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId} from "v4-core/src/types/PoolId.sol";
import {BalanceDelta} from "v4-core/src/types/BalanceDelta.sol";
import {ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";
import {IPositionManager} from "v4-periphery/src/interfaces/IPositionManager.sol";
import {poolAndPositionKey} from "@typed-v4/libraries/PoolPositionKeyLib.sol";
import {ILAccountingStorage, ILAccountingLib} from "./modules/ILAccounting.sol";

using Hooks for IHooks;
using StateLibrary for IPoolManager;

function hasILTrackerHookFlags(address addr) pure returns (bool) {
    return IHooks(addr).hasPermission(Hooks.AFTER_ADD_LIQUIDITY_FLAG)
        && IHooks(addr).hasPermission(Hooks.AFTER_REMOVE_LIQUIDITY_FLAG);
}

/// @notice afterAddLiquidity + afterRemoveLiquidity hook that snapshots entry prices for IL computation.
/// @dev IL is path-independent: only entry price and current price matter. No afterSwap needed.
///      LVR (path-dependent) is a separate concern for a separate module.
contract ILTracker is UniConsumer {
    IPositionManager internal immutable _POSITION_MANAGER;

    constructor(IPoolManager uniV4, IPositionManager v4PositionManager) UniConsumer(uniV4) {
        _POSITION_MANAGER = v4PositionManager;
    }

    function afterAddLiquidity(
        address sender,
        PoolKey calldata key,
        ModifyLiquidityParams calldata params,
        BalanceDelta,
        BalanceDelta,
        bytes calldata
    ) external returns (bytes4, BalanceDelta) {
        _onlyUniV4();

        (PoolId id, bytes32 positionKey) = poolAndPositionKey(key, sender, params);
        ILAccountingStorage storage accounting = ILAccountingLib.load();

        if (!accounting.exists(id, positionKey)) {
            (uint160 sqrtPriceX96,,,) = UNI_V4.getSlot0(id);
            accounting.snapshot(id, positionKey, sqrtPriceX96);
        }

        return (this.afterAddLiquidity.selector, BalanceDelta.wrap(0));
    }

    function afterRemoveLiquidity(
        address sender,
        PoolKey calldata key,
        ModifyLiquidityParams calldata params,
        BalanceDelta,
        BalanceDelta,
        bytes calldata
    ) external returns (bytes4, BalanceDelta) {
        _onlyUniV4();

        (PoolId id, bytes32 positionKey) = poolAndPositionKey(key, sender, params);
        ILAccountingStorage storage accounting = ILAccountingLib.load();

        if (accounting.isLive(id, positionKey)) {
            uint128 remainingLiquidity = UNI_V4.getPositionLiquidity(id, positionKey);
            if (remainingLiquidity == 0) {
                (uint160 sqrtPriceX96,,,) = UNI_V4.getSlot0(id);
                accounting.freeze(id, positionKey, sqrtPriceX96);
            }
        }

        return (this.afterRemoveLiquidity.selector, BalanceDelta.wrap(0));
    }
}
