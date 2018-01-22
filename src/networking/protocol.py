from networking.chinkieHandlerClient import ChinkieHandlerClient
from networking.chinkieHandlerServer import ChinkieHandlerServer
from networking.heartbeat import Heartbeat, HeartbeatChecker
from networking.networkHandlerUDP import NetworkHandlerUDP


class Protocol:
    def __init__(self):
        pass

    def rec_prot(self, data, addr):
        pass

    def get_byte(self, b: bytes, i: int):
        return bytes([b[i]])

    # MESSAGE packet
    # - 1 byte header (\x00)
    # - rest for utf-8 encoded string (message)
    def wrap_msg(self, msg):
        return b'\x00' + msg.encode('utf-8')

    # HEARTBEAT packet
    # - 1 byte header (\x01)
    # - rest for utf-8 encoded string (name)
    def wrap_hb(self, name):
        return b'\x01' + name.encode('utf-8')

    # x1,y1,x2,y2,x3,y3,xb,yb
    def wrap_top_view(self, x1, y1, x2, y2, x3, y3, xb, yb):
        return b'\x02'

    def int_to_bytes2(self, n):
        b = [0, 0]
        b[1] = n & 0xFF
        b[0] = (n >> 8) & 0xFF
        return bytes(b)

    def bytes2_to_int(self, b, offset):
        return (b[offset] << 8) + b[offset+1]


class ClientProtocol(Protocol):
    def __init__(self, nwh: 'NetworkHandlerUDP', chinkie: 'ChinkieHandlerClient', hb: 'Heartbeat'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie
        self.hb = hb

    def rec_prot(self, data, addr):
        header = self.get_byte(data, 0)

        if header == b'\x00':
            msg = str(data[1:], 'utf-8')
            self.chinkie.rec_msg(msg)
        elif header == b'\x01':
            pass


class ServerProtocol(Protocol):
    def __init__(self, nwh: 'NetworkHandlerUDP', chinkie: 'ChinkieHandlerServer', hb: 'HeartbeatChecker'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie
        self.hb = hb

    def rec_prot(self, data, addr):
        header = self.get_byte(data, 0)

        if header == b'\x00':
            self.chinkie.rec_msg(str(data[1:], 'utf-8'), addr)
        elif header == b'\x01':
            self.hb.rec_hb(str(data[1:], 'utf-8'), addr)
