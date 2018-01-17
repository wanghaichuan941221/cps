import time


log_on = True


def log(src, msg):
    if log_on:
        print('{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)
