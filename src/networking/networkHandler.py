import socket
from threading import Thread
import log


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
            log.log('networkHandler', 'Now receiving...')
            data, addr = self.sock.recvfrom(1024)
            log.log('networkHandler', 'Received message ' + str(data.decode()) + ' from ' + str(addr))

    def send_msg(self, msg, ip, port):
        # Send a message
        self.sock.sendto(msg.encode(), (ip, port))
        log.log('networkHandler', 'Sent message: ' + msg)
