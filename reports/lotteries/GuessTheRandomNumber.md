# Guess the random number

## Objectives

This time the number is generated based on a couple fairly random sources.

## Solution

We can deduct the number from the keccak256 hash of the block hash and the time in which the contract is deployed. 

Alternatively, we can just pull the number from the state variable `answer` in the storage slot `0x`.

I did the latter as follows:

```python
answer = int(web3.eth.get_storage_at(guess_the_random_number.address, '0x').hex(), 16)
```

## Submission transaction

https://ropsten.etherscan.io/tx/0xdd49b0fffad32c5de917f4a6436ca975e7c33358fa009407c86ef7954f9a0d98
