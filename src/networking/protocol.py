class Protocol:
    def __init__(self):
        pass

    def rec_prot(self, data):
        pass

    def wrap(self, prot, msg):
        pass


class ChinkieClientProtocol(Protocol):
    def __init__(self, nwh, chinkie):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data):
        prot = data[0]
        if prot == 0:
            return  # do stuffs
        elif prot == 1:
            return  # do stuffs


class ChinkieServerProtocol(Protocol):
    def __init__(self, nwh, chinkie):
        # Run constructor of parent
        Protocol.__init__(self)

        self.nwh = nwh
        self.chinkie = chinkie

    def rec_prot(self, data):
        prot = data[0]
        if prot == 0:
            return  # do stuffs
        elif prot == 1:
            return  # do stuffs
