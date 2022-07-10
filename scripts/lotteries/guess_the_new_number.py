from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import GuessTheNewNumberChallenge, GuessTheNewNumberAttack
import struct

##########################################
# Goal of the exercise
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        guess_the_new_number = load_challenge(ContractObject=GuessTheNewNumberChallenge, instance_key='guess_the_new_number')
    else:
        guess_the_new_number = deploy_locally(ContractObject=GuessTheNewNumberChallenge, from_account=_from | {'value':1e18})
    
    # deploy attacker contract
    attacker = GuessTheNewNumberAttack.deploy(guess_the_new_number.address, _from | {'value':1e18})

    # determine if the challenge is complete
    result = guess_the_new_number.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
