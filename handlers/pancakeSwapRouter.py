import json

from factory import w3
from const.pancakeRouter import abi
from const.addresses import currency_address
from factory.w3 import W3
from handlers.pancakeSwapFactory import PancakeSwapFactory
from handlers.pancakeSwapLP import PancakeSwapLP


class PancakeSwapRouter:
    def __init__(self, address):
        self.lp = None
        self.w3 = W3().getWeb3()
        self.router = self.w3.eth.contract(address=address, abi=abi)

    def get_factory(self) -> str:
        return self.router.functions.factory().call()

    def set_lp(self, token):
        factory = PancakeSwapFactory(self.get_factory())
        self.lp: PancakeSwapLP = factory.getLP(currency_address()["base"], currency_address()[token])

    def pair_has_sufficient_liquidity(self, price_prediction) -> bool:
        reserves = self.lp.getReserves()
        reserves.pop()
        if price_prediction[0] > price_prediction[1] and reserves[0] < reserves[1]:
            holder = reserves.pop(0)
            reserves.append(holder)
        if price_prediction[0] < price_prediction[1] and reserves[0] > reserves[1]:
            holder = reserves.pop(0)
            reserves.append(holder)
        ratios = [price_prediction[i] / reserves[i] for i in [0, 1]]
        if min(ratios) < 0.1:
            return True
        return False

    def getPrice(self, token):
        return self.router.functions.getAmountsOut(
            int("120" + ("0" * 18)),
            [currency_address()["base"], currency_address()[token]]
        ).call()

    def getPriceReverse(self, token, price):
        return self.router.functions.getAmountsOut(
            int(price),
            [currency_address()[token], currency_address()["base"]]
        ).call()

    def swapExactTokensForTokens(self, amountIn, amountOutMin, path, to, deadline):
        tx = self.router.functions.swapExactTokensForTokens(
            amountIn,
            amountOutMin,
            path,
            to,
            deadline
        ).buildTransaction(W3().get_tx_args())
        print(tx)
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
        try:
            sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(sentTx)
            return self.w3.eth.get_transaction_receipt(sentTx)
        except ValueError as e:
            if e.args[0]['code'] == 1002:
                print("Nonce Error Increasing Nonce By 1")
                tx_args = W3().get_tx_args()
                tx_args['nonce'] = W3().velasW3.eth.getTransactionCount(W3().executor_wallet) + 1

                tx = self.router.functions.swapExactTokensForTokens(
                    amountIn,
                    amountOutMin,
                    path,
                    to,
                    deadline
                ).buildTransaction(tx_args)
                signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=W3().get_private_key())
                sentTx = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                self.w3.eth.wait_for_transaction_receipt(sentTx)
                return self.w3.eth.get_transaction_receipt(sentTx)
            else:
                print(e)
                raise e

    def getAmountsOut(self, amountIn: int, path: list[str]) -> list[int]:
        return self.router.functions.getAmountsOut(int(amountIn), path).call()
