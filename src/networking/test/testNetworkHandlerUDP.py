import socket
from threading import Thread, RLock
from logger import Logger

# Wi-Fi
# SSID: CPSRSACRPU
# password: cpsgroup1
# ip: 10.0.0.1


class NetworkHandlerUDP(Thread):

    def __init__(self, port, log: 'Logger'):
        Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.running = True
        self.counter = 0
        self.log = log

    def run(self):
        while self.running:
            self.sock.recvfrom(1024)
            self.counter += 1

    def send_msg(self, msg, ip, port):

        self.sock.sendto(msg, (ip, port))
