import time


class Timer:

    def __init__(self, sleep):

        self.sleep = sleep
        self.finishTime = time.time() + sleep
        self.doneProcent = False
        self.done = False

    def update(self):

        self.doneProcent = (self.finishTime - time.time()) / self.sleep * 100

        if self.doneProcent >= 100:
            self.done = True

        if time.time() >= self.finishTime:
            self.done = True