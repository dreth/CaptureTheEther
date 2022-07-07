# Guess the number

## Objectives

I’m thinking of a number. All you have to do is guess it.

## Solution

The solution is in the state variable `answer`, which is 42. All we have to do is call `guess()` passing 42 and with a value of 1 ether. This will return the entire balance of the contract, which is 1 ether on deployment as per the constructor + 1 ether that we send to be able to call `guess()`.

## Submission transaction

https://ropsten.etherscan.io/tx/0x9d8685713a4bbbdc744b5ce040c8c2107e9e5be7e0a672d1621943f08b8460b0
