import json
import pprint
import time
import decimal
from web3 import Web3

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware

def send_transaction_for_airdrop(account):
    nonce = w3.eth.get_transaction_count(account.address)
    #print("nonce: "+ str(nonce))
    if nonce > 3000:
         print("완료된 계정입니다 !")
         return
    matic_balance = w3.eth.get_balance(account.address)
    matic_balance = Web3.from_wei(matic_balance, "ether")
    if matic_balance > 50 :
         send_transaction_matic_to_wmatic(account)
    else:
         send_transaction_wmatic_to_matic(account)
    
def send_transaction_wmatic_to_matic(account):
    transaction = {
        'chainId': 137,
        'from': account.address,
        'to': '0x7B36dFD5304562952E2B4DE9C8048ED155c6115d',
        'value': 0,
        'nonce': w3.eth.get_transaction_count(account.address),
        'data': '0x98cf9d5100000000000000000000000000000000000000000000000106505e1a19c0dff8',
        'gas': gas,
        'maxFeePerGas': Web3.to_wei(max_gwei, 'gwei'), #
        'maxPriorityFeePerGas': Web3.to_wei(max_priority_gwei, 'gwei'), #
    }      
    signed = w3.eth.account.sign_transaction(transaction, eth_private_key )
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    tx_hash_string = tx_hash.hex()
    print( tx_hash_string)

def send_transaction_matic_to_wmatic(account):
    transaction = {
        'chainId': 137,
        'from': account.address,
        'to': '0x7B36dFD5304562952E2B4DE9C8048ED155c6115d',
        'value': amountInWei,
        'nonce': w3.eth.get_transaction_count(account.address),
        'data': '0x98cf9d51000000000000000000000000000000000000000000000001141eb3e5945f4018',
        'gas': gas,
        'maxFeePerGas': Web3.to_wei(max_gwei, 'gwei'), #
        'maxPriorityFeePerGas': Web3.to_wei(max_priority_gwei, 'gwei'), #
    }
    signed = w3.eth.account.sign_transaction(transaction, eth_private_key )
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    tx_hash_string = tx_hash.hex()
    print( tx_hash_string)
    
#TODO: 
#가스비 높아서 트잭 지연될 때 {'code': -32000, 'message': 'replacement transaction underpriced'} 오류 해결
#가스비 적게 값 바꾸기
#swap으로 바꾸기

# 설정법: secrets.json 파일 만들고 아래 형식대로 ~~~에 개인키 넣기
# {
#     "eth_private_key": ["~~~"]
# }

# 파이썬 정밀한 소수 계산법이 이상해서 임시로 Wei값 직접 적음
# amountInEther = decimal.Decimal(19.996020692399520915)
# amountInWei = Web3.to_wei(amountInEther, 'ether')
# print(amountInWei)
gas = 2000000
max_gwei = '201'
max_priority_gwei = '40'
amountInWei = 19996020692399520915

w3 = Web3(Web3.HTTPProvider("https://polygon-pokt.nodies.app"))
with open('./secrets.json') as f:
            secret_data = json.load(f)
            eth_private_keys = secret_data["eth_private_keys"]

accounts = []
for eth_private_key in eth_private_keys:
    account = Account.from_key(eth_private_key)
    accounts.append(account)     
    print(f"Your wallet address is {account.address}")

while True:
    for account in accounts:
        try:
            send_transaction_for_airdrop(account)
            time.sleep(10)
        except:
            print("가스비를 높여주세요.")
            time.sleep(60)