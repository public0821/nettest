from .base import Packet
from .fields import IntegerField, MacField, Ipv4Field


ARPOP_REQUEST = 0x01  # ARP request  
ARPOP_REPLY = 0x02  # ARP reply 
ARPOP_RREQUEST = 0x01  # RARP request
ARPOP_RREPLY = 0x02  # RARP reply  
    
class Arp(Packet):
    ar_hrd = IntegerField(length=2, default=0x0001)  # format of hardware address
    ar_pro = IntegerField(length=2, default=0x0800)  # format of protocol address
    ar_hln = IntegerField(length=1, default=6)  # length of hardware address
    ar_pln = IntegerField(length=1, default=4)  # length of protocol address 
    ar_op = IntegerField(length=2, default=1)  # ARP opcode (command)  
    ar_sha = MacField(default='00:00:00:00:00:00')  # sender hardware address 
    ar_spa = Ipv4Field(default='0.0.0.0')  # sender protocol address 
    ar_tha = MacField(default='ff:ff:ff:ff:ff:ff')  # target hardware address 
    ar_tpa = Ipv4Field(default='0.0.0.0')  # target protocol address
    
    fields = ['ar_hrd', 'ar_pro', 'ar_hln', 'ar_pln', 'ar_op']
    fields += ['ar_sha', 'ar_spa', 'ar_tha', 'ar_tpa']

class Arp6(Arp):
    fields = ()
    def __init__(self):
        raise NotImplementedError(_("Arp6 not implemented"))

