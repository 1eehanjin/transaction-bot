import json
from web3 import Web3

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware

w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth_goerli"))

with open('./secrets.json') as f:
            secret_data = json.load(f)
            eth_private_key = secret_data["eth_private_key"]



account: LocalAccount = Account.from_key(eth_private_key)

print(f"Your hot wallet address is {account.address}")


some_address = "0x700A0F4442D1F0fa1ee02bE1fE897f32d4A4AB39"

# 1. Build a new tx
transaction = {
    'chainId': 5,
    'from': account.address,
    'to': some_address,
    'value': 100000000,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 200000,
    'maxFeePerGas': 2000000000,
    'maxPriorityFeePerGas': 1000000000,
}

# 2. Sign tx with a private key
signed = w3.eth.account.sign_transaction(transaction, eth_private_key )

# 3. Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
tx = w3.eth.get_transaction(tx_hash)
assert tx["from"] == account.address