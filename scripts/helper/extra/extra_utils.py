from curses import raw
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def get_raw_tx_from_tx_hash_etherscan(tx_hash, chainId):
    # use diff etherscan depending on the chainId
    etherscan_site = {
        1: 'etherscan.io',
        3: 'ropsten.etherscan.io',
        4: 'rinkeby.etherscan.io',
        5: 'goerli.etherscan.io',
        42: 'kovan.etherscan.io',
        11155111: 'sepolia.etherscan.io'
    }[chainId]

    # setting options
    opts = Options()
    opts.headless = True

    # defining browser
    browser = Firefox(executable_path="geckodriver", service_log_path=None, options=opts)

    # browse to ropsten etherscan site with the tx hash
    browser.get(f"https://{etherscan_site}/getRawTx?tx={tx_hash}")

    # get the content on the site after the request
    content = browser.find_element("xpath","/html/body/div[1]/main/div[2]/form/div[3]/div/div/pre").text

    # get the raw tx from the content
    raw_tx = content[content.find("0x"):]
    return raw_tx

