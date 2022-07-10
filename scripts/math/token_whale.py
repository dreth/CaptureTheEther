from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import TokenWhaleChallenge

##########################################
# Goal of the exercise
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        token_whale = load_challenge(ContractObject=TokenWhaleChallenge, instance_key='token_whale')
    else:
        token_whale = deploy_locally(ContractObject=TokenWhaleChallenge, from_account=_from)
    


def main():
    solve_challenge()
