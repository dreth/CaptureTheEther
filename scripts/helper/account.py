from brownie import accounts
import os

# main account to use
acc = accounts.load('acc', password=os.environ['ACCOUNT_PASSWORD'])
_from = {'from':acc}

# 2nd account
acc2 = accounts.load('acc2', password=os.environ['ACCOUNT_PASSWORD2'])
_from2 = {'from':acc2}
