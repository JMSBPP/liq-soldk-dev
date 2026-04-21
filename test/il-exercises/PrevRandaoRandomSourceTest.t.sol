// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {Test} from "forge-std/Test.sol";
import {console} from "forge-std/console.sol";
import "@libraries/PrevRandaoRandomSource.sol" as PrevRandaoRandomSourceLib;

contract PrevRandaoRandomSourceHarness{
    function getShock() public returns(uint256){
	return PrevRandaoRandomSourceLib.getShock();
    }
}


contract PrevRandaoRandomSourceTest is Test{
    function setUp() public {
 
    }

    function test__placeHolder() public {}
}



