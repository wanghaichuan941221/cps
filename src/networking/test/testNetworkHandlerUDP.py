import socket
from threading import Thread, RLock

# Wi-Fi
# SSID: CPSRSACRPU
# password: cpsgroup1
# ip: 10.0.0.1
import time


class NetworkHandlerUDP(Thread):

    def __init__(self, port):
        Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.running = True
        self.counter = 0
        self.received = False

    def run(self):
        while self.running:
            # print('cereivning')
            if self.counter % 10000 == 0:
                print(self.counter)
            data, addr = self.sock.recvfrom(1024)
            if not self.received:
                start_time = time.time()
                self.received = True
            self.counter += 1
            if data == b'\x01':
                print(self.counter)
                end_time = time.time()
                print(start_time - end_time)

    def send_msg(self, msg, ip, port):
        # print('sendeded')
        self.sock.sendto(msg, (ip, port))
