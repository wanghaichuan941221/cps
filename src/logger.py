import time


class Logger:
    def __init__(self):
        self.log_on = True

    def log(self, src, msg):
        if self.log_on:
            print('\r{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)
