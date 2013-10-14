from nettest.packets.base import Packet
from nettest.packets.fields import IntegerField

SOL_UDP =   17     # sockopt level for UDP 


class UdpHeader(Packet):
    uh_sport = IntegerField(length=2) # source port
    uh_dport = IntegerField(length=2)    # destination port 
    uh_ulen = IntegerField(length=2) # udp length 
    uh_sum = IntegerField(length=2)# udp checksum
    
    fields = ['uh_sport', 'uh_dport', 'uh_ulen', 'uh_sum']
