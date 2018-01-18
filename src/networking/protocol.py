from networking.chinkieHandlerClient import ChinkieHandlerClient
from networking.chinkieHandlerServer import ChinkieHandlerServer
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
    # - rest for utf-8 encoded string
    def wrap_msg(self, msg):
        return b'\x00' + msg.encode('utf-8')


class ClientProtocol(Protocol):
    def __init__(self, nwh: 'NetworkHandlerUDP', chinkie: 'ChinkieHandlerClient'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data, addr):
        header = self.get_byte(data, 0)

        if header == b'\x00':
            msg = str(data[1:], 'utf-8')
            self.chinkie.rec_msg(msg)
        elif header == b'\x01':
            pass


class ServerProtocol(Protocol):
    def __init__(self, nwh: 'NetworkHandlerUDP', chinkie: 'ChinkieHandlerServer'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data, addr):
        header = self.get_byte(data, 0)

        if header == b'\x00':
            self.chinkie.rec_msg(str(data[1:], 'utf-8'), addr)
        elif header == b'\x01':
            pass
