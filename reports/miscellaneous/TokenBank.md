# Token bank

## Objectives

> I created a token bank. It allows anyone to deposit tokens by transferring them to the bank and then to withdraw those tokens later. It uses ERC 223 to accept the incoming tokens.\
> The bank deploys a token called “Simple ERC223 Token” and assigns half the tokens to me and half to you. You win this challenge if you can empty the bank.

## Solution

The ERC223 standard differs from the ERC20 standard in that it notifies the contract receiving the tokens when they're sent. In this case, the implementation does it through a fallback function called `tokenFallback()` which should be implemented in the contract receiving the tokens. 

The TokenBankChallenge contract implements it along with a `withdraw()` function. However, given this flexibility and how the `withdraw()` function is coded in TokenBankChallenge, there is a re-entrancy vulnerability that allows us to call the function multiple times before the balance is updated. Not only this, but given the version of the compiler the contracts are coded in (`0.4.21` as all challenges in capture the ether), the `withdraw()` function also causes an integer overflow in the `balanceOf` array for the contract address we're using to interact with it.

To solve it, we must code a contract that implements a function that calls `withdraw()` in the TokenBankChallenge contract, for example:

```js
function withdraw() public {
    if (token.balanceOf(address(challenge)) > 0) {
        challenge.withdraw(challenge.balanceOf(address(this)));
    }
}
```

Where `challenge` is an interface.

In this case, we will only call `withdraw()` again if there's funds still available in the contract.

A `tokenFallback()` function must also be implemented because the SimpleERC223Token contract will call it. This function must also include a call to the `withdraw()` in our attacker contract, I implemented it like this:

```js
function tokenFallback(address sender, uint256 value, bytes data) external {
    if (sender == address(challenge)) {
        withdraw();
    }
}
```

We only want to call withdraw when the TokenBankChallenge contract transfers funds to the attacker contract through `require(token.transfer(msg.sender, amount));` (line 106 in the challenge contract). 

The reentrancy vulnerability would be impossible to execute if the balance is updated prior to calling transfer in the token contract:

```js
function withdraw(uint256 amount) public {
    require(balanceOf[msg.sender] >= amount);
    balanceOf[msg.sender] -= amount;
    require(token.transfer(msg.sender, amount));
}
```

However, the contract is coded as follows:

```js
function withdraw(uint256 amount) public {
    require(balanceOf[msg.sender] >= amount);

    require(token.transfer(msg.sender, amount));
    balanceOf[msg.sender] -= amount;
}
```

## Submission transaction

https://ropsten.etherscan.io/tx/0xd172a0fe62e154b55ca71d98f8003835121977c5ff18a1c4d76c97b5c4e380fb
