import json
import pprint
import time
import decimal
from web3 import Web3

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware

#TODO: 
#가스비 높아서 트잭 지연될 때 {'code': -32000, 'message': 'replacement transaction underpriced'} 오류 해결
#가스비 적게 값 바꾸기
#swap으로 바꾸기

# 설정법: secrets.json 파일 만들고 아래 형식대로 ~~~에 개인키 넣기
# {
#     "eth_private_key": "~~~"
# }

# 파이썬 정밀한 소수 계산법이 이상해서 임시로 Wei값 직접 적음
# amountInEther = decimal.Decimal(19.996020692399520915)
# amountInWei = Web3.to_wei(amountInEther, 'ether')
# print(amountInWei)
amountInWei = 19996020692399520915
w3 = Web3(Web3.HTTPProvider("https://polygon-pokt.nodies.app"))
with open('./secrets.json') as f:
            secret_data = json.load(f)
            eth_private_key = secret_data["eth_private_key"]

account: LocalAccount = Account.from_key(eth_private_key)
print(f"Your wallet address is {account.address}")

for i in range(10):
# #MATIC TO W-MATIC
    transaction = {
        'chainId': 137,
        'from': account.address,
        'to': '0x7B36dFD5304562952E2B4DE9C8048ED155c6115d',
        'value': amountInWei,
        'nonce': w3.eth.get_transaction_count(account.address),
        'data': '0x98cf9d51000000000000000000000000000000000000000000000001141eb3e5945f4018',
        'gas': 300000,
        'maxFeePerGas': Web3.to_wei('240', 'gwei'), #
        'maxPriorityFeePerGas': Web3.to_wei('40', 'gwei'), #
    }
    signed = w3.eth.account.sign_transaction(transaction, eth_private_key )
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    tx_hash_string = tx_hash.hex()
    print( tx_hash_string)

    time.sleep(5)

    #W-MATIC TO MATIC
    transaction = {
        'chainId': 137,
        'from': account.address,
        'to': '0x7B36dFD5304562952E2B4DE9C8048ED155c6115d',
        'value': 0,
        'nonce': w3.eth.get_transaction_count(account.address),
        'data': '0x98cf9d5100000000000000000000000000000000000000000000000106505e1a19c0dff8',
        'gas': 300000,
        'maxFeePerGas': Web3.to_wei('240', 'gwei'), #
        'maxPriorityFeePerGas': Web3.to_wei('40', 'gwei'), #
    }
    signed = w3.eth.account.sign_transaction(transaction, eth_private_key )
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    tx_hash_string = tx_hash.hex()
    print(tx_hash_string)

    time.sleep(5)