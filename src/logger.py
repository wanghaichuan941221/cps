import time
import curses

class Logger:
    def __init__(self):
        self.log_on = True

    def log(self, src, msg):
        if self.log_on:
            # window = curses.initscr()
            # y, x = window.getyx()
            # window.move(y, 0)
            print('{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)
            # window.move(y + 1, x)
            # curses.endwin()
