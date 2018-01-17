import time
import log
from networking.networkHandlerUDP import NetworkHandlerUDP

# Specify own IP and port
UDP_PORT = 5005

T_UDP_IP = '10.0.0.1'  # <---- only thing we need to change
# T_UDP_IP = '130.89.136.245'  # <---- only thing we need to change
T_UDP_PORT = 5005

log.log('sensor', 'Init UDP PORT: ' + str(UDP_PORT))

# Create the UDP network handlers
sensors = []
for i in range(0, 1):
    net_hand_udp = NetworkHandlerUDP(UDP_PORT + i)
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

#pw = cpsgroup1
#ssid = CPSRSACRPU
#own ip = 10.0.0.1
#range ip = 10.0.0.2-10.0.0.255




