from threading import Thread


class ChinkieHandlerClient(Thread):
    def __init__(self, nwh):
        # Run constructor of parent
        Thread.__init__(self)

        self.nwh = nwh

    def run(self):
        while True:
            msg = input()
            bmsg = self.nwh.protocol.wrap(b'\x00', msg.encode())
            self.nwh.multisend(bmsg)

    def rec_msg(self, msg, addr):
        print(str(msg, 'utf-8'))
