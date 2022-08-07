from typing import List, Mapping, Any

from factory import w3
from const.pancakeLP import abi
from factory.w3 import W3


class PancakeSwapLP:
    def __init__(self, address):
        self.w3 = W3().getWeb3()
        self.lp = self.w3.eth.contract(address=address, abi=abi)
        self.address = address

    def getReserves(self) -> List[int]:
        return self.lp.functions.getReserves().call()

    def getReserveAddresses(self) -> List[str]:
        return [self.lp.functions.token0().call(), self.lp.functions.token1().call()]

    def asDict(self) -> dict[str, List[Any]]:
        return {
            "addresses": self.getReserveAddresses(),
            "reserves": self.getReserves(),
            "address": self.address
        }
