# Capture the Ether solutions

This repo contains my solutions and methodology to solve the [Capture the Ether CTF](https://capturetheether.com/). I solved the challenges locally using brownie. Then did it on chain on brownie on the ropsten test network through the Infura API. To fork ropsten I also used the Infura API, though not always successfully.

## My local environment setup

1. Install relevant libraries

```
pip install eth-brownie rlp eth-account eth-utils hexbytes ecdsa
```

2. Get a new instance of every challenge by going on the capture the ether site and clicking on `Begin Challenge`.

3. Paste all the challenge addresses under their corresponding key in the `scripts/helper/challenges.py` script.

4. Add an account to brownie using the CLI: 

```
brownie accounts new <account name>
```

Then paste the private key of the account used to deploy the instances in step 1. For safety reasons, do not use an account that has funds on mainnet or any other network that isn't a testnet.

5. Once the account is added, go to the `account.py` helper file, where you can define the account object to then be imported into the scripts. I used two accounts, so I defined two, the main one `acc` and `acc2`. In my case, `acc` also coincides with the account creating and submitting the Capture the Ether instances. I do this because after testing locally, I simply changed networks to ropsten in order to submit the transactions as they were submitted in my local development network or a local forked ropsten network (as described in step 9)

6. Do each challenge in a script within the `/scripts` folder and use the template (`template.py`) in `/scripts/template/` for each script.

Modify the variables at the start of `solve_challenge()` accordingly:

* `ContractName`: name of the contract object, as defined in the solidity scripts

* `'contract_name'`: key of the contract address as present in `/scripts/helper/challenges.py`

If you want to play around in your local development blockchain, then just pass `locally=True` to `solve_challenge()` under `main()` and make sure to run the script passing `development` under the network flag, like this:  `brownie run ScriptName --network development`. Subtitute `ScriptName` for the name of the script you're running. 

7. Run everything in a forked ropsten testnet local network, first add the network. Optionally use a specific block (`@block`):

```
brownie networks add development ropsten-fork cmd=ganache host=http://127.0.0.1 fork=https://ropsten.infura.io/v3/$ETHERSCAN_API_KEY@block accounts=10 mnemonic=brownie port=8545
```

As ropsten will soon be deprecated, you can only use Infura for this. Watch out in the future when these contracts are deployed in Goerli, Sepolia or another testnet.

8. Then run whatever script you want to run using this local forked network:

```
brownie run <script> --network ropsten-fork
```

or just use a development network:

```
brownie run <script> --network development
```

If you choose to use a development network, you should make some changes to this part of a challenge, for example, for the Predict the Block Hash challenge:

Note the comments in this specific fragment of code that explain the functions `define_from_acc()` and `deploy_locally()`. These functions are both in `scripts/helper/utils.py`, which also contains lots of other functions I defined to solve the challenges.

```python
# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        predict_the_block_hash = load_challenge(ContractObject=PredictTheBlockHashChallenge, instance_key='predict_the_block_hash')
    else:
        # DEFINE THE ACCOUNTS YOU WILL USE
        # acc, _from = define_from_acc(1) for ONE account
        # acc, _from, acc2, _from2 = define_from_acc(2) for TWO accounts
        # and so on
        acc, _from = define_from_acc(1) 

        # In the deploy_locally function, you should add anything needed to deploy the contract
        # for example, the lottery challenges require sending ONE ETH when you run the constructor, so `from_account` should be a dictionary containing the deployer address and the amount of wei to send
        # therefore `from_account= {'from':acc, 'value':1e18}
        # If the constructor of a contract takes any parameters
        # you can pass the argument `constructor_params` which takes a list
        # this list should contain all the objects you want to pass to the constructor in order
        predict_the_block_hash = deploy_locally(ContractObject=PredictTheBlockHashChallenge, from_account=_from | {'value':1e18})
```

9. **Once you're ready to submit your instance**, in order to make the submission, just change what network you run the script in to ropsten _after_ you have confirmed it works in your forked ropsten instance. After each tx confirms, you can submit your instance.

```
brownie run ScriptName --network ropsten
```

Again, substitute `ScriptName` with the name of your script. If your script is in a subfolder, you have to also write the subfolder, e.g. `lotteries/guess_the_new_number`.

**NOTE: [The ropsten test network is deprecated](https://ethereum.org/en/developers/docs/networks/#ropsten) in favor of the Sepolia/Görli testnet. There's a high chance that after ropsten has been deprecated, SMARX will deploy Capture the Ether in the Sepolia, Görli or some other testnet.** As a result of this, you should keep in mind that steps 7-9 of my setup will likely be on a different testnet.

## Helper scripts

Under `/scripts/helper` I have included a few convenience scripts that I imported in every script (as needed), the contents of all these scripts are imported in all challenges as I solved them. 

The helper scripts are:

- `account.py`: imports the account to be used to solve the challenges, the actual account that I use to deploy/submit my instances. Any additional accounts can be added here. I also added a second one for challenges that required a second EOA.
- `challenges.py`: contains all the instance addresses.
- `utils.py`: contains some basic functions that I use in each script. I always do a full import of everything in this script because here I defined the `load_challenge()` function which loads the instance of each challenge as well as many other useful and sometimes necessary functions that I defined for some specific challenges.
- `web3.py`: contains an instance of web3 which I use for whatever utility from the web3.py library that I might need. This is imported in `utils.py` already, as some functions use it. I named the instance `web3` but you can change this if you want.

## Templates

I have also added a small template for scripts, reports and attacker/interaction contracts I might need. They're under the `template` folder of `reports`, `contracts` and `scripts`.

## My solutions

All my solutions are layed out in [this article](https://dac.ac/blog/capture_the_ether_solutions/) on my blog, however, you can also see the solutions here on github in the markdown documents under `/reports`. You can view whichever you want by clicking on its name:

1. Warmup
   + [Call me](https://github.com/dreth/CaptureTheEther/blob/main/reports/warmup/CallMe.md)
   + [Choose a nickname](https://github.com/dreth/CaptureTheEther/blob/main/reports/warmup/ChooseANickname.md)
  
2. Lotteries
   + [Guess the number](https://github.com/dreth/CaptureTheEther/blob/main/reports/lotteries/GuessTheNumber.md)
   + [Guess the secret number](https://github.com/dreth/CaptureTheEther/blob/main/reports/lotteries/GuessTheSecretNumber.md)
   + [Guess the random number](https://github.com/dreth/CaptureTheEther/blob/main/reports/lotteries/GuessTheRandomNumber.md)
   + [Guess the new number](https://github.com/dreth/CaptureTheEther/blob/main/reports/lotteries/GuessTheNewNumber.md)
   + [Predict the future](https://github.com/dreth/CaptureTheEther/blob/main/reports/lotteries/PredictTheFuture.md)
   + [Predict the block hash](https://github.com/dreth/CaptureTheEther/blob/main/reports/lotteries/PredictTheBlockHash.md)

3. Math
   + [Token sale](https://github.com/dreth/CaptureTheEther/blob/main/reports/math/TokenSale.md)
   + [Token whale](https://github.com/dreth/CaptureTheEther/blob/main/reports/math/TokenWhale.md)
   + [Retirement fund](https://github.com/dreth/CaptureTheEther/blob/main/reports/math/RetirementFund.md)
   + [Mapping](https://github.com/dreth/CaptureTheEther/blob/main/reports/math/Mapping.md)
   + [Donation](https://github.com/dreth/CaptureTheEther/blob/main/reports/math/Donation.md)
   + [Fifty years](https://github.com/dreth/CaptureTheEther/blob/main/reports/math/FiftyYears.md)

4. Accounts
   + [Fuzzy identity](https://github.com/dreth/CaptureTheEther/blob/main/reports/accounts/FuzzyIdentity.md)
   + [Public key](https://github.com/dreth/CaptureTheEther/blob/main/reports/accounts/PublicKey.md)
   + [Account takeover](https://github.com/dreth/CaptureTheEther/blob/main/reports/accounts/AccountTakeover.md)

5. Miscellaneous
   + [Assume ownership](https://github.com/dreth/CaptureTheEther/blob/main/reports/miscellaneous/AssumeOwnership.md)
   + [Token bank](https://github.com/dreth/CaptureTheEther/blob/main/reports/miscellaneous/TokenBank.md)



