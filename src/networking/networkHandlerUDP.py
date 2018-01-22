import socket
from threading import Thread, RLock
from logger import Logger


class NetworkHandlerUDP(Thread):
    """The NetworkHandlerUPD class is used to manage all the connections for a client or server node. The class
    implements the sending and receiving of messages using Wi-Fi and the IP and UDP protocols.
    """

    def __init__(self, port, log: 'Logger'):
        """The constructor of the HeartbeatChecker class, which is an extension of the threading.Thread class."""

        # Run constructor of super class
        Thread.__init__(self)

        # Create a socket with the IP and UDP protocol.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket on the provided port, and own IP.
        self.sock.bind(('', port))
        # Initialize the variables connections, protocol, log, lock and running to their initial values.
        self.connections = dict()
        self.protocol = None
        self.log = log
        self.lock = RLock()
        self.running = True

    def add_protocol(self, protocol):
        """This function sets/adds a protocol to the network handler."""

        self.protocol = protocol

    def run(self):
        """The run function that gets called when the thread is started. The function loops is constantly listening
        for a message. Once a message is received, the protocol is called and used to decide what should be done.
        """

        # Indicate that the network handler is now running and receiving messages.
        self.log.log('networkHandlerUDP', self.getName() + ' Now receiving...')
        # Main loop.
        while self.running:
            # Constantly receive a message.
            data, addr = self.sock.recvfrom(1024)
            self.log.log('networkHandlerUDP', self.getName() + ' Received message ' + str(data) + ' from ' + str(addr))
            # Pass the message to the protocol.
            self.protocol.rec_prot(data, addr)

    def send_msg(self, msg, ip, port):
        """The send_msg() function is used to send a message to a specific address using IP and UDP."""

        # Send a message.
        self.sock.sendto(msg, (ip, port))
        self.log.log('networkHandlerUDP', self.getName() + ' Sent message ' + str(msg) + ' to ' + str((ip, port)))

    def multisend(self, msg):
        """This function sends a message to all known connections of the network handler. It uses send_msg()."""

        # Because multiple threads might access the connection list, protect it with a lock.
        self.lock.acquire()
        try:
            # For every known connection, send the message.
            for key, conn in self.connections.items():
                conn.send_msg(msg)
        finally:
            # Release the lock.
            self.lock.release()

    def forward_exclude(self, msg, not_conn):
        """Forwards a message to all known connection except for one specified connection, usually the source of the
        message that is to be forwarded.
        """

        # Because multiple threads might access the connection list, protect it with a lock.
        self.lock.acquire()
        try:
            # For every known connection, except the specified one, send the message.
            for key, conn in self.connections.items():
                if not not_conn == conn:
                    conn.send_msg(msg)
        finally:
            # Release the lock.
            self.lock.release()

    def get_connection(self, key):
        """A simple function to get a connection from the list using the key."""

        # Because multiple threads might access the connection list, protect it with a lock.
        self.lock.acquire()
        try:
            # Get the connection from the list.
            r = self.connections[key]
        finally:
            # Release the lock.
            self.lock.release()
        return r

    def add_connection(self, ip, port, name):
        """Add a connection to the list of known connections."""

        # Because multiple threads might access the connection list, protect it with a lock.
        self.lock.acquire()
        try:
            # Create a new connection and add it to the list.
            conn = Connection(ip, port, name, self)
            self.connections[(ip, port)] = conn
            self.log.log('networkHandlerUDP', str(conn) + ' connected.')
        finally:
            # Release the lock.
            self.lock.release()

    def remove_dead_clients(self, alive):
        """This funciton compares the list of known connections with the list of the alive clients determined by
        the HeartbeatChecker class. When connections are not in the alive list, but are in the connection list,
        remove them.
        """

        # Because multiple threads might access the connection list, protect it with a lock.
        self.lock.acquire()
        try:
            # Make a temporary list to avoid modification while looping over it.
            remove_list = []
            remove_list.extend(self.connections.keys())
            # Remove all alive connections from temporary list.
            for key in alive:
                remove_list.remove(key)
            # All the connections that are still in the list are removed from the actual connection list.
            for key in remove_list:
                conn = self.connections.pop(key)
                self.log.log('networkHandlerUDP', str(conn) + ' disconnected')
        finally:
            # Release the lock.
            self.lock.release()


class Connection:
    """This class is an implementation of a connection. A connection has an ip, a port and a name as attributes."""

    def __init__(self, ip, port, name, nwh: 'NetworkHandlerUDP'):
        """The constructor for the Connection class."""

        # Set the variables ip, port, name and nwh to their initial values.
        self.ip = ip
        self.port = port
        self.name = name
        self.nwh = nwh

    def send_msg(self, msg):
        """If send_msg() is called on a connection, it uses its own address and the network handler send_msg() function
        to send the message.
        """

        # Send a message with own address.
        self.nwh.send_msg(msg, self.ip, self.port)

    def __str__(self):
        return 'Connection(' + self.ip + ', ' + str(self.port) + ', ' + self.name + ')'

    def __eq__(self, other):
        return (self.ip == other.ip) and (self.port == other.port) and (self.nwh == other.nwh)

    def __ne__(self, other):
        return (self.ip != other.ip) or (self.port != other.port) or (self.nwh != other.nwh)
