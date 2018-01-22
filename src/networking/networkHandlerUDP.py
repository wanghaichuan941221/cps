import socket
from threading import Thread, RLock
from logger import Logger


class NetworkHandlerUDP(Thread):
    def __init__(self, port, log: 'Logger'):
        # Run constructor of super class
        Thread.__init__(self)

        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.connections = dict()
        self.protocol = None
        self.log = log
        self.lock = RLock()
        self.running = True

    def add_protocol(self, protocol):
        self.protocol = protocol

    def run(self):
        self.log.log('networkHandlerUDP', self.getName() + ' Now receiving...')
        while self.running:
            # Constantly receive a message
            data, addr = self.sock.recvfrom(1024)
            self.log.log('networkHandlerUDP', self.getName() + ' Received message ' + str(data) + ' from ' + str(addr))

            self.protocol.rec_prot(data, addr)


    # msg is bytes
    def send_msg(self, msg, ip, port):
        # Send a message
        self.sock.sendto(msg, (ip, port))
        self.log.log('networkHandlerUDP', self.getName() + ' Sent message ' + str(msg) + ' to ' + str((ip, port)))

    # msg is bytes
    def multisend(self, msg):
        self.lock.acquire()
        try:
            for key, conn in self.connections.items():
                conn.send_msg(msg)
        finally:
            self.lock.release()

    # msg is bytes
    def forward_exclude(self, msg, not_conn):
        self.lock.acquire()
        try:
            for key, conn in self.connections.items():
                if not not_conn == conn:
                    conn.send_msg(msg)
        finally:
            self.lock.release()

    def get_connection(self, key):
        self.lock.acquire()
        try:
            r = self.connections[key]
        finally:
            self.lock.release()
        return r

    def add_connection(self, ip, port, name):
        self.lock.acquire()
        try:
            conn = Connection(ip, port, name, self)
            self.connections[(ip, port)] = conn
            self.log.log('networkHandlerUDP', str(conn) + ' connected')
        finally:
            self.lock.release()

    def remove_dead_clients(self, alive):
        self.lock.acquire()
        try:
            remove_list = []
            remove_list.extend(self.connections.keys())
            for key in alive:
                remove_list.remove(key)
            for key in remove_list:
                conn = self.connections.pop(key)
                self.log.log('networkHandlerUDP', str(conn) + ' disconnected')
        finally:
            self.lock.release()


class Connection:
    def __init__(self, ip, port, name, nwh: 'NetworkHandlerUDP'):
        self.ip = ip
        self.port = port
        self.name = name
        self.nwh = nwh

    def send_msg(self, msg):
        # Send a message
        self.nwh.send_msg(msg, self.ip, self.port)

    def __str__(self):
        return 'Connection(' + self.ip + ', ' + str(self.port) + ', ' + self.name + ')'

    def __eq__(self, other):
        return (self.ip == other.ip) and (self.port == other.port) and (self.nwh == other.nwh)

    def __ne__(self, other):
        return (self.ip != other.ip) or (self.port != other.port) or (self.nwh != other.nwh)
