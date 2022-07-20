# Fuzzy identity

## Objectives

>This contract can only be used by me (smarx). I don’t trust myself to remember my private key, so I’ve made it so whatever address I’m using in the future will work:
>
>1. I always use a wallet contract that returns “smarx” if you ask its name.
>2. Everything I write has bad code in it, so my address always includes the hex string badc0de.
>
>To complete this challenge, steal my identity!

## Solution

There's two conditions we need to satisfy to successfully pass the two require statements in `authenticate()`:

1. When we call the `authenticate()` function from a contract, there must be a `name()` function defined in the calling contract that returns "smarx", I defined it as follows:

```js
function name() public view returns (bytes32) {
    return bytes32("smarx");
}
```

2. We need that our contract address has the particular property that when it is operated with the `mask` as defined in `isBadCode` using a bitwise and (`&`) that its returning value is the value of `id`, which is any hex with `badc0de` in it, in any position. 

This last particular qualiy is especially difficult to attain (at least compared to the first one). The reason for this is that we need to bruteforce the address of this to-be-deployed contract that we will use to interact with the FuzzyIdentityChallenge contract.

Given that contract addresses are deterministic and computed using the deployer's address and the nonce in which the contract wil be deployed, we can generate lots of different contract addresses in three ways in order to bruteforce it:

1. Utilizing one address and increasing the nonce by one until we find it

2. Utilizing many addresses and the nonce 0, meaning that the first transaction each address makes will be the attacker contract deployment

3. Mixing 1 and 2 by creating many addresses and testing each address up to a specific nonce

No matter the approach, we then have to bruteforce one address+nonce combination for which the condition in `isBadCode()` is met.

This takes a _long_ time. There probability that the string `badc0de` appears written exactly like that is of $\frac{1}{16^{7}} \approx 0.000000004$, which is slightly alleviated by the fact that we can have it in 34 different positions, which increases the probability significantly ($\frac{1}{16^{7}} * 34 \approx 0.000000136$, but this still requires millions of tries.

It certainly does not particularly help that I chose python to do this, as python is notoriously slow, this would've been much faster to run in a compiled, low-level programming language, albeit much more time consuming to code.

Once the account+nonce is found, all we have to do is run `authenticate()` from a contract deployed by this account at the nonce we found.

## Submission transaction


