from testNetworkHandlerUDP import NetworkHandlerUDP
import atexit


# Specify own IP and port.
UDP_PORT = 5005
T_IP = '10.0.0.1'

# Create the UDP network handler.
net_hand_udp = NetworkHandlerUDP(UDP_PORT)
net_hand_udp.setName('UDP Server')

net_hand_udp.start()

for i in range(0, 1000000):
    net_hand_udp.send_msg(b'\x00', T_IP, UDP_PORT)

net_hand_udp.send_msg(b'\x01', T_IP, UDP_PORT)
print('==========DONE==========')

net_hand_udp.join()


def exit_handler():
    print(net_hand_udp.counter)


atexit.register(exit_handler)