from threading import Thread
from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP

import platform
import os

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
            msg = input()

            if msg.startswith('/'):
                self.command(msg)
            else:
                self.log.print('Type /help for a list of commands')

    def rec_msg(self, msg):
        self.log.print(msg)

    def command(self, line):
        split_msg = line.split(' ')

        if len(split_msg[0]) > 1:
            command = split_msg[0][1:]
        else:
            command = ''


        if command == '' or command == 'log':
            self.log.log_on = not self.log.log_on
            if self.log.log_on:
                self.log.print('Enabled logger')
            else:
                self.log.print('Disabled logger')
        elif command == 'exit':
            self.log.print('Exiting...')
            os._exit(0)
        elif command == 'connections':
            conns = self.nwh.connections.copy().values()
            self.log.print('CONNECTIONS:')
            for conn in conns:
                self.log.print('  ' + conn.name + ' (' + conn.ip + ':' + str(conn.port) + ')')
        elif command == 'r' or command == 'remote':
            if len(split_msg) < 2:
                self.log.print('USAGE:')
                self.log.print('  /remote <host_name> <command> [<arguments>] ')
            #TODO implement dis shiit

        elif command == 'help':
            self.log.print('COMMANDS:')
            self.log.print('  /log or /      toggle logging')
            self.log.print('  /exit          exit program')
            self.log.print('  /connections   list the current connections')
            self.log.print('  /remote or /r  execute a command on a connected device')
            self.log.print('  /help          show list of commands')
