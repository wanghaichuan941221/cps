from threading import Thread

from networking.networkHandlerUDP import NetworkHandlerUDP


class ChinkieHandlerServer(Thread):
    def __init__(self, nwh: 'NetworkHandlerUDP'):
        # Run constructor of parent
        Thread.__init__(self)

        self.nwh = nwh

    def run(self):
        while True:
            msg = input()
            bmsg = self.nwh.protocol.wrap(b'0', msg.encode())
            self.nwh.multisend(bmsg)

    def rec_msg(self, msg, addr):
        print(str(msg, 'utf-8'))
        new_msg = self.nwh.protocol.wrap(b'0', msg)

        self.nwh.forward_exclude(new_msg, self.nwh.connections[addr])

