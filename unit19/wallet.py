# Imported libraries
import subprocess
import json
import os

from constants import *
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

load_dotenv()

# Imported mnemonic from env
filepath=".env"
p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

mnemonic = os.getenv('MNEMONIC')
print(mnemonic)

# Connected to local ETH/geth
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Defined function to derive wallet
def derive_wallets(mnemonic, coin, numderive):
    """Use the subprocess library to call the php file script from Python"""
    command = f'php ./hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --cols=path,address,privkey,pubkey --format=json' 
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return  keys

# Created a dictionary object called coins to store the output from `derive_wallets`.
coins = {"eth", "btc", "btc-test"}
print(coins)
numderive = 3

key = {}
for coin in coins:
    key[coin]= derive_wallets(os.getenv('mnemonic'), coin, numderive=3)
    

eth_PrivateKey = key["eth"][0]['privkey']
btc_PrivateKey = key["btc-test"][0]['privkey']

print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))

print(json.dumps(key, indent=4, sort_keys=True))


# Created a function called `priv_key_to_account` that converts privkey strings to account objects.

def priv_key_to_account(coin,priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    

# Created a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin,account, recipient, amount):
    if coin == ETH: 
        gasEstimate = w3.eth.estimateGas(
            {"from":eth_acc.address, "to":recipient, "value": amount}
        )
        return { 
            "from": eth_acc.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
    

# Created a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_txn(coin,account,recipient, amount):
    txn = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)
    

# Connecting to HTTP with address
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


# Created a function called 'create_raw_tx'

def create_raw_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }

# Created a function called 'send_tx'

def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

# BTC-TEST 
btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)

create_tx(BTCTEST,btc_acc,"mzKe2XK1Vb4Cxnxi2h6N3g9pxGUppTUCnm", 0.0001)

# Send BTC Transaction
send_txn(BTCTEST,btc_acc,"mzKe2XK1Vb4Cxnxi2h6N3g9pxGUppTUCnm", 0.00001)

# ETH TEST

eth_acc = priv_key_to_account(ETH,eth_PrivateKey)



