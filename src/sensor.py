from networking.networkHandler import *

# Specify own IP and port
UDP_IP = '130.89.180.208'
UDP_PORT = 5005

print('{:<21}'.format(str(time.time())), '{:<24}'.format('sensor'), ('UDP IP: ' + str(UDP_IP)))
print('{:<21}'.format(str(time.time())), '{:<24}'.format('sensor'), ('UDP PORT: ' + str(UDP_PORT)))

# Create the network handler
net_hand = NetworkHandler(UDP_IP, UDP_PORT)
net_hand.setName('Network Handler')

# Start the network handler
net_hand.start()

# Wait for the network handler before terminating
net_hand.join()

