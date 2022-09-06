from __future__ import annotations
import json

from const.addresses import exchange_address
from handlers.pancakeSwapFactory import PancakeSwapFactory
from handlers.pancakeSwapLP import PancakeSwapLP
from handlers.pancakeSwapRouter import PancakeSwapRouter
from handlers.threadmanager import ThreadManager
from const.controlls import num_threads, data_file_path, data_refresh_file_path
import math


class ChainData:
    pairs: dict[str, list[dict[str, list[str] | list[int]]]] = []
    token_address_to_decimal: dict[str, int] = []

    def getPair(self, swap: str, i: int, factory: PancakeSwapFactory):
        self.pairs[swap][i] = factory.getPair(i).asDict()
        self.pairs[swap][i].update({"idx": i})

    def getDataFromChain(self) -> list[dict[str, list[str] | list[int]]]:
        print("reading data from chain")
        exchanges = exchange_address()
        tm = ThreadManager(num_threads)
        for swap in exchanges:
            known_pairs = len(self.pairs.get(exchanges[swap], []))
            print(swap, "known pairs:", known_pairs)
            router = PancakeSwapRouter(exchanges[swap])
            factory = PancakeSwapFactory(router.get_factory())
            n = factory.getNumberOfPairs()
            print("found pairs:", n)
            self.pairs[exchanges[swap]] = [0] * n
            # skips existing pairs on initial run
            if n > known_pairs:
                for i in range(known_pairs, n):
                    if (math.floor((i / n) * 1000) % 10 == 0):
                        print(f"Exchange({swap}) {(i/n)*100}% complete")
                    tm.execute(target=self.getPair, args=(exchanges[swap], i, factory,))
                    # if i % 1000 == 0:
                    #     tm.endAll()
                    #     self.writeDataToFile()
                tm.endAll()

    def refresh(self):
        lp_addresses = {}
        print("reading refresh data from file")
        with open(data_refresh_file_path, "r") as f:
            file = f.read()
            lp_addresses = json.loads(file)
        print("refreshing chain data")
        def update(_addr):
            self.pairs[_addr["router-addr"]][_addr["idx"]].update(
                PancakeSwapLP(_addr["lp-addr"]).asDict()
            )
        tm = ThreadManager(num_threads)
        for i, addr in enumerate(lp_addresses):
            tm.execute(target=update, args=(addr,))
        tm.endAll()

    def write_refresh_data(self, lp_addresses):
        with open(data_refresh_file_path, "w") as f:
            f.write(json.dumps(lp_addresses))

    def readDataFromFile(self):
        print("reading data from file")
        with open(data_file_path, "r") as f:
            file = f.read()
            self.pairs = json.loads(file)

    def getTokenAddressToDecimals(self):
        token_address_to_decimal = {}
        for swap in self.pairs:
            if swap != "token_address_to_decimal":
                for pair in self.pairs[swap]:
                    if pair != 0:
                        addresses = pair["addresses"]
                        decimals = pair["decimals"]
                        token_address_to_decimal[addresses[0]] = decimals[0]
                        token_address_to_decimal[addresses[1]] = decimals[1]
        return token_address_to_decimal

    def writeDataToFile(self):
        print("writing data to file")
        self.pairs["token_address_to_decimal"] = self.getTokenAddressToDecimals()

        with open(data_file_path, "w") as f:
            f.write(json.dumps(self.pairs))
