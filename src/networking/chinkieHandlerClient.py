from threading import Thread

from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP


class ChinkieHandlerClient(Thread):
    def __init__(self, nwh: 'NetworkHandlerUDP', log: 'Logger'):
        # Run constructor of parent
        Thread.__init__(self)

        self.log = log
        self.nwh = nwh

    def run(self):
        while True:
            msg = input()

            packet = self.nwh.protocol.wrap_msg(msg)
            self.nwh.multisend(packet)

    def rec_msg(self, msg):
        print(msg)
