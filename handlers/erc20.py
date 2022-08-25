import json

from const.config import trade_volume_limiter
from const.erc20 import abi
from factory.w3 import W3

decimals_cache = {} # decimals never change, it makes no sense not to cache


class ERC20:
    def __init__(self, address: str):
        self.w3 = W3().getWeb3()
        self.token = self.w3.eth.contract(address=address, abi=abi)
        self.address = address

    def approve(self, address, amount):
        tx = self.token.functions.approve(address, amount).buildTransaction(W3().get_tx_args())
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
        try:
            sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(sentTx)
        except ValueError as e:
            if e.args[0]['code'] == 1002:
                print("Nonce Error Increasing Nonce By 1")
                tx_args = W3().get_tx_args()
                tx_args['nonce'] = W3().velasW3.eth.getTransactionCount(W3().executor_wallet) + 1

                tx = self.token.functions.approve(address, amount).\
                    buildTransaction(tx_args)
                signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
                sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                self.w3.eth.wait_for_transaction_receipt(sentTx)
            else:
                print(e)
                raise e

        return sentTx

    def getBalance(self, address):
        return int(self.token.functions.balanceOf(address).call() * trade_volume_limiter)

    def getDecimals(self):
        if self.address not in decimals_cache:
            decimals_cache[self.address] = self.token.functions.decimals().call()
        return decimals_cache[self.address]
