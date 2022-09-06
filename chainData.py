from workers.getChainData import ChainData
from time import sleep, time

def main():
    cd = ChainData()
    cd.readDataFromFile()
    cd.getDataFromChain()
    cd.writeDataToFile()
    while True:
        t0 = time()
        try:
            cd.refresh()
            cd.writeDataToFile()
        except:
            pass
        print("Time to update graph", time() - t0)
        time_to_sleep = 60
        print(f"sleeping for {time_to_sleep} seconds")
        sleep(time_to_sleep)


if __name__ == '__main__':
    main()
