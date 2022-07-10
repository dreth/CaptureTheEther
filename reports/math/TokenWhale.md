# Token whale

## Objectives

> This ERC20-compatible token is hard to acquire. There’s a fixed supply of 1,000 tokens, all of which are yours to start with.
> Find a way to accumulate at least 1,000,000 tokens to solve this challenge.

## Solution

The `transferFrom()` function in this contract is using the same `_transfer()` internal function as `transfer()`, however, `transferFrom()` should be deducting tokens from the address whose tokens are being moved out, so the address we pass as `from` in `transferFrom()`, however, it instead deducts it from `msg.sender`.

Because of this bug and the fact that the contract is using Solidity 0.4.21, this opens the contract up for an integer overflow bug. All we have to do to exploit it is to:

1. Call `approve()` from address 1 to approve address 2 to move tokens out of address 1

2. Call `transferFrom()` from address 2 and make sure that the receiving address is either address 1 or another address that is not address 2

3. Call `transfer()` from address 2 to send at least 1M tokens to address 1

4. Call `isComplete()` to check


## Submission transaction

https://ropsten.etherscan.io/tx/0x038d72cb3b179c25582068f2d8a2ac3d701eabcf997ce918a424525ccf21bef5
