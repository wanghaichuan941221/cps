import socket
from threading import Thread, RLock

# Wi-Fi
# SSID: CPSRSACRPU
# password: cpsgroup1
# ip: 10.0.0.1


class NetworkHandlerUDP(Thread):

    def __init__(self, port):
        Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.running = True
        self.counter = 0

    def run(self):
        while self.running:
            # print('cereivning')
            if self.counter % 10000 == 0:
                print(self.counter)
            data, addr = self.sock.recvfrom(1024)
            self.counter += 1
            if data == b'\x01':
                print(self.counter)

    def send_msg(self, msg, ip, port):
        # print('sendeded')
        self.sock.sendto(msg, (ip, port))
