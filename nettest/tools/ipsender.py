#!/usr/bin/env python3
import sys
from nettest.exceptions import NettestError
from nettest.sockets import IpSocket
from nettest.tools.base import MultiSender
from nettest.packets.ip import ipproto_dict
from nettest.packets.ip import IpHeader
import socket

class IpSender(MultiSender):
    def _setup_args(self, parser, need_data=True):
        super(IpSender, self)._setup_args(parser)
        parser.add_argument('protocol', type=str, help=_("Specifies the data protocol to be sent"))
        parser.add_argument('destip', type=str, help=_("Specifies the dest ip send to"))
        if need_data:
            parser.add_argument('--data', type=str, help=_("Specifies the data to be sent"))
        parser.add_argument('--srcip', type=str, help=_("Specifies the src ip send from"))
     
    def _after_setup_args(self):
        if 'data' in self.args and not self.args.data and self.args.processes:
            raise NettestError(_("must specifies --data option when use multiprocess"))
        proto_id = ipproto_dict.get(self.args.protocol.upper())
        if proto_id is None:
            proto_id = int(self.args.protocol)
        self._protocol = proto_id
 
    def _before_send(self):
        if self.args.srcip:
            self._sock = IpSocket(socket.IPPROTO_RAW)
            self._sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
            self._data = self._get_raw_data()
        else:
            self._sock = IpSocket(self._protocol)
            self._data = self._get_data()
        
    def _send(self):
        addr  = (self.args.destip, 0)
        self._sock.sendto(self._data, addr)
        
    def _after_send(self):
        self._sock.close()
             
    def _get_data(self):
        if self.args.data:
            return self.args.data.encode()
        else:
            return sys.stdin.read(65535).encode()
            
    def _get_raw_data(self):
        iphdr = IpHeader()
        iphdr.protocol = self._protocol
        if self.args.srcip:
            iphdr.saddr = self.args.srcip
        iphdr.daddr = self.args.destip
        data = self._get_data()
        iphdr.ihl = iphdr.length >> 2    
        return iphdr.dump() + data

if __name__ == '__main__':
    try:
        tool = IpSender()
        tool.start()
    except NettestError as e:
        print(e)
