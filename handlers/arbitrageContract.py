from typing import List, Mapping, Any

from factory import w3
from const.arbitrageContract import arbitrage_contract_abi
from factory.w3 import W3
from handlers.erc20 import ERC20
from handlers.networkHelpers import infinite_retry
from const.config import arbitrage_contract_address, wallet_address


class ArbitrageContract:
    _instance = None
    w3 = None


    def __init__(self):
        self.w3 = W3().getWeb3()
        self.arbitrage_contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(arbitrage_contract_address), abi=arbitrage_contract_abi)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ArbitrageContract, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    @infinite_retry(1)
    def getTradeBalance(self, instructions) -> List[int]:
        return self.arbitrage_contract.functions.getTradeBalance().call({'from': wallet_address})

    @infinite_retry(1)
    def get_expected_output(self, instructions) -> List[int]:
        return self.arbitrage_contract.functions.get_expected_output(
            [instruction.params() for instruction in instructions]
            ).call({'from': wallet_address})

    def execute_arbitrage(self, instructions, min_output):
        for i in range(len(instructions)):
            instructions[i].inpt = min_output[i][0]
            instructions[i].output = min_output[i][-1]
        
        tx = self.arbitrage_contract.functions.execute_trade(
            [instruction.params() for instruction in instructions]
            ).buildTransaction(W3().get_tx_args())
        print(tx)
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
        try:
            sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(sentTx)
            return self.w3.eth.get_transaction_receipt(sentTx)
        except Exception as e:
            print(e)
        
