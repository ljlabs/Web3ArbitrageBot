from factory import w3
from const.pancakeFactory import abi
from factory.w3 import W3
from handlers.pancakeSwapLP import PancakeSwapLP
from typing import List


class PancakeSwapFactory:
    def __init__(self, address):
        self.w3 = W3().getWeb3()
        self.factory = self.w3.eth.contract(address=address, abi=abi)

    def getLP(self, a, b) -> PancakeSwapLP:
        lp_address = self.factory.functions.getPair(a, b).call()
        return PancakeSwapLP(lp_address)

    def getNumberOfPairs(self) -> int:
        return self.factory.functions.allPairsLength().call()

    def getPair(self, i) -> PancakeSwapLP:
        return PancakeSwapLP(self.factory.functions.allPairs(i).call())
