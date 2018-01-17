import socket
from threading import Thread
import log


class NetworkHandlerTCPClient(Thread):
    def __init__(self, sip, sport):
        # Run constructor of parent
        Thread.__init__(self)

        #Store server
        self.sip = sip

        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.log('networkHandlerTCPClient', 'Now connecting...')
        self.sock.connect((sip, sport))

    def run(self):
        try:
            while True:
                # Constantly receive a message
                log.log('networkHandlerTCPClient', 'Now receiving...')
                data = self.sock.recv(1024)
                log.log('networkHandlerTCPClient', 'Received message ' + str(data) + ' from ' + str(self.sip))
        finally:
            self.sock.close()

    # msg is a bytearray
    def send_msg(self, msg):
        # Send a message
        self.sock.send(msg)
        log.log('networkHandlerTCPClient', 'Sent message: ' + str(msg))
