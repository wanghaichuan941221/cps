from networking.networkHandlerTCPServer import NetworkHandlerTCPServer

TCP_IP = '130.89.179.187'
TCP_PORT = 5006

tcp_server = NetworkHandlerTCPServer(TCP_IP, TCP_PORT)
tcp_server.setName('TCP Server')
tcp_server.start()

tcp_server.join()
