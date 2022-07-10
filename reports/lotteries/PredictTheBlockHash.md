# Predict the block hash

## Objectives

> Guessing an 8-bit number is apparently too easy. This time, you need to predict the entire 256-bit block hash for a future block.

## Solution

In both the Solidity compiler version 0.4.21 (for `block.blockhash()`) and ^0.8.0 (for `blockhash()`), the function to obtain the block hash from a block number only returns the hash for the 256 most recent blocks. 

As a result, to pass the challenge we must:

1. Call `lockInGuess()` with the `hash` value `0x0000000000000000000000000000000000000000000000000000000000000000`
2. Wait for this previous transaction to have about 256 block confirmations 
3. Call the `settle()` function, which should now _always_ return `0x0000000000000000000000000000000000000000000000000000000000000000` for `answer`, given that `settlementBlockNumber` will be 256+ blocks in the past.

## Submission transaction

