# Fifty years

## Objectives

>This contract locks away ether. The initial ether is locked away until 50 years has passed, and subsequent contributions are locked until even later.
>All you have to do to complete this challenge is wait 50 years and withdraw the ether. If you’re not that patient, you’ll need to combine several techniques to hack this contract.

## Solution

Theres some exploitable mistakes in `upsert()`. We can solve this challenge as follows:

1. Call `upsert()` with:
   + `index` as a value larger than 0 (length of `queue`), in my case I used 1, this would send us to the else block of that if statement.
   + `timestamp` as the largest uint256 minus the seconds in a day (86400). We know block timestamps are set in unix time, which is measured in seconds, and that the require statement in the else block checks that the timestamp we input is larger than the timestamp of the previous element to the one we add + one day (86400 seconds).
   + Sending exactly 1 wei, which makes `queue.length = 1`, we need this to be able to add an additional element to `queue`. 

Calling `upsert()` with these parameters will cause the code in the `else` block to run, which never initializes `contribution`. Therefore, we would be overwriting:
* The contents of `queue`'s length, because the length of a dynamically-sized array is the first property of it that's stored in a contract's storage.
* The contents of `head` with the value of this block timestamp. This is not particularly relevant because we will then overwrite the contents of `head` again, but it's important to mention that it will also do this.

2. Call `upsert()` again with:
    + `index` as 1, which would still go to the else block
    + `timestamp` as 0. in this case we want to overwrite the value of `head` with 0, since we made it $2^{256} - 86400$ before and this would not allow us to call `withdraw()`, because the current `block.timestamp` would be much smaller than $2^{256} - 86400$
    + Sending exactly 1 wei, as we want to retain the length of `queue`.

In this case, we now have `head` as 0, which allows us to call `withdraw()` and also include the first contract deposit in the withdrawal amount, which is the first element of the `queue` array.

3. Call `withdraw()` with `index = 1`. We now can call `withdraw()` because the timestamp in the second struct of the array is 0, which is always lower than `block.timestamp` and because `head` is still 0, it'll allow us to withdraw the full contract balance.

## Submission transaction

https://ropsten.etherscan.io/tx/0xce1ed34369e62875cbab92681c06960b8edbd8b2cc6b71da2eca5c617559e7bf
