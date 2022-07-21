# Assume ownership

## Objectives

> To complete this challenge, become the `owner`.

## Solution

In this challenge, the constructor function `AssumeOwmershipChallenge()` has a typo, in `Ownership`, it's written as `Owmership`. This means that what was supposed to be a constructor never ran during deployment and as a result, `owner` is the null address. 

This also means we can call this `AssumeOwmershipChallenge()` function and become `owner`, which allows us to call `authenticate()` and pass the require statement that checks if we're owner.

## Submission transaction

https://ropsten.etherscan.io/tx/0xb4f21a05d9620e5884ffe28b5abf285c5b6c4124998435c13b2fb685820c2276
