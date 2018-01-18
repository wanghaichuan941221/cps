from networking.chinkieHandlerClient import ChinkieHandlerClient
from networking.chinkieHandlerServer import ChinkieHandlerServer


class Protocol:
    def __init__(self):
        pass

    def rec_prot(self, data, addr):
        pass

    def wrap(self, prot, msg):
        return prot + msg


class ChinkieClientProtocol(Protocol):
    def __init__(self, nwh, chinkie: 'ChinkieHandlerClient'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data, addr):
        prot = data[0]
        print('DEBUG (Client): ', prot, data[0], data)
        if prot == b'0':
            print('DEBUG (Client): forwarded to chinkieClientHandler')
            self.chinkie.rec_msg(data[1:], addr)
        elif prot == b'1':
            pass


class ChinkieServerProtocol(Protocol):
    def __init__(self, nwh, chinkie: 'ChinkieHandlerServer'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data, addr):
        prot = data[0]
        print('DEBUG (Server): ', prot, data[0], data)
        if prot == b'0':
            print('DEBUG (Server): forwarded to chinkieServerHandler')
            self.chinkie.rec_msg(data[1:], addr)
        elif prot == b'1':
            pass
