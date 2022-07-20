# Account takeover

## Objectives

> To complete this challenge, send a transaction from the owner's account.

## Solution

An Ethereum transaction is composed of several different things. In particular, transactions prior to EIP-1559, have the following parameters:

```json
{
    "nonce": 0,
    "gasPrice": 1000000000,
    "gasLimit": 21000,
    "to": "0x92b28647Ae1F3264661f72fb2eB9625A89D88A31",
    "value": 1230000000000000000,
    "data": "0x",
    "v": 41,
    "r": "0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166",
    "s": "0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8"
}
```

The Keccak256 hash of the RLP encoding of the concatenation of these values is this transaction's hash (its unique identifier).

In particular, the parameters `v`, `r` and `s` are used to sign Ethereum transactions using the private key of the sender of this transaction. Ethereum transaction signatures use a specification of ECDSA defined in [Appendix F of the Ethereum yellowpaper](https://ethereum.github.io/yellowpaper/paper.pdf#appendix.F).

According to ECDSA, the value of `k` (**I will refer to it as `r`** given that this is the letter used to refer to `k` in Ethereum) has to be a cryptografically secure random integer. This integer has to _necessarily_ be chosen in a cryptografically secure random way, it should *never* be the same for two transactions and it should also never be predictable (if tx A uses `r`, tx B should _not_ use something like `r+1`).

In this challenge, the address in question (`0x6B477781b0e68031109f21887e6B5afEAaEB002b`), specified in the `owner` state variable of the challenge contract, has used `r` in two distinct transactions. As a result of this repeated use of `r`, we can actually derive the private key of this address (more on why this is possible in [this excellent wikipedia article](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm#Signature_generation_algorithm)) solving a simple system of equations.

To solve the system of equations, we need to first gather some information from these transactions. This _should_ be trivial, but Ethereum has changed quite significantly since the creation of this challenge, so obtaining some of the information required to solve the system of equations is certainly, in my opinion, not the easiest task in the universe, but it's possible.

### Parameters required

#### `r`

* `r`: We need to get the repeated `r` value used for both transactions. This is relatively easy, all you need to do is pull _all_ the transactions the address has made and look for the ones that have the same `r`. I did this by pulling all the data for this address from the Etherscan API:

```python
txs = requests.get(f'https://api-ropsten.etherscan.io/api?module=account&action=txlist&address=0x6b477781b0e68031109f21887e6b5afeaaeb002b&startblock=0&endblock=99999999&page=1&offset=269&sort=asc&apikey={os.environ["ETHERSCAN_API_KEY"]}').json()
```

After this, I gathered all the hashes for all the transactions and loaded them into python using web3.py:

```python
txs = [web3.eth.get_transaction(tx['hash']) for tx in txs['result']]
```

I then used `Counter` from the awesome `collections` library to count all the `r` values and see which is the repeated one:

```python
repeated_r = list({v:k for k,v in Counter([tx['r'].hex() for tx in txs]).items() if v > 1}.values())[0]
```

And then identified which were the transactions that had this `r` value, and they turn out to be the first and second transactions the address has made:

```python
txs_with_repeated_r = [tx for tx in txs if tx['r'].hex() == repeated_r]
```

Now that we have identified the transactions and acquired the `r`, we can now continue gathering what we need to derive the private key. For later, let's call this value $r$.

#### `s`

* `s`: This is trivial, we have the transaction objects and all we need to get is the `s` for _both_ transactions, we can call these $s_1$ (for the first tx) and $s_2$ (for the second tx). To get them in python, I did this:

```python
s1,s2 = (tx['s'].hex() for tx in txs_with_repeated_r)
```

#### `z`

* `z`: There's going to be two values of `z`, one per transaction, let's call them $z_1$ and $z_2$.

$z$ is the message hash. For this you take all the transaction's parameters that are used to create the transaction hash and change a few important fields.

In this case, the message hash will be a simulated transaction with the ordinary parameters that goes into its hash, but with `v` changed for its chain id (3 for ropsten), `r` empty and `s` empty.

1. For transaction 1 (nonce 0), with the corresponding changes:

```json
{
    "nonce": 0,
    "gasPrice": 1000000000,
    "gasLimit": 21000,
    "to": "0x92b28647Ae1F3264661f72fb2eB9625A89D88A31",
    "value": 1230000000000000000,
    "data": "", 
    // changes here 
    "v": 3, 
    "r": "", 
    "s": ""
}
```

2. For transaction 2 (nonce 1) with the corresponding changes:


```json
{
    "nonce": 1,
    "gasPrice": 1000000000,
    "gasLimit": 21000,
    "to": "0x92b28647Ae1F3264661f72fb2eB9625A89D88A31",
    "value": 1811266580600000000,
    "data": "",
    // changes here
    "v": 3,
    "r": "",
    "s": ""
}
```

Also important to note is that obviously, prior to encoding, the values should all be in bytes and should all be concatenated. As a result, your transactions' parameters should look like this:

1. For transaction 1

  + In hex:

```json
{
    "nonce": "",
    "gasPrice": "0x3b9aca00",
    "gasLimit": "0x5208",
    "to": "0x92b28647ae1f3264661f72fb2eb9625a89d88a31",
    "value": "0x1111d67bb1bb0000",
    "data": "",
    "v": "0x03",
    "r": "",
    "s": ""
}
```

  + In python as bytes:

```python
{
    'nonce': b'', 
    'gasPrice': HexBytes('0x3b9aca00'), 
    'gasLimit': HexBytes('0x5208'), 
    'to': HexBytes('0x92b28647ae1f3264661f72fb2eb9625a89d88a31'), 
    'value': HexBytes('0x1111d67bb1bb0000'), 
    'data': b'', 
    'v': HexBytes('0x03'), 
    'r': b'', 
    's': b''
}
```

1. For transaction 2

  + in hex:

```json
{
    "nonce": "0x01",
    "gasPrice": "0x3b9aca00",
    "gasLimit": "0x5208",
    "to": "0x92b28647ae1f3264661f72fb2eb9625a89d88a31",
    "value": "0x1922e95bca330e00",
    "data": "",
    "v": "0x03",
    "r": "",
    "s": ""
}
```

  + in python as bytes:

```python
{
    'nonce': b'\x01', 
    'gasPrice': HexBytes('0x3b9aca00'), 
    'gasLimit': HexBytes('0x5208'), 
    'to': HexBytes('0x92b28647ae1f3264661f72fb2eb9625a89d88a31'), 
    'value': HexBytes('0x1922e95bca330e00'), 
    'data': b'', 
    'v': HexBytes('0x03'), 
    'r': b'', 
    's': b''
}
```

Now that we have these values as bytes, all we have to do is concatenate them and then get the Keccak256 hash of its RLP encoding. In python I defined a set of functions for this entire process which you can find in `scripts/helper/utils.py`, but in a nutshell, if you have an object like the one we defined before, you can do this:

```python
import rlp
import web3

reconstructed_tx_1 = {
    'nonce': b'', 
    'gasPrice': HexBytes('0x3b9aca00'), 
    'gasLimit': HexBytes('0x5208'), 
    'to': HexBytes('0x92b28647ae1f3264661f72fb2eb9625a89d88a31'), 
    'value': HexBytes('0x1111d67bb1bb0000'), 
    'data': b'', 
    'v': HexBytes('0x03'), 
    'r': b'', 
    's': b''
}

reconstructed_tx_2 = {
    'nonce': b'\x01', 
    'gasPrice': HexBytes('0x3b9aca00'), 
    'gasLimit': HexBytes('0x5208'), 
    'to': HexBytes('0x92b28647ae1f3264661f72fb2eb9625a89d88a31'), 
    'value': HexBytes('0x1922e95bca330e00'), 
    'data': b'', 
    'v': HexBytes('0x03'), 
    'r': b'', 
    's': b''
}

z1 = web3.sha3(hexstr=rlp.encode(list(reconstructed_tx_1.values())).hex()).hex()
z2 = web3.sha3(hexstr=rlp.encode(list(reconstructed_tx_2.values())).hex()).hex()
```

And you've got $z_1$ and $z_2$.

### Obtaining the private key

1. Get $r$, which we obtained previously by looking at the transactions with repeated $r$.

2. Compute $z$, which is the difference between $z_1$ and $z_2$:

$$ z = z_1 - z_2 $$

3. Compute $s$, for which we need to contemplate all the following scenarios:

1. $s = s_1 + s_2$
2. $s = s_1 - s_2$
3. $s = - s_1 + s_2$
4. $s = - s_1 - s_2$

Or more generally:

$$s = s_1*i + s_2*j$$

Where:

$$i,j \in \{1,-1\}$$

This can be easily done in a double loop:

```python 
for i in [1,-1]:
    for j in [1,-1]:
        s = s1*i + s2*j
```

4. Define an inverse modulus function which can compute the modular multiplicative inverse of an integer. After python 3.8 you can define it like this:

```python
def inverse_mod(a, m):
    if a == 0:
        return 0
    return pow(a, -1, m)
```

Which is exactly how it's defined in the `ecdsa` library. You can import this same function like this:

```python
from ecdsa.numbertheory import inverse_mod
```

The purpose of this function is to be able to obtain the modular multiplicative inverse of integers with modulus `n`, where `n` is the order `n` of `G` of a SECP256K1 elliptic curve as used in Ethereum.

In hex, the value of this prime number is `0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141`.

More generally:

$$inverse\_mod(a) = \bar{x} \mid \bar{a} *_n \bar{x} \equiv \bar{1}$$

Where:

* $a$ is the number for which we want to find the modular multiplicative inverse $x$, modulus $m$
* $n = \text{0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141}$

5. Using this function and the previously obtained values, compute `k`:

$$k = z * inverse\_mod(s) \mod n$$

And then compute the private key $d$

$$d = inverse\_mod(r) * (s_1 * k - z_1) \mod n$$

If you're using integers, convert this final result $d$ into hex.

#### Python implementation

I have written a python implementation, modified from Eric Chen's answer on the Bitcoin StackExchange:

```python
# get private key with two k's using ecdsa-private-key-recovery
def get_private_key(r, s1, s2, z1, z2):
    """Get private key of an ethereum account 
    when the account has used a duplicate (or predictable) `r` (or `k` in ECDSA)
    based on Eric Chen's answer on the Bitcoin Stackexchange: https://bitcoin.stackexchange.com/a/110827
    """
    # convert everything to integer if it's a hex string
    hex_to_int = lambda x: int(x, 16) if isinstance(x, str) else x
    r, s1, s2, z1, z2 = map(hex_to_int, (r, s1, s2, z1, z2))

    # SECP256K1 order n of G
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # possible private keys
    possible_pks = []

    # loop over possible s1, s2 scenarios
    for i in [1,-1]:
        for j in [1,-1]:
            z = z1 - z2
            s = s1*i + s2*j
            r_inv = inverse_mod(r, p)
            s_inv = inverse_mod(s, p)
            k = (z * s_inv) % p
            d = (r_inv * (s1 * k - z1)) % p
            possible_pks.append(hex(d))

    return list(set(possible_pks))
```

## Submission transaction

https://ropsten.etherscan.io/tx/0xe912a2b3ab8dee5e51e2f321bd21e753fba4fe82f7b09f09d010f6cf722a1196
