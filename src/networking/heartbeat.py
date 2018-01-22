from threading import Thread
from time import sleep
from networking.networkHandlerUDP import NetworkHandlerUDP
from platform import node


class Heartbeat(Thread):
    """The Heartbeat class is used to continuously send a heartbeat signal to the server so the server knows that
    the client is still online. This class/thread is only run by clients.
    """

    def __init__(self, interval: 'float', nwh: 'NetworkHandlerUDP'):
        """The constructor of the Heartbeat class, which is an extension of the threading.Thread class."""

        # Run the constructor of the threading.Thread superclass.
        Thread.__init__(self)

        # Create a network handler and set the variables for the interval en running state.
        self.interval = interval
        self.nwh = nwh
        self.running = True

    def run(self):
        """The run function that gets called when the thread is started. The function loops and sends a message to
        all known connections (in the case of the client this is only the server).
        """

        # Main loop.
        while self.running:
            # Send a heartbeat message.
            self.nwh.multisend(self.nwh.protocol.wrap_hb(node()))
            # The thread sleeps for the duration of the given interval.
            sleep(self.interval)


class HeartbeatChecker(Thread):
    """The HeartbeatChecker class is used to continuously check for heartbeat signals from clients, as well as
    maintaining the connections list of the server. This includes adding new connections if a heartbeat is found, and
    removing connections if for a connection no heartbeat has been heard for some specified interval.
    """

    def __init__(self, interval: 'float', nwh: 'NetworkHandlerUDP'):
        """The constructor of the HeartbeatChecker class, which is an extension of the threading.Thread class."""

        # Run the constructor of the superclass.
        Thread.__init__(self)

        # Create a network handler and set the variables interval, alive and running to their initial values.
        self.interval = interval
        self.nwh = nwh
        self.alive = set()
        self.running = True

    def run(self):
        """The run function that gets called when the thread is started. The function loops and updates the "alive"
        list, containing all known connections that have send a heartbeat, on a set interval. After that, notify the
        network handler with the alive list so it can update it's connections (remove dead connections).
        """

        # Main loop.
        while self.running:
            self.alive = set()
            sleep(self.interval)
            self.nwh.remove_dead_clients(self.alive)

    def add_alive(self, key):
        """This function gets called by the rec_hb() funciton. It adds a connection to the alive list."""
        self.alive.add(key)

    def rec_hb(self, name, addr):
        """This function gets called by the protocol when a heartbeat is received. The functions checks if the
        network handler already knows the client connection. If not, it is added to the network handler. After that,
        the connection is added to the alive list.
        """

        # Check if the connection is already in the network handler, and if not (KeyError), add it.
        try:
            self.nwh.get_connection(addr)
        except KeyError:
            self.nwh.add_connection(addr[0], addr[1], name)
        # Add to local alive list
        self.alive.add(addr)
