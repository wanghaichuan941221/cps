from threading import Thread
from time import sleep

from networking.networkHandlerUDP import NetworkHandlerUDP

from platform import node


class Heartbeat(Thread):

    def __init__(self, interval: 'float', nwh: 'NetworkHandlerUDP'):
        # Run constructor of super class
        Thread.__init__(self)

        self.interval = interval
        self.nwh = nwh
        self.running = True
        self.hb_packet = self.nwh.protocol.wrap_hb(node())

    def run(self):
        while self.running:
            self.nwh.multisend(self.hb_packet)
            sleep(self.interval)


class HeartbeatChecker(Thread):

    def __init__(self, interval: 'float', nwh: 'NetworkHandlerUDP'):
        # Run constructor of super class
        Thread.__init__(self)

        self.interval = interval
        self.nwh = nwh
        self.alive = []
        self.running = True

    def run(self):
        while self.running:
            self.alive = []
            sleep(self.interval)
