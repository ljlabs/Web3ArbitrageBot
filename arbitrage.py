from decimal import Decimal

from workers.arbitrage import execute_arbitrage, getOptimalAmount, should_execute, simulate_execute_arbitrage
from workers.getChainData import ChainData
from workers.graph import Graph


def main():
    # init phase
    cd = ChainData()
    cd.readDataFromFile()
    graph = Graph()
    while True:
        graph.buildGraphFromChainData(cd.pairs)
        graph.findMostProfitableCircuit()

        # execute arbitrage trades
        operations = []
        maxOps = 129
        if len(graph.options) > maxOps:
            operations = [
                graph.options[i] for i in range(
                    len(graph.options) - 1,
                    len(graph.options) - (maxOps + 1),
                    -1
                )
            ]
        else:
            operations = graph.options
        for op in operations:
            best_input_amount = getOptimalAmount(graph, op)
            if best_input_amount is not None:
                print(f"the best trade size is {best_input_amount}, graph.tradeSize = {graph.tradeSize.value}")
            if best_input_amount is None:
                best_input_amount = graph.tradeSize.rawValue
            if best_input_amount < graph.tradeSize.rawValue * Decimal(0.01):
                best_input_amount = int(graph.tradeSize.rawValue * Decimal(0.1))
            min_output = simulate_execute_arbitrage(graph, op, best_input_amount)
            if should_execute(op, min_output):
                print("executing a trade")
                execute_arbitrage(op, min_output, best_input_amount)
                graph.update_trade_size()
                print("=" * 10)
        try:
            print("writing update data to file")
            cd.write_refresh_data(graph.activeLPAddrs)
            cd.readDataFromFile()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            pass
