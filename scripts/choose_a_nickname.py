from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import NicknameChallenge, CaptureTheEther

##########################################
# To complete this challenge, set your nickname to a non-empty string.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        choose_a_nickname = load_challenge(ContractObject=NicknameChallenge, instance_key='choose_a_nickname')
        cte = load_challenge(ContractObject=CaptureTheEther, instance_key='cte')
    else:
        choose_a_nickname = deploy_locally(ContractObject=NicknameChallenge, from_account=_from)
    
    # choose nickname
    cte.setNickname("zooberto".encode('utf8').hex(), _from)

    # check if challenge is complete
    result = choose_a_nickname.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
