from threading import Thread

from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP


class ChinkieHandlerServer(Thread):
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

    def rec_msg(self, msg, addr):
        print(msg)

        packet = self.nwh.protocol.wrap_msg(msg)
        self.nwh.forward_exclude(packet, self.nwh.connections[addr])

