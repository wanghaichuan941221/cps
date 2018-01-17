import socket
from threading import Thread
import log


class NetworkHandlerTCPServer(Thread):
    def __init__(self, ip, port):
        # Run constructor of parent
        Thread.__init__(self)

        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(1)

    def run(self):
        conn, addr = self.sock.accept()
        try:
            while True:
                # Constantly receive a message
                log.log('networkHandlerTCPServer', 'Now receiving...')
                data = conn.recv(1024)
                log.log('networkHandlerTCPServer', 'Received message ' + str(data) + ' from ' + str(addr))
        finally:
            conn.close()

    # msg is a bytearray
    def send_msg(self, msg):
        # Send a message
        self.sock.send(msg)
        log.log('networkHandlerTCPServer', 'Sent message: ' + str(msg))
