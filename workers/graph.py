from __future__ import annotations

from decimal import Decimal
from turtle import update
from typing import Union
from const.addresses import currency_address
from const.controlls import getMaxCircuitDepth, lowLiquidityBar, sufficientNumberOfExchanges, \
    maxEdgeLiquidityTxRatio
from factory.w3 import W3
from handlers.BigIntDecimals import BigIntDecimals
from handlers.arbitrageContract import ArbitrageContract
from handlers.erc20 import ERC20
from const.config import arbitrage_contract_address

already_removed = {}

# # this is done earlier now
# def isLowLiquidity(pair):
#     bigger_than = lowLiquidityBar()
#     if pair[0] < bigger_than or pair[1] < bigger_than:
#         return True
#     return False


# need new filters
def isValidPair(pair):
    # if isLowLiquidity(pair):
    #     return False
    return True


def isFinalPath(path) -> bool:
    if len(path) <= 2:
        return False
    start = path[0].split("_")[0]
    end = path[-1].split("_")[1]
    if start != end:
        return False
    ex_prev = path[0].split("_")[2]
    num_exchanges = 1
    for step in path[1:]:
        if step.split("_")[2] != ex_prev:
            num_exchanges += 1
        ex_prev = step.split("_")[2]
    if not sufficientNumberOfExchanges(num_exchanges):
        return False
    return True


class Graph:
    graph: dict[str, list[str]] = {}
    edges: dict[str, list[str] | list[int]] = {}
    maxDepth = getMaxCircuitDepth()
    swaps = []
    tradeSize = None
    activeLPAddrs: str = []
    options = []
    chainData: dict[str, list[dict[str, list[str] | list[int]]]] = {}
    token_address_to_decimal = {}

    def __init__(self) -> None:
        if arbitrage_contract_address is not None:
            self.tradeSize = BigIntDecimals(
                ERC20(currency_address()["base"]).getBalance(
                    arbitrage_contract_address),
                ERC20(currency_address()["base"]).getDecimals()
            )
        else:
            self.tradeSize = BigIntDecimals(
                ERC20(currency_address()["base"]).getBalance(
                    W3().executor_wallet),
                ERC20(currency_address()["base"]).getDecimals()
            )

    def update_trade_size(self):
        base_currency = ERC20(currency_address()["base"])
        if arbitrage_contract_address is not None:
            self.tradeSize = BigIntDecimals(
                base_currency.getBalance(arbitrage_contract_address),
                self.token_address_to_decimal[currency_address()["base"]]
            )
        else:
            self.tradeSize = BigIntDecimals(
                base_currency.getBalance(W3().executor_wallet),
                self.token_address_to_decimal[currency_address()["base"]]
            )

    def filter_bad_chain_data(self):
        for swap in self.chainData:
            i = 0
            while i < len(self.chainData[swap]):
                was_popped = False
                if self.chainData[swap][i] == 0:
                    self.chainData[swap].pop(i)
                    was_popped = True
                if not was_popped:
                    a = BigIntDecimals(self.chainData[swap][i]["reserves"][0],
                                       self.chainData[swap][i]["decimals"][0]
                                       )
                    b = BigIntDecimals(self.chainData[swap][i]["reserves"][1],
                                       self.chainData[swap][i]["decimals"][1]
                                       )
                    if a < lowLiquidityBar() or b < lowLiquidityBar():
                        self.chainData[swap].pop(i)
                        was_popped = True
                if not was_popped:
                    i += 1

    def buildGraphFromChainData(self, data: dict[str, list[dict[str, list[str] | list[int]]]]):
        self.graph = {}
        self.edges = {}
        self.swaps = []
        self.token_address_to_decimal = data["token_address_to_decimal"]
        del data["token_address_to_decimal"]
        self.chainData = data
        self.filter_bad_chain_data()
        self.activeLPAddrs = []
        for swap in self.chainData:
            self.swaps.append(swap)
            for vert in self.chainData[swap]:
                a = vert["addresses"][0]
                b = vert["addresses"][1]
                reserves = [
                    BigIntDecimals(vert["reserves"][i], vert["decimals"][i])
                    for i in [0, 1]
                ]
                vert["reserves"] = reserves
                if isValidPair(vert["reserves"]):
                    self.activeLPAddrs.append({
                        "lp-addr": vert["address"],
                        "router-addr": swap,
                        "idx": vert["idx"]
                    })
                    if a not in self.graph:
                        self.graph[a] = [b]
                        self.edges[f"{a}_{b}_{swap}"] = vert["reserves"]
                    else:
                        if b not in self.graph[a]:
                            self.graph[a].append(b)
                            self.edges[f"{a}_{b}_{swap}"] = vert["reserves"]
                    if b not in self.graph:
                        self.graph[b] = [a]
                        reserves = [vert["reserves"][1], vert["reserves"][0]]
                        self.edges[f"{b}_{a}_{swap}"] = reserves
                    else:
                        if a not in self.graph[b]:
                            self.graph[b].append(a)
                            reserves = [vert["reserves"]
                                        [1], vert["reserves"][0]]
                            self.edges[f"{b}_{a}_{swap}"] = reserves

    def findMostProfitableCircuit(self):
        base = currency_address()["base"]
        self.options = []
        resp = self.transverse(base, base, [], self.tradeSize, [])
        return resp

    def isValidSwap(self, at, to, swap):
        return f"{at}_{to}_{swap}" in self.edges

    def getEdgeValue(self, at, to, at_tokens, swap) -> Union[str, int]:
        reserve = self.edges[f"{at}_{to}_{swap}"]
        con = reserve[0] * reserve[1]
        out = reserve[1].value - con / (at_tokens + reserve[0])
        out *= Decimal(0.80)  # fees
        # if out <= 0:
        #     raise Exception(f"How is there no edge value here:  {at, to, at_tokens}")
        return f"{at}_{to}_{swap}", out

    def stopUpdatingLowLP(self, edge):
        global already_removed
        at, to, swap = edge.split("_")
        at_to = f"{at}_{to}"
        lp_address = ""
        if at_to not in already_removed:
            # get lp address
            for lp_data in self.chainData[swap]:
                if at in lp_data["addresses"] and to in lp_data["addresses"]:
                    lp_address = lp_data["address"]
                    already_removed[at_to] = True
                    break
        if lp_address not in already_removed:
            # remove lp address from activeLPAddrs
            for i in range(len(self.activeLPAddrs)):
                if self.activeLPAddrs[i]["lp-addr"] == lp_address:
                    self.activeLPAddrs.pop(i)
                    already_removed[lp_address] = True
                    break

    def isEdgeValueLiquidityIsSafe(self, edge, tokens) -> str:
        reserve = self.edges[edge]
        constant = reserve[0] * reserve[1]
        output = reserve[1].value - constant / (tokens + reserve[0])
        is_safe = output / reserve[1] < maxEdgeLiquidityTxRatio() and \
            tokens / reserve[0] < maxEdgeLiquidityTxRatio()
        if not is_safe:
            self.stopUpdatingLowLP(edge)
        return is_safe

    def transverse(self, base, at, path, num_tokens, visited):
        if len(path) > 0 and at == base:
            return path, num_tokens
        if len(path) == self.maxDepth:
            return path, num_tokens

        best_output_amount = 0
        best_path = []
        for swap in self.swaps:
            for neighbour in self.graph.get(at, []):
                if (neighbour == base or neighbour not in visited) and self.isValidSwap(at, neighbour, swap):
                    next_path_step, output_token_amount = self.getEdgeValue(
                        at, neighbour, num_tokens, swap)
                    if output_token_amount > 0 and self.isEdgeValueLiquidityIsSafe(next_path_step, num_tokens):
                        new_path, paths_output_amount = self.transverse(
                            base,
                            neighbour,
                            path + [next_path_step],
                            output_token_amount,
                            visited + [at]
                        )
                        if isFinalPath(
                                new_path) and paths_output_amount > best_output_amount and new_path not in self.options:
                            self.options.append(new_path)
                            best_output_amount = paths_output_amount
                            best_path = new_path

        return best_path, best_output_amount
