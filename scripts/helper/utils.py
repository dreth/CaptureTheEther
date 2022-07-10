from scripts.helper.challenges import *
from brownie import accounts

# redefine _from and acc for local use
def define_from_acc(qty=1):
    # accounts to return
    accs = []

    # compose output
    for i in range(qty):
        accs.append({'from':accounts[i]})
        accs.append(accounts[i])

    # return values
    return tuple(accs)


# test locally
def deploy_locally(ContractObject, from_account, constructor_params=[]):
    # prepare the params that pass to the constructor as a string
    # that looks like "param1, param2, param3," etc
    if constructor_params:
        params = ''
        for param in constructor_params:
            # if the param is an address, it needs to pass as a string
            if param[0:2] == '0x':
                params += f'"{param}",'
            # otherwise, it's fine passing as it is
            else:
                params += f'{param},'
        contract = eval(f'ContractObject.deploy({params} from_account)')
    else:
        contract = eval(f'ContractObject.deploy(from_account)')
    return contract

# load challenge from instances
def load_challenge(ContractObject, instance_key):
    return ContractObject.at(CaptureTheEtherContracts[instance_key])
