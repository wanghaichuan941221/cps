from threading import Thread
from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP

import platform

class ChinkieHandlerClient(Thread):
    def __init__(self, nwh: 'NetworkHandlerUDP', log: 'Logger'):
        # Run constructor of parent
        Thread.__init__(self)

        self.log = log
        self.nwh = nwh

    def run(self):
        while True:
            print(platform.node() + ': ', end='')
            msg = input()

            if msg.startswith('/'):
                command = msg.split(' ')[0][1:]

                if command == 'log':
                    self.log.log_on = not self.log.log_on
                    if self.log.log_on:
                        print('Enabled logger')
                    else:
                        print('Disabled logger')
            else:
                packet = self.nwh.protocol.wrap_msg(platform.node() + ': ' + msg)
                self.nwh.multisend(packet)

    def rec_msg(self, msg):
        print(msg)
