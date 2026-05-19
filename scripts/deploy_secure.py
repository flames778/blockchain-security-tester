from web3 import Web3
import json
import sys

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():
    print("❌ Anvil not running. Start with: anvil --port 8545")
    sys.exit(1)

with open("contracts/build/SecureBank.bin", "r") as f:
    bytecode = "0x" + f.read().strip()
with open("contracts/build/SecureBank.abi", "r") as f:
    abi = json.load(f)

account = w3.eth.accounts[0]
w3.eth.default_account = account
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ SecureBank deployed at: {tx_receipt.contractAddress}")
