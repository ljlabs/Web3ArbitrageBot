import threading


class ThreadManager:
    def __init__(self, max_threads):
        self.maxThreads = max_threads
        self.threads = []

    def execute(self, target, args):
        x = threading.Thread(target=target, args=args)
        if len(self.threads) == self.maxThreads:
            self.endOldest()
        self.threads.append(x)
        x.start()

    def endOldest(self):
        if len(self.threads) > 0:
            thread = self.threads.pop(0)
            thread.join()

    def endAll(self):
        while len(self.threads) > 0:
            self.endOldest()
