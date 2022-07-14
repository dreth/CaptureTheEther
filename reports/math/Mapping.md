# Mapping

## Objectives

> Who needs mappings? I’ve created a contract that can store key/value pairs using just an array.

## Solution

Through the `set()` function, it's possible to overflow the length of the array by passing in the maximum allowable uint256 minus 2 (as `key`).

```js
function set(uint256 key, uint256 value) public {
    // Expand dynamic array as needed
    if (map.length <= key) {
        map.length = key + 1;
    }

    map[key] = value;
}
```

After passing this value as `key`, the length of the array will be the maximum allowable uint256, which allows us to manipulate every single element in this contract's storage, including `isComplete`.

Given that `isComplete` is in the first contract storage slot, we can find the hash of this item as if it was part of the `map[]` array. That position will simply be the keccak256 hash of a uint256 that is `1`, in this case:

$$0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6$$

We then subtract the value of this hash from the size of slots in memory that a contract can have, which is the maximum uint256 + 1, so $2^{256}$, therefore:

$$2^{256} - int(0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6)$$

The hex value of this number is:

$$0x4ef1d2ad89edf8c4d91132028e8195cdf30bb4b5053d4f8cd260341d4805f30a$$

With this value we can now call `set()` with `key = 0x4ef1d2ad89edf8c4d91132028e8195cdf30bb4b5053d4f8cd260341d4805f30a` and with `value = 1`. Which overwrites the `0x0000000000000000000000000000000000000000000000000000000000000000` that is held in this memory slot representing the value of `isComplete` with `0x0000000000000000000000000000000000000000000000000000000000000001` which as a `bool` represents the value `true`.

Therefore, when we call the getter `isComplete()` for this state variable (since it's a public variable), we get `true` and the challenge is complete. 

## Submission transaction

https://ropsten.etherscan.io/tx/0x9e77f98e6cf3eba43ed8d4ce2f176d9c25e7f0116d2a7b2e0a51fbfb058eba52
