from threading import Thread
from logger import Logger
from image.imageProcessor import ImageProcessor
from networking.networkHandlerUDP import NetworkHandlerUDP
import platform
import os


class ChinkieHandlerClient(Thread):
    """The ChinkieHandlerClient class is used to collect user input and process it correctly. Besides this, the class
    also handles any remote commands that are received by the network handler.
    """

    def __init__(self, nwh: 'NetworkHandlerUDP', img_proc: 'ImageProcessor', log: 'Logger'):
        """Constructor of the ChinkieHandlerClient class, which is an extension of the threading.Thread class."""

        # Run the constructor of parent.
        Thread.__init__(self)

        # Create a logger, network handler and set the "running" variable to be True.
        self.log = log
        self.img_proc = img_proc
        self.nwh = nwh
        self.running = True

    def run(self):
        """Override the threading.Thread.run() function. Called when thread is created."""

        # Start a loop.
        while self.running:
            # Read the system input from user and block until a return/newline.
            msg = input()
            # Check if the message is a command (starts with "/").
            if msg.startswith('/'):
                # If the message is a command, call the command() function to execute the command.
                self.command(msg)
            else:
                # If the message is not a command, notify the user.
                self.log.print('Type /help for a list of commands.')

    def rec_msg(self, msg):
        """When a message is received by the network handler and the protocol indicates that it is a command message,
        the protocol calls this function.
        """

        # Print the received message
        self.log.print(msg)

        # Split the message on space characters to separate words, commands and arguments.
        split_msg = msg.split(' ')
        # Check if the message contains anything at all.
        if len(split_msg[0]) > 0:
            # Check if the received message was a "remote" command.
            if split_msg[0] == '/remote' or split_msg[0] == '/r':
                # Check if the target for the remote command is this device.
                if platform.node() == split_msg[1]:
                    # Reconstruct the command.
                    comm = ''
                    for i in range(2, len(split_msg)):
                        comm = comm + ' ' + split_msg[i]
                    # Execute the command.
                    self.command(comm.strip())

    def command(self, line):
        """If a command is received, either through user input or by the network handler as a remote command, this
        function checks and executes the command.
        """

        # Split the message on space characters to separate words, commands and arguments.
        split_msg = line.split(' ')

        # Check if the first word in the command contains at least 2 characters.
        if len(split_msg[0]) > 1:
            # If the first word contains at least 2 characters, remove the / character.
            command = split_msg[0][1:]
        else:
            # Else the command word is empty.
            command = ''

        # Check the type of the command, and act accordingly.
        if command == '' or command == 'log':
            # If the command is empty or "log", toggle the logging feature of the console.
            self.log.log_on = not self.log.log_on
            if self.log.log_on:
                self.log.print('Enabled logger')
            else:
                self.log.print('Disabled logger')
        elif command == 'exit':
            # If the command is "exit", shut down the system. //TODO Make it neater.
            self.log.print('Exiting...')
            os._exit(0)
        elif command == 'connections':
            # If the command is "connections", show a list of known connections.
            conns = self.nwh.connections.copy().values()
            self.log.print('CONNECTIONS:')
            for conn in conns:
                self.log.print('  ' + conn.name + ' (' + conn.ip + ':' + str(conn.port) + ')')
        elif command == 'r' or command == 'remote':
            # If the command is "r" or "remote", send the command to all known connections.
            if len(split_msg) < 2:
                self.log.print('USAGE:')
                self.log.print('  /remote <host_name> <command> [<arguments>] ')
            else:
                self.nwh.multisend(self.nwh.protocol.wrap_msg(line))
        elif command == 'img':
            self.img_proc.toggle_write_img()
            if self.img_proc.write_img:
                self.log.print('Enabled image writing')
            else:
                self.log.print('Disabled image writing')
        elif command == 'help':
            # If the command is "help", show a list of possible commands and their usages.
            self.log.print('COMMANDS:')
            self.log.print('  /log or /      toggle logging')
            self.log.print('     Usage: /log(/)')
            self.log.print('  /exit          exit program')
            self.log.print('     Usage: /exit')
            self.log.print('  /connections   list the current connections')
            self.log.print('     Usage: /connections')
            self.log.print('  /remote or /r  execute a command on any other connected device')
            self.log.print('     Usage: /remote(/r) <host_name> <command> [<arguments>]')
            self.log.print('  /img           toggles the writing of images')
            self.log.print('     Usage: /img')
            self.log.print('  /help          show list of commands')
            self.log.print('     Usage: /help')
        else:
            # If the command is not recognized, notify the user.
            self.log.print('Not a valid command. Type /help for a list of commands.')
