import time


def log(src, msg):
    print('{:<21}'.format(str(time.time())), '{:<24}'.format(src), msg)
