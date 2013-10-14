import socket
from nettest.packets.ether import ETH_P_ALL

class BaseSocket(socket.socket):

    def __init__(self, family, type, proto=0):
        super(BaseSocket, self).__init__(family, type, proto)
        
class EthernetSocket(BaseSocket):
    
    def __init__(self, ifname, protocol):
        super(EthernetSocket, self).__init__(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(protocol))
        self.bind((ifname, 0))

class IpSocket(BaseSocket):
    def __init__(self, protocol, ipv6=False):
        if ipv6:
            super(IpSocket, self).__init__(socket.AF_INET6, socket.SOCK_RAW, protocol)
        else:
            super(IpSocket, self).__init__(socket.AF_INET, socket.SOCK_RAW, protocol)

class UdpSocket(BaseSocket):
   
    def __init__(self, ipv6=False):
        if ipv6:
            super(UdpSocket, self).__init__(socket.AF_INET6, socket.SOCK_DGRAM, 0)
        else:
            super(UdpSocket, self).__init__(socket.AF_INET, socket.SOCK_DGRAM, 0)

class TcpSocket(BaseSocket):
   
    def __init__(self, ipv6=False):
        if ipv6:
            super(TcpSocket, self).__init__(socket.AF_INET6, socket.SOCK_STREAM, 0)
        else:
            super(TcpSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM, 0)


