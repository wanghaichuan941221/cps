from threading import Thread
from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP
from networking.inputHandler import getch

import platform

class ChinkieHandlerClient(Thread):
    def __init__(self, nwh: 'NetworkHandlerUDP', log: 'Logger'):
        # Run constructor of parent
        Thread.__init__(self)

        self.log = log
        self.nwh = nwh
        self.running = True

    def run(self):
        while self.running:
            # print(platform.node() + ': ', end='')
            msg = self.input()
            print('GOT INPUT: ', msg)

            if msg.startswith('/'):
                command = msg.split(' ')[0][1:]

                if command == 'log':
                    self.log.log_on = not self.log.log_on
                    if self.log.log_on:
                        print('Enabled logger')
                    else:
                        print('Disabled logger')
                elif command == 'exit':
                    exit()

            else:
                packet = self.nwh.protocol.wrap_msg(platform.node() + ': ' + msg)
                self.nwh.multisend(packet)

    def rec_msg(self, msg):
        print(msg)

    def input(self):
        while True:
            ch = getch()
            if ch is not None:
                if ch == '\n\r':
                    return self.log.flush_usr_input()
                self.log.add_usr_input(ch)
