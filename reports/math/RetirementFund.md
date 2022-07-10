# Retirement fund

## Objectives

> This retirement fund is what economists call a commitment device. I’m trying to make sure I hold on to 1 ether for retirement.
> I’ve committed 1 ether to the contract below, and I won’t withdraw it until 10 years have passed. If I do withdraw early, 10% of my ether goes to the beneficiary (you!).
> I really don’t want you to have 0.1 of my ether, so I’m resolved to leave those funds alone until 10 years from now. Good luck!

## Solution

The function `collectPenalty()` allows us to withdraw the entire balance of the contract if:

1. `startBalance` is more than the total contract balance
2. If there's an overflow where the balance of the contract is larger than `startBalance`

In this case, we simply cannot call `withdraw()` or somehow move funds away from the contract in any other way aside from option number 2. Therefore, because the contract has no payable function, we have to somehow force funds into the contract. 

An easy way to do this is to deploy another contract, fund it with at least 1 wei and then destroy it calling `selfdestruct()` in any of the contract functions and directing the contract funds into the retirement fund contract. This will allow us to cause an overflow that causes `withdrawn` to be larger than 0 and therefore drains the contract.

The buggy line in question:

```js
uint256 withdrawn = startBalance - address(this).balance;
```

Nothing critical that allows drainage of funds should rely on the value of the contract balance. At least not on the upside, since anyone can simply force funds into the contract.

## Submission transaction

https://ropsten.etherscan.io/tx/0x2e1da049d1bc5a70bccc081c4734c9ebd3f8ada241252ffdbd261fc230918f86
