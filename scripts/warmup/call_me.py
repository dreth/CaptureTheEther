from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import CallMeChallenge

##########################################
# To complete this challenge, all you need to do is call a function.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        call_me = load_challenge(ContractObject=CallMeChallenge, instance_key='call_me')
    else:
        call_me = deploy_locally(ContractObject=CallMeChallenge, from_account=_from)
    
    # call the callme() function
    call_me.callme(_from)

    # check if it's complete
    result = call_me.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
