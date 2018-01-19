from logger import Logger
from networking.chinkieHandlerServer import ChinkieHandlerServer
from networking.networkHandlerUDP import NetworkHandlerUDP
from networking.protocol import ServerProtocol


CHINKIE = True
log = Logger()

# Specify own IP and port
UDP_PORT = 5005

log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the UDP network handler
net_hand_udp = NetworkHandlerUDP(UDP_PORT, log)
net_hand_udp.setName('UDP Server')
chinkie = ChinkieHandlerServer(net_hand_udp, log)
chinkie.setName('Chinkie Server')

if CHINKIE:
    net_hand_udp.add_protocol(ServerProtocol(net_hand_udp, chinkie))
    chinkie.start()

# Start the UDP network handler
net_hand_udp.start()
net_hand_udp.join()

if CHINKIE:
    chinkie.join()