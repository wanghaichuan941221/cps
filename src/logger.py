import time


class Logger:
    def __init__(self):
        self.log_on = True
        self.usr_input = ''

    def add_usr_input(self, char):
        self.usr_input += char
        print(char, end='')

    def flush_usr_input(self):
        r = self.usr_input
        self.usr_input = ''
        print()
        return r

    def log(self, src, msg):
        if self.log_on:
            print('\r{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)
            print(self.usr_input, end='')

    def print(self, msg):
        print('\r' + msg)
        print(self.usr_input, end='')
