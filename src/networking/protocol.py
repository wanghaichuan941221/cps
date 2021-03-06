from control.controller import Controller
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

    # TOP-VIEW-DATA packet
    # - 1 byte header (\x02)
    # - 16 bytes data (x1,y1,x2,y2,x3,y3,xb,yb)
    #   - 2 bytes for every integer (8 integers)
    def wrap_top_view(self, coords):
        if len(coords) == 8:
            res = b'\x02'
            for i in range(0, len(coords)):
                res = res + self.int_to_bytes2(coords[i])
            return res
        else:
            raise ValueError("Top view coordinate array is not 8: length was " + str(len(coords)))

    # SIDE-VIEW-DATA packet
    # - 1 byte header (\x03)
    # - 20 bytes data (clx, cly, x2, y2, x3, y3, x4, y4, crx, cry)
    #   - 2 bytes for every integer (10 integers)
    def wrap_side_view(self, coords):
        if len(coords) == 10:
            res = b'\x03'
            for i in range(0, len(coords)):
                res = res + self.int_to_bytes2(coords[i])
            return res
        else:
            raise ValueError("Side view coordinate array is not 8: length was " + str(len(coords)))



    def int_to_bytes2(self, n: 'int'):
        b = [0, 0]
        b[1] = int(n & 0xFF)
        b[0] = int((n >> 8) & 0xFF)
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
            pass  # Not needed for client
        elif header == b'\x02':
            pass  # Not needed for client
        elif header == b'\x03':
            pass  # Not needed for client


class ServerProtocol(Protocol):
    def __init__(self, nwh: 'NetworkHandlerUDP', chinkie: 'ChinkieHandlerServer', hb: 'HeartbeatChecker', con: 'Controller'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie
        self.hb = hb
        self.con = con

    def rec_prot(self, data, addr):
        header = self.get_byte(data, 0)

        if header == b'\x00':
            self.chinkie.rec_msg(str(data[1:], 'utf-8'), addr)
        elif header == b'\x01':
            self.hb.rec_hb(str(data[1:], 'utf-8'), addr)
        elif header == b'\x02':
            res = []
            values = data[1:]
            for i in range(0, 8):
                res.append(self.bytes2_to_int(values, i*2))
            self.con.update_top_view_data(res)
        elif header == b'\x03':
            if addr in self.nwh.connections.keys():
                res = []
                values = data[1:]
                for i in range(0, 10):
                    res.append(self.bytes2_to_int(values, i * 2))

                if self.nwh.connections[addr].name == 'CPS1-4':
                    self.con.update_left_view_data(res)
                elif self.nwh.connections[addr].name == 'CPS1-1':
                    self.con.update_right_view_data(res)
                else:
                    self.nwh.log.print('UNKNOWN SIDE VIEW CAMERA: ' + self.nwh.connections[addr].name)

