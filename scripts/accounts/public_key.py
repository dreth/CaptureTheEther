from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import PublicKeyChallenge

##########################################
# Recall that an address is the last 20 bytes of the keccak-256 hash of the address’s public key.
# To complete this challenge, find the public key for the owner's account.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        public_key = load_challenge(ContractObject=PublicKeyChallenge, instance_key='public_key')
    else:
        public_key = deploy_locally(ContractObject=PublicKeyChallenge, from_account=_from)
    
    # get public key using the tx hash of one transaction the address in question has made
    tx = web3.eth.get_transaction('0xabc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb')
    pk = get_public_key_from_tx_obj(tx, web3)
    
    # pass the public key to the contract
    public_key.authenticate(str(pk), _from)

    # check if the challenge is complete
    result = public_key.isComplete()
    print(result)
    
    # return the result
    return result

def main():
    solve_challenge()
