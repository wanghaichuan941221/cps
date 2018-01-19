import time
import curses

class Logger:
    def __init__(self):
        self.log_on = True

    def log(self, src, msg):
        if self.log_on:
            curses.initscr()
            y, x = curses.getsyx()
            curses.setsyx(y, 0)
            print('{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)
            curses.setsyx(y + 1, x)
            curses.endwin()
