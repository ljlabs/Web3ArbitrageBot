from const.config import network
from handlers.BigIntDecimals import BigIntDecimals


def getMaxCircuitDepth():
    if network == "vlx":
        return 10
    elif network == "matic":
        return 7
    else:
        raise Exception("Unsupported network")


def lowLiquidityBar() -> int:
    if network == "vlx":
        return BigIntDecimals(10, 0)
    elif network == "matic":
        return BigIntDecimals(100000, 0)
    else:
        raise Exception("Unsupported network")


def maxEdgeLiquidityTxRatio() -> int:
    if network == "vlx":
        return BigIntDecimals(0.09, 0)
    elif network == "matic":
        return BigIntDecimals(0.001, 0)
    else:
        raise Exception("Unsupported network")


def minRoiRequirement() -> int:
    if network == "vlx":
        return BigIntDecimals(1.0001, 0)
    elif network == "matic":
        return BigIntDecimals(1.001, 0)
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