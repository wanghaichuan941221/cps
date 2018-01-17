from threading import Thread
from networking.networkHandlerUDP import NetworkHandlerUDP


class ChinkieClient(Thread):
    def __init__(self, nwh):
        # Run constructor of parent
        Thread.__init__(self)

        self.nwh = nwh

    def run(self):
        while True:
            msg = input()
            bmsg = msg.encode()
            self.nwh.multisend(bmsg)
