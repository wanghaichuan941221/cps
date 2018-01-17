import time
import log
from networking.networkHandlerUDP import NetworkHandlerUDP
from networking.networkHandlerTCPClient import NetworkHandlerTCPClient
from networking.networkHandlerTCPServer import NetworkHandlerTCPServer

# Specify own IP and port
UDP_IP = '130.89.179.187'
UDP_PORT = 5005

TCP_IP = '130.89.179.187'
TCP_PORT = 5006

log.log('sensor', 'Init UDP IP: ' + str(UDP_IP))
log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))

log.log('sensor', 'Init TCP IP: ' + str(TCP_IP))
log.log('sensor', 'Init TCP PORT: ' + str(TCP_PORT))

# Create the UDP network handler
net_hand_udp = NetworkHandlerUDP(UDP_IP, UDP_PORT)
net_hand_udp.setName('Network Handler UDP')

# Start the UDP network handler
net_hand_udp.start()

# Do stuff here
time.sleep(1)
for i in range(0, 256):
    bmsg = bytearray(b'\x01\x02\x03')
    bmsg.append(i)
    net_hand_udp.send_msg(bmsg, UDP_IP, UDP_PORT)

tcp_client = NetworkHandlerTCPClient(TCP_IP, TCP_PORT)
tcp_client.setName('TCP Client')
tcp_client.start()

time.sleep(1)
for i in range(0, 256):
    bmsg = bytearray(b'\x01\x02\x03')
    bmsg.append(i)
    tcp_client.send_msg(bmsg)

# Wait for the network handlers before terminating
net_hand_udp.join()
tcp_client.join()
