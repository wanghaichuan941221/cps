import socket
from threading import Thread
from random import randint
import time
import struct

UDP_IP = "130.89.180.208"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print("UDP IP:", UDP_IP)
print("UDP port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

class NetworkHandler(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            print("start rec")
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print("received message:", data, time.time())

    def send_msg(self, msg, ip, port):
        sock.sendto(msg, (ip, port))
        print("message sent")

net_hand = NetworkHandler(sock)
net_hand.setName('Network Handler')

net_hand.start()

time.sleep(2)

net_hand.join()

print('Main Terminating...')
