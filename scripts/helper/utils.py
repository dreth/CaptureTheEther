from scripts.helper.challenges import *
from scripts.helper.web3 import web3
from brownie import accounts
from eth_utils import keccak, to_checksum_address, to_bytes
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict, encode_transaction, ALLOWED_TRANSACTION_KEYS
import rlp
from ecdsa.numbertheory import inverse_mod
from hexbytes import HexBytes

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

# compute address of a given contract to be deployed from
# the deployer address + nonce, as stated in the Section 7 
# of the Ethereum yellowpaper for contracts created using CREATE
def mk_contract_address(sender: str, nonce: int) -> str:
    """Create a contract address using eth-utils.
    Modified from Mikko Ohtamaa's original answer which was later edited by Utgarda
    Obtained from https://ethereum.stackexchange.com/questions/760/how-is-the-address-of-an-ethereum-contract-computed
    """
    sender_bytes = to_bytes(hexstr=sender)
    raw = rlp.encode([sender_bytes, nonce])
    h = keccak(raw)
    address_bytes = h[12:]
    return to_checksum_address(address_bytes)

# get tx object from hash
def get_tx_object_from_tx_hash(tx_hash, web3_instance):
    # get transaction object from hash
    return web3_instance.eth.get_transaction(tx_hash)

# get chain id from tx v
def get_chain_id_from_tx_v(tx_object):
    return extract_chain_id(tx_object.v)

# get signature from tx
def get_signature_from_tx_obj(tx_object, web3_instance):
    # get signature
    return web3_instance.eth.account._keys.Signature(vrs=(
        to_standard_v(get_chain_id_from_tx_v(tx_object)[1]),
        web3_instance.toInt(tx_object.r),
        web3_instance.toInt(tx_object.s)
    ))

# get message from tx
def reconstruct_unsigned_tx_from_tx_obj(tx_object):
    # chain id
    chain_id = get_chain_id_from_tx_v(tx_object)

    # get tx info to reconstruct the msg
    msg = {k:tx_object[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId','data'}}
    msg['data'] = tx_object.input # get actual data from the tx
    msg['chainId'] = chain_id[0] # get the correct chainid

    return serializable_unsigned_transaction_from_dict(msg)

# get account public key function
def get_public_key_from_tx_obj(tx_object, web3_instance):
    """Get the public key of an account from a transaction hash
    Created from tworec's answer on stackexchange
    With some changes to adapt to changes in eth-account since 2019
    Obtained from: https://ethereum.stackexchange.com/a/67398/
    """
    # get signature
    signature = get_signature_from_tx_obj(tx_object, web3_instance)

    # get message
    msg = reconstruct_unsigned_tx_from_tx_obj(tx_object)

    # reconstruct the transaction and recover the public key from it
    return signature.recover_public_key_from_msg_hash(msg.hash())

# get private key with two k's using ecdsa-private-key-recovery
def get_private_key(r, s1, s2, z1, z2):
    """Get private key of an ethereum account 
    when the account has used a duplicate (or predictable) `r` (or `k` in ECDSA)
    based on Eric Chen's answer on the Bitcoin Stackexchange: https://bitcoin.stackexchange.com/a/110827
    """
    # convert everything to integer if it's a hex string
    hex_to_int = lambda x: int(x, 16) if isinstance(x, str) else x
    r, s1, s2, z1, z2 = map(hex_to_int, (r, s1, s2, z1, z2))

    # SECP256K1 order n of G
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # possible private keys
    possible_pks = []

    # loop over possible s1, s2 scenarios
    for i in [1,-1]:
        for j in [1,-1]:
            z = z1 - z2
            s = s1*i + s2*j
            r_inv = inverse_mod(r, p)
            s_inv = inverse_mod(s, p)
            k = (z * s_inv) % p
            d = (r_inv * (s1 * k - z1)) % p
            possible_pks.append(hex(d))

    return list(set(possible_pks))

# convert value from hexbytes to int if it's actually a hexbytes object
def hex_to_int(value):
    if isinstance(value, HexBytes(0).__class__) or (isinstance(value,str) and value[0:2] == '0x'):
        return int(value,16)
    else:
        return value

# reconstruct raw tx from tx object
def reconstruct_tx_from_tx_obj(tx_object):
    # get relevant data about the tx
    reconstructed_tx = {
        'nonce': tx_object['nonce'],
        'gasPrice': tx_object['gasPrice'],
        'gasLimit': tx_object['gas'],
        'to': tx_object['to'],
        'value': tx_object['value'],
        'data': b'' if tx_object['input'] == '0x' else tx_object['input'],
        'v': tx_object['v'],
        'r': tx_object['r'],
        's': tx_object['s']
    }

    return reconstructed_tx

# convert tx reconstructed tx object to bytes
def reconstructed_tx_object_to_bytes(tx_object):
    # get relevant data about the tx
    tx_info = reconstruct_tx_from_tx_obj(tx_object)

    # make the nonce bytes
    int_to_bytes = lambda x: bytes.fromhex('0' + hex(x)[2:]) if x < 16 else bytes.fromhex(hex(x)[2:])
    tx_info['nonce'] = b'' if tx_info['nonce'] == 0 else int_to_bytes(tx_info['nonce'])

    # return the raw tx, which is the rlp encoding of tx_info
    to_hexbytes = lambda x: HexBytes(x) if (not isinstance(x, HexBytes(0).__class__) and not isinstance(x, bytes)) else x
    tx_info_values = {k:to_hexbytes(x) for k,x in tx_info.items()}

    # convert to bytes
    return tx_info_values

# get raw tx from a tx object, this only works for legacy transactions
# which had `gasPrice`. After EIP1559, this doesn't work.
def get_raw_tx_from_tx_object(tx_object):
    # make a list of the values from the reconstructed tx
    # in order to encode them using rlp
    reconstructed_tx = tx_object if isinstance(tx_object, list) else list(reconstructed_tx_object_to_bytes(tx_object))
    rlp_tx_info = rlp.encode(reconstructed_tx)
    return rlp_tx_info.hex()

# get message hash from tx object, for legacy transactions
# I got this definition from ethereumjs-tx's Transaction `hash` method
# this uses the EIP 155 spec
def get_message_hash_from_raw_tx(tx_object, web3_instance):
    # get the reconstructed tx
    reconstructed_tx = reconstructed_tx_object_to_bytes(tx_object)
    
    # make `v` the chain id
    reconstructed_tx['v'] = HexBytes(get_chain_id_from_tx_v(tx_object)[0])

    # make `r` and `s` zero
    reconstructed_tx['r'] = bytes(0)
    reconstructed_tx['s'] = bytes(0)

    # hash the rlp encoding of the reconstructed raw tx
    # with v,r,s changed
    raw_tx = get_raw_tx_from_tx_object(list(reconstructed_tx.values()))
    hashed_raw_tx = web3_instance.sha3(hexstr=raw_tx)

    return hashed_raw_tx.hex()
