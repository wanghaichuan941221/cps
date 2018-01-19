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
        self.alive = set()
        self.running = True

    def run(self):
        while self.running:
            self.alive = set()
            sleep(self.interval)
            self.nwh.remove_dead_clients(self.alive)

    def add_alive(self, key):
        self.alive.add(key)

    def rec_hb(self, name, addr):
        try:
            self.nwh.get_connection(addr)
        except KeyError:
            self.nwh.add_connection(addr[0], addr[1], name)
        self.alive.add(addr)
