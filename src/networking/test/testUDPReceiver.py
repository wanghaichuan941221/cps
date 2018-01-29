from logger import Logger
from networking.test.testNetworkHandlerUDP import NetworkHandlerUDP
import atexit


log = Logger()

# Specify own IP and port.
UDP_PORT = 5005
log.log('main', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the UDP network handler.
net_hand_udp = NetworkHandlerUDP(UDP_PORT, log)
net_hand_udp.setName('UDP Server')

net_hand_udp.start()

net_hand_udp.join()


def exit_handler():
    log.log('EXIT', net_hand_udp.counter)


atexit.register(exit_handler)
