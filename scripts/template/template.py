from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import ContractName

##########################################
# Goal of the exercise
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        contract_name = load_challenge(ContractObject=ContractName, instance_key='contract_name')
    else:
        contract_name = deploy_locally(ContractObject=ContractName, from_account=_from)
    


def main():
    solve_challenge()
