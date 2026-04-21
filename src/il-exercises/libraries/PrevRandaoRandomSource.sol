// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;


// @dev: MUST return 2 OR 1/2
function getShock() returns(uint256){
    return (block.prevrandao % 100) + 1;
}
