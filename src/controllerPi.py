from logger import Logger
from networking.chinkieHandlerServer import ChinkieHandlerServer
from networking.heartbeat import HeartbeatChecker
from networking.networkHandlerUDP import NetworkHandlerUDP
from networking.protocol import ServerProtocol
from control.controller import Controller


# Create a program-wide logger.
log = Logger()

# Specify own IP and port.
UDP_PORT = 5005
log.log('main', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the Controller
controller = Controller()
controller.connect_usb_arm()

# Create the UDP network handler.
net_hand_udp = NetworkHandlerUDP(UDP_PORT, log)
net_hand_udp.setName('UDP Server')

# Create the Chinkie (commands) handler.
chinkie = ChinkieHandlerServer(net_hand_udp, log, controller)
chinkie.setName('Chinkie Server')

# Create the heartbeat checker.
hbc = HeartbeatChecker(3, net_hand_udp)
hbc.setName('Heartbeat Checker')

# Add a protocol to the network handler.
net_hand_udp.add_protocol(ServerProtocol(net_hand_udp, chinkie, hbc, controller))

# Start the several threads.
hbc.start()
net_hand_udp.start()
chinkie.start()


# TODO Stuff goes here!


# Wait for the threads to finish.
net_hand_udp.join()
chinkie.join()
hbc.join()
