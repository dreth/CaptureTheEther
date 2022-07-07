from web3 import Web3
import os

web3 = Web3(Web3.HTTPProvider(f"https://ropsten.infura.io/v3/{os.environ['WEB3_INFURA_PROJECT_ID']}"))
