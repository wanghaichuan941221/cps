import socket
from threading import Thread
import log


class NetworkHandlerUDP(Thread):
    def __init__(self, port):
        # Run constructor of parent
        Thread.__init__(self)

        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.connections = dict()

    def run(self):
        while True:
            # Constantly receive a message
            log.log('networkHandlerUDP', self.getName() + ' Now receiving...')
            data, addr = self.sock.recvfrom(1024)

            protocol.decide()
            log.log('networkHandlerUDP', self.getName() + ' Received message ' + str(data) + ' from ' + str(addr))

            if addr not in self.connections.keys():
                self.connections[addr] = Connection(addr[0], addr[1], self)
                rmsg = str(self.connections[addr]) + ' acknowledged'
                self.connections[addr].send_msg(rmsg.encode())

    # msg is bytes
    def send_msg(self, msg, ip, port):
        # Send a message
        self.sock.sendto(msg, (ip, port))
        log.log('networkHandlerUDP', self.getName() + ' Sent message ' + str(msg) + ' to ' + str((ip, port)))

    # msg is bytes
    def multisend(self, msg):
        for key, conn in self.connections.items():
            conn.send_msg(msg)

    # msg is bytes
    def forward_exclude(self, msg, not_conn):
        for key, conn in self.connections.items():
            if not not_conn == conn:
                conn.send_msg(msg)

class Connection:
    def __init__(self, ip, port, nwh:'NetworkHandlerUDP'):
        self.ip = ip
        self.port = port
        self.nwh = nwh

    def send_msg(self, msg):
        # Send a message
        self.nwh.send_msg(msg, self.ip, self.port)

    def __str__(self):
        return 'Connection(' + self.ip + ', ' + str(self.port) + ')'

    def __eq__(self, other):
        return (self.ip == other.ip) and (self.port == other.port) and (self.nwh == other.nwh)

    def __ne__(self, other):
        return (self.ip != other.ip) or (self.port != other.port) or (self.nwh != other.nwh)

    # PROTOCOL: 0=chat 1=data