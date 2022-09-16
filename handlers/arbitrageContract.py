from typing import List, Mapping, Any
from const.controlls import minRoiRequirement

from factory import w3
from const.arbitrageContract import arbitrage_contract_abi
from factory.w3 import W3
from handlers.erc20 import ERC20
from handlers.networkHelpers import infinite_retry
from const.config import arbitrage_contract_address, wallet_address
from model.tradeInstructions import TradeInstruction


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

    def shrink_expected_output(self, instructions: list[TradeInstruction], shrink_factor: int) -> list[TradeInstruction]:
        for i, x in range(len(instructions)):
            if i != 0:
                instructions[i].inpt = int(instructions[i].inpt * shrink_factor)
            instructions[i].outpt = int(instructions[i].outpt * shrink_factor)
        return instructions

    def instructions_are_valid(self, instructions: list[TradeInstruction]) -> bool:
        if instructions[-1].outpt / instructions[0].inpt < minRoiRequirement():
            return False
        return True


    def execute_arbitrage(self, instructions: list[TradeInstruction], count=0):        
        tx_raw = self.arbitrage_contract.functions.execute_trade(
            [instruction.params() for instruction in instructions]
            )
        tx = tx_raw.buildTransaction(W3().get_tx_args())
        print(tx)
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
        try:
            sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(sentTx)
        except ValueError as e:
            if e.args[0]['code'] == 1002:
                print("Nonce Error Increasing Nonce By 1")
                tx_args = W3().get_tx_args()
                tx_args['nonce'] = W3().velasW3.eth.getTransactionCount(W3().executor_wallet) + 1
                tx = tx_raw.buildTransaction(tx_args)
                signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
                sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                self.w3.eth.wait_for_transaction_receipt(sentTx)
            else:
                print(e)
                raise Exception(f"Unexpected error with code: {e.args[0]['code']}")
        except Exception as e:
            new_instructions = self.shrink_expected_output(instructions, 0.999)
            if self.instructions_are_valid(new_instructions) and count < 2:
                self.execute_arbitrage(new_instructions, count + 1)
        
