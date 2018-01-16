import time
from networking.networkHandler import *

# Specify own IP and port
UDP_IP = '130.89.178.11'
UDP_PORT = 5005

log.log('sensor', 'Init UDP IP: ' + str(UDP_IP))
log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the network handler
net_hand = NetworkHandler(UDP_IP, UDP_PORT)
net_hand.setName('Network Handler')

# Start the network handler
net_hand.start()

# Do stuff here
time.sleep(1)
for i in range(0, 10000):
    net_hand.send_msg('HOI' + str(i), UDP_IP, UDP_PORT)


# Wait for the network handler before terminating
net_hand.join()

