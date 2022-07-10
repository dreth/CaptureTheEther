from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import GuessTheNumberChallenge

##########################################
# I’m thinking of a number. All you have to do is guess it.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        guess_the_number = load_challenge(ContractObject=GuessTheNumberChallenge, instance_key='guess_the_number')
    else:
        guess_the_number = deploy_locally(ContractObject=GuessTheNumberChallenge, from_account=_from)
    
    # call guess() function
    guess_the_number.guess(42, _from | {'value':1e18})

    # check the balance to see if the contract is drained
    result = guess_the_number.isComplete()
    print(result)

    # return the result
    return result


def main():
    solve_challenge()
