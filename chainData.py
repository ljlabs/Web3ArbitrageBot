from workers.getChainData import ChainData
from time import sleep, time

def main():
    cd = ChainData()
    # cd.readDataFromFile()
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
        print("sleeping for 0.1 seconds")
        sleep(0.1)


if __name__ == '__main__':
    main()
