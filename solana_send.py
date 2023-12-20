import json
from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair

client = Client("https://api.mainnet-beta.solana.com")
with open('./secrets.json') as f:
            secret_data = json.load(f)
            solana_private_key = secret_data["solana_private_key"]
sender = Keypair.from_private_key(solana_private_key)
receiver = PublicKey("6kwdsWVQYAwdTJsgwkyWEQg5csyMxkKj8drHDo6ZQQAD")

instruction = transfer(
        from_public_key=sender.public_key,
        to_public_key=receiver, 
        lamports=100
    )

transaction = Transaction(instructions=[instruction], signers=[sender])

result = client.send_transaction(transaction)
print("Transaction response: ", result)