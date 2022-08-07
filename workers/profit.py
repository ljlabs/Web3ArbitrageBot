import threading

from handlers.pancakeSwapRouter import PancakeSwapRouter
from const.addresses import exchange_address, currency_address
from time import time


def get_most_profitable_path(token, scores):
    best_buy = None
    best_sell = None
    for k in exchange_address().keys():
        v = exchange_address()[k]
        swap = PancakeSwapRouter(v)
        swap.set_lp(token)
        try:
            price = swap.getPrice(token)
            if swap.pair_has_sufficient_liquidity(price):
                if best_buy is None or price[1] > best_buy[1][1]:
                    best_buy = [k, price]
        except Exception as e:
            # print(e)
            pass
    if best_buy is None:
        return 0, []
    for k in exchange_address().keys():
        v = exchange_address()[k]
        swap = PancakeSwapRouter(v)
        swap.set_lp(token)
        try:
            price = swap.getPriceReverse(token, best_buy[1][1])
            if k != best_buy[0] and swap.pair_has_sufficient_liquidity(price):
                if best_sell is None or price[1] > best_sell[1][1]:
                    best_sell = [k, price]
        except Exception as e:
            # print(e)
            pass
    if best_sell is None:
        return 0, []

    profit = best_sell[1][1] / best_buy[1][0]

    scores.append([
        profit,
        [best_buy, best_sell],
        token
    ])


def get_most_profitable_token_and_path():
    threads = list()
    scores = []
    t0 = time()
    for key in currency_address().keys():
        if key != "base":
            x = threading.Thread(target=get_most_profitable_path, args=(key,scores,))
            threads.append(x)
            x.start()

    for index, thread in enumerate(threads):
        thread.join()

    print(time() - t0)
    scores = sorted(scores, key=lambda y: y[0])
    if len(scores) == 0:
        return []
    ret = scores[-1]
    scores = []
    return ret
