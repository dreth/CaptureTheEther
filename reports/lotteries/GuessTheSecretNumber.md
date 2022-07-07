# Guess the secret number

## Objectives

This time I’ve only stored the hash of the number. Good luck reversing a cryptographic hash!

## Solution

It's not easy to reverse a hash, but it's easy to try out the entire possible set of answers ($2^8 - 1$), as the answer `n` is a uint8. We can easily bruteforce this by just hashing all $x$ with $0 \leq x \leq 2^8 - 1$ and comparing the resulting hash with `answerHash`. 

The correct `n` turns out to be 170.

## Submission transaction

https://ropsten.etherscan.io/tx/0x338819d91537aa6dc17be67cf32dbc1e14fd7ef341a3d50239bc9b9de129be31
