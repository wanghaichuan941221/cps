import log
from networking.networkHandlerUDP import NetworkHandlerUDP

# Specify own IP and port
UDP_PORT = 5005

log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the UDP network handler
net_hand_udp = NetworkHandlerUDP(UDP_PORT)
net_hand_udp.setName('Network Handler UDP')

# Start the UDP network handler
net_hand_udp.start()
net_hand_udp.join()
