import socket
from threading import Thread
import log


class NetworkHandlerUDP(Thread):
    def __init__(self, ip, port):
        # Run constructor of parent
        Thread.__init__(self)

        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def run(self):
        while True:
            # Constantly receive a message
            log.log('networkHandlerUDP', 'Now receiving...')
            data, addr = self.sock.recvfrom(1024)
            log.log('networkHandlerUDP', 'Received message ' + str(data) + ' from ' + str(addr))

    # msg is a bytearray
    def send_msg(self, msg, ip, port):
        # Send a message
        self.sock.sendto(msg, (ip, port))
        log.log('networkHandlerUDP', 'Sent message: ' + str(msg))
