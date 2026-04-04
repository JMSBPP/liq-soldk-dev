// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.8.26;

import {PoolId} from "v4-core/src/types/PoolId.sol";

/// @dev Diamond-style storage namespace.
///      `keccak256("il-tracker-v1_0.il-accounting.slot")[0:4]`
bytes32 constant IL_ACCOUNTING_SLOT = bytes32(uint256(0x8a3b6e42));

/// @notice Per-position IL snapshot.
/// @dev entry != 0, exit == 0 → live position
///      entry != 0, exit != 0 → exited, IL frozen
///      entry == 0             → never tracked
struct ILSnapshot {
    uint160 entrySqrtPriceX96;
    uint160 exitSqrtPriceX96;
}

/// @notice Storage layout for IL accounting.
struct ILAccountingStorage {
    mapping(PoolId id => mapping(bytes32 positionKey => ILSnapshot)) snapshots;
}

using ILAccountingLib for ILAccountingStorage global;

/// @notice Handles sstore/sload operations for IL tracking.
library ILAccountingLib {
    function load() internal pure returns (ILAccountingStorage storage s) {
        bytes32 slot = IL_ACCOUNTING_SLOT;
        assembly ("memory-safe") {
            s.slot := slot
        }
    }

    function snapshot(
        ILAccountingStorage storage self,
        PoolId id,
        bytes32 positionKey,
        uint160 entrySqrtPriceX96
    ) internal {
        self.snapshots[id][positionKey].entrySqrtPriceX96 = entrySqrtPriceX96;
    }

    function freeze(
        ILAccountingStorage storage self,
        PoolId id,
        bytes32 positionKey,
        uint160 exitSqrtPriceX96
    ) internal {
        self.snapshots[id][positionKey].exitSqrtPriceX96 = exitSqrtPriceX96;
    }

    function getSnapshot(
        ILAccountingStorage storage self,
        PoolId id,
        bytes32 positionKey
    ) internal view returns (ILSnapshot storage) {
        return self.snapshots[id][positionKey];
    }

    function isLive(
        ILAccountingStorage storage self,
        PoolId id,
        bytes32 positionKey
    ) internal view returns (bool) {
        ILSnapshot storage s = self.snapshots[id][positionKey];
        return s.entrySqrtPriceX96 != 0 && s.exitSqrtPriceX96 == 0;
    }

    function isFrozen(
        ILAccountingStorage storage self,
        PoolId id,
        bytes32 positionKey
    ) internal view returns (bool) {
        ILSnapshot storage s = self.snapshots[id][positionKey];
        return s.entrySqrtPriceX96 != 0 && s.exitSqrtPriceX96 != 0;
    }

    function exists(
        ILAccountingStorage storage self,
        PoolId id,
        bytes32 positionKey
    ) internal view returns (bool) {
        return self.snapshots[id][positionKey].entrySqrtPriceX96 != 0;
    }
}
