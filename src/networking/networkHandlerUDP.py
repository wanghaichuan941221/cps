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
        self.connections = dict()

    def run(self):
        while True:
            # Constantly receive a message
            log.log('networkHandlerUDP', self.getName() + ' Now receiving...')
            data, addr = self.sock.recvfrom(1024)
            log.log('networkHandlerUDP', self.getName() + ' Received message ' + str(data) + ' from ' + str(addr))
            if addr not in self.connections.keys():
                self.connections[addr] = Connection(addr[0], addr[1], self)
                self.connections[addr].send_msg('HOI BAI'.encode())

    # msg is a bytearray
    def send_msg(self, msg, ip, port):
        # Send a message
        self.sock.sendto(msg, (ip, port))
        log.log('networkHandlerUDP', self.getName() + ' Sent message: ' + str(msg))

    # msg is bytearray
    def multisend(self, msg):
        for key, conn in self.connections.items():
            conn.send_msg(msg)

class Connection:
    def __init__(self, ip, port, nwh:'NetworkHandlerUDP'):
        self.ip = ip
        self.port = port
        self.nwh = nwh

    def send_msg(self, msg):
        # Send a message
        self.nwh.send_msg(msg, self.ip, self.port)