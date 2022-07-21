from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import AccountTakeoverChallenge
import requests
import json
import os
import pickle
from collections import Counter

##########################################
# To complete this challenge, send a transaction from the owner's account.
#########################################

# solve the challenge
def solve_challenge(locally=False, dump_data=False, read_serialized_web3_txs_obj=True):
    # load challenge
    if not locally:
        account_takeover = load_challenge(ContractObject=AccountTakeoverChallenge, instance_key='account_takeover')
    else:
        account_takeover = deploy_locally(ContractObject=AccountTakeoverChallenge, from_account=_from)

    # get tx data from etherscan
    if dump_data:
        # get txs from the owner address
        txs = requests.get(f'https://api-ropsten.etherscan.io/api?module=account&action=txlist&address=0x6b477781b0e68031109f21887e6b5afeaaeb002b&startblock=0&endblock=99999999&page=1&offset=269&sort=asc&apikey={os.environ["ETHERSCAN_API_KEY"]}').json()

        with open('./scripts/extras/AccountTakeover/account_takeover_txs.json', 'w') as f:
            json.dump(txs, f)
    else:
        # read local tx data
        with open('./scripts/extras/AccountTakeover/account_takeover_txs.json', 'r') as f:
            txs = json.load(f)

    # if the data has been dumped and read, we obtain tx info using web3 and the tx hashes
    if read_serialized_web3_txs_obj:
        # read the data from the pickle dump
        with open('./scripts/extras/AccountTakeover/account_takeover_txs_obj.pickle', 'rb') as f:
            txs = pickle.load(f)
    else:
        # get all txs from their hash using web3
        txs = [web3.eth.get_transaction(tx['hash']) for tx in txs['result']]

        # dump the data
        with open('./scripts/extras/AccountTakeover/account_takeover_txs_obj.pickle', 'wb') as f:
            pickle.dump(txs, f)
    
    # check if 'r' is repeated ('k' in ECDSA)
    repeated_r = list({v:k for k,v in Counter([tx['r'].hex() for tx in txs]).items() if v > 1}.values())[0]

    # get txs with repeated 'r'
    txs_with_repeated_r = [tx for tx in txs if tx['r'].hex() == repeated_r]

    # txs 's'
    s1,s2 = (tx['s'].hex() for tx in txs_with_repeated_r)

    # get message hashes for the transactions
    eip155_hashed_raw_tx_1, eip155_hashed_raw_tx_2 = (get_message_hash_from_raw_tx(tx, web3) for tx in txs_with_repeated_r)


    # # generate potential private keys
    pks = get_private_key(repeated_r, s1, s2, eip155_hashed_raw_tx_1, eip155_hashed_raw_tx_2)
    
    # load account from private key
    for pk in pks:
        try:
            print(f'Testing private key: {pk}')
            taken_over = accounts.add(private_key=pk)
            print(f'Account taken over: {taken_over.address}')

            # fund the account to takeover
            acc.transfer(taken_over.address, 1e16)

            # use the taken over account to call the contract
            account_takeover.authenticate({'from':taken_over} | {'allow_revert':True})
        
            # check if the challenge is complete
            result = account_takeover.isComplete()

            # show the result
            print(result)

            # if the key is found, stop trying
            if result:
                break
        except:
            pass

    # return the result
    return True

def main():
    solve_challenge()
