#!/usr/bin/env python3
from nettest.packets.icmp import IcmpEcho, ICMP_ECHO, ICMP_ECHOREPLY
from nettest.packets.ip import IpHeader
from nettest.sockets import IpSocket
from nettest.tools.base import Sender
from nettest.utils import checksum
import socket
import struct
import time

class Ping(Sender):
    name = _("ping tool")
    def _setup_args(self, parser):
        super(Ping, self)._setup_args(parser)
        parser.add_argument('destip', type=str, help=_("Specifies the dest ip send to"))
        parser.add_argument('--data', type=str, help=_("Specifies the optional data to be sent"))
        
    def _before_send(self):
        super(Ping, self)._before_send()
        self._sock = IpSocket(socket.IPPROTO_ICMP)
        self._icmp_echo = IcmpEcho()
        self._icmp_echo.header.type = ICMP_ECHO
        print('PING {0} {1} bytes of data.'.format(self.args.destip, self._icmp_echo.length))
                        
        
    def _send(self):
        if self._icmp_echo.sequence > 0:
            time.sleep(1)
        self._icmp_echo.sequence += 1
        addr  = (self.args.destip, 0)
        self._icmp_echo.timestamp = int(time.time()*1000) & 0xffffffff
        self._icmp_echo.header.checksum = 0
        self._icmp_echo.header.checksum = socket.ntohs(checksum(self._icmp_echo.dump()))
        self._sock.sendto(self._icmp_echo.dump(), addr)

        try:
            timeout = 2
            start_timestamp = time.time()
            while timeout > 0:
                self._sock.settimeout(timeout)
                data, raddr = self._sock.recvfrom(1024)
                recv_timestamp= int(time.time()*1000) & 0xffffffff
                if raddr == addr:
                    iphdr = IpHeader()
                    iphdr.load(data)
                    icmp_data = data[iphdr.ihl*4:]
                    icmp_echo_reply = IcmpEcho()
                    icmp_echo_reply.load(icmp_data)
                    if icmp_echo_reply.header.type == ICMP_ECHOREPLY \
                            and icmp_echo_reply.id == self._icmp_echo.id \
                            and icmp_echo_reply.sequence == self._icmp_echo.sequence:
                        print('{0} bytes from {1}: icmp_req={2} ttl={3} time={4} ms'.format(
                                len(icmp_data), addr[0], self._icmp_echo.sequence, iphdr.ttl, abs(recv_timestamp-self._icmp_echo.timestamp)))
                        break
                timeout -= time.time() - start_timestamp
                if timeout < 0:
                    raise socket.timeout()
        except socket.timeout:
            print('timeout')
        
        
    def _get_iphdr_len(self, data):
        ver_len = struct.unpack('!B', data[0])
        return (ver_len & 0x0f)*4
        
    def _after_send(self):
#         super(Ping, self)._after_send()
        self._sock.close()
             
        
            
if __name__ == '__main__':
    tool = Ping()
    tool.start()
