from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import GuessTheSecretNumberChallenge

##########################################
# This time I’ve only stored the hash of the number. Good luck reversing a cryptographic hash!
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        guess_the_secret_number = load_challenge(ContractObject=GuessTheSecretNumberChallenge, instance_key='guess_the_secret_number')
    else:
        guess_the_secret_number = deploy_locally(ContractObject=GuessTheSecretNumberChallenge, from_account=_from | {'value':1e18})
    
    # get the secret number
    answerHash = '0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365'
    answer = [x for x in range(2**8 - 1) if web3.sha3(x).hex() == answerHash][0]

    # guess the secret number
    guess_the_secret_number.guess(answer, _from | {'value':1e18})

    # check the result
    result = guess_the_secret_number.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
