from threading import Thread
from logger import Logger
from networking.networkHandlerUDP import NetworkHandlerUDP

import platform
import os


class ChinkieHandlerServer(Thread):
    def __init__(self, nwh: 'NetworkHandlerUDP', log: 'Logger'):
        # Run constructor of parent
        Thread.__init__(self)

        self.log = log
        self.nwh = nwh

    def run(self):
        while True:
            # print(platform.node() + ': ', end='')
            msg = input()

            if msg.startswith('/'):
                self.command(msg)
            else:
                self.log.print('Type /help for a list of commands.')

    def rec_msg(self, msg, addr):
        self.log.print(msg)

        packet = self.nwh.protocol.wrap_msg(msg)
        self.nwh.forward_exclude(packet, self.nwh.connections[addr])

        split_msg = msg.split(' ')
        if len(split_msg[0]) > 0:
            if split_msg[0] == '/remote' or split_msg[0] == '/r':
                if platform.node() == split_msg [1]:
                    comm = ''
                    for i in range(2, len(split_msg)):
                        comm = comm + split_msg[i]

                    self.command(comm.strip())

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
            #TODO stop motors
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
            else:
                self.nwh.multisend(self.nwh.protocol.wrap_msg(line))
        elif command == 'help':
            self.log.print('COMMANDS:')
            self.log.print('  /log or /      toggle logging')
            self.log.print('     Usage: /log(/)')
            self.log.print('  /exit          exit program')
            self.log.print('     Usage: /exit')
            self.log.print('  /connections   list the current connections')
            self.log.print('     Usage: /connections')
            self.log.print('  /remote or /r  execute a command on any other connected device')
            self.log.print('     Usage: /remote(/r) <host_name> <command> [<arguments>]')
            self.log.print('  /help          show list of commands')
            self.log.print('     Usage: /help')
        else:
            self.log.print('Not a valid command. Type /help for a list of commands.')

