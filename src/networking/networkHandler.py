import socket
from threading import Thread
from random import randint
import time
import struct


class NetworkHandler(Thread):
    def __init__(self, ip, port):
        # Run constructor of parent
        Thread.__init__(self)

        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def run(self):
        while True:
            # Constantly receive a message
            print('{:<21}'.format(str(time.time())), '{:<24}'.format('networkHandler'), ('Start receiving...'))
            data, addr = self.sock.recvfrom(1024)
            print('{:<21}'.format(str(time.time())), '{:<24}'.format('networkHandler'), ('Received message ' + str(data.decode) + ' from ' + str(addr)))

    def send_msg(self, msg, ip, port):
        # Send a message
        self.sock.sendto(msg, (ip, port))
        print('{:<21}'.format(str(time.time())), '{:<24}'.format('networkHandler'), ('Sent message: ' + msg))
