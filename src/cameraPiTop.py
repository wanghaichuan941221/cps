from image.imageProcessor import ImageProcessor
from logger import Logger
from networking.chinkieHandlerClient import ChinkieHandlerClient
from networking.heartbeat import Heartbeat
from networking.networkHandlerUDP import NetworkHandlerUDP
from networking.protocol import ClientProtocol


# Create a program-wide logger.
log = Logger()

# Specify own IP and port.
UDP_PORT = 5005

# Specify server IP and port.
T_UDP_IP = '10.0.0.1'
T_UDP_PORT = 5005
log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))
log.log('sensor', 'Init Target UDP IP: ' + str(T_UDP_IP))
log.log('sensor', 'Init Target UDP PORT: ' + str(T_UDP_PORT))

# Create the UDP network handler.
net_hand_udp = NetworkHandlerUDP(UDP_PORT, log)
net_hand_udp.setName('UDP Client')

# Create the image processor
imgProcessor = ImageProcessor(net_hand_udp, log, True)
imgProcessor.setName('Image Processor')

# Create the Chinkie (commands) handler.
chinkie = ChinkieHandlerClient(net_hand_udp, imgProcessor, log)
chinkie.setName('Chinkie Client')

# Create the heartbeat.
hb = Heartbeat(1, net_hand_udp)
hb.setName('Heartbeat')

# Add a protocol to the network handler.
net_hand_udp.add_protocol(ClientProtocol(net_hand_udp, chinkie, hb))

# Add the server to the connections of the network handler.
net_hand_udp.add_connection(T_UDP_IP, T_UDP_PORT, 'CPS1-0')


# Start the several threads.
net_hand_udp.start()
chinkie.start()
hb.start()
imgProcessor.start()


# TODO Stuff goes here!


# Wait for the threads to finish.
net_hand_udp.join()
chinkie.join()
hb.join()
imgProcessor.join()
