from testNetworkHandlerUDP import NetworkHandlerUDP
import atexit


# Specify own IP and port.
UDP_PORT = 5005

# Create the UDP network handler.
net_hand_udp = NetworkHandlerUDP(UDP_PORT)
net_hand_udp.setName('UDP Server')

net_hand_udp.start()

net_hand_udp.join()


def exit_handler():
    print(net_hand_udp.counter)


atexit.register(exit_handler)
