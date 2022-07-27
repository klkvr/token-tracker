import json

from web3 import Web3

from app.config import BASE_DIR
from app.models import Chain

with open(BASE_DIR / "abis" / "erc20.abi.json") as file:
    erc20_abi = json.load(file)

class Ethereum:
    def __init__(self, chain: Chain):
        self.web3 = Web3(Web3.HTTPProvider(chain.rpc))
        self.token_contract = self.web3.eth.contract(chain.token_contract_address, abi=erc20_abi)

    def get_transfer_events(self, from_block: int, to_block: int):
        return self.token_contract.events.Transfer().getLogs(fromBlock=from_block, toBlock=to_block)

    def token_decimals(self):
        return self.token_contract.functions.decimals().call()
