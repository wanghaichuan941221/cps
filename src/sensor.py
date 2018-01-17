import time
import log
from networking.networkHandlerUDP import NetworkHandlerUDP

# Specify own IP and port
UDP_IP = '130.89.179.187'
UDP_PORT = 5005

T_UDP_IP = '130.89.136.245'
T_UDP_PORT = 5005

log.log('sensor', 'Init UDP IP: ' + str(UDP_IP))
log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the UDP network handlers
sensors = []
for i in range(0, 3):
    net_hand_udp = NetworkHandlerUDP(UDP_IP, UDP_PORT + i)
    net_hand_udp.setName('Network Handler UDP Client ' + str(i))
    sensors.append(net_hand_udp)
    # Start the UDP network handler
    net_hand_udp.start()

time.sleep(1)
for i in range(0, 10):
    for sensor in sensors:
        bmsg = bytearray(b'\x01\x02\x03')
        bmsg.append(i)
        sensor.send_msg(bmsg, T_UDP_IP, T_UDP_PORT)

for sensor in sensors:
    sensor.join()




