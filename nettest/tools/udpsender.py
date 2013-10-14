#!/usr/bin/env python3
import sys
from nettest.sockets import UdpSocket
from nettest.tools.base import MultiSender
from nettest.sockets import IpSocket
from nettest.exceptions import NettestError
from nettest.packets.udp import UdpHeader
from nettest.packets.ip import IpHeader
import random


import socket

class UdpSender(MultiSender):
    def _setup_args(self, parser, need_data=True):
        super(UdpSender, self)._setup_args(parser)
        parser.add_argument('destip', type=str, help=_("Specifies the dest ip send to"))
        parser.add_argument('destport', type=int, help=_("Specifies the dest port send to"))
        parser.add_argument('--srcport', type=int, help=_("Specifies the src port send from"))
        if need_data:
            parser.add_argument('--data', type=str, help=_("Specifies the data to be sent"))
        parser.add_argument('--srcip', type=str, help=_("Specifies the src ip send from"))

    def _after_setup_args(self):
        if 'data' in self.args and not self.args.data and self.args.processes:
            raise NettestError(_("must specifies --data option when use multiprocess")) 

    def _before_send(self):
        if self.args.srcip:
            self._sock = IpSocket(socket.IPPROTO_RAW)
            self._sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
            self._data = self._get_raw_data()
        else:
            self._sock = UdpSocket()
            if self.args.srcport:
                self._sock.bind(('0.0.0.0', self.args.srcport))
            self._data = self._get_data()
        
    def _send(self):
        if self.args.srcip:
            addr  = (self.args.destip, self.args.destport)
        else:
            addr = (self.args.destip, 0)
        self._sock.sendto(self._data, addr)
        
    def _after_send(self):
        self._sock.close()
    
    def _get_data(self):
        if self.args.data:
            return self.args.data.encode()
        else:
            return sys.stdin.read(65535).encode()
     
    def _get_raw_data(self):
        data = self._get_data()

        iphdr = IpHeader()
        iphdr.protocol = socket.IPPROTO_UDP
        if self.args.srcip:
            iphdr.saddr = self.args.srcip
        iphdr.daddr = self.args.destip
        iphdr.ihl = iphdr.length >> 2    

        udphdr = UdpHeader()
        udphdr.uh_sport = self.args.srcport if self.args.srcport else random.randint(30000,40000)
        udphdr.uh_dport = self.args.destport
        udphdr.uh_ulen = len(data) + udphdr.length
        udphdr.uh_sum = 0

        return iphdr.dump() + udphdr.dump() + data


            
if __name__ == '__main__':
    try:
        tool = UdpSender()
        tool.start()
    except NettestError as e:
        print(e)
