from const.config import network


def getMaxCircuitDepth():
    if network == "vlx":
        return 10
    elif network == "matic":
        return 7
    else:
        raise Exception("Unsupported network")


def lowLiquidityBar() -> int:
    if network == "vlx":
        return 10 * 10 ** 18
    elif network == "matic":
        return 100000 * 10 ** 18
    else:
        raise Exception("Unsupported network")


def minEdgeLiquidityTxRatio() -> int:
    if network == "vlx":
        return 0.0001
    elif network == "matic":
        return 0.001
    else:
        raise Exception("Unsupported network")


def minRoiRequirement() -> int:
    if network == "vlx":
        return 1.001
    elif network == "matic":
        return 1.001
    else:
        raise Exception("Unsupported network")


# this will return true if the reuired number of exchanges for a given network is met
# else will return false
# Params:
#   n: is the number of excahnges in a circuit
def sufficientNumberOfExchanges(n: int) -> bool:
    if network == "vlx":
        if n == 1:
            return True
    elif network == "matic":
        if n == 1:
            return True
    else:
        raise Exception("Unsupported network")
    return False


# operational
num_threads = 1
data_file_path = f"data.{network}.json"
data_refresh_file_path = f"data.refresh.{network}.json"