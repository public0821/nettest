#!/usr/bin/env python3
from nettest.packets.ether import ETH_P_ARP, EtherHeader
from nettest.packets.arp import Arp, ARPOP_REPLY, ARPOP_REQUEST
from nettest.sockets import EthernetSocket
from nettest.tools.base import Sender
import socket
import struct
import time
from nettest.platform import get_if_addr, get_if_hwaddr
        
        
class Arping(Sender):
    name = _("arpping tool")
    def _setup_args(self, parser):
        super(Arping, self)._setup_args(parser)
        parser.add_argument('destip', type=str, help=_("Specifies the dest ip send to"))
        parser.add_argument('-i', '--interface', type=str, required=True, help=_("Specifies the interface"))

        
    def _before_send(self):
        super(Arping, self)._before_send()
        self._sock = EthernetSocket(self.args.interface, ETH_P_ARP)
        self._arp = Arp()
        self._etherhdr = EtherHeader()
        self._etherhdr.h_source = get_if_hwaddr(self.args.interface)
        self._etherhdr.h_dest = 'ff:ff:ff:ff:ff:ff'
        self._etherhdr.h_proto = ETH_P_ARP
        self._arp.ar_sha = self._etherhdr.h_source
        self._arp.ar_tha = self._etherhdr.h_dest
        self._arp.ar_spa = get_if_addr(self.args.interface)
        self._arp.ar_tpa = self.args.destip
        self._arp.ar_op = ARPOP_REQUEST
        self._data = self._etherhdr.dump() + self._arp.dump()
        print('ARPING {0} from {1} {2}'.format(self.args.destip, socket.inet_ntoa(self._arp.ar_spa), self.args.interface))
        self._is_first_ping = True

    def _send(self):
        if self._is_first_ping:
            self._is_first_ping = False
        else:
            time.sleep(1)
        start_timestamp = time.time()
        self._sock.send(self._data)
        try:
            timeout = 2
            while timeout > 0:
                self._sock.settimeout(timeout)
                data, raddr = self._sock.recvfrom(1500)
                recv_timestamp= time.time()
                etherhdr = EtherHeader()
                etherhdr.load(data)
                if etherhdr.h_proto == ETH_P_ARP:
                    arp = Arp()
                    arp.load(data[etherhdr.length:])
                    if arp.ar_op == ARPOP_REPLY:
                        if arp.ar_spa == self.args.destip:
                            print('replay from {0} [{1}] {2:.3f} ms'.format(
                                self.args.destip, arp.ar_sha, recv_timestamp - start_timestamp))
                        break
                timeout -= time.time() - start_timestamp
                if timeout < 0:
                    raise socket.timeout()
        except socket.timeout:
            print('timeout')
        
    def _after_send(self):
#         super(Ping, self)._after_send()
        self._sock.close()
             
        
            
if __name__ == '__main__':
    tool = Arping()
    tool.start()
