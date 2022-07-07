# Choose a nickname

## Objectives

To complete this challenge, set your nickname to a non-empty string.

## Solution

All we have to do is call `setNickname()` on the CaptureTheEther contract with the nickname as hex. In brownie I did this by encoding the string and passing in the hex value:

```python
cte.setNickname("zooberto".encode('utf8').hex(), _from)
```

## Submission transaction

https://ropsten.etherscan.io/tx/0x5033e566d085e7a00206039798fbaa7e88e8eba1212853351a28358672d4fb48
