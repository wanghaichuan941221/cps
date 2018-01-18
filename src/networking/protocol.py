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
        if prot == 0:
            self.chinkie.rec_msg(data[1:], addr)
        elif prot == 1:
            pass


class ChinkieServerProtocol(Protocol):
    def __init__(self, nwh, chinkie: 'ChinkieHandlerServer'):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data, addr):
        prot = data[0]
        if prot == 0:
            self.chinkie.rec_msg(data[1:], addr)
        elif prot == 1:
            pass
