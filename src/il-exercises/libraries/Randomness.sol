// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

struct RandomShocksHistory {
    uint32 lastBlockNumber;
    mapping(uint32 blockNumber => uint256 shockMagnitude) blockShocks;
}
    
//keccak256("random-shocks-history.storage")
bytes32 constant RANDOM_SHOCKS_HISTORY = 0xf598bd22be33c6d0f077abfb4237e7f1fdf2371eee836ca150b24cb4c72665f7;
bytes4 constant PREVRANDAO_GET_SHOCK_SELECTOR = 0xd7627a38;

function getRandomShockHistoryStorage() pure returns(RandomShocksHistory storage $){
    bytes32 pos = RANDOM_SHOCKS_HISTORY;
    assembly{
       $.slot := pos
    }
}
    
function writeShock(address randomSource) {
    RandomShocksHistory storage $ = getRandomShockHistoryStorage();
	
    if (block.number > $.lastBlockNumber) {
	(bool ok, bytes memory res) = randomSource.call(
							abi.encodeWithSelector(
									       PREVRANDAO_GET_SHOCK_SELECTOR));
	// todo: MUST check it returns 2 or 1/2
	uint256 shock = abi.decode(res, (uint256));
	$.blockShocks[uint32(block.number)] = shock;
	
    }
}

function getShock() view returns(uint256){
    RandomShocksHistory storage $ = getRandomShockHistoryStorage();
    return $.blockShocks[uint32(block.number)];
}
