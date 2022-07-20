# Public key

## Objectives

>Recall that an address is the last 20 bytes of the keccak-256 hash of the address’s public key.
>To complete this challenge, find the public key for the owner's account.

## Solution

The public key associated with an address can be derived from a transaction signature. In this case, the account's public key we need can indeed be derives as the account has made at least _one_ transaction.

The transaction in question has the following hash: [`0xabc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb`](https://ropsten.etherscan.io/tx/0xabc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb).

This transaction is the _only_ transaction that this account has signed, but because it was signed by this address and it's an _outgoing_ transaction, we can derive the public key from this specific transaction's `v`, `r` and `s`.

This is detailed in [Appendix F of the ethereum yellowpaper](https://ethereum.github.io/yellowpaper/paper.pdf#subsection.4.2), where the methodology of generating transaction signatures is defined.

Putting these three values together we can reconstruct the signature and recover the public key from the message hash. Which turns out to be:

```
0x613a8d23bd34f7e568ef4eb1f68058e77620e40079e88f705dfb258d7a06a1a0364dbe56cab53faf26137bec044efd0b07eec8703ba4a31c588d9d94c35c8db4
```

## Submission transaction

https://ropsten.etherscan.io/tx/0xce1ed34369e62875cbab92681c06960b8edbd8b2cc6b71da2eca5c617559e7bf
