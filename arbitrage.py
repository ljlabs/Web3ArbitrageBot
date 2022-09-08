from decimal import Decimal
from handlers.arbitrageContract import ArbitrageContract
from handlers.threadmanager import ThreadManager
from model.tradeInstructions import TradeInstruction

from workers.arbitrage import execute_arbitrage, getOptimalAmount, should_execute, should_execute_using_contract, simulate_execute_arbitrage
from workers.getChainData import ChainData
from workers.graph import Graph
from const.config import arbitrage_contract_address
import sys

def trade_with_contract_threadeable(op, graph):
    best_input_amount = graph.tradeSize.rawValue
    trade_instructions = TradeInstruction.transform(op)
    trade_instructions[0].inpt = best_input_amount
    arb_contract = ArbitrageContract()
    min_output = arb_contract.get_expected_output(trade_instructions)
    while should_execute_using_contract(min_output):
        print("executing a trade")
        arb_contract.execute_arbitrage(trade_instructions, min_output)
        graph.update_trade_size()
        print("=" * 10)
        min_output = arb_contract.get_expected_output(trade_instructions)


def trade_with_contract(circuits, graph):
    num_threads = 5
    tm = ThreadManager(num_threads)
    for op in circuits:
        tm.execute(target=trade_with_contract_threadeable, args=(op, graph,))
    tm.endAll()
            


def trade_without_contract(circuits, graph):
    for op in circuits:
        best_input_amount = getOptimalAmount(graph, op)
        if best_input_amount is not None:
            print(f"the best trade size is {best_input_amount}, graph.tradeSize = {graph.tradeSize.value}")
        if best_input_amount is None:
            best_input_amount = graph.tradeSize.rawValue
        if best_input_amount < graph.tradeSize.rawValue * Decimal(0.05):
            best_input_amount = int(graph.tradeSize.rawValue * Decimal(0.05))
        min_output = simulate_execute_arbitrage(graph, op, best_input_amount)
        if should_execute(op, min_output):
            print("executing a trade")
            execute_arbitrage(op, min_output, best_input_amount)
            graph.update_trade_size()
            print("=" * 10)




def main():
    # init phase
    cd = ChainData()
    graph = Graph()
    cd.readDataFromFile()
    approved_list_only = False
    if "-f" in sys.argv or "-fastPaths" in sys.argv:
        approved_list_only = True
    while True:
        graph.buildGraphFromChainData(cd.pairs, approved_list_only)
        graph.findMostProfitableCircuit()

        # execute arbitrage trades
        circuits = []
        # maxOps = 129
        # if len(graph.options) > maxOps:
        #     circuits = [
        #         graph.options[i] for i in range(
        #             len(graph.options) - 1,
        #             len(graph.options) - (maxOps + 1),
        #             -1
        #         )
        #     ]
        # else:
        circuits = graph.options
        print(f"Found {len(circuits)} paths")
        # this is to switch between simplistic and complex trading conditions
        if arbitrage_contract_address is None:
            trade_without_contract(circuits, graph)
        else:
            trade_with_contract(circuits, graph)

        try:
            print("writing update data to file")
            cd.write_refresh_data(graph.activeLPAddrs)
            cd.readDataFromFile()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':

    if "-h" in sys.argv or "-help" in sys.argv:
        print ("""
This is the help menu of the arbitrage bot:
    -h or -help prints this help menu
    -f or -fastPaths filters the universe of possible arbitrage paths to only thos approved in the adresses.py file         

**If no params are supplied the bot will operate as usual**
""")
    else:
        while True:
            try:
                main()
            except:
                pass
